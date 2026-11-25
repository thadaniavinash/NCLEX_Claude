/* App start-up and view routing. Loaded last, after every other script has defined its functions. */

/* ================= INITIALIZATION & ROUTING ================= */
async function initApp() {
  // The editor's live preview loads this page in a frame: player only, content arrives by message.
  if (new URLSearchParams(window.location.search).get('preview') === '1') {
    initPreviewFrame();
    return;
  }

  initTheme();
  initRouter();
  initAppShell();
  initAccount();

  await loadAllData();
  initDashboardEvents();
  initSessionBuilder();
  initEditorEvents();
  initPlayerEvents();
  initResultsEvents();
  initAttemptSaving();
  initHome();
  initShareDialog();
  initProgressEvents();
  initOverviewEvents();
  initCalculator();
  makeCalculatorDraggable();
  
  await restoreAdminSession();
  applyAdminState();

  startRouting();
  // Back from a password-reset email (js/account.js).
  if (handlePasswordResetReturn()) return;

  // Check URL parameters for direct case study launch, exam/mode launches, or authoring
  const urlParams = new URLSearchParams(window.location.search);
  const directCaseId = urlParams.get('case') || urlParams.get('caseId') || urlParams.get('cases') || urlParams.get('id');
  const directStandaloneId = urlParams.get('standalone') || urlParams.get('question') || urlParams.get('q');
  const examMode = urlParams.get('mode');
  const examId = urlParams.get('exam');
  const isAuthorParam = isStudioAddress(urlParams);
  const codeParam = urlParams.get('code');

  // 1-2. A case study or question opened from a link the author shared (?case= / ?standalone=, with
  // &mode=test for exam conditions). Hidden items open too: the author decides who gets the link.
  const linkMode = (examMode === 'test' || examMode === 'exam') ? 'test' : 'review';
  const findById = (list, id) => list.find(x => x.id === id || x.id.toLowerCase() === id.toLowerCase());
  if (directCaseId) {
    const targetCase = findById(caseStudies, directCaseId);
    if (targetCase) {
      markInitialLinkEntry();
      startLinkSession(targetCase, linkMode);
      return;
    }
    console.warn(`Direct launch case ID "${directCaseId}" not found in bank.`);
    showToast('This case study link does not match any case study. Check the link with your instructor.', 'error');
  }
  if (directStandaloneId) {
    const targetQ = findById(standaloneQuestions, directStandaloneId);
    if (targetQ) {
      markInitialLinkEntry();
      startLinkSession(targetQ, linkMode);
      return;
    }
    console.warn(`Direct launch question ID "${directStandaloneId}" not found in bank.`);
    showToast('This question link does not match any question. Check the link with your instructor.', 'error');
  }

  // ?code=C-7KD4M (a code in a link) opens like a code typed on Home.
  if (codeParam) {
    const req = parseOpenRequest(codeParam);
    if (req.items.length && !req.unknown.length) {
      markInitialLinkEntry();
      if (req.items.length === 1) startLinkSession(req.items[0], linkMode);
      else startCompiledSession(req.items.filter(i => !isStandaloneItem(i)), req.items.filter(isStandaloneItem), linkMode);
      return;
    }
    showToast('This code does not match any case study or question. Check it with your instructor.', 'error');
  }

  // 3. The page the address names (js/router.js: Home, My progress, Practise, the studio), or Practise in
  // exam mode for the old ?mode=test address.
  if (isAuthorParam) {
    switchView(viewFromUrl());
  } else if ((examMode === 'test' || examId) && studentPortalOpenForViewer()) {
    switchView('student');
    const testCard = document.getElementById('mode-card-test');
    if (testCard) testCard.click();
  } else if (urlParams.get('signin') === '1') {
    openSignIn('overview');
  } else {
    switchView(viewFromUrl());
  }
}

if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}

// Screens inside the app frame (top bar + sidebar) and the area whose navigation they show.
// The exam player and the editor fill the whole window instead.
const SHELL_VIEWS = { home: 'student', student: 'student', progress: 'student', results: 'student', paused: 'student', overview: 'studio', dashboard: 'studio' };

// Whether this visitor may use the Practise page (see STUDENT_PORTAL_OPEN in js/state.js).
function studentPortalOpenForViewer() {
  return STUDENT_PORTAL_OPEN || isAdminLoggedIn || isLocalServerHost();
}

function switchView(viewId) {
  // Practise (the session builder) is closed to students for now: they stay on Home.
  if (viewId === 'student' && !studentPortalOpenForViewer()) viewId = 'home';
  // The studio needs the author signed in (except on the local server): show the sign-in page.
  if ((viewId === 'overview' || viewId === 'dashboard') && studioNeedsSignIn()) {
    signinReturnView = viewId;
    if (currentShellView() !== 'signin') { openSignIn(viewId); return; }
    viewId = 'signin';
  }
  if (typeof setAccountMenuOpen === 'function') setAccountMenuOpen(false);
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const targetView = document.getElementById(`${viewId}-view`);
  if (targetView) targetView.classList.add('active');

  const shell = document.getElementById('app-shell');
  const area = SHELL_VIEWS[viewId];
  if (shell) {
    shell.classList.toggle('hidden', !area);
    if (area) shell.dataset.area = area;
    const navId = ['results', 'paused'].includes(viewId) ? 'home' : viewId;
    shell.querySelectorAll('[data-nav]').forEach(b => {
      if (b.dataset.nav === navId) b.setAttribute('aria-current', 'page');
      else b.removeAttribute('aria-current');
    });
    if (targetView && area) targetView.scrollTop = 0;
  }
  if (typeof renderAccountButton === 'function') renderAccountButton();
  if (viewId !== 'signin') document.title = `${APP_NAME} · ${APP_TAGLINE}`;
  recordViewInHistory(viewId);

  if (viewId === 'dashboard') {
    renderDashboard();
  } else if (viewId === 'student') {
    renderStudentPortal();
  } else if (viewId === 'home') {
    renderHomeView();
  } else if (viewId === 'progress') {
    renderAuthorPreviewNote(document.getElementById('progress-preview-note'));
    renderProgressView();
  } else if (viewId === 'overview') {
    renderOverview();
  }
}

function initAppShell() {
  // Buttons and links that open another page of the app (data-nav-to="progress", "overview", ...).
  document.addEventListener('click', e => {
    const nav = e.target.closest('[data-nav-to]');
    if (nav) { e.preventDefault(); switchView(nav.dataset.navTo); }
  });
  document.querySelectorAll('#app-shell [data-nav]').forEach(btn => {
    btn.addEventListener('click', () => switchView(btn.dataset.nav));
  });
}

function renderStudentPortal() {
  renderPractiseNavState();
  renderAuthorPreviewNote(document.getElementById('portal-preview-note'));
  renderPortalResume();
  renderSessionTopicsList();
  renderManualSelectionLists();
  updateSessionCountsAndBounds();
}

// Table toolbar, cell navigation and template hints in the authoring text boxes (js/table-tools.js)
if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', initTableTools);
} else {
  initTableTools();
}
