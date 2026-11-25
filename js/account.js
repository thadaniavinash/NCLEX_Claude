/* The person using the site: the account button in the top bar, its menu, and the sign-in page.

   Today there are two kinds of visitor: a guest (every student; progress stays in this browser, see
   js/progress.js) and the author (signed in through Supabase Auth, js/auth.js). Student accounts are
   planned (user decision, November 2026: the easiest sign-in for students, an emailed one-time code with
   no password); they would use the same top-bar button and the same sign-in page.

   The studio needs the author signed in: opening ?author=1 while signed out shows the sign-in page
   (except on the local server, which saves to cases-data.js without signing in). */

let signinReturnView = 'overview';
let passwordResetSession = null;

function setAppIdentityText() {
  document.querySelectorAll('[data-app-name]').forEach(el => { el.textContent = APP_NAME; });
  document.querySelectorAll('[data-app-tagline]').forEach(el => { el.textContent = APP_TAGLINE; });
  document.querySelectorAll('[data-trademark]').forEach(el => { el.textContent = TRADEMARK_NOTICE; });
  document.querySelectorAll('[data-brand-home]').forEach(a => { if (a.classList.contains('app-brand')) a.setAttribute('aria-label', `${APP_NAME}: home`); });
}

/* ---- Top bar account button ---- */

function renderAccountButton() {
  const avatar = document.getElementById('account-avatar');
  const name = document.getElementById('account-name');
  const sub = document.getElementById('account-sub');
  const head = document.getElementById('account-menu-head');
  if (!avatar) return;
  const email = (authSession && authSession.email) || '';
  if (isAdminLoggedIn) {
    avatar.textContent = (email[0] || 'A').toUpperCase();
    avatar.classList.add('author');
    name.textContent = 'Author';
    sub.textContent = email || 'Signed in';
    head.innerHTML = `<strong>Signed in as the author</strong><span>${escapeHTML(email)}</span>`;
  } else {
    avatar.textContent = 'G';
    avatar.classList.remove('author');
    const inStudio = document.getElementById('app-shell').dataset.area === 'studio';
    name.textContent = inStudio ? 'Not signed in' : 'Guest';
    sub.textContent = inStudio ? 'Local copy' : 'Progress saved on this device';
    head.innerHTML = inStudio
      ? '<strong>Not signed in</strong><span>On this computer the studio saves to the local copy. Sign in to save to the database.</span>'
      : '<strong>Guest</strong><span>Your results are kept in this browser only. Nothing is sent to anyone.</span>';
  }
  const show = (action, on) => {
    const el = document.querySelector(`#account-menu [data-account-action="${action}"]`);
    if (el) el.classList.toggle('hidden', !on);
  };
  show('studio', isAdminLoggedIn);
  show('signout', isAdminLoggedIn);
  // No sign-in for students yet: only the author's studio offers it (on the local server).
  show('signin', !isAdminLoggedIn && document.getElementById('app-shell').dataset.area === 'studio');
}

function setAccountMenuOpen(open) {
  const btn = document.getElementById('account-btn');
  const menu = document.getElementById('account-menu');
  if (!btn || !menu) return;
  if (open) {
    renderAccountButton();
    const theme = menu.querySelector('[data-account-theme]');
    if (theme) theme.textContent = currentTheme() === 'dark' ? 'Light theme' : 'Dark theme';
  }
  menu.classList.toggle('hidden', !open);
  btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  if (open) {
    const first = [...menu.querySelectorAll('[role="menuitem"]')].find(b => b.offsetParent !== null);
    if (first) first.focus();
  }
}

function onAccountMenuAction(action) {
  setAccountMenuOpen(false);
  if (action === 'progress') switchView('progress');
  else if (action === 'home') switchView('home');
  else if (action === 'studio') switchView('overview');
  else if (action === 'signin') openSignIn(currentShellView() || 'overview');
  else if (action === 'signout') {
    const inStudio = document.getElementById('app-shell').dataset.area === 'studio';
    signOutAdmin();
    showToast('Signed out.', 'success');
    applyAdminState();
    if (inStudio) switchView('overview'); // shows the sign-in page unless on the local server
  }
}

function currentShellView() {
  const active = document.querySelector('.view.active');
  return active ? active.id.replace(/-view$/, '') : null;
}

/* ---- Sign-in page ---- */

// The studio's pages need a signed-in author, except on the local server.
function studioNeedsSignIn() {
  return !isAdminLoggedIn && !isLocalServerHost();
}

function showSignInMode(mode) {
  ['signin', 'reset-request', 'reset-password'].forEach(m => {
    const form = document.getElementById(m === 'signin' ? 'signin-form' : `${m}-form`);
    if (form) form.classList.toggle('hidden', m !== mode);
  });
  document.querySelectorAll('.signin-msg').forEach(el => { el.classList.add('hidden'); el.textContent = ''; });
  const focus = { signin: 'signin-email', 'reset-request': 'reset-email', 'reset-password': 'reset-password' }[mode];
  if (mode === 'reset-request') {
    const email = document.getElementById('signin-email').value.trim();
    if (email) document.getElementById('reset-email').value = email;
  }
  const el = document.getElementById(focus);
  if (el) setTimeout(() => el.focus(), 0);
}

function openSignIn(returnView, mode) {
  signinReturnView = returnView || 'overview';
  const stats = document.getElementById('signin-side-stats');
  if (stats && typeof caseStudies !== 'undefined' && caseStudies.length) {
    stats.textContent = `${caseStudies.length} case studies and ${standaloneQuestions.length} stand-alone questions in the bank.`;
  }
  showSignInMode(mode || 'signin');
  document.title = `Sign in · ${APP_NAME}`;
  switchView('signin');
}

