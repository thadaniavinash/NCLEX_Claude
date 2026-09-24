/* App start-up and view routing. Loaded last, after every other script has defined its functions. */

/* ================= INITIALIZATION & ROUTING ================= */
async function initApp() {
  let savedTheme = 'dark';
  try {
    savedTheme = localStorage.getItem('nclex_theme') || 'dark';
  } catch (e) {
    console.warn("localStorage is blocked in this context:", e);
  }
  if (savedTheme === 'light') {
    toggleTheme(true);
  } else {
    toggleTheme(false);
  }

  await loadAllData();
  initDashboardEvents();
  initSessionBuilder();
  initEditorEvents();
  initPlayerEvents();
  initResultsEvents();
  initCalculator();
  makeCalculatorDraggable();
  
  initAdminEvents();
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
    const targetCase = caseStudies.find(c => c.id === directCaseId || c.id.toLowerCase() === directCaseId.toLowerCase());
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
    const targetQ = standaloneQuestions.find(q => q.id === directStandaloneId || q.id.toLowerCase() === directStandaloneId.toLowerCase());
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
    switchView('dashboard');
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

function switchView(viewId) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const targetView = document.getElementById(`${viewId}-view`);
  if (targetView) targetView.classList.add('active');
  
  if (viewId === 'dashboard') {
    renderDashboard();
  } else if (viewId === 'student') {
    renderStudentPortal();
  }
}

function renderStudentPortal() {
  const bankStatusEl = document.getElementById('student-bank-status-text');
  if (bankStatusEl) {
    bankStatusEl.textContent = `Local Bank: ${caseStudies.length} Cases \u2022 ${standaloneQuestions.length} Standalone`;
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
