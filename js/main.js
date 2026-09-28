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

  // 1. Direct Case Study Launch (for LMS links)
  if (directCaseId) {
    const targetCase = studentCaseStudies().find(c => c.id === directCaseId || c.id.toLowerCase() === directCaseId.toLowerCase());
    if (targetCase) {
      const targetMode = examMode === 'test' ? 'test' : 'review';
      startPlayer(targetCase, {
        mode: targetMode,
        isRemediation: false,
        allowBacktrack: targetMode !== 'test'
      });
      return;
    } else {
      console.warn(`Direct launch case ID "${directCaseId}" not found in bank.`);
      showToast(`Case Study "${directCaseId}" not found. Showing main portal.`, 'error');
    }
  }

  // 2. Direct Stand-alone Question Launch (for LMS links)
  if (directStandaloneId) {
    const targetQ = studentStandaloneQuestions().find(q => q.id === directStandaloneId || q.id.toLowerCase() === directStandaloneId.toLowerCase());
    if (targetQ) {
      const targetMode = examMode === 'test' ? 'test' : 'review';
      startPlayer(targetQ, {
        mode: targetMode,
        isRemediation: false,
        allowBacktrack: targetMode !== 'test'
      });
      return;
    } else {
      console.warn(`Direct launch question ID "${directStandaloneId}" not found in bank.`);
      showToast(`Question "${directStandaloneId}" not found. Showing main portal.`, 'error');
    }
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
const SHELL_VIEWS = { student: 'student', progress: 'student', results: 'student', overview: 'studio', dashboard: 'studio' };

function switchView(viewId) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const targetView = document.getElementById(`${viewId}-view`);
  if (targetView) targetView.classList.add('active');

  const shell = document.getElementById('app-shell');
  const area = SHELL_VIEWS[viewId];
  if (shell) {
    shell.classList.toggle('hidden', !area);
    if (area) shell.dataset.area = area;
    const navId = viewId === 'results' ? 'student' : viewId;
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
  renderSessionTopicsList();
  renderManualSelectionLists();
  updateSessionCountsAndBounds();
}

// Run initializer on window load
if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', setupTableInteractionMenu);
} else {
  setupTableInteractionMenu();
}
