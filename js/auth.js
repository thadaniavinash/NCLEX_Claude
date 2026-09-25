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

function authFetch(path, body, token) {
  return fetch(`${SUPABASE_URL}/auth/v1/${path}`, {
    method: 'POST',
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