function finishSignIn(message) {
  document.getElementById('signin-password').value = '';
  showToast(message, 'success');
  document.title = `${APP_NAME} · ${APP_TAGLINE}`;
  applyAdminState();
  switchView(signinReturnView === 'signin' ? 'overview' : signinReturnView);
}

function showSignInMessage(id, text, tone) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = text;
  el.classList.toggle('error', tone !== 'ok');
  el.classList.toggle('ok', tone === 'ok');
  el.classList.remove('hidden');
}

async function withBusyButton(form, label, fn) {
  const btn = form.querySelector('button[type="submit"]');
  const old = btn.textContent;
  btn.disabled = true;
  btn.textContent = label;
  try { return await fn(); } finally { btn.disabled = false; btn.textContent = old; }
}

function initSignInPage() {
  const signinForm = document.getElementById('signin-form');
  signinForm.addEventListener('submit', async e => {
    e.preventDefault();
    const email = document.getElementById('signin-email').value.trim();
    const password = document.getElementById('signin-password').value;
    if (!email || !password) { showSignInMessage('signin-error', 'Enter your email and your password.'); return; }
    document.getElementById('signin-error').classList.add('hidden');
    const result = await withBusyButton(signinForm, 'Signing in…', () => signInAdmin(email, password));
    if (result.ok) finishSignIn('Signed in.');
    else showSignInMessage('signin-error', result.message);
  });

  const requestForm = document.getElementById('reset-request-form');
  requestForm.addEventListener('submit', async e => {
    e.preventDefault();
    const email = document.getElementById('reset-email').value.trim();
    if (!/^\S+@\S+\.\S+$/.test(email)) { showSignInMessage('reset-request-msg', 'Enter the email address of your author account.'); return; }
    const result = await withBusyButton(requestForm, 'Sending…', () => requestPasswordReset(email));
    if (result.ok) showSignInMessage('reset-request-msg', `If ${email} has an author account, a reset link is on its way. Open it on this device; it works once and expires after an hour.`, 'ok');
    else showSignInMessage('reset-request-msg', result.message);
  });

  const newForm = document.getElementById('reset-password-form');
  newForm.addEventListener('submit', async e => {
    e.preventDefault();
    const a = document.getElementById('reset-password').value;
    const b = document.getElementById('reset-password-again').value;
    if (a.length < 8) { showSignInMessage('reset-password-msg', 'Use at least 8 characters.'); return; }
    if (a !== b) { showSignInMessage('reset-password-msg', 'The two passwords are not the same.'); return; }
    if (!passwordResetSession) { showSignInMessage('reset-password-msg', 'This page has no reset link. Ask for a new one.'); return; }
    const result = await withBusyButton(newForm, 'Saving…', () => setNewPassword(passwordResetSession, a));
    if (result.ok) {
      passwordResetSession = null;
      document.getElementById('reset-password').value = '';
      document.getElementById('reset-password-again').value = '';
      finishSignIn('Password changed. You are signed in.');
    } else {
      showSignInMessage('reset-password-msg', result.message);
    }
  });

  document.getElementById('signin-view').addEventListener('click', e => {
    const modeBtn = e.target.closest('[data-signin-mode]');
    if (modeBtn) { showSignInMode(modeBtn.dataset.signinMode); return; }
    const show = e.target.closest('[data-show-password]');
    if (show) {
      const input = document.getElementById(show.dataset.showPassword);
      const visible = input.type === 'password';
      input.type = visible ? 'text' : 'password';
      show.textContent = visible ? 'Hide' : 'Show';
      show.setAttribute('aria-pressed', visible ? 'true' : 'false');
      show.setAttribute('aria-label', visible ? 'Hide password' : 'Show password');
    }
  });
}

// A password-reset link brought the author back here: returns true when the page shows the reset form.
function handlePasswordResetReturn() {
  const back = takePasswordResetReturn();
  if (!back) return false;
  if (back.session) {
    passwordResetSession = back.session;
    openSignIn('overview', 'reset-password');
  } else {
    openSignIn('overview', 'reset-request');
    showSignInMessage('reset-request-msg', `${back.error} Ask for a new reset link below.`);
  }
  return true;
}

function initAccount() {
  setAppIdentityText();
  initSignInPage();
  const btn = document.getElementById('account-btn');
  const menu = document.getElementById('account-menu');
  btn.addEventListener('click', e => {
    e.stopPropagation();
    setAccountMenuOpen(menu.classList.contains('hidden'));
  });
  menu.addEventListener('click', e => {
    const item = e.target.closest('[data-account-action]');
    if (item) onAccountMenuAction(item.dataset.accountAction);
    else if (e.target.closest('[data-theme-toggle]')) setAccountMenuOpen(false);
  });
  menu.addEventListener('keydown', e => {
    const items = [...menu.querySelectorAll('[role="menuitem"]')].filter(b => b.offsetParent !== null);
    const i = items.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); items[(i + 1) % items.length].focus(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); items[(i - 1 + items.length) % items.length].focus(); }
  });
  document.addEventListener('click', e => {
    if (!menu.classList.contains('hidden') && !e.target.closest('.account')) setAccountMenuOpen(false);
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !menu.classList.contains('hidden')) { setAccountMenuOpen(false); btn.focus(); }
  });
  document.querySelectorAll('[data-brand-home]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    const inStudio = a.closest('#app-shell') && document.getElementById('app-shell').dataset.area === 'studio';
    switchView(inStudio ? 'overview' : 'home');
  }));
}
