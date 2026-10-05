/* App start-up and view routing. Loaded last, after every other script has defined its functions. */

/* ================= INITIALIZATION & ROUTING ================= */
async function initApp() {
  // The editor's live preview loads this page in a frame: player only, content arrives by message.
  if (new URLSearchParams(window.location.search).get('preview') === '1') {
    initPreviewFrame();
    return;
  }

  initTheme();
  initAppShell();

  await loadAllData();
  initDashboardEvents();
  initSessionBuilder();
  initEditorEvents();
  initPlayerEvents();
  initResultsEvents();
  initAttemptSaving();
  renderStudentBankStatus();
  initShareDialog();
  initProgressEvents();
  initOverviewEvents();
  initCalculator();
  makeCalculatorDraggable();
  
  initAdminEvents();
  await restoreAdminSession();
  applyAdminState();

  // Check URL parameters for direct case study launch, exam/mode launches, or authoring
  const urlParams = new URLSearchParams(window.location.search);
  const directCaseId = urlParams.get('case') || urlParams.get('caseId') || urlParams.get('cases') || urlParams.get('id');
  const directStandaloneId = urlParams.get('standalone') || urlParams.get('question') || urlParams.get('q');
  const examMode = urlParams.get('mode');
  const examId = urlParams.get('exam');
  const isAuthorParam = urlParams.get('author') === '1' || urlParams.get('studio') === '1';

  // 1-2. A case study or question opened from a link the author shared (?case= / ?standalone=, with
  // &mode=test for exam conditions). Hidden items open too: the author decides who gets the link.
  const linkMode = (examMode === 'test' || examMode === 'exam') ? 'test' : 'review';
  const findById = (list, id) => list.find(x => x.id === id || x.id.toLowerCase() === id.toLowerCase());
  if (directCaseId) {
    const targetCase = findById(caseStudies, directCaseId);
    if (targetCase) {
      startLinkSession(targetCase, linkMode);
      return;
    }
    console.warn(`Direct launch case ID "${directCaseId}" not found in bank.`);
    showToast('This case study link does not match any case study. Check the link with your instructor.', 'error');
  }
  if (directStandaloneId) {
    const targetQ = findById(standaloneQuestions, directStandaloneId);
    if (targetQ) {
      startLinkSession(targetQ, linkMode);
      return;
    }
    console.warn(`Direct launch question ID "${directStandaloneId}" not found in bank.`);
    showToast('This question link does not match any question. Check the link with your instructor.', 'error');
  }

  // 3. Authoring or Exam Simulation Mode
  if (isAuthorParam) {
    switchView('overview');
  } else if (examMode === 'test' || examId) {
    // Launch directly into Test Mode simulation
    switchView('student');
    const testCard = document.getElementById('mode-card-test');
    if (testCard) testCard.click();
  } else {
    // Start on Student Portal
    switchView('student');
  }
}

if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}

// Screens inside the app frame (top bar + sidebar) and the area whose navigation they show.
// The exam player and the editor fill the whole window instead.
const SHELL_VIEWS = { student: 'student', progress: 'student', results: 'student', paused: 'student', overview: 'studio', dashboard: 'studio' };

function switchView(viewId) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const targetView = document.getElementById(`${viewId}-view`);
  if (targetView) targetView.classList.add('active');

  const shell = document.getElementById('app-shell');
  const area = SHELL_VIEWS[viewId];
  if (shell) {
    shell.classList.toggle('hidden', !area);
    if (area) shell.dataset.area = area;
    const navId = viewId === 'results' || viewId === 'paused' ? 'student' : viewId;
    shell.querySelectorAll('[data-nav]').forEach(b => {
      if (b.dataset.nav === navId) b.setAttribute('aria-current', 'page');
      else b.removeAttribute('aria-current');
    });
    if (targetView && area) targetView.scrollTop = 0;
  }

  if (viewId === 'dashboard') {
    renderDashboard();
  } else if (viewId === 'student') {
    renderStudentPortal();
  } else if (viewId === 'progress') {
    renderProgressView();
  } else if (viewId === 'overview') {
    renderOverview();
  }
}

function initAppShell() {
  document.querySelectorAll('#app-shell [data-nav]').forEach(btn => {
    btn.addEventListener('click', () => switchView(btn.dataset.nav));
  });
}

function renderStudentPortal() {
  renderStudentBankStatus();
  renderPortalResume();
  renderSessionTopicsList();
  renderManualSelectionLists();
  updateSessionCountsAndBounds();
}

// Top bar: how many items students can practise (or that the backup copy is showing).
function renderStudentBankStatus() {
  const bankStatusEl = document.getElementById('student-bank-status-text');
  if (bankStatusEl) {
    const counts = `${studentCaseStudies().length} case studies \u2022 ${studentStandaloneQuestions().length} questions`;
    bankStatusEl.textContent = isDatabaseUnavailable ? `Offline backup: ${counts}` : counts;
    const indicator = bankStatusEl.closest('.app-status');
    if (indicator) {
      indicator.classList.toggle('offline', isDatabaseUnavailable);
      indicator.title = (isDatabaseUnavailable ? `${bankStatusEl.textContent}. ` : '') + (isDatabaseUnavailable
        ? 'The question bank could not be reached, so a saved backup copy is shown. It may be missing the newest questions.'
        : 'Questions available to practise');
    }
  }
}

// Table toolbar, cell navigation and template hints in the authoring text boxes (js/table-tools.js)
if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', initTableTools);
} else {
  initTableTools();
}
