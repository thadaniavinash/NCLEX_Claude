/* Administrator sign-in through Supabase Auth. The database only accepts saves from
   signed-in accounts listed in nclex_admins (supabase/002_admin_logins.sql), so this is
   what actually protects the question bank; the admin UI just reflects it. */

const AUTH_STORAGE_KEY = 'nclex_admin_session';
let authSession = null; // { access_token, refresh_token, expires_at (ms), email }

function storeAuthSession(session) {
  authSession = session;
  try {
    if (session) sessionStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
    else sessionStorage.removeItem(AUTH_STORAGE_KEY);
  } catch (e) {
    // Storage blocked: the session still lasts until the page is closed.
  }
}

function sessionFromTokenResponse(data) {
  return {
    access_token: data.access_token,
    refresh_token: data.refresh_token,
    expires_at: Date.now() + (data.expires_in || 3600) * 1000,
    email: data.user && data.user.email
  };
}

function authFetch(path, body, token, method) {
  return fetch(`${SUPABASE_URL}/auth/v1/${path}`, {
    method: method || 'POST',
    headers: {
      'apikey': SUPABASE_ANON_KEY,
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    },
    body: JSON.stringify(body || {})
  });
}

// true / false, or null when the database has no is_nclex_admin() yet (before
// 002_admin_logins.sql is run; the database then decides on its own).
async function checkIsAdmin(token) {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/is_nclex_admin`, {
      method: 'POST',
      headers: { 'apikey': SUPABASE_ANON_KEY, 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: '{}'
    });
    if (res.status === 404) return null;
    if (!res.ok) return false;
    return (await res.json()) === true;
  } catch (e) {
    return null;
  }
}

// Signs in with a session that is already known (from a password-reset link), if it is an admin.
async function adoptAdminSession(session) {
  const admin = await checkIsAdmin(session.access_token);
  if (admin === false) {
    authFetch('logout', {}, session.access_token).catch(() => {});
    return { ok: false, message: 'This account is not an author account.' };
  }
  storeAuthSession(session);
  isAdminLoggedIn = true;
  return { ok: true };
}

async function signInAdmin(email, password) {
  let res, data;
  try {
    res = await authFetch('token?grant_type=password', { email, password });
    data = await res.json().catch(() => ({}));
  } catch (e) {
    return { ok: false, message: 'Could not reach the sign-in service. Check your connection and try again.' };
  }
  if (!res.ok) {
    return { ok: false, message: res.status === 400 ? 'Incorrect email or password.' : (data.error_description || data.msg || 'Sign-in failed.') };
  }
  const session = sessionFromTokenResponse(data);
  if ((await checkIsAdmin(session.access_token)) === false) {
    authFetch('logout', {}, session.access_token).catch(() => {});
    return { ok: false, message: 'This account is not an administrator.' };
  }
  storeAuthSession(session);
  isAdminLoggedIn = true;
  return { ok: true };
}

/* ---- Forgotten password ----
   Supabase emails a link back to this page (the studio address, ./?studio); it arrives with
   #access_token=...&refresh_token=...&type=recovery (or #error=...&error_description=...).
   The link only comes back here if this page's address is the project's Site URL or is listed under
   Authentication > URL Configuration > Redirect URLs in Supabase. */

function passwordResetReturnUrl() {
  const { origin, pathname } = window.location;
  return `${origin}${pathname}?studio`;
}

async function requestPasswordReset(email) {
  try {
    const res = await authFetch(`recover?redirect_to=${encodeURIComponent(passwordResetReturnUrl())}`, { email });
    if (res.status === 429) return { ok: false, message: 'Too many requests. Wait a minute, then try again.' };
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      return { ok: false, message: data.error_description || data.msg || 'The reset email could not be sent.' };
    }
    return { ok: true };
  } catch (e) {
    return { ok: false, message: 'Could not reach the sign-in service. Check your connection and try again.' };
  }
}

// Reads (and removes from the address bar) what a password-reset link brought back.
// Returns null, { session } or { error }.
function takePasswordResetReturn() {
  const hash = window.location.hash.replace(/^#/, '');
  if (!hash) return null;
  const p = new URLSearchParams(hash);
  let result = null;
  if (p.get('type') === 'recovery' && p.get('access_token')) {
    result = { session: {
      access_token: p.get('access_token'),
      refresh_token: p.get('refresh_token'),
      expires_at: Date.now() + (Number(p.get('expires_in')) || 3600) * 1000,
      email: null
    } };
  } else if (p.get('error') || p.get('error_code')) {
    result = { error: (p.get('error_description') || 'The link is not valid.').replace(/\+/g, ' ') };
  }
  if (result) history.replaceState(null, '', window.location.pathname + window.location.search);
  return result;
}

async function setNewPassword(session, password) {
  try {
    const res = await authFetch('user', { password }, session.access_token, 'PUT');
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      return { ok: false, message: data.error_description || data.msg || 'The password could not be changed. Ask for a new reset link.' };
    }
    session.email = data.email || (data.user && data.user.email) || null;
    return adoptAdminSession(session);
  } catch (e) {
    return { ok: false, message: 'Could not reach the sign-in service. Check your connection and try again.' };
  }
}

async function refreshAuthSession() {
  if (!authSession || !authSession.refresh_token) return false;
  try {
    const res = await authFetch('token?grant_type=refresh_token', { refresh_token: authSession.refresh_token });
    if (!res.ok) throw new Error(`refresh failed: ${res.status}`);
    storeAuthSession(sessionFromTokenResponse(await res.json()));
    return true;
  } catch (e) {
    storeAuthSession(null);
    isAdminLoggedIn = false;
    return false;
  }
}

// A valid access token for saving, refreshed if it is about to expire; null when signed out.
async function getAdminAccessToken() {
  if (!authSession) return null;
  if (Date.now() > authSession.expires_at - 60 * 1000 && !(await refreshAuthSession())) return null;
  return authSession.access_token;
}

async function signOutAdmin() {
  const token = authSession && authSession.access_token;
  storeAuthSession(null);
  isAdminLoggedIn = false;
  if (token) authFetch('logout', {}, token).catch(() => {});
}

// On page load: pick up a session from earlier in this browser tab.
async function restoreAdminSession() {
  try {
    const raw = sessionStorage.getItem(AUTH_STORAGE_KEY);
    authSession = raw ? JSON.parse(raw) : null;
  } catch (e) {
    authSession = null;
  }
  isAdminLoggedIn = !!(await getAdminAccessToken());
}
