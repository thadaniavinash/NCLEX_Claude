/* ================= STATE & STATE INITIALIZATION ================= */
const PATHOPHYSIOLOGY_DISORDERS = [
  "Blood Disorders",
  "Cardiovascular Disorders",
  "EENT Disorders",
  "Endocrine Disorders",
  "Fluid/Electrolyte/Acid-Base Disorders",
  "Genetic and Developmental Disorders",
  "GI Disorders",
  "Immune disorders",
  "Integumentary Disorders and Burns",
  "Leukemias and Lymphomas",
  "Musculoskeletal Disorders",
  "Neoplasia",
  "Neurological Disorders",
  "Others",
  "Reproductive Disorders",
  "Respiratory Disorders",
  "Urinary Disorders"
];

const CURRICULUM_COURSES = {
  "NURS 1017": [
    "Unit 1 (Introduction to Pathophysiology)",
    "Unit 2 (Cellular Basis of Disease)",
    "Unit 3 (Genetic and Developmental Disorders)",
    "Unit 4 (Neoplasia)",
    "Unit 5 (Integumentary Disorders and Burns)",
    "Unit 6 (Musculoskeletal Disorders)",
    "Unit 7 (Neurological Disorders)",
    "Unit 8 (Pain)",
    "Unit 9 (Disorders of the Eyes and Ears)",
    "Unit 10 (Stress and Disease)",
    "Unit 11 (Endocrine Disorders)"
  ],
  "NURS 1021": [
    "Unit 1 (Blood Disorders)",
    "Unit 2 (Cardiovascular Disorders)",
    "Unit 3 (Respiratory Disorders)",
    "Unit 4 (Inflammation and Immune Disorders)",
    "Unit 5 (Leukemias and Lymphomas)",
    "Unit 6 (Gastrointestinal Disorders)",
    "Unit 7 (Urinary Disorders)",
    "Unit 8 (Fluid, Electrolytes, and Acid-Base Imbalances)",
    "Unit 9 (Reproductive Disorders)"
  ]
};

let authorCurrentTab = 'cases'; // 'cases' | 'standalone'
let authorCourseFilter = 'ALL';
let authorUnitFilter = 'ALL';
let authorSearchQuery = '';

let studentCourseFilter = 'ALL';
let studentUnitFilter = 'ALL';

let caseStudies = [];
let standaloneQuestions = [];
// True when a ?cases= or ?standalone= link loaded only part of the bank. Saving
// would then overwrite the full bank with that subset, so saves are refused.
let isBankFiltered = false;
let currentCase = null;
let currentStepIndex = 0; // For Editor
let activeTabId = ''; // For Editor active tab
let highlightActiveTabId = ''; // For Editor active highlight tab
let playerStepIndex = 0; // For Player
let playerActiveTabId = ''; // For Player active tab
let playerHighlightActiveTabId = ''; // For Player active highlight tab
let activeDashboardTab = 'cases'; // 'cases', 'standalone', 'generator'
let isCasesFolderExpanded = false;
let isStandaloneFolderExpanded = false;
let activeCasesDisorderFilter = '';
let activeStandaloneDisorderFilter = '';
let isAdminLoggedIn = (typeof sessionStorage !== 'undefined') ? (sessionStorage.getItem('isAdmin') === 'true') : false;

// Player interaction tracking
let playerAnswers = {}; // { stepIndex: answersObject }
let submittedAnswers = {}; // { stepIndex: boolean }
let playerScores = {}; // { stepIndex: { score: X, max: Y } }
let sessionConfig = {
  mode: 'review', // 'review' | 'test'
  isRemediation: false, // true during post-exam review
  allowBacktrack: true
};

// Calculator state
let calcInput = '0';
let calcPrevInput = null;
let calcOp = null;
let calcMemory = 0;
let calcResetOnNext = false;
let mrcPressCount = 0;
let clearPressCount = 0;

// IndexedDB database reference
const DB_NAME = 'NCLEX_STUDIO_DB';
const DB_VERSION = 1;
let db = null;

function initDatabase() {
  return new Promise((resolve) => {
    try {
      const request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onerror = (e) => {
        console.warn("IndexedDB failed to open, falling back to localStorage", e);
        resolve(null);
      };
      request.onsuccess = (e) => {
        db = e.target.result;
        resolve(db);
      };
      request.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains('case_studies')) {
          db.createObjectStore('case_studies', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('standalone_questions')) {
          db.createObjectStore('standalone_questions', { keyPath: 'id' });
        }
      };
    } catch (err) {
      console.warn("IndexedDB not supported, falling back to localStorage", err);
      resolve(null);
    }
  });
}

function getAllFromStore(storeName) {
  return new Promise((resolve) => {
    if (!db) {
      resolve([]);
      return;
    }
    try {
      const transaction = db.transaction(storeName, 'readonly');
      const store = transaction.objectStore(storeName);
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result || []);
      request.onerror = () => resolve([]);
    } catch (err) {
      console.error(`Error reading from store ${storeName}:`, err);
      resolve([]);
    }
  });
}

function putInStore(storeName, item) {
  if (!db) return;
  try {
    const transaction = db.transaction(storeName, 'readwrite');
    const store = transaction.objectStore(storeName);
    store.put(item);
  } catch (err) {
    console.error(`Error writing to store ${storeName}:`, err);
  }
}

function deleteFromStore(storeName, id) {
  if (!db) return;
  try {
    const transaction = db.transaction(storeName, 'readwrite');
    const store = transaction.objectStore(storeName);
    store.delete(id);
  } catch (err) {
    console.error(`Error deleting from store ${storeName}:`, err);
  }
}

/* ================= TOAST NOTIFICATION UTILITY ================= */
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) reverse forwards';
    toast.addEventListener('animationend', () => toast.remove());
  }, 3000);
}

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

// Question content is authored HTML (tables, bold, notes) and is rendered with
// innerHTML, while the database accepts writes from anyone holding the public key.
// Strip anything that can run script before the content is used anywhere.
const UNSAFE_TAGS = 'script, iframe, frame, frameset, object, embed, applet, link, meta, base, form, style, noscript, template';
const UNSAFE_URL = /^\s*(javascript|vbscript|data:text\/html)/i;

function sanitizeRichText(html) {
  if (typeof html !== 'string' || !html.includes('<')) return html;
  const tpl = document.createElement('template'); // parses inertly: no scripts run, nothing loads
  tpl.innerHTML = html;
  let changed = false;
  tpl.content.querySelectorAll(UNSAFE_TAGS).forEach(el => { el.remove(); changed = true; });
  tpl.content.querySelectorAll('*').forEach(el => {
    Array.from(el.attributes).forEach(attr => {
      const name = attr.name.toLowerCase();
      if (name.startsWith('on') || name === 'srcdoc' ||
          (['href', 'src', 'action', 'formaction', 'xlink:href'].includes(name) && UNSAFE_URL.test(attr.value))) {
        el.removeAttribute(attr.name);
        changed = true;
      }
    });
  });
  // Only re-serialize when something was removed, so safe content stays exactly as authored.
  return changed ? tpl.innerHTML : html;
}

function sanitizeItemContent(value) {
  if (typeof value === 'string') return sanitizeRichText(value);
  if (Array.isArray(value)) return value.map(sanitizeItemContent);
  if (value && typeof value === 'object') {
    Object.keys(value).forEach(k => { value[k] = sanitizeItemContent(value[k]); });
  }
  return value;
}

function migrateCaseTypes(c) {
  if (!c || !c.screens) return;
  sanitizeItemContent(c);
  c.screens.forEach(screen => {
    if (screen.question && screen.question.type) {
      const t = screen.question.type;
      if (t === 'sata') screen.question.type = 'select_all';
      else if (t === 'matrix') screen.question.type = 'matrix_mc';
      else if (t === 'cloze') screen.question.type = 'dropdown_cloze';
      else if (t === 'single') screen.question.type = 'multiple_choice';
      else if (t === 'selectN') screen.question.type = 'select_n';
    }
    if (screen.question) {
      migrateLegacyDropdownCloze(screen.question);
      migrateLegacyHighlightText(screen.question, `ht_${c.id}_${screen.step}`);
      migratePlainTextLineBreaks(screen.question);
    }
  });
}

// Rationales are rendered as HTML, so plain "\n" line breaks (used by numbered
// "1. ... 2. ..." rationales) collapse into one paragraph. Convert them to <br>
// when the rationale has no HTML block structure of its own.
function migratePlainTextLineBreaks(q) {
  const text = q.explanation;
  if (typeof text !== 'string' || !text.includes('\n') || /<(br|p|div|li|ul|ol|table)\b/i.test(text)) return;
  q.explanation = text.trim().replace(/\r?\n/g, '<br>');
}

// Older highlight questions kept their passage in `highlightText`; the player and
// editor now use `highlightTabs`. Convert once on load with a stable tab id, rather
// than letting the player rewrite the question every time it is displayed.
function migrateLegacyHighlightText(q, tabId) {
  if ((q.type !== 'highlight' && q.type !== 'highlight_2') || q.highlightTabs || typeof q.highlightText !== 'string') return;
  q.highlightTabs = [{ id: tabId, title: "Nurses' Notes", content: q.highlightText }];
}

// Older drop-down questions were stored as
//   dropdown_cloze: { sentences: ['... [drp1] ...'], dropdowns: [{ id, options: ['...'], correctIndex }] }
// but the player and editor read
//   cloze: { text: '... [[drop0]] ...', dropdowns: [{ placeholder, options: [{ text, correct }] }] }
// Convert on load so those questions show their drop-downs.
function migrateLegacyDropdownCloze(q) {
  const legacy = q.dropdown_cloze;
  if (!legacy || typeof legacy !== 'object' || q.cloze) return;
  const dropdowns = legacy.dropdowns || [];
  const slotById = {};
  dropdowns.forEach((d, i) => { slotById[d.id] = i; });
  const text = (legacy.sentences || []).map(s => String(s).trim()).join(' ')
    .replace(/\[(\w+)\]/g, (m, id) => (id in slotById ? `[[drop${slotById[id]}]]` : m));
  q.cloze = {
    text,
    dropdowns: dropdowns.map(d => ({
      placeholder: 'Select...',
      options: (d.options || []).map((opt, i) => ({ text: String(opt), correct: i === d.correctIndex }))
    }))
  };
  delete q.dropdown_cloze;
}

const SUPABASE_URL = 'https://taprukpiubqsckahocaz.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_V1u7recZMcdc2-DXhoMwoQ_BEVWej3g';
// NCLEX_Claude is an experimental copy: keep it disconnected from the original
// app's Supabase database so nothing here can read stale or overwrite live data.
// Content is loaded from cases-data.js in this repository instead.
const USE_SUPABASE = false;

async function loadAllData() {
  // Try fetching from Supabase database
  let loadedFromSupabase = false;
  if (USE_SUPABASE) try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/nclex_data?select=key,data`, {
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
      }
    });
    if (response.ok) {
      const records = await response.json();
      const casesRecord = records.find(r => r.key === 'cases');
      const standaloneRecord = records.find(r => r.key === 'standalone');
      
      if (casesRecord) {
        caseStudies = casesRecord.data || [];
        caseStudies.forEach(migrateCaseTypes);
      }
      if (standaloneRecord) {
        standaloneQuestions = standaloneRecord.data || [];
        standaloneQuestions.forEach(migrateCaseTypes);
      }
      loadedFromSupabase = true;
    } else {
      console.warn('Supabase fetch failed, falling back to local files/storage.', response.status);
    }
  } catch (err) {
    console.error('Error fetching from Supabase:', err);
  }

  // Fallback if Supabase fetch failed (or returned nothing)
  if (!loadedFromSupabase) {
    if (window.NCLEX_CASES && window.NCLEX_CASES.length > 0) {
      caseStudies = window.NCLEX_CASES;
      caseStudies.forEach(migrateCaseTypes);
    } else {
      await initDatabase();
      if (db) {
        caseStudies = await getAllFromStore('case_studies');
        caseStudies.forEach(migrateCaseTypes);
      } else {
        let stored = null;
        try {
          stored = localStorage.getItem('nclex_cases');
        } catch (e) {
          console.warn("localStorage is blocked:", e);
        }
        if (stored) {
          try {
            caseStudies = JSON.parse(stored);
            caseStudies.forEach(migrateCaseTypes);
          } catch (e) {
            console.error("Error reading from localStorage", e);
            caseStudies = [];
          }
        }
      }
    }

    if (window.NCLEX_STANDALONE && window.NCLEX_STANDALONE.length > 0) {
      standaloneQuestions = window.NCLEX_STANDALONE;
      standaloneQuestions.forEach(migrateCaseTypes);
    } else {
      await initDatabase();
      if (db) {
        standaloneQuestions = await getAllFromStore('standalone_questions');
        standaloneQuestions.forEach(migrateCaseTypes);
      } else {
        let storedStandalone = null;
        try {
          storedStandalone = localStorage.getItem('nclex_standalone');
        } catch (e) {
          console.warn("localStorage is blocked:", e);
        }
        if (storedStandalone) {
          try {
            standaloneQuestions = JSON.parse(storedStandalone);
            standaloneQuestions.forEach(migrateCaseTypes);
          } catch (e) {
            console.error("Error reading standalone from localStorage", e);
            standaloneQuestions = [];
          }
        }
      }
    }
  }

  // Apply query parameter filtering if specified in the URL (e.g. ?cases=id1,id2)
  const urlParams = new URLSearchParams(window.location.search);
  const casesFilter = urlParams.get('cases');
  if (casesFilter) {
    const allowedIds = casesFilter.split(',');
    caseStudies = caseStudies.filter(c => allowedIds.includes(c.id));
    isBankFiltered = true;
  }
  const standaloneFilter = urlParams.get('standalone');
  if (standaloneFilter) {
    const allowedIds = standaloneFilter.split(',');
    standaloneQuestions = standaloneQuestions.filter(q => allowedIds.includes(q.id));
    isBankFiltered = true;
  }
}

function refuseSaveIfBankFiltered() {
  if (!isBankFiltered) return false;
  showToast('Saving is disabled on filtered links. Open the app without ?cases= or ?standalone= to edit.', 'error');
  return true;
}

async function saveToLocalBackend(cases, standalone) {
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  if (!isLocal) return false;
  try {
    const res = await fetch('/api/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cases, standalone })
    });
    if (res.ok) {
      return true;
    }
  } catch (e) {
    console.warn('[LOCAL SERVER] /api/save unavailable:', e.message);
  }
  return false;
}

function downloadBlob(content, filename, contentType) {
  const blob = new Blob([content], { type: contentType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  showToast(`Exported ${filename}!`);
}

// The app loads from the database, or from cases-data.js when none is connected,
// so a save that only reached browser storage will not appear after a reload.
function showSaveResult(savedToLocalServer, savedToSupabase) {
  if (savedToLocalServer) {
    showToast("Saved directly to cases-data.js on your hard drive!");
  } else if (savedToSupabase) {
    showToast("Changes saved to cloud database.");
  } else {
    showToast("Not saved permanently: no database is connected, so this change will be lost when the page reloads.", "warning");
  }
}

async function saveCasesToStorage() {
  if (refuseSaveIfBankFiltered()) return;
  // 1. IndexedDB / localStorage fallback
  if (db) {
    caseStudies.forEach(c => putInStore('case_studies', c));
  } else {
    try {
      localStorage.setItem('nclex_cases', JSON.stringify(caseStudies));
    } catch (e) {
      console.warn("localStorage is blocked:", e);
    }
  }

  // 2. Direct save to Local Server if running locally
  const savedToLocalServer = await saveToLocalBackend(caseStudies, standaloneQuestions);

  // 3. Push updates to Supabase
  let savedToSupabase = false;
  if (USE_SUPABASE) try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/nclex_data?key=eq.cases`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
      },
      body: JSON.stringify({ data: caseStudies })
    });
    if (response.ok) {
      savedToSupabase = true;
    }
  } catch (err) {
    console.error('Error saving cases to Supabase:', err);
  }

  showSaveResult(savedToLocalServer, savedToSupabase);
}

async function saveStandaloneToStorage() {
  if (refuseSaveIfBankFiltered()) return;
  // 1. IndexedDB / localStorage fallback
  if (db) {
    standaloneQuestions.forEach(q => putInStore('standalone_questions', q));
  } else {
    try {
      localStorage.setItem('nclex_standalone', JSON.stringify(standaloneQuestions));
    } catch (e) {
      console.warn("localStorage is blocked:", e);
    }
  }

  // 2. Direct save to Local Server if running locally
  const savedToLocalServer = await saveToLocalBackend(caseStudies, standaloneQuestions);

  // 3. Push updates to Supabase
  let savedToSupabase = false;
  if (USE_SUPABASE) try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/nclex_data?key=eq.standalone`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
      },
      body: JSON.stringify({ data: standaloneQuestions })
    });
    if (response.ok) {
      savedToSupabase = true;
    }
  } catch (err) {
    console.error('Error saving standalone to Supabase:', err);
  }

  showSaveResult(savedToLocalServer, savedToSupabase);
}

function saveCurrentCaseOrStandalone() {
  if (currentCase) {
    if (currentCase.isStandalone) {
      saveStandaloneToStorage();
    } else {
      saveCasesToStorage();
    }
  }
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

/* ================= DASHBOARD ENGINE (FACULTY AUTHORING PORTAL) ================= */
function initDashboardEvents() {
  const authorToStudentBtn = document.getElementById('author-to-student-btn');
  if (authorToStudentBtn) {
    authorToStudentBtn.addEventListener('click', () => switchView('student'));
  }

  const tabCases = document.getElementById('author-tab-cases');
  const tabStandalone = document.getElementById('author-tab-standalone');
  if (tabCases) {
    tabCases.addEventListener('click', () => switchAuthorTab('cases'));
  }
  if (tabStandalone) {
    tabStandalone.addEventListener('click', () => switchAuthorTab('standalone'));
  }

  const createBtn = document.getElementById('create-btn');
  if (createBtn) {
    createBtn.addEventListener('click', () => {
      if (authorCurrentTab === 'cases') {
        createNewCase();
      } else {
        createStandaloneQuestion();
      }
    });
  }

  const courseFilter = document.getElementById('author-course-filter');
  if (courseFilter) {
    courseFilter.addEventListener('change', (e) => {
      authorCourseFilter = e.target.value;
      updateAuthorUnitFilterOptions();
      applyAuthorTableFilters();
    });
  }

  const unitFilter = document.getElementById('author-unit-filter');
  if (unitFilter) {
    unitFilter.addEventListener('change', (e) => {
      authorUnitFilter = e.target.value;
      applyAuthorTableFilters();
    });
  }

  const tableSearch = document.getElementById('author-table-search');
  if (tableSearch) {
    tableSearch.addEventListener('input', (e) => {
      authorSearchQuery = e.target.value.toLowerCase().trim();
      applyAuthorTableFilters();
    });
  }
}

function switchAuthorTab(tab) {
  authorCurrentTab = tab;
  const tabCases = document.getElementById('author-tab-cases');
  const tabStandalone = document.getElementById('author-tab-standalone');
  const casesTableView = document.getElementById('author-cases-table-view');
  const standaloneTableView = document.getElementById('author-standalone-table-view');
  const createLabel = document.getElementById('create-btn-label');

  if (tab === 'cases') {
    if (tabCases) tabCases.classList.add('active');
    if (tabStandalone) tabStandalone.classList.remove('active');
    if (casesTableView) casesTableView.classList.remove('hidden');
    if (standaloneTableView) standaloneTableView.classList.add('hidden');
    if (createLabel) createLabel.textContent = 'Create New Case Study';
  } else {
    if (tabStandalone) tabStandalone.classList.add('active');
    if (tabCases) tabCases.classList.remove('active');
    if (standaloneTableView) standaloneTableView.classList.remove('hidden');
    if (casesTableView) casesTableView.classList.add('hidden');
    if (createLabel) createLabel.textContent = 'Create New Stand-alone Question';
  }

  applyAuthorTableFilters();
}

function updateAuthorUnitFilterOptions() {
  const unitFilter = document.getElementById('author-unit-filter');
  if (!unitFilter) return;

  const currentVal = authorUnitFilter;
  let html = '<option value="ALL">All Units</option>';

  if (authorCourseFilter === 'ALL') {
    html += `
      <optgroup label="NURS 1017 (Pathophysiology 1)">
        ${CURRICULUM_COURSES["NURS 1017"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
      <optgroup label="NURS 1021 (Pathophysiology 2)">
        ${CURRICULUM_COURSES["NURS 1021"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
      <optgroup label="Other Topics">
        <option value="Others">Others (Unassigned)</option>
      </optgroup>
    `;
  } else if (authorCourseFilter === 'NURS 1017') {
    html += `
      <optgroup label="NURS 1017 (Pathophysiology 1)">
        ${CURRICULUM_COURSES["NURS 1017"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
    `;
  } else if (authorCourseFilter === 'NURS 1021') {
    html += `
      <optgroup label="NURS 1021 (Pathophysiology 2)">
        ${CURRICULUM_COURSES["NURS 1021"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
    `;
  } else if (authorCourseFilter === 'Others') {
    html += '<option value="Others">Others (Unassigned)</option>';
  }

  unitFilter.innerHTML = html;
  const exists = Array.from(unitFilter.options).some(opt => opt.value === currentVal);
  if (exists) {
    unitFilter.value = currentVal;
  } else {
    authorUnitFilter = 'ALL';
    unitFilter.value = 'ALL';
  }
}

function renderDashboard() {
  // 1. Calculate KPI Summary Metrics
  const totalCases = caseStudies.length;
  const totalScreens = caseStudies.reduce((sum, c) => sum + (c.screens ? c.screens.length : 0), 0);
  const totalStandalone = standaloneQuestions.length;

  const count1017 = caseStudies.filter(c => c.course === 'NURS 1017').length +
                    standaloneQuestions.filter(q => q.course === 'NURS 1017').length;

  const count1021 = caseStudies.filter(c => c.course === 'NURS 1021').length +
                    standaloneQuestions.filter(q => q.course === 'NURS 1021').length;

  // 2. Update KPI Elements in DOM
  const kpiCasesCount = document.getElementById('author-kpi-cases-count');
  const kpiCasesScreens = document.getElementById('author-kpi-cases-screens');
  const kpiStandaloneCount = document.getElementById('author-kpi-standalone-count');
  const kpi1017Count = document.getElementById('author-kpi-1017-count');
  const kpi1021Count = document.getElementById('author-kpi-1021-count');

  if (kpiCasesCount) kpiCasesCount.textContent = `${totalCases} Cases`;
  if (kpiCasesScreens) kpiCasesScreens.textContent = `${totalScreens} Unfolding Clinical Screens`;
  if (kpiStandaloneCount) kpiStandaloneCount.textContent = `${totalStandalone} Questions`;
  if (kpi1017Count) kpi1017Count.textContent = `${count1017} Items`;
  if (kpi1021Count) kpi1021Count.textContent = `${count1021} Items`;

  // 3. Update Tab Badges
  const tabCasesBadge = document.getElementById('author-tab-cases-badge');
  const tabStandaloneBadge = document.getElementById('author-tab-standalone-badge');
  if (tabCasesBadge) tabCasesBadge.textContent = totalCases;
  if (tabStandaloneBadge) tabStandaloneBadge.textContent = totalStandalone;

  // 4. Render Tables
  renderAuthorCasesTable();
  renderAuthorStandaloneTable();
  applyAuthorTableFilters();
}

function renderAuthorCasesTable() {
  const tbody = document.getElementById('author-cases-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (caseStudies.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:32px; color:#64748b; font-style:italic;">No case studies available. Click "Create New Case Study" to begin.</td></tr>`;
    return;
  }

  caseStudies.forEach(c => {
    const tr = document.createElement('tr');
    tr.className = 'author-case-row';
    tr.dataset.course = c.course || 'Others';
    tr.dataset.unit = c.unit || c.topic || 'Others';
    tr.dataset.id = c.id;
    tr.dataset.title = (c.title || '').toLowerCase();
    tr.dataset.desc = (c.description || '').toLowerCase();

    const courseBadge = c.course === 'NURS 1017'
      ? `<span class="badge-course-1017">NURS 1017</span>`
      : c.course === 'NURS 1021'
        ? `<span class="badge-course-1021">NURS 1021</span>`
        : `<span class="badge-course-other">Unassigned</span>`;

    const unitBadge = `<span class="badge-unit">${escapeHTML(c.unit || c.topic || 'Others')}</span>`;
    const screensCount = c.screens ? c.screens.length : 0;
    const screensBadge = `<span class="badge-screens">${screensCount} Screens</span>`;

    tr.innerHTML = `
      <td>
        <div class="author-scenario-title">${escapeHTML(c.title || 'Untitled Case')}</div>
        <div class="author-scenario-desc">${escapeHTML(c.description || 'No description.')}</div>
        <span class="author-scenario-id card-id-badge" data-id="${c.id}" title="Click to copy direct LMS link for students"><svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-1px; margin-right:3px;"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>ID: ${escapeHTML(c.id)}</span>
      </td>
      <td>${courseBadge}</td>
      <td>${unitBadge}</td>
      <td>${screensBadge}</td>
      <td class="author-actions-cell">
        <div class="author-actions-wrapper">
          <button class="btn-author-edit edit-case-btn" data-id="${c.id}">Edit</button>
          <button class="btn-author-launch play-case-btn" data-id="${c.id}">Launch</button>
          <button class="btn-author-delete delete-case-btn" data-id="${c.id}">Delete</button>
        </div>
      </td>
    `;

    tr.querySelector('.edit-case-btn').addEventListener('click', () => startEditor(c));
    tr.querySelector('.play-case-btn').addEventListener('click', () => startPlayer(c));
    tr.querySelector('.delete-case-btn').addEventListener('click', () => {
      const caseTitle = c.title || 'Untitled Case';
      if (confirm(`Are you sure you want to delete case study "${caseTitle}"? This action cannot be undone.`)) {
        caseStudies = caseStudies.filter(x => x.id !== c.id);
        saveCasesToStorage();
        if (db) deleteFromStore('case_studies', c.id);
        showToast(`Case study "${caseTitle}" deleted.`);
        renderDashboard();
      }
    });

    tr.querySelector('.card-id-badge').addEventListener('click', (e) => {
      e.stopPropagation();
      const baseUrl = window.location.protocol.startsWith('http')
        ? (window.location.origin + window.location.pathname)
        : 'https://thadaniavinash.github.io/NCLEX/';
      const directUrl = `${baseUrl}?case=${encodeURIComponent(c.id)}`;
      navigator.clipboard.writeText(directUrl);
      showToast(`Copied LMS link for "${c.title}"!`);
    });

    tbody.appendChild(tr);
  });
}

function getQuestionTypeLabel(type) {
  const mapping = {
    'dropdown_cloze': 'Drop-Down Cloze',
    'drag_drop_cloze': 'Drag-and-Drop Cloze',
    'dropdown_table': 'Drop-Down Table',
    'matrix_mc': 'Matrix Multiple Choice',
    'select_n': 'Select N Multiple Response',
    'bowtie': 'Bowtie',
    'multiple_choice': 'Multiple Choice',
    'fill_blank': 'Fill-in-the-Blank',
    'hotspot': 'Hotspot',
    'ordered_response': 'Ordered Response',
    'select_all': 'Select All (SATA)',
    'highlight': 'Highlight Text/Table',
    'highlight_2': 'Highlight Text/Table-2',
    'matrix_mr': 'Matrix Multiple Response',
    'grouped_mr': 'Grouped Multiple Response',
    'trend': 'Trend',
    'dyad': 'Dyad Rationale',
    'triad': 'Triad Rationale'
  };
  return mapping[type] || type;
}

function renderAuthorStandaloneTable() {
  const tbody = document.getElementById('author-standalone-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (standaloneQuestions.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:32px; color:#64748b; font-style:italic;">No stand-alone questions available. Click "Create New Stand-alone Question" to begin.</td></tr>`;
    return;
  }

  standaloneQuestions.forEach(q => {
    const tr = document.createElement('tr');
    tr.className = 'author-standalone-row';
    tr.dataset.course = q.course || 'Others';
    tr.dataset.unit = q.unit || q.topic || 'Others';
    tr.dataset.id = q.id;
    tr.dataset.title = (q.title || '').toLowerCase();
    tr.dataset.desc = (q.description || '').toLowerCase();

    const courseBadge = q.course === 'NURS 1017'
      ? `<span class="badge-course-1017">NURS 1017</span>`
      : q.course === 'NURS 1021'
        ? `<span class="badge-course-1021">NURS 1021</span>`
        : `<span class="badge-course-other">Unassigned</span>`;

    const unitBadge = `<span class="badge-unit">${escapeHTML(q.unit || q.topic || 'Others')}</span>`;
    const qType = q.screens && q.screens[0] && q.screens[0].question ? q.screens[0].question.type : '';
    const formatBadge = `<span class="badge-screens" style="background:#f1f5f9; color:#334155; border-color:#cbd5e1;">${escapeHTML(getQuestionTypeLabel(qType))}</span>`;

    tr.innerHTML = `
      <td>
        <div class="author-scenario-title">${escapeHTML(q.title || 'Untitled Question')}</div>
        <div class="author-scenario-desc">${escapeHTML(q.description || 'No description.')}</div>
        <span class="author-scenario-id card-id-badge" data-id="${q.id}" title="Click to copy direct LMS link for students"><svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-1px; margin-right:3px;"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>ID: ${escapeHTML(q.id)}</span>
      </td>
      <td>${courseBadge}</td>
      <td>${unitBadge}</td>
      <td>${formatBadge}</td>
      <td class="author-actions-cell">
        <div class="author-actions-wrapper">
          <button class="btn-author-edit edit-q-btn" data-id="${q.id}">Edit</button>
          <button class="btn-author-launch play-q-btn" data-id="${q.id}">Launch</button>
          <button class="btn-author-delete delete-q-btn" data-id="${q.id}">Delete</button>
        </div>
      </td>
    `;

    tr.querySelector('.edit-q-btn').addEventListener('click', () => startEditor(q));
    tr.querySelector('.play-q-btn').addEventListener('click', () => startPlayer(q));
    tr.querySelector('.delete-q-btn').addEventListener('click', () => {
      const qTitle = q.title || 'Untitled Question';
      if (confirm(`Are you sure you want to delete stand-alone question "${qTitle}"? This action cannot be undone.`)) {
        standaloneQuestions = standaloneQuestions.filter(x => x.id !== q.id);
        saveStandaloneToStorage();
        if (db) deleteFromStore('standalone_questions', q.id);
        showToast(`Stand-alone question "${qTitle}" deleted.`);
        renderDashboard();
      }
    });

    tr.querySelector('.card-id-badge').addEventListener('click', (e) => {
      e.stopPropagation();
      const baseUrl = window.location.protocol.startsWith('http')
        ? (window.location.origin + window.location.pathname)
        : 'https://thadaniavinash.github.io/NCLEX/';
      const directUrl = `${baseUrl}?standalone=${encodeURIComponent(q.id)}`;
      navigator.clipboard.writeText(directUrl);
      showToast(`Copied LMS link for "${q.title}"!`);
    });

    tbody.appendChild(tr);
  });
}

function applyAuthorTableFilters() {
  const currentTabIsCases = (authorCurrentTab === 'cases');
  const rows = currentTabIsCases
    ? document.querySelectorAll('#author-cases-tbody .author-case-row')
    : document.querySelectorAll('#author-standalone-tbody .author-standalone-row');

  let visibleCount = 0;
  const totalCount = rows.length;

  rows.forEach(tr => {
    const rowCourse = tr.dataset.course;
    const rowUnit = tr.dataset.unit;
    const rowId = (tr.dataset.id || '').toLowerCase();
    const rowTitle = tr.dataset.title || '';
    const rowDesc = tr.dataset.desc || '';

    let matchesCourse = (authorCourseFilter === 'ALL' || rowCourse === authorCourseFilter);
    let matchesUnit = (authorUnitFilter === 'ALL' || rowUnit === authorUnitFilter);
    let matchesSearch = (!authorSearchQuery || rowTitle.includes(authorSearchQuery) || rowDesc.includes(authorSearchQuery) || rowId.includes(authorSearchQuery));

    if (matchesCourse && matchesUnit && matchesSearch) {
      tr.style.display = '';
      visibleCount++;
    } else {
      tr.style.display = 'none';
    }
  });

  const countText = document.getElementById('author-filtered-count-text');
  if (countText) {
    const itemType = currentTabIsCases ? 'Case Studies' : 'Stand-alone Questions';
    countText.textContent = `Showing ${visibleCount} of ${totalCount} ${itemType}`;
  }
}

/* ================= ADMIN MANAGEMENT SYSTEM ================= */
function initAdminEvents() {
  const adminLoginBtn = document.getElementById('admin-login-btn');
  const adminLogoutBtn = document.getElementById('admin-logout-btn');
  const loginModal = document.getElementById('login-modal');
  const loginCancelBtn = document.getElementById('login-cancel-btn');
  const adminLoginForm = document.getElementById('admin-login-form');
  const loginUsernameInput = document.getElementById('login-username');
  const loginPasswordInput = document.getElementById('login-password');
  const loginErrorMsg = document.getElementById('login-error-msg');

  if (adminLoginBtn) {
    adminLoginBtn.addEventListener('click', () => {
      if (loginUsernameInput) loginUsernameInput.value = '';
      if (loginPasswordInput) loginPasswordInput.value = '';
      if (loginErrorMsg) loginErrorMsg.classList.add('hidden');
      if (loginModal) {
        loginModal.classList.remove('hidden');
        if (loginUsernameInput) loginUsernameInput.focus();
      }
    });
  }

  if (loginCancelBtn && loginModal) {
    loginCancelBtn.addEventListener('click', () => {
      loginModal.classList.add('hidden');
    });
  }

  if (loginModal) {
    loginModal.addEventListener('click', (e) => {
      if (e.target === loginModal) {
        loginModal.classList.add('hidden');
      }
    });
  }

  if (adminLoginForm) {
    adminLoginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const username = loginUsernameInput.value.trim();
      const password = loginPasswordInput.value;

      if (username === 'athadani' && password === '0911Keen!') {
        isAdminLoggedIn = true;
        if (typeof sessionStorage !== 'undefined') sessionStorage.setItem('isAdmin', 'true');
        if (loginModal) loginModal.classList.add('hidden');
        showToast("Logged in as Administrator", "success");
        applyAdminState();
      } else {
        if (loginErrorMsg) loginErrorMsg.classList.remove('hidden');
      }
    });
  }

  if (adminLogoutBtn) {
    adminLogoutBtn.addEventListener('click', () => {
      if (confirm("Are you sure you want to log out of admin mode?")) {
        isAdminLoggedIn = false;
        if (typeof sessionStorage !== 'undefined') sessionStorage.removeItem('isAdmin');
        showToast("Logged out of Admin Mode", "success");
        applyAdminState();
      }
    });
  }
}

function applyAdminState() {
  const loggedOutEl = document.getElementById('admin-status-logged-out');
  const loggedInEl = document.getElementById('admin-status-logged-in');
  if (isAdminLoggedIn) {
    if (loggedOutEl) loggedOutEl.classList.add('hidden');
    if (loggedInEl) loggedInEl.classList.remove('hidden');
  } else {
    if (loggedOutEl) loggedOutEl.classList.remove('hidden');
    if (loggedInEl) loggedInEl.classList.add('hidden');
  }

  renderDashboard();
}

function populateEditorUnitSelect(selectedCourse, selectedUnit) {
  const unitSelect = document.getElementById('case-unit-select');
  if (!unitSelect) return;

  let html = '<option value="">Unit: Select Unit</option>';
  if (selectedCourse === 'NURS 1017' && CURRICULUM_COURSES["NURS 1017"]) {
    html += CURRICULUM_COURSES["NURS 1017"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('');
  } else if (selectedCourse === 'NURS 1021' && CURRICULUM_COURSES["NURS 1021"]) {
    html += CURRICULUM_COURSES["NURS 1021"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('');
  } else {
    html += '<option value="Others">Others</option>';
  }
  unitSelect.innerHTML = html;
  if (selectedUnit) {
    unitSelect.value = selectedUnit;
  }
}

function createStandaloneQuestion() {
  const newId = 'standalone_' + Date.now();
  const newQ = {
    id: newId,
    title: 'New Stand-alone Question',
    description: '',
    isStandalone: true,
    screens: [
      {
        step: 1,
        leftContent: {
          intro: '',
          tabs: []
        },
        question: {
          type: 'select_all',
          stem: '',
          options: [
            { text: '', correct: false },
            { text: '', correct: false },
            { text: '', correct: false },
            { text: '', correct: false },
            { text: '', correct: false }
          ],
          explanation: ''
        }
      }
    ]
  };
  
  standaloneQuestions.push(newQ);
  saveStandaloneToStorage();
  startEditor(newQ);
  showToast("New standalone question initialized.");
}

/* ================= NEXTGEN NCLEX SESSION BUILDER ================= */
let sessionBuilderTopics = [];
let sessionBuilderMode = 'review'; // 'review' | 'test'

function initSessionBuilder() {
  // Mode selection cards
  const reviewCard = document.getElementById('mode-card-review');
  const testCard = document.getElementById('mode-card-test');
  const reviewRadio = document.querySelector('input[name="session-mode"][value="review"]');
  const testRadio = document.querySelector('input[name="session-mode"][value="test"]');
  const launchBtnLabel = document.getElementById('launch-btn-label');

  function setSessionMode(mode) {
    sessionBuilderMode = mode;
    if (mode === 'review') {
      if (reviewCard) reviewCard.classList.add('selected');
      if (testCard) testCard.classList.remove('selected');
      if (reviewRadio) reviewRadio.checked = true;
      if (launchBtnLabel) launchBtnLabel.textContent = 'Start Practice Session (Review Mode)';
    } else {
      if (testCard) testCard.classList.add('selected');
      if (reviewCard) reviewCard.classList.remove('selected');
      if (testRadio) testRadio.checked = true;
      if (launchBtnLabel) launchBtnLabel.textContent = 'Start NCLEX Exam Simulation (Test Mode)';
    }
    updateSessionCountsAndBounds();
  }

  if (reviewCard) reviewCard.addEventListener('click', () => setSessionMode('review'));
  if (testCard) testCard.addEventListener('click', () => setSessionMode('test'));
  if (reviewRadio) reviewRadio.addEventListener('change', () => setSessionMode('review'));
  if (testRadio) testRadio.addEventListener('change', () => setSessionMode('test'));

  // Preset buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const cases = parseInt(btn.dataset.cases || '0', 10);
      const standalone = parseInt(btn.dataset.standalone || '0', 10);

      // If no topics are selected currently, auto-select all topics so preset can apply
      if (!sessionBuilderTopics || sessionBuilderTopics.length === 0) {
        document.querySelectorAll('#generator-topics-list .session-topic-checkbox').forEach(cb => {
          cb.checked = true;
          cb.closest('.topic-chip-card')?.classList.add('active');
        });
        const checkboxes = document.querySelectorAll('.session-topic-checkbox:checked');
        sessionBuilderTopics = Array.from(checkboxes).map(cb => cb.value);
      }

      updateSessionCountsAndBounds();

      const casesSlider = document.getElementById('generator-cases-slider');
      const casesInput = document.getElementById('generator-cases-input');
      const stdSlider = document.getElementById('generator-standalone-slider');
      const stdInput = document.getElementById('generator-standalone-input');

      if (casesSlider) casesSlider.value = cases;
      if (casesInput) casesInput.value = cases;
      if (stdSlider) stdSlider.value = standalone;
      if (stdInput) stdInput.value = standalone;

      updateSessionCountsAndBounds();
    });
  });

  // Quantity Sliders & Number inputs sync
  const casesSlider = document.getElementById('generator-cases-slider');
  const casesInput = document.getElementById('generator-cases-input');
  const stdSlider = document.getElementById('generator-standalone-slider');
  const stdInput = document.getElementById('generator-standalone-input');

  if (casesSlider && casesInput) {
    casesSlider.addEventListener('input', () => {
      casesInput.value = casesSlider.value;
      updateSessionCountsAndBounds();
    });
    casesInput.addEventListener('input', () => {
      casesSlider.value = casesInput.value;
      updateSessionCountsAndBounds();
    });
  }

  if (stdSlider && stdInput) {
    stdSlider.addEventListener('input', () => {
      stdInput.value = stdSlider.value;
      updateSessionCountsAndBounds();
    });
    stdInput.addEventListener('input', () => {
      stdSlider.value = stdInput.value;
      updateSessionCountsAndBounds();
    });
  }

  // Launch button
  const launchBtn = document.getElementById('generate-play-btn');
  if (launchBtn) {
    launchBtn.addEventListener('click', generateAndStartSession);
  }

  // Authoring button in student header
  const authBtn = document.getElementById('student-authoring-btn');
  if (authBtn) {
    authBtn.addEventListener('click', () => switchView('dashboard'));
  }

  // Student Course & Unit Filters
  const studentCourseFilterEl = document.getElementById('student-course-filter');
  if (studentCourseFilterEl) {
    studentCourseFilterEl.addEventListener('change', (e) => {
      studentCourseFilter = e.target.value;
      updateStudentUnitFilterOptions();
      filterSessionTopicCards();
    });
  }

  const studentUnitFilterEl = document.getElementById('student-unit-filter');
  if (studentUnitFilterEl) {
    studentUnitFilterEl.addEventListener('change', (e) => {
      studentUnitFilter = e.target.value;
      filterSessionTopicCards();
    });
  }

  // Topic search filter
  const topicSearchInput = document.getElementById('topic-search-input');
  if (topicSearchInput) {
    topicSearchInput.addEventListener('input', () => {
      filterSessionTopicCards();
    });
  }

  // Select All Topics (selects visible topic cards)
  const selectAllTopicsBtn = document.getElementById('topics-select-all-btn');
  if (selectAllTopicsBtn) {
    selectAllTopicsBtn.addEventListener('click', () => {
      document.querySelectorAll('#generator-topics-list .topic-chip-card').forEach(card => {
        if (card.style.display !== 'none') {
          const cb = card.querySelector('.session-topic-checkbox');
          if (cb) {
            cb.checked = true;
            card.classList.add('active');
          }
        }
      });
      updateSessionTopicsFromCheckboxes();
    });
  }

  // Clear All Topics
  const clearAllTopicsBtn = document.getElementById('topics-clear-all-btn');
  if (clearAllTopicsBtn) {
    clearAllTopicsBtn.addEventListener('click', () => {
      document.querySelectorAll('#generator-topics-list .session-topic-checkbox').forEach(cb => {
        cb.checked = false;
        cb.closest('.topic-chip-card')?.classList.remove('active');
      });
      updateSessionTopicsFromCheckboxes();
    });
  }

  updateStudentUnitFilterOptions();
  renderSessionTopicsList();
  renderManualSelectionLists();
}

function updateStudentUnitFilterOptions() {
  const unitFilter = document.getElementById('student-unit-filter');
  if (!unitFilter) return;

  const currentVal = studentUnitFilter;
  let html = '<option value="ALL">All Units</option>';

  if (studentCourseFilter === 'ALL') {
    html += `
      <optgroup label="NURS 1017 (Pathophysiology 1)">
        ${CURRICULUM_COURSES["NURS 1017"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
      <optgroup label="NURS 1021 (Pathophysiology 2)">
        ${CURRICULUM_COURSES["NURS 1021"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
      <optgroup label="Other Topics">
        <option value="Others">Others (Unassigned)</option>
      </optgroup>
    `;
  } else if (studentCourseFilter === 'NURS 1017') {
    html += `
      <optgroup label="NURS 1017 (Pathophysiology 1)">
        ${CURRICULUM_COURSES["NURS 1017"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
    `;
  } else if (studentCourseFilter === 'NURS 1021') {
    html += `
      <optgroup label="NURS 1021 (Pathophysiology 2)">
        ${CURRICULUM_COURSES["NURS 1021"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
    `;
  } else if (studentCourseFilter === 'Others') {
    html += '<option value="Others">Others (Unassigned)</option>';
  }

  unitFilter.innerHTML = html;
  const exists = Array.from(unitFilter.options).some(opt => opt.value === currentVal);
  if (exists) {
    unitFilter.value = currentVal;
  } else {
    studentUnitFilter = 'ALL';
    unitFilter.value = 'ALL';
  }
}

function filterSessionTopicCards() {
  const q = (document.getElementById('topic-search-input')?.value || '').toLowerCase().trim();
  const cards = document.querySelectorAll('#generator-topics-list .topic-chip-card');
  let visibleCount = 0;

  cards.forEach(card => {
    const cardCourse = card.dataset.course || '';
    const cardUnit = card.dataset.unit || '';
    const cardText = card.textContent.toLowerCase();

    const matchesCourse = (studentCourseFilter === 'ALL' || cardCourse === studentCourseFilter);
    const matchesUnit = (studentUnitFilter === 'ALL' || cardUnit === studentUnitFilter);
    const matchesSearch = (!q || cardText.includes(q));

    if (matchesCourse && matchesUnit && matchesSearch) {
      card.style.display = 'flex';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });

  // If a specific unit was selected in dropdown (not 'ALL'), auto-select its checkbox if none is selected
  if (studentUnitFilter !== 'ALL') {
    cards.forEach(card => {
      if (card.dataset.unit === studentUnitFilter) {
        const cb = card.querySelector('.session-topic-checkbox');
        if (cb && !cb.checked) {
          cb.checked = true;
          card.classList.add('active');
          updateSessionTopicsFromCheckboxes();
        }
      }
    });
  }

  let emptyMsg = document.getElementById('generator-topics-empty-msg');
  if (visibleCount === 0) {
    if (!emptyMsg) {
      emptyMsg = document.createElement('div');
      emptyMsg.id = 'generator-topics-empty-msg';
      emptyMsg.style.cssText = 'color:#64748b; font-style:italic; padding: 16px; text-align: center;';
      emptyMsg.textContent = 'No matching units or topics found for the selected course and unit.';
      document.getElementById('generator-topics-list')?.appendChild(emptyMsg);
    } else {
      emptyMsg.style.display = 'block';
    }
  } else if (emptyMsg) {
    emptyMsg.style.display = 'none';
  }
}

function renderSessionTopicsList() {
  const container = document.getElementById('generator-topics-list');
  if (!container) return;

  const topicDescriptions = {
    'Unit 1 (Introduction to Pathophysiology)': 'Cell injury, adaptation, homeostasis, disease etiology',
    'Unit 2 (Cellular Basis of Disease)': 'Hypertrophy, hyperplasia, metaplasia, dysplasia, necrosis',
    'Unit 3 (Genetic and Developmental Disorders)': 'Chromosomal, Mendelian, Down, Turner, Klinefelter syndromes',
    'Unit 4 (Neoplasia)': 'Carcinogenesis, oncogenes, tumor suppressors, benign vs malignant',
    'Unit 5 (Integumentary Disorders and Burns)': 'Skin lesions, infections, burns (Rule of 9s, Parkland, depths)',
    'Unit 6 (Musculoskeletal Disorders)': 'Fractures, osteoporosis, arthritis, compartment syndrome',
    'Unit 7 (Neurological Disorders)': 'Stroke, intracranial pressure, seizures, neurological deficit',
    'Unit 8 (Pain)': 'Nociceptive, neuropathic, pain management, assessment',
    'Unit 9 (Disorders of the Eyes and Ears)': 'Glaucoma, cataracts, macular degeneration, hearing loss',
    'Unit 10 (Stress and Disease)': 'GAS, cortisol, neuroendocrine response, stress adaptation',
    'Unit 11 (Endocrine Disorders)': 'DKA, HHS, thyroid storm, adrenal disorders, diabetes care',
    'Unit 1 (Blood Disorders)': 'Anemias, coagulopathies, sickle cell disease, transfusions',
    'Unit 2 (Cardiovascular Disorders)': 'Heart failure, MI, dysrhythmias, hypertension, shock',
    'Unit 3 (Respiratory Disorders)': 'COPD, asthma, pulmonary embolism, ARDS, pneumonia',
    'Unit 4 (Inflammation and Immune Disorders)': 'Sepsis, autoimmune, anaphylaxis, hypersensitivity',
    'Unit 5 (Leukemias and Lymphomas)': 'Acute/chronic leukemia, Hodgkin/non-Hodgkin lymphoma',
    'Unit 6 (Gastrointestinal Disorders)': 'Pancreatitis, cirrhosis, bowel obstruction, GI bleed, IBD',
    'Unit 7 (Urinary Disorders)': 'AKI, CKD, nephrotic syndrome, glomerulonephritis',
    'Unit 8 (Fluid, Electrolytes, and Acid-Base Imbalances)': 'Hyponatremia, hyperkalemia, acidosis, alkalosis',
    'Unit 9 (Reproductive Disorders)': 'Reproductive tract pathology, hormonal imbalances',
    'Cardiovascular Disorders': 'Heart failure, MI, dysrhythmias, hypertension',
    'Endocrine Disorders': 'DKA, HHS, thyroid storm, diabetes care',
    'Respiratory Disorders': 'COPD, asthma, pulmonary embolism, ARDS',
    'GI Disorders': 'Pancreatitis, cirrhosis, bowel obstruction, GI bleed',
    'Neurological Disorders': 'Stroke, increased ICP, seizures, neuro checks',
    'Immune disorders': 'Sepsis, anaphylaxis, infection control, immunity',
    'Others': 'General pathophysiology, fundamentals, multisystem'
  };

  const topicsMap = {};

  // 1. Pre-populate ALL curriculum units in strict course order so units with 0 cases (e.g. Unit 1 Blood Disorders) are visible
  CURRICULUM_COURSES["NURS 1017"].forEach(u => {
    topicsMap[u] = { cases: 0, standalone: 0, course: "NURS 1017" };
  });
  CURRICULUM_COURSES["NURS 1021"].forEach(u => {
    topicsMap[u] = { cases: 0, standalone: 0, course: "NURS 1021" };
  });
  topicsMap["Others"] = { cases: 0, standalone: 0, course: "Others" };
  
  // 2. Collect topics from cases
  caseStudies.forEach(c => {
    const t = (c.unit || c.topic || c.disorder || 'Others').trim();
    if (!topicsMap[t]) {
      topicsMap[t] = { cases: 0, standalone: 0, course: c.course || 'Others' };
    }
    topicsMap[t].cases++;
    if (c.course && !topicsMap[t].course) topicsMap[t].course = c.course;
  });

  // 3. Collect topics from standalone
  standaloneQuestions.forEach(s => {
    const t = (s.unit || s.topic || s.disorder || 'Others').trim();
    if (!topicsMap[t]) {
      topicsMap[t] = { cases: 0, standalone: 0, course: s.course || 'Others' };
    }
    topicsMap[t].standalone++;
    if (s.course && !topicsMap[t].course) topicsMap[t].course = s.course;
  });

  // 4. Sort topics: All NURS 1017 units first, followed by NURS 1021, followed by Others
  const sortedTopics = Object.keys(topicsMap).sort((a, b) => {
    const isAOther = (a.toLowerCase() === 'others' || a.toLowerCase().startsWith('other'));
    const isBOther = (b.toLowerCase() === 'others' || b.toLowerCase().startsWith('other'));
    if (isAOther && !isBOther) return 1;
    if (!isAOther && isBOther) return -1;

    const idxA1017 = CURRICULUM_COURSES["NURS 1017"].indexOf(a);
    const idxB1017 = CURRICULUM_COURSES["NURS 1017"].indexOf(b);
    const idxA1021 = CURRICULUM_COURSES["NURS 1021"].indexOf(a);
    const idxB1021 = CURRICULUM_COURSES["NURS 1021"].indexOf(b);

    // If both are NURS 1017, order by curriculum sequence (Unit 1 to 11)
    if (idxA1017 !== -1 && idxB1017 !== -1) return idxA1017 - idxB1017;
    // NURS 1017 always comes before NURS 1021 and Others
    if (idxA1017 !== -1) return -1;
    if (idxB1017 !== -1) return 1;

    // If both are NURS 1021, order by curriculum sequence (Unit 1 to 9)
    if (idxA1021 !== -1 && idxB1021 !== -1) return idxA1021 - idxB1021;
    // NURS 1021 always comes before Others
    if (idxA1021 !== -1) return -1;
    if (idxB1021 !== -1) return 1;

    return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
  });
  container.innerHTML = '';

  if (sortedTopics.length === 0) {
    container.innerHTML = '<div style="color:#64748b; font-style:italic; padding: 8px;">No topics found in library.</div>';
    return;
  }

  sortedTopics.forEach(topic => {
    const counts = topicsMap[topic];
    const desc = topicDescriptions[topic] || 'Clinical scenario practice';

    // Determine course
    let course = counts.course || '';
    if (!course) {
      if (CURRICULUM_COURSES["NURS 1017"].includes(topic)) {
        course = "NURS 1017";
      } else if (CURRICULUM_COURSES["NURS 1021"].includes(topic)) {
        course = "NURS 1021";
      } else {
        course = "Others";
      }
    }

    const card = document.createElement('label');
    card.className = 'topic-chip-card';
    card.dataset.course = course;
    card.dataset.unit = topic;
    card.innerHTML = `
      <div class="topic-chip-left">
        <input type="checkbox" class="session-topic-checkbox" value="${escapeHTML(topic)}" style="accent-color: #025287; cursor: pointer; width: 16px; height: 16px;">
        <div>
          <div class="topic-chip-name">
            ${escapeHTML(topic)}
            ${course && course !== 'Others' ? `<span class="topic-course-tag ${course === 'NURS 1021' ? 'course-1021' : 'course-1017'}">${escapeHTML(course)}</span>` : ''}
          </div>
          <div style="font-size: 11px; color: #64748b; font-weight: normal; margin-top: 1px;">${escapeHTML(desc)}</div>
        </div>
      </div>
      <span class="topic-chip-counts">${counts.cases} Cases &bull; ${counts.standalone} Qs</span>
    `;

    const cb = card.querySelector('.session-topic-checkbox');
    cb.addEventListener('change', () => {
      if (cb.checked) card.classList.add('active');
      else card.classList.remove('active');
      updateSessionTopicsFromCheckboxes();
    });

    container.appendChild(card);
  });

  filterSessionTopicCards();
  updateSessionTopicsFromCheckboxes();
}

function updateSessionTopicsFromCheckboxes() {
  const checkboxes = document.querySelectorAll('.session-topic-checkbox:checked');
  sessionBuilderTopics = Array.from(checkboxes).map(cb => cb.value);
  updateSessionCountsAndBounds();
}

function updateSessionCountsAndBounds() {
  // Available pool from selected topics
  const availableCases = caseStudies.filter(c => sessionBuilderTopics.includes((c.topic || c.disorder || 'General').trim()));
  const availableStandalone = standaloneQuestions.filter(s => sessionBuilderTopics.includes((s.topic || s.disorder || 'General').trim()));

  const maxCases = Math.min(3, availableCases.length);
  const maxStandalone = Math.min(67, availableStandalone.length);

  const casesAvailEl = document.getElementById('cases-avail-text');
  const stdAvailEl = document.getElementById('standalone-avail-text');
  if (casesAvailEl) casesAvailEl.textContent = `Avail: ${availableCases.length} (Max 3)`;
  if (stdAvailEl) stdAvailEl.textContent = `Avail: ${availableStandalone.length} (Max 67)`;

  const casesSlider = document.getElementById('generator-cases-slider');
  const casesInput = document.getElementById('generator-cases-input');
  const stdSlider = document.getElementById('generator-standalone-slider');
  const stdInput = document.getElementById('generator-standalone-input');

  if (casesSlider && casesInput) {
    casesSlider.max = maxCases;
    casesInput.max = maxCases;
    if (parseInt(casesInput.value || '0', 10) > maxCases) {
      casesInput.value = maxCases;
      casesSlider.value = maxCases;
    }
  }

  if (stdSlider && stdInput) {
    stdSlider.max = maxStandalone;
    stdInput.max = maxStandalone;
    if (parseInt(stdInput.value || '0', 10) > maxStandalone) {
      stdInput.value = maxStandalone;
      stdSlider.value = maxStandalone;
    }
  }

  let casesVal = parseInt(casesInput ? casesInput.value : '0', 10) || 0;
  let stdVal = parseInt(stdInput ? stdInput.value : '0', 10) || 0;

  // Enforce 85 questions cap: (cases * 6) + standalone <= 85
  const maxQuestionsCap = 85;
  const casesQuestions = casesVal * 6;
  if (casesQuestions + stdVal > maxQuestionsCap) {
    stdVal = maxQuestionsCap - casesQuestions;
    if (stdVal < 0) stdVal = 0;
    if (stdInput) stdInput.value = stdVal;
    if (stdSlider) stdSlider.value = stdVal;
  }

  const totalQuestions = casesQuestions + stdVal;

  const casesNote = document.getElementById('cases-questions-note');
  const stdNote = document.getElementById('standalone-questions-note');
  if (casesNote) casesNote.textContent = `${casesVal} Case Stud${casesVal === 1 ? 'y' : 'ies'} = ${casesQuestions} Questions`;
  if (stdNote) stdNote.textContent = `${stdVal} Stand-alone Question${stdVal === 1 ? '' : 's'}`;

  const totalValEl = document.getElementById('session-total-questions-val');
  const statusBadge = document.getElementById('session-total-status-badge');
  const launchBtn = document.getElementById('generate-play-btn');

  if (totalValEl) totalValEl.textContent = totalQuestions;

  const estMins = Math.round(totalQuestions * 1.3);
  const estTimeEl = document.getElementById('session-est-time-val');
  if (estTimeEl) estTimeEl.textContent = estMins;

  const pillTotalEl = document.getElementById('pill-total-text');
  if (pillTotalEl) pillTotalEl.textContent = `${totalQuestions} Questions`;

  const pillTimeEl = document.getElementById('pill-time-text');
  if (pillTimeEl) pillTimeEl.textContent = `(Est. ${estMins} Mins)`;

  const pillModeEl = document.getElementById('pill-mode-text');
  if (pillModeEl) pillModeEl.textContent = (sessionBuilderMode === 'review' ? 'Review Mode' : 'Test Mode');

  const topicsBadge = document.getElementById('topics-selected-count-badge');
  const allTopicCards = document.querySelectorAll('#generator-topics-list .topic-chip-card');
  const activeTopicCards = document.querySelectorAll('#generator-topics-list .topic-chip-card.active');
  if (topicsBadge) {
    topicsBadge.textContent = `${activeTopicCards.length} of ${allTopicCards.length} Selected`;
  }

  const poolCountsText = document.getElementById('topic-pool-counts-text');
  if (poolCountsText) {
    const poolCaseQuestions = availableCases.length * 6;
    poolCountsText.textContent = `${availableCases.length} Cases (${poolCaseQuestions} Qs) + ${availableStandalone.length} Standalone`;
  }

  if (statusBadge) {
    if (totalQuestions === 0) {
      statusBadge.textContent = 'Select at least 1 Question';
      statusBadge.className = 'total-status error';
      if (launchBtn) launchBtn.disabled = true;
    } else {
      statusBadge.textContent = `Ready (${sessionBuilderMode === 'review' ? 'Practice' : 'Exam'})`;
      statusBadge.className = 'total-status';
      if (launchBtn) launchBtn.disabled = false;
    }
  }
}

function renderManualSelectionLists() {
  const casesList = document.getElementById('generator-cases-list');
  const standaloneList = document.getElementById('generator-standalone-list');
  if (!casesList || !standaloneList) return;

  casesList.innerHTML = '';
  standaloneList.innerHTML = '';

  if (caseStudies.length === 0) {
    casesList.innerHTML = '<p style="color:var(--text-dash-secondary); font-style:italic; padding:8px;">No case studies available.</p>';
  } else {
    caseStudies.forEach(c => {
      const item = document.createElement('label');
      item.className = 'generator-item-label';
      item.innerHTML = `
        <input type="checkbox" class="generator-case-checkbox" data-id="${c.id}">
        <span class="item-name">${escapeHTML(c.title)}</span>
        <span class="item-meta">(${c.screens ? c.screens.length : 0} screens &bull; ${escapeHTML(c.topic || c.disorder || '')})</span>
      `;
      casesList.appendChild(item);
    });
  }

  if (standaloneQuestions.length === 0) {
    standaloneList.innerHTML = '<p style="color:var(--text-dash-secondary); font-style:italic; padding:8px;">No stand-alone questions available.</p>';
  } else {
    standaloneQuestions.forEach(q => {
      const item = document.createElement('label');
      item.className = 'generator-item-label';
      item.innerHTML = `
        <input type="checkbox" class="generator-standalone-checkbox" data-id="${q.id}">
        <span class="item-name">${escapeHTML(q.title)}</span>
        <span class="item-meta">(1 screen &bull; ${escapeHTML(q.topic || q.disorder || '')})</span>
      `;
      standaloneList.appendChild(item);
    });
  }
}

function generateAndStartSession() {
  // Check if manual selection was explicitly made in the advanced accordion
  const manualCaseCbs = Array.from(document.querySelectorAll('.generator-case-checkbox:checked'));
  const manualStdCbs = Array.from(document.querySelectorAll('.generator-standalone-checkbox:checked'));

  let selectedCaseStudies = [];
  let selectedStandalone = [];

  if (manualCaseCbs.length > 0 || manualStdCbs.length > 0) {
    // Use manual selection
    selectedCaseStudies = manualCaseCbs.map(cb => caseStudies.find(x => x.id === cb.dataset.id)).filter(Boolean);
    selectedStandalone = manualStdCbs.map(cb => standaloneQuestions.find(x => x.id === cb.dataset.id)).filter(Boolean);
  } else {
    // Use Topic & Quantity configuration
    const availableCases = caseStudies.filter(c => sessionBuilderTopics.includes((c.topic || c.disorder || 'General').trim()));
    const availableStandalone = standaloneQuestions.filter(s => sessionBuilderTopics.includes((s.topic || s.disorder || 'General').trim()));

    const casesInput = document.getElementById('generator-cases-input');
    const stdInput = document.getElementById('generator-standalone-input');
    const casesQty = Math.min(3, parseInt(casesInput ? casesInput.value : '0', 10) || 0);
    const stdQty = Math.min(67, parseInt(stdInput ? stdInput.value : '0', 10) || 0);

    // Shuffle and slice requested count
    const shuffledCases = [...availableCases].sort(() => 0.5 - Math.random());
    const shuffledStd = [...availableStandalone].sort(() => 0.5 - Math.random());

    selectedCaseStudies = shuffledCases.slice(0, casesQty);
    selectedStandalone = shuffledStd.slice(0, stdQty);
  }

  if (selectedCaseStudies.length === 0 && selectedStandalone.length === 0) {
    showToast("Please select topics and questions to generate your session.", "error");
    return;
  }

  const compiledCase = {
    id: 'compiled_session_' + Date.now(),
    title: sessionBuilderMode === 'review' ? 'NCLEX Practice Session' : 'NextGen NCLEX Exam Simulation',
    description: `A custom ${sessionBuilderMode} testing session containing ${selectedCaseStudies.length} case studies and ${selectedStandalone.length} stand-alone questions.`,
    screens: []
  };

  let currentStepNum = 1;

  // 1. Add Case Studies (each with full 6 chronological unfolding screens)
  selectedCaseStudies.forEach(c => {
    if (c && c.screens) {
      c.screens.forEach((screen, screenIdx) => {
        const screenCopy = JSON.parse(JSON.stringify(screen));
        screenCopy.step = currentStepNum++;
        screenCopy.caseId = c.id;
        screenCopy.caseTitle = c.title;
        screenCopy.isCaseStart = (screenIdx === 0);
        screenCopy.isStandalone = false;
        compiledCase.screens.push(screenCopy);
      });
    }
  });

  // 2. Add Stand-alone Questions
  selectedStandalone.forEach(q => {
    if (q && q.screens) {
      q.screens.forEach(screen => {
        const screenCopy = JSON.parse(JSON.stringify(screen));
        screenCopy.step = currentStepNum++;
        screenCopy.isStandalone = true;
        screenCopy.caseTitle = q.title || 'Stand-alone Question';
        compiledCase.screens.push(screenCopy);
      });
    }
  });

  startPlayer(compiledCase, {
    mode: sessionBuilderMode,
    isRemediation: false,
    allowBacktrack: (sessionBuilderMode === 'review')
  });
}

function createNewCase() {
  const newId = 'case_' + Date.now();
  const newCase = {
    id: newId,
    title: 'New Case Study',
    description: '',
    screens: [
      {
        step: 1,
        leftContent: {
          intro: '',
          tabs: [
            { id: 'nn_' + Date.now(), title: "Nurses' Notes", content: '' }
          ]
        },
        question: {
          type: 'select_all',
          stem: '',
          options: [
            { text: '', correct: false },
            { text: '', correct: false },
            { text: '', correct: false },
            { text: '', correct: false },
            { text: '', correct: false }
          ],
          explanation: ''
        }
      }
    ]
  };
  
  caseStudies.push(newCase);
  saveCasesToStorage();
  startEditor(newCase);
  showToast("New case study initialized.");
}

function updateToolbarStates(editor) {
  const container = editor.closest('.rich-editor-container');
  if (!container) return;
  const toolbar = container.querySelector('.rich-editor-toolbar');
  if (!toolbar) return;

  toolbar.querySelectorAll('.toolbar-btn[data-cmd]').forEach(btn => {
    const cmd = btn.dataset.cmd;
    try {
      if (document.queryCommandState(cmd)) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    } catch (e) {
      // queryCommandState might fail for some commands
    }
  });
}

function initRichTextEditors() {
  // Prevent focus loss from contenteditable on mousedown
  document.body.addEventListener('mousedown', (e) => {
    const btn = e.target.closest('.rich-editor-toolbar .toolbar-btn');
    if (btn) {
      e.preventDefault();
    }
  });

  document.body.addEventListener('click', (e) => {
    const btn = e.target.closest('.rich-editor-toolbar .toolbar-btn');
    if (!btn) return;
    
    e.preventDefault();
    
    const container = btn.closest('.rich-editor-container');
    if (!container) return;
    
    const editor = container.querySelector('.rich-text-editor');
    if (!editor) return;
    
    const isAlreadyFocused = (document.activeElement === editor || editor.contains(document.activeElement));
    
    // Save current selection range before applying command
    const selection = window.getSelection();
    let savedRange = null;
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      if (editor.contains(range.commonAncestorContainer)) {
        savedRange = range.cloneRange();
      }
    }
    
    const cmd = btn.dataset.cmd;
    const symbol = btn.dataset.symbol;
    
    if (cmd) {
      document.execCommand(cmd, false, null);
    } else if (symbol) {
      document.execCommand('insertText', false, symbol);
    } else if (btn.classList.contains('table-insert-btn')) {
      insertTableAtCursor(editor, 3, 2);
    }
    
    // Restore focus and selection range (only if not already focused, or if text was selected)
    if (!isAlreadyFocused) {
      editor.focus();
    }
    if (savedRange && !savedRange.collapsed) {
      selection.removeAllRanges();
      selection.addRange(savedRange);
    }
    
    // Immediately update toolbar active states
    updateToolbarStates(editor);
  });

  // Keep toolbar states synced on cursor movement / selection change
  document.body.addEventListener('keyup', (e) => {
    const editor = e.target.closest('.rich-text-editor');
    if (editor) updateToolbarStates(editor);
  });
  document.body.addEventListener('mouseup', (e) => {
    const editor = e.target.closest('.rich-text-editor');
    if (editor) updateToolbarStates(editor);
  });
  document.body.addEventListener('click', (e) => {
    const editor = e.target.closest('.rich-text-editor');
    if (editor) updateToolbarStates(editor);
  });
  document.body.addEventListener('focusin', (e) => {
    const editor = e.target.closest('.rich-text-editor');
    if (editor) updateToolbarStates(editor);
  });

  // Force plain text paste in contenteditable editors to prevent font modifications
  document.addEventListener('paste', (e) => {
    const editor = e.target.closest('.rich-text-editor');
    if (!editor) return;

    e.preventDefault();
    const text = (e.originalEvent || e).clipboardData.getData('text/plain');
    document.execCommand('insertText', false, text);
  });
}



function insertTableAtCursor(editorDiv, rows, cols) {
  let tableHTML = '<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">';
  // Header Row
  tableHTML += '<thead><tr>';
  for (let j = 0; j < cols; j++) {
    tableHTML += `<th placeholder="Header ${j+1}" style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;"></th>`;
  }
  tableHTML += '</tr></thead><tbody>';
  // Data Rows
  for (let i = 0; i < rows; i++) {
    tableHTML += '<tr>';
    for (let j = 0; j < cols; j++) {
      tableHTML += '<td placeholder="Cell" style="border:1px solid #ccd8e0; padding:8px; min-width:80px; background:white; color:#1e293b;"></td>';
    }
    tableHTML += '</tr>';
  }
  tableHTML += '</tbody></table><p><br></p>';
  
  editorDiv.focus();
  const selection = window.getSelection();
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    // Ensure selection is inside the editor
    if (editorDiv.contains(range.commonAncestorContainer)) {
      range.deleteContents();
      const el = document.createElement('div');
      el.innerHTML = tableHTML;
      const frag = document.createDocumentFragment();
      let node, lastNode;
      while ((node = el.firstChild)) {
        lastNode = frag.appendChild(node);
      }
      range.insertNode(frag);
      if (lastNode) {
        range.setStartAfter(lastNode);
        range.collapse(true);
        selection.removeAllRanges();
        selection.addRange(range);
      }
      return;
    }
  }
  // Fallback if not focused/inside editor
  editorDiv.innerHTML += tableHTML;
}

function toggleTheme(forceLight) {
  let targetLight;
  if (typeof forceLight === 'boolean') {
    targetLight = forceLight;
  } else {
    const isCurrentlyLight = document.body.classList.contains('light-mode');
    targetLight = !isCurrentlyLight;
  }
  
  if (targetLight) {
    document.body.classList.add('light-mode');
    try {
      localStorage.setItem('nclex_theme', 'light');
    } catch (e) {
      console.warn("localStorage is blocked:", e);
    }
  } else {
    document.body.classList.remove('light-mode');
    try {
      localStorage.setItem('nclex_theme', 'dark');
    } catch (e) {
      console.warn("localStorage is blocked:", e);
    }
  }

  // Sync both buttons
  ['editor-theme-toggle-btn', 'dashboard-theme-toggle-btn'].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) {
      const sunIcon = btn.querySelector('.sun-icon');
      const moonIcon = btn.querySelector('.moon-icon');
      if (targetLight) {
        if (sunIcon) sunIcon.style.display = 'none';
        if (moonIcon) {
          moonIcon.style.display = 'block';
          moonIcon.classList.remove('hidden');
        }
      } else {
        if (sunIcon) sunIcon.style.display = 'block';
        if (moonIcon) {
          moonIcon.style.display = 'none';
          moonIcon.classList.add('hidden');
        }
      }
    }
  });
}

/* ================= TEMPLATE GENERATION TOOL (EDITOR) ================= */
function initEditorEvents() {
  initRichTextEditors();
  
  const themeToggleBtn = document.getElementById('editor-theme-toggle-btn');
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', toggleTheme);
  }

  const courseSelect = document.getElementById('case-course-select');
  if (courseSelect) {
    courseSelect.addEventListener('change', (e) => {
      populateEditorUnitSelect(e.target.value, '');
    });
  }

  document.getElementById('editor-back-btn').addEventListener('click', () => {
    if (!saveCurrentStepData(false, true)) return;
    saveCurrentCaseOrStandalone();
    switchView('dashboard');
  });
  
  document.getElementById('editor-save-btn').addEventListener('click', () => {
    if (!saveCurrentStepData()) return;
    saveCurrentCaseOrStandalone();
    showToast("Progress saved successfully.");
  });

  document.getElementById('editor-export-btn').addEventListener('click', () => {
    if (!saveCurrentStepData()) return;
    saveCurrentCaseOrStandalone();
    exportCaseStudy(currentCase);
  });

  // Question Image Configuration Event Listeners
  const chooseImgBtn = document.getElementById('choose-question-image-btn');
  const imgFileInput = document.getElementById('question-image-file-input');
  const removeImgBtn = document.getElementById('remove-question-image-btn');
  
  if (chooseImgBtn && imgFileInput && removeImgBtn) {
    chooseImgBtn.addEventListener('click', () => imgFileInput.click());
    
    imgFileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
          const base64Str = event.target.result;
          const step = currentCase.screens[currentStepIndex];
          if (step && step.question) {
            step.question.questionImage = base64Str;
            updateImagePreview(base64Str);
          }
        };
        reader.readAsDataURL(file);
      }
    });
    
    removeImgBtn.addEventListener('click', () => {
      const step = currentCase.screens[currentStepIndex];
      if (step && step.question) {
        step.question.questionImage = null;
        imgFileInput.value = '';
        updateImagePreview(null);
      }
    });
  }
  
  document.getElementById('editor-play-btn').addEventListener('click', () => {
    if (!saveCurrentStepData()) return;
    saveCurrentCaseOrStandalone();
    startPlayer(currentCase);
  });

  document.getElementById('add-step-btn').addEventListener('click', addStepToCase);
  document.getElementById('add-tab-btn').addEventListener('click', addTabToStep);
  document.getElementById('delete-active-tab-btn').addEventListener('click', deleteActiveTab);
  
  document.getElementById('tab-title-input').addEventListener('input', (e) => {
    const activeTabItem = document.querySelector(`.tab-editor-item[data-id="${activeTabId}"] span`);
    if (activeTabItem) {
      activeTabItem.textContent = e.target.value;
    }
  });

  document.getElementById('tab-text-input').addEventListener('blur', () => {
    saveActiveTabContent();
  });

  document.getElementById('tab-text-input').addEventListener('focus', (e) => {
    if (!activeTabId) return;
    const step = currentCase.screens[currentStepIndex];
    if (!step) return;
    const tabs = step.leftContent.tabs;
    const tab = tabs.find(t => t.id === activeTabId);
    if (tab && tab.title && /nurse|note|log|progress/i.test(tab.title)) {
      const stripped = stripNursesNotesFormatting(e.target.innerHTML);
      if (e.target.innerHTML !== stripped) {
        e.target.innerHTML = stripped;
      }
    }
  });

  document.getElementById('tab-text-input').addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      document.execCommand('insertHTML', false, '&nbsp;&nbsp;&nbsp;&nbsp;');
    }
  });

  document.getElementById('question-type-select').addEventListener('change', (e) => {
    const prevType = currentCase.screens[currentStepIndex].question.type;
    if (!saveCurrentStepData(true)) {
      e.target.value = prevType;
      return;
    }
    const q = currentCase.screens[currentStepIndex].question;
    q.type = e.target.value;
    
    // Prepopulate defaults based on NGN type
    initializeQuestionTypeDefaults(q);
    
    renderEditorStep(currentStepIndex);
  });
}

function initializeQuestionTypeDefaults(q) {
  // 0/1 Scoring
  if (q.type === 'dropdown_cloze' || q.type === 'drag_drop_cloze' || q.type === 'dyad' || q.type === 'triad') {
    if (!q.cloze) {
      q.cloze = { text: '', dropdowns: [] };
    }
    
    const textStr = q.cloze.text || '';
    const isStandardDefault = !textStr || textStr === 'The patient should be ordered [[drop0]] due to [[drop1]].' || textStr === 'The patient should...[[drop0]]...due to...[[drop1]]';
    const isTriadText = textStr.includes('[[drop2]]') || textStr.includes('and [[drop2]]');
    const isDyadText = !isTriadText && textStr.includes('[[drop1]]');

    if (q.type === 'dyad') {
      if (isStandardDefault || isTriadText || !textStr) {
        q.cloze.text = 'The nurse should...[[drop0]]...as most evidenced by...[[drop1]]';
      }
      // Enforce exactly 2 slots for Dyad
      if (q.cloze.dropdowns.length !== 2) {
        q.cloze.dropdowns = [
          q.cloze.dropdowns[0] || { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] },
          q.cloze.dropdowns[1] || { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] }
        ];
      }
    } else if (q.type === 'triad') {
      if (isStandardDefault || isDyadText || !textStr) {
        q.cloze.text = 'The nurse should...[[drop0]]...as most evidenced by...[[drop1]] and [[drop2]]';
      }
      // Enforce exactly 3 slots for Triad
      if (q.cloze.dropdowns.length !== 3) {
        q.cloze.dropdowns = [
          q.cloze.dropdowns[0] || { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] },
          q.cloze.dropdowns[1] || { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] },
          q.cloze.dropdowns[2] || { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] }
        ];
      }
    } else if (q.type === 'dropdown_cloze' || q.type === 'drag_drop_cloze') {
      const cleanStem = (q.stem || '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, '').trim();
      if (!cleanStem) {
        q.stem = 'Complete the following sentence by choosing from the lists of options.';
      }
      if (!textStr) {
        q.cloze.text = 'The patient should...[[drop0]]...due to...[[drop1]]';
        q.cloze.dropdowns = [
          { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] },
          { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] }
        ];
      }
    }
  } else if (q.type === 'dropdown_table') {
    const cleanStem = (q.stem || '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, '').trim();
    if (!cleanStem) {
      q.stem = 'Complete the following table by...';
    }
    q.dropdownTableHeader1 = '';
    q.dropdownTableHeader2 = '';
    if (!q.dropdownTableRows) {
      q.dropdownTableRows = [
        { label: '', placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }] },
        { label: '', placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }] }
      ];
    }
  } else if (q.type === 'matrix_mc') {
    const cleanStem = (q.stem || '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, '').trim();
    if (!cleanStem || cleanStem === 'For each..., click to specify...') {
      q.stem = '';
    }
    if (!q.matrix) {
      q.matrix = {
        firstColumnHeader: '',
        columns: ['Indicated', 'Not Indicated'],
        rows: [
          { text: '', correctIndex: 0, correctIndices: [0] },
          { text: '', correctIndex: 0, correctIndices: [0] }
        ]
      };
    } else {
      if (q.matrix.firstColumnHeader === 'Potential Interventions' || q.matrix.firstColumnHeader === 'Findings') {
        q.matrix.firstColumnHeader = '';
      }
      const genericRows = ['clear liquid diet', 'soapsuds enema', 'polyuria', 'weight gain', 'New Row 1', 'New Row 2'];
      q.matrix.rows.forEach(r => {
        if (genericRows.includes(r.text)) {
          r.text = '';
        }
      });
      while (q.matrix.columns.length < 2) q.matrix.columns.push('');
      if (q.matrix.columns.length > 2) q.matrix.columns = q.matrix.columns.slice(0, 2);
    }
  } else if (q.type === 'matrix_mr') {
    const cleanStem = (q.stem || '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, '').trim();
    if (!cleanStem) {
      q.stem = 'For each assessment finding below, click to specify if the finding is consistent with the disease process of ... . Each finding may support more than 1 disease process.';
    }
    if (!q.matrix) {
      q.matrix = {
        firstColumnHeader: '',
        columns: ['', '', ''],
        rows: [
          { text: '', correctIndices: [] },
          { text: '', correctIndices: [] }
        ]
      };
    } else {
      const genericRows = ['clear liquid diet', 'soapsuds enema', 'polyuria', 'weight gain', 'New Row 1', 'New Row 2'];
      q.matrix.rows.forEach(r => {
        if (genericRows.includes(r.text)) {
          r.text = '';
        }
      });
      while (q.matrix.columns.length < 3) q.matrix.columns.push('');
      if (q.matrix.columns.length > 3) q.matrix.columns = q.matrix.columns.slice(0, 3);
    }
  } else if (q.type === 'select_n') {
    if (!q.options) {
      q.options = [
        { text: 'Option 1', correct: true },
        { text: 'Option 2', correct: true },
        { text: 'Option 3', correct: false }
      ];
    }
    q.limit = q.limit || 2;
  } else if (q.type === 'bowtie') {
    if (!q.bowtieActions) {
      q.bowtieActions = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
      q.bowtieConditions = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
      q.bowtieParams = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
    }
  } else if (q.type === 'multiple_choice') {
    if (!q.options || q.options.length !== 4) {
      const currentOpts = q.options || [];
      q.options = [
        currentOpts[0] || { text: '', correct: true },
        currentOpts[1] || { text: '', correct: false },
        currentOpts[2] || { text: '', correct: false },
        currentOpts[3] || { text: '', correct: false }
      ];
      const hasCorrect = q.options.some(o => o.correct);
      if (!hasCorrect) {
        q.options[0].correct = true;
      }
    }
  } else if (q.type === 'fill_blank') {
    const cleanStem = (q.stem || '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, '').trim();
    if (!cleanStem || cleanStem === 'Add question...') {
      q.stem = '';
    }
    if (!q.correctAnswer || q.correctAnswer === '12.5') {
      q.correctAnswer = '';
    }
  } else if (q.type === 'hotspot') {
    if (!q.imageUrl) {
      q.imageUrl = 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600'; // clinic / anatomy fallback
      q.rect = { x1: 30, y1: 30, x2: 70, y2: 70 };
    }
  } else if (q.type === 'ordered_response') {
    if (!q.orderedOptions) {
      q.orderedOptions = ['First action', 'Second action', 'Third action'];
    }
  }
  // +/- Scoring
  else if (q.type === 'select_all' || q.type === 'trend') {
    if (q.type === 'select_all') {
      if (!q.options || q.options.length < 5) {
        q.options = [
          { text: '', correct: false },
          { text: '', correct: false },
          { text: '', correct: false },
          { text: '', correct: false },
          { text: '', correct: false }
        ];
      }
    } else {
      if (!q.options) {
        q.options = [{ text: 'Fever', correct: true }, { text: 'Cough', correct: false }, { text: 'Dyspnea', correct: true }];
      }
    }
  } else if (q.type === 'highlight' || q.type === 'highlight_2') {
    if (!q.highlightTabs) {
      q.highlightTabs = [
        { id: 'ht_' + Date.now(), title: "Nurses' Notes", content: q.highlightText || 'The client reports {pain in left calf|correct}. Respirations are {shallow and labored|correct}. Temperature is {98.6 F}.' }
      ];
    }
  } else if (q.type === 'grouped_mr') {
    if (!q.groupedRows) {
      q.groupedRows = [
        {
          title: 'Non-pharmacological',
          options: [{ text: 'restrict fluids', correct: true }, { text: 'bed rest', correct: false }]
        },
        {
          title: 'Pharmacological',
          options: [{ text: 'furosemide', correct: true }, { text: 'normal saline bolus', correct: false }]
        }
      ];
    }
  }
}

function startEditor(c) {
  migrateCaseTypes(c);
  currentCase = c;
  currentStepIndex = 0;
  
  const courseSelect = document.getElementById('case-course-select');
  const unitSelect = document.getElementById('case-unit-select');
  if (courseSelect) {
    courseSelect.value = c.course || '';
    populateEditorUnitSelect(c.course || '', c.unit || '');
  }

  const select = document.getElementById('case-disorder-select');
  if (select) {
    select.innerHTML = '<option value="">Categorize Case Study</option>' + 
      PATHOPHYSIOLOGY_DISORDERS.map(d => `<option value="${escapeHTML(d)}">${escapeHTML(d)}</option>`).join('');
    select.value = c.disorder || '';
  }
  
  document.getElementById('case-title-input').value = c.title || '';
  document.getElementById('case-desc-input').value = c.description || '';
  
  const stepsSidebar = document.querySelector('.editor-steps-sidebar');
  if (stepsSidebar) {
    if (c.isStandalone) {
      stepsSidebar.classList.add('hidden');
    } else {
      stepsSidebar.classList.remove('hidden');
    }
  }
  
  switchView('editor');
  renderEditorStep(0);
}

function renderEditorStep(stepIdx) {
  currentStepIndex = stepIdx;
  const step = currentCase.screens[stepIdx];
  if (!step) return;

  currentCase.title = document.getElementById('case-title-input').value;
  currentCase.description = document.getElementById('case-desc-input').value;
  
  renderStepsSidebar();
  
  const stdChartEditor = document.getElementById('standard-chart-editor');
  const highlightPlaceholder = document.getElementById('highlight-chart-placeholder');
  const q = step.question;
  
  if (stdChartEditor && highlightPlaceholder) {
    if (q.type === 'highlight') {
      stdChartEditor.classList.add('hidden');
      highlightPlaceholder.classList.remove('hidden');
    } else {
      stdChartEditor.classList.remove('hidden');
      highlightPlaceholder.classList.add('hidden');
    }
  }
  
  document.getElementById('step-intro-input').innerHTML = step.leftContent.intro || '';
  renderEditorTabs(step.leftContent.tabs);
  
  document.getElementById('question-type-select').value = q.type;
  document.getElementById('question-preamble-input').innerHTML = q.preamble || '';
  
  const stemInput = document.getElementById('question-stem-input');
  if (q.type === 'matrix_mc') {
    stemInput.setAttribute('placeholder', 'For each..., click to specify...');
  } else if (q.type === 'dropdown_table') {
    stemInput.setAttribute('placeholder', 'Complete the following table by...');
  } else if (q.type === 'dropdown_cloze' || q.type === 'drag_drop_cloze') {
    stemInput.setAttribute('placeholder', 'Complete the following sentence by choosing from the lists of options.');
  } else if (q.type === 'fill_blank') {
    stemInput.setAttribute('placeholder', 'Add question...');
  } else {
    stemInput.setAttribute('placeholder', 'e.g. Which of the following findings require follow-up? Select all that apply.');
  }
  stemInput.innerHTML = q.stem || '';
  document.getElementById('question-explanation-input').innerHTML = q.explanation || '';
  
  // Update image preview in editor
  updateImagePreview(q.questionImage || null);
  
  renderDynamicQuestionConfigurator(q);
}

function updateImagePreview(base64Str) {
  const container = document.getElementById('question-image-preview-container');
  const img = document.getElementById('question-image-preview');
  const removeBtn = document.getElementById('remove-question-image-btn');
  
  if (container && img && removeBtn) {
    if (base64Str) {
      img.src = base64Str;
      container.classList.remove('hidden');
      removeBtn.classList.remove('hidden');
    } else {
      img.src = '';
      container.classList.add('hidden');
      removeBtn.classList.add('hidden');
    }
  }
}

function renderStepsSidebar() {
  const stepsList = document.getElementById('editor-steps-list');
  stepsList.innerHTML = '';
  
  currentCase.screens.forEach((step, idx) => {
    const item = document.createElement('div');
    item.className = `step-nav-item ${idx === currentStepIndex ? 'active' : ''}`;
    item.innerHTML = `
      <span>Screen ${idx + 1}</span>
      ${currentCase.screens.length > 1 ? `
        <button class="btn-step-delete" title="Delete Screen">
          <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
        </button>
      ` : ''}
    `;
    
    item.addEventListener('click', (e) => {
      if (e.target.closest('.btn-step-delete')) {
        e.stopPropagation();
        deleteStep(idx);
      } else {
        if (!saveCurrentStepData()) return;
        renderEditorStep(idx);
      }
    });
    
    stepsList.appendChild(item);
  });
}

function addStepToCase() {
  if (!saveCurrentStepData()) return;
  const nextNum = currentCase.screens.length + 1;
  
  // Carry over tabs and intro from previous screen if available, otherwise set default Nurses' Notes
  const prevStep = currentCase.screens[currentCase.screens.length - 1];
  let carriedTabs = [];
  let carriedIntro = '';
  if (prevStep && prevStep.leftContent) {
    if (prevStep.leftContent.tabs) {
      carriedTabs = JSON.parse(JSON.stringify(prevStep.leftContent.tabs));
    }
    carriedIntro = prevStep.leftContent.intro || '';
  } else {
    carriedTabs = [
      { id: 'nn_' + Date.now(), title: "Nurses' Notes", content: '' }
    ];
  }
  
  const newStep = {
    step: nextNum,
    leftContent: {
      intro: carriedIntro,
      tabs: carriedTabs
    },
    question: {
      type: 'select_all',
      stem: '',
      options: [
        { text: '', correct: false },
        { text: '', correct: false },
        { text: '', correct: false },
        { text: '', correct: false },
        { text: '', correct: false }
      ],
      explanation: ''
    }
  };
  
  currentCase.screens.push(newStep);
  renderEditorStep(currentCase.screens.length - 1);
  showToast("Added screen " + nextNum);
}

function deleteStep(idx) {
  if (confirm(`Are you sure you want to delete Screen ${idx + 1}?`)) {
    currentCase.screens.splice(idx, 1);
    currentCase.screens.forEach((s, i) => s.step = i + 1);
    
    const newIdx = Math.max(0, currentStepIndex - 1);
    renderEditorStep(newIdx);
    showToast("Screen deleted.");
  }
}

function renderEditorTabs(tabs) {
  const list = document.getElementById('editor-tabs-list');
  list.innerHTML = '';
  
  if (tabs.length === 0) {
    document.getElementById('tab-content-editor').classList.add('hidden');
    activeTabId = '';
    return;
  }
  
  document.getElementById('tab-content-editor').classList.remove('hidden');
  
  if (!activeTabId || !tabs.find(t => t.id === activeTabId)) {
    activeTabId = tabs[0].id;
  }
  
  tabs.forEach((t) => {
    const tabEl = document.createElement('div');
    tabEl.className = `tab-editor-item ${t.id === activeTabId ? 'active' : ''}`;
    tabEl.setAttribute('data-id', t.id);
    tabEl.innerHTML = `<span>${escapeHTML(t.title)}</span>`;
    
    tabEl.addEventListener('click', () => {
      saveActiveTabContent();
      activeTabId = t.id;
      renderEditorTabs(tabs);
    });
    
    list.appendChild(tabEl);
  });
  
  const activeTab = tabs.find(t => t.id === activeTabId);
  document.getElementById('tab-title-input').value = activeTab.title;
  document.getElementById('tab-text-input').innerHTML = activeTab.content || '';
  document.getElementById('active-tab-label').textContent = `Content for "${activeTab.title}"`;
}

function saveActiveTabContent() {
  if (!activeTabId) return;
  const step = currentCase.screens[currentStepIndex];
  if (!step) return;
  const tabs = step.leftContent.tabs;
  const tab = tabs.find(t => t.id === activeTabId);
  if (tab) {
    tab.title = document.getElementById('tab-title-input').value;
    const rawContent = document.getElementById('tab-text-input').innerHTML;
    tab.content = formatNursesNotes(rawContent, tab.title);
    document.getElementById('tab-text-input').innerHTML = tab.content;
  }
}

function addTabToStep() {
  saveActiveTabContent();
  const tabs = currentCase.screens[currentStepIndex].leftContent.tabs;
  const newId = 'tab_' + Date.now();
  const newTab = {
    id: newId,
    title: 'New Tab',
    content: ''
  };
  
  tabs.push(newTab);
  activeTabId = newId;
  renderEditorStep(currentStepIndex);
}

function deleteActiveTab() {
  const tabs = currentCase.screens[currentStepIndex].leftContent.tabs;
  if (tabs.length <= 1) {
    alert("Must keep at least one chart tab.");
    return;
  }
  
  if (confirm("Delete this chart tab?")) {
    const idx = tabs.findIndex(t => t.id === activeTabId);
    tabs.splice(idx, 1);
    activeTabId = tabs[0].id;
    renderEditorStep(currentStepIndex);
  }
}

function saveCurrentStepData(isChangingType = false, isBackingOut = false) {
  if (!currentCase || currentCase.screens.length === 0) return true;
  
  const courseSelect = document.getElementById('case-course-select');
  const unitSelect = document.getElementById('case-unit-select');
  if (courseSelect && unitSelect) {
    currentCase.course = courseSelect.value || '';
    currentCase.unit = unitSelect.value || '';
    currentCase.disorder = currentCase.unit || currentCase.course || 'Others';
    currentCase.topic = currentCase.unit || currentCase.course || 'Others';
  } else {
    const select = document.getElementById('case-disorder-select');
    if (select) {
      currentCase.disorder = select.value;
    }
  }
  
  currentCase.title = document.getElementById('case-title-input').value;
  currentCase.description = document.getElementById('case-desc-input').value;
  
  const step = currentCase.screens[currentStepIndex];
  if (!step) return true;
  
  step.leftContent.intro = document.getElementById('step-intro-input').innerHTML;
  saveActiveTabContent();
  
  const q = step.question;
  
  q.preamble = document.getElementById('question-preamble-input').innerHTML;
  q.stem = document.getElementById('question-stem-input').innerHTML;
  q.explanation = document.getElementById('question-explanation-input').innerHTML;
  
  // Specific complex sync
  if (q.type === 'fill_blank') {
    const el = document.getElementById('fill-blank-correct-input');
    if (el) q.correctAnswer = el.value;
    const unitEl = document.getElementById('fill-blank-unit-input');
    if (unitEl) q.unit = unitEl.value;
  } else if (q.type === 'hotspot') {
    const el = document.getElementById('hotspot-url-input');
    if (el) q.imageUrl = el.value;
  } else if (q.type === 'highlight' || q.type === 'highlight_2') {
    const el = document.getElementById('highlight-tab-text-input');
    if (el && q.highlightTabs) {
      const activeTab = q.highlightTabs.find(t => t.id === highlightActiveTabId);
      if (activeTab) {
        activeTab.content = el.innerHTML;
      }
    }
    const titleEl = document.getElementById('highlight-tab-title-input');
    if (titleEl && q.highlightTabs) {
      const activeTab = q.highlightTabs.find(t => t.id === highlightActiveTabId);
      if (activeTab) {
        activeTab.title = titleEl.value;
      }
    }
    const maxInput = document.getElementById('highlight-max-correct-input');
    if (maxInput) q.maxCorrectSelections = parseInt(maxInput.value) || null;
  }
  
  const cIdx = caseStudies.findIndex(x => x.id === currentCase.id);
  if (cIdx !== -1) {
    caseStudies[cIdx] = currentCase;
  } else {
    // Also save standalone question back to its array
    const qIdx = standaloneQuestions.findIndex(x => x.id === currentCase.id);
    if (qIdx !== -1) {
      standaloneQuestions[qIdx] = currentCase;
    }
  }
  return true;
}

function exportCaseStudy(c) {
  const jsonStr = JSON.stringify(c, null, 2);
  const blob = new Blob([jsonStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `${c.title.replace(/\s+/g, '_')}_NGN_Quiz.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  showToast("Quiz JSON exported successfully.");
}

/* ================= 17 DYNAMIC EDITOR RENDERERS ================= */
function renderDynamicQuestionConfigurator(q) {
  const box = document.getElementById('question-details-editor');
  box.innerHTML = '';

  switch (q.type) {
    case 'dropdown_cloze':
    case 'drag_drop_cloze':
    case 'dyad':
    case 'triad':
      renderClozeConfigurator(q, box);
      break;
    case 'dropdown_table':
      renderDropdownTableConfigurator(q, box);
      break;
    case 'matrix_mc':
      renderMatrixMcConfigurator(q, box);
      break;
    case 'matrix_mr':
      renderMatrixMrConfigurator(q, box);
      break;
    case 'select_n':
      renderSelectNConfigurator(q, box);
      break;
    case 'bowtie':
      renderBowtieConfigurator(q, box);
      break;
    case 'multiple_choice':
      renderMultipleChoiceConfigurator(q, box);
      break;
    case 'fill_blank':
      renderFillBlankConfigurator(q, box);
      break;
    case 'hotspot':
      renderHotspotConfigurator(q, box);
      break;
    case 'ordered_response':
      renderOrderedResponseConfigurator(q, box);
      break;
    case 'select_all':
    case 'trend':
      renderSataConfigurator(q, box);
      break;
    case 'highlight':
    case 'highlight_2':
      renderHighlightConfigurator(q, box);
      break;
    case 'grouped_mr':
      renderGroupedMrConfigurator(q, box);
      break;
  }
}

function getClozeSegments(text, expectedCount) {
  const regex = /\[\[d(?:r)?op(\d+)\]\]/gi;
  let match;
  const matches = [];
  while ((match = regex.exec(text)) !== null) {
    matches.push({
      index: parseInt(match[1]),
      start: match.index,
      end: regex.lastIndex
    });
  }
  
  matches.sort((a, b) => a.index - b.index);
  
  const segments = [];
  let lastIndex = 0;
  for (let i = 0; i < expectedCount; i++) {
    const currentMatch = matches.find(m => m.index === i);
    if (currentMatch) {
      segments.push(text.substring(lastIndex, currentMatch.start));
      lastIndex = currentMatch.end;
    } else {
      segments.push('');
    }
  }
  segments.push(text.substring(lastIndex));
  return segments;
}

// 1. Cloze (Shared for Dropdown Cloze, Drag & Drop, Dyad, Triad)
function renderClozeConfigurator(q, box) {
  const c = q.cloze || { text: '', dropdowns: [] };
  const wrapper = document.createElement('div');
  
  const isDyadOrTriad = (q.type === 'dyad' || q.type === 'triad');
  
  let instructions = 'Sentence contains drop-down options. Set the choices and placeholder for each slot below.';
  if (q.type === 'dyad') instructions = 'Dyad requires exactly 2 slots: [[drop0]] and [[drop1]]. Both must be correct to score 1 point.';
  if (q.type === 'triad') instructions = 'Triad requires exactly 3 slots: [[drop0]], [[drop1]], and [[drop2]]. All must be correct.';
  
  let expectedSlots;
  if (q.type === 'dyad') {
    expectedSlots = 2;
  } else if (q.type === 'triad') {
    expectedSlots = 3;
  } else {
    if (!c.dropdowns || c.dropdowns.length === 0) {
      c.dropdowns = [
        { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] },
        { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] }
      ];
    }
    expectedSlots = c.dropdowns.length;
  }
  
  const segments = getClozeSegments(c.text || '', expectedSlots);
  let segmentInputsHTML = '';
  
  for (let i = 0; i <= expectedSlots; i++) {
    let placeholder = 'Text...';
    if (q.type === 'dyad') {
      if (i === 0) placeholder = 'The nurse should...';
      else if (i === 1) placeholder = '...as most evidenced by...';
      else if (i === 2) placeholder = 'Suffix text (optional)...';
    } else if (q.type === 'triad') {
      if (i === 0) placeholder = 'The nurse should...';
      else if (i === 1) placeholder = '...as most evidenced by...';
      else if (i === 2) placeholder = '...and...';
      else if (i === 3) placeholder = 'Suffix text (optional)...';
    } else {
      if (i === 0) placeholder = 'The patient should...';
      else if (i === 1) placeholder = '...due to...';
      else placeholder = 'Suffix text (optional)...';
    }
    
    segmentInputsHTML += `<input type="text" class="cloze-segment-input form-control" data-index="${i}" style="flex: 1; min-width: 140px; font-size:12px; padding:6px;" value="${escapeHTML(segments[i] || '')}" placeholder="${placeholder}">`;
    
    if (i < expectedSlots) {
      segmentInputsHTML += `<span class="cloze-slot-badge" style="background:#025287; color:white; padding:4px 8px; border-radius:4px; font-weight:600; font-size:11px; white-space:nowrap; user-select:none;">[Slot ${i + 1}]</span>`;
    }
  }
  
  const actionButtonsHTML = !isDyadOrTriad ? `
    <div style="margin-top: 10px; display: flex; gap: 8px;">
      <button id="add-cloze-slot-btn" class="btn btn-secondary btn-xs">+ Add Dropdown Slot</button>
      ${expectedSlots > 1 ? `<button id="remove-cloze-slot-btn" class="btn btn-danger btn-xs">- Remove Last Slot</button>` : ''}
    </div>
  ` : '';
  
  wrapper.innerHTML = `
    <div class="cloze-warning">${instructions}</div>
    <div class="form-group">
      <label>Question</label>
      <div style="display:flex; flex-direction:column; gap:10px; background:rgba(255,255,255,0.03); padding:12px; border-radius:var(--radius-sm); border:1px solid var(--border-dash);">
        <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
          ${segmentInputsHTML}
        </div>
        ${actionButtonsHTML}
      </div>
    </div>
    <div id="cloze-dropdowns-settings" style="margin-top: 16px;"></div>
  `;
  
  box.appendChild(wrapper);
  
  const settingsBox = document.getElementById('cloze-dropdowns-settings');
  
  const parseCloze = () => {
    const inputs = Array.from(wrapper.querySelectorAll('.cloze-segment-input'));
    inputs.sort((a, b) => parseInt(a.dataset.index) - parseInt(b.dataset.index));
    const segs = inputs.map(inp => inp.value);
    
    let assembledText = '';
    for (let i = 0; i < expectedSlots; i++) {
      assembledText += (segs[i] || '') + `[[drop${i}]]`;
    }
    assembledText += (segs[expectedSlots] || '');
    c.text = assembledText;
    
    settingsBox.innerHTML = '';
    const regex = /\[\[d(?:r)?op(\d+)\]\]/gi;
    let match;
    const foundIndices = [];
    while ((match = regex.exec(c.text)) !== null) {
      foundIndices.push(parseInt(match[1]));
    }
    const unique = [...new Set(foundIndices)].sort((a,b) => a-b);
    
    const temp = [];
    unique.forEach(idx => {
      if (!c.dropdowns[idx]) {
        c.dropdowns[idx] = {
          placeholder: 'Select...',
          options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }]
        };
      }
      const dd = c.dropdowns[idx];
      temp[idx] = dd;
      
      const card = document.createElement('div');
      card.className = 'cloze-dropdown-card';
      card.innerHTML = `
        <h6>Slot [[drop${idx}]]</h6>
        <input type="text" class="cloze-placeholder-input form-control" value="${escapeHTML(dd.placeholder)}" placeholder="Add placeholder...">
        <div class="options-config-title">
          <span>Choices</span>
          <button class="btn btn-text btn-xs add-choice-btn">+ Add Option</button>
        </div>
        <div class="choices-list"></div>
      `;
      
      card.querySelector('.cloze-placeholder-input').addEventListener('input', (e) => {
        dd.placeholder = e.target.value;
      });
      
      const choicesList = card.querySelector('.choices-list');
      const renderChoices = () => {
        choicesList.innerHTML = '';
        dd.options.forEach((opt, oIdx) => {
          const row = document.createElement('div');
          row.className = 'option-config-row';
          const placeholderText = `Choice ${String.fromCharCode(65 + oIdx)}`;
          
          let val = opt.text || '';
          const genericDefaults = [
            'Choice A', 'Choice B', 'Choice C', 'Choice D', 'Choice E',
            'Choice X', 'Choice Y', 'Choice Z',
            'Choice 1', 'Choice 2', 'Choice 3',
            'Correct Option', 'Incorrect Option', 'New Choice'
          ];
          if (genericDefaults.includes(val)) {
            val = '';
            opt.text = '';
          }
          
          row.innerHTML = `
            <input type="radio" name="cloze-correct-${idx}" class="choice-correct-toggle" ${opt.correct ? 'checked' : ''}>
            <input type="text" class="option-text-input form-control" style="font-size:12px; padding:6px;" value="${escapeHTML(val)}" placeholder="${placeholderText}">
            <button class="btn-option-delete">&times;</button>
          `;
          
          row.querySelector('.option-text-input').addEventListener('input', (e) => {
            opt.text = e.target.value;
          });
          row.querySelector('.choice-correct-toggle').addEventListener('change', () => {
            dd.options.forEach((o, oi) => o.correct = oi === oIdx);
          });
          row.querySelector('.btn-option-delete').addEventListener('click', () => {
            dd.options.splice(oIdx, 1);
            renderChoices();
          });
          choicesList.appendChild(row);
        });
      };
      
      card.querySelector('.add-choice-btn').addEventListener('click', () => {
        dd.options.push({ text: '', correct: false });
        renderChoices();
      });
      
      renderChoices();
      settingsBox.appendChild(card);
    });
    c.dropdowns = temp;
  };
  
  wrapper.querySelectorAll('.cloze-segment-input').forEach(inp => {
    inp.addEventListener('input', parseCloze);
  });
  
  if (!isDyadOrTriad) {
    const addBtn = wrapper.querySelector('#add-cloze-slot-btn');
    if (addBtn) {
      addBtn.addEventListener('click', () => {
        const inputs = Array.from(wrapper.querySelectorAll('.cloze-segment-input'));
        inputs.sort((a, b) => parseInt(a.dataset.index) - parseInt(b.dataset.index));
        const segs = inputs.map(inp => inp.value);
        
        let assembledText = '';
        for (let i = 0; i < expectedSlots; i++) {
          assembledText += (segs[i] || '') + `[[drop${i}]]`;
        }
        assembledText += (segs[expectedSlots] || '');
        c.text = assembledText + `[[drop${expectedSlots}]]`;
        
        c.dropdowns.push({
          placeholder: 'Select...',
          options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }]
        });
        
        renderDynamicQuestionConfigurator(q);
      });
    }
    
    const removeBtn = wrapper.querySelector('#remove-cloze-slot-btn');
    if (removeBtn) {
      removeBtn.addEventListener('click', () => {
        if (expectedSlots <= 1) return;
        
        const inputs = Array.from(wrapper.querySelectorAll('.cloze-segment-input'));
        inputs.sort((a, b) => parseInt(a.dataset.index) - parseInt(b.dataset.index));
        const segs = inputs.map(inp => inp.value);
        
        let assembledText = '';
        for (let i = 0; i < expectedSlots - 1; i++) {
          assembledText += (segs[i] || '') + `[[drop${i}]]`;
        }
        assembledText += (segs[expectedSlots - 1] || '') + (segs[expectedSlots] || '');
        c.text = assembledText;
        
        c.dropdowns.pop();
        
        renderDynamicQuestionConfigurator(q);
      });
    }
  }
  
  parseCloze();
}

// 2. Drop-Down Table Configurator
function renderDropdownTableConfigurator(q, box) {
  const rows = q.dropdownTableRows || [];
  
  if (rows.length === 0) {
    rows.push({
      label: '',
      placeholder: 'Select...',
      options: [{ text: '', correct: true }, { text: '', correct: false }]
    });
    rows.push({
      label: '',
      placeholder: 'Select...',
      options: [{ text: '', correct: true }, { text: '', correct: false }]
    });
    q.dropdownTableRows = rows;
  }

  const wrapper = document.createElement('div');
  wrapper.className = 'dropdown-table-editor-wrapper';
  wrapper.style.marginTop = '12px';

  const renderTable = () => {
    wrapper.innerHTML = '';
    
    const tableContainer = document.createElement('div');
    tableContainer.style.overflowX = 'auto';
    
    const table = document.createElement('table');
    table.className = 'matrix-grid-designer-table';
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';
    table.style.marginBottom = '12px';
    
    // THEAD
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    // Headers are reset when the question type changes (initializeQuestionTypeDefaults),
    // not on every render, so headers an author typed are never erased.
    const h1Val = q.dropdownTableHeader1 || '';
    const h2Val = q.dropdownTableHeader2 || '';
    
    // Column 1 Header Input
    const th1 = document.createElement('th');
    th1.style.padding = '8px';
    th1.style.minWidth = '200px';
    th1.innerHTML = `
      <input type="text" class="form-control dropdown-table-header-1-input" style="font-weight:bold; font-size:12px; padding:6px;" value="${escapeHTML(h1Val)}" placeholder="Column 1 Header Text">
    `;
    th1.querySelector('.dropdown-table-header-1-input').addEventListener('input', (e) => {
      q.dropdownTableHeader1 = e.target.value;
    });
    headerRow.appendChild(th1);
    
    // Column 2 Header Input
    const th2 = document.createElement('th');
    th2.style.padding = '8px';
    th2.style.minWidth = '280px';
    th2.innerHTML = `
      <input type="text" class="form-control dropdown-table-header-2-input" style="font-weight:bold; font-size:12px; padding:6px;" value="${escapeHTML(h2Val)}" placeholder="Column 2 Header Text">
    `;
    th2.querySelector('.dropdown-table-header-2-input').addEventListener('input', (e) => {
      q.dropdownTableHeader2 = e.target.value;
    });
    headerRow.appendChild(th2);
    
    // Action column header
    const thAction = document.createElement('th');
    thAction.style.width = '50px';
    thAction.innerHTML = '';
    headerRow.appendChild(thAction);
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // TBODY
    const tbody = document.createElement('tbody');
    rows.forEach((row, rIdx) => {
      const tr = document.createElement('tr');
      
      // Clean generic row label strings to empty for placeholder behavior
      let rLabel = row.label || '';
      const genericRows = ['Sensory Perception', 'Moisture', 'Activity', 'Mobility', 'Nutrition', 'Friction and Shear'];
      if (genericRows.includes(rLabel)) {
        rLabel = '';
        row.label = '';
      }
      
      // Left Cell: Row label input
      const tdLabel = document.createElement('td');
      tdLabel.style.padding = '8px';
      tdLabel.style.verticalAlign = 'top';
      tdLabel.innerHTML = `
        <input type="text" class="form-control row-label-input" style="font-size:12px; padding:6px; font-weight:500;" value="${escapeHTML(rLabel)}" placeholder="Text...">
      `;
      tdLabel.querySelector('.row-label-input').addEventListener('input', (e) => {
        row.label = e.target.value;
      });
      tr.appendChild(tdLabel);
      
      // Right Cell: Placeholder and Dropdown options configurator
      const tdOptions = document.createElement('td');
      tdOptions.style.padding = '8px';
      tdOptions.innerHTML = `
        <div style="display:flex; flex-direction:column; gap:6px;">
          <input type="text" class="form-control row-placeholder-input" style="font-size:11px; padding:4px 8px; font-style:italic;" value="${escapeHTML(row.placeholder || 'Select...')}" placeholder="Placeholder (e.g. Select...)">
          <div class="row-options-container" style="display:flex; flex-direction:column; gap:4px; margin-top:4px;"></div>
          <button class="btn btn-text btn-xs add-row-option-btn" style="align-self:flex-start; font-size:10px; margin-top:2px;">+ Add Option</button>
        </div>
      `;
      
      const placeholderInput = tdOptions.querySelector('.row-placeholder-input');
      placeholderInput.addEventListener('input', (e) => {
        row.placeholder = e.target.value;
      });
      
      const optionsContainer = tdOptions.querySelector('.row-options-container');
      const renderRowOptions = () => {
        optionsContainer.innerHTML = '';
        const opts = row.options || [];
        opts.forEach((opt, oIdx) => {
          const optDiv = document.createElement('div');
          optDiv.style.display = 'flex';
          optDiv.style.alignItems = 'center';
          optDiv.style.gap = '6px';
          
          let val = opt.text || '';
          const genericDefaults = [
            'Choice A', 'Choice B', 'Choice C',
            'Option 1', 'Option 2', 'Option 3',
            '1 - Correct', '2 - Incorrect', 'Correct Answer', 'Incorrect Answer', 'New Option', 'New Choice'
          ];
          if (genericDefaults.includes(val)) {
            val = '';
            opt.text = '';
          }
          const placeholderText = `Option ${oIdx + 1}`;
          
          optDiv.innerHTML = `
            <input type="radio" name="dropdown-table-correct-radio-${rIdx}" class="row-opt-correct-toggle" ${opt.correct ? 'checked' : ''} style="cursor:pointer;">
            <input type="text" class="form-control row-opt-text-input" style="font-size:11px; padding:4px 6px; flex-grow:1;" value="${escapeHTML(val)}" placeholder="${placeholderText}">
            <button class="delete-opt-btn" style="background:transparent; border:none; color:#ef4444; font-size:16px; cursor:pointer; padding:0 4px;">&times;</button>
          `;
          
          optDiv.querySelector('.row-opt-text-input').addEventListener('input', (e) => {
            opt.text = e.target.value;
          });
          optDiv.querySelector('.row-opt-correct-toggle').addEventListener('change', () => {
            opts.forEach((o, oi) => o.correct = oi === oIdx);
          });
          optDiv.querySelector('.delete-opt-btn').addEventListener('click', () => {
            opts.splice(oIdx, 1);
            renderRowOptions();
          });
          
          optionsContainer.appendChild(optDiv);
        });
      };
      
      tdOptions.querySelector('.add-row-option-btn').addEventListener('click', () => {
        if (!row.options) row.options = [];
        row.options.push({ text: '', correct: false });
        renderRowOptions();
      });
      
      renderRowOptions();
      tr.appendChild(tdOptions);
      
      // Delete Row Button Cell
      const tdDel = document.createElement('td');
      tdDel.style.padding = '8px';
      tdDel.style.verticalAlign = 'top';
      tdDel.style.textAlign = 'center';
      tdDel.innerHTML = `
        <button class="delete-row-btn" style="background:transparent; border:none; color:#ef4444; font-size:18px; cursor:pointer; padding:4px 0 0 0;">&times;</button>
      `;
      tdDel.querySelector('.delete-row-btn').addEventListener('click', () => {
        rows.splice(rIdx, 1);
        renderTable();
      });
      tr.appendChild(tdDel);
      
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    tableContainer.appendChild(table);
    wrapper.appendChild(tableContainer);
    
    // Bottom Action Buttons
    const btnContainer = document.createElement('div');
    btnContainer.style.display = 'flex';
    btnContainer.style.marginTop = '10px';
    
    const addRowBtn = document.createElement('button');
    addRowBtn.className = 'btn btn-secondary btn-xs';
    addRowBtn.textContent = '+ Add Row';
    addRowBtn.addEventListener('click', () => {
      rows.push({
        label: '',
        placeholder: 'Select...',
        options: [{ text: '', correct: true }, { text: '', correct: false }]
      });
      renderTable();
    });
    btnContainer.appendChild(addRowBtn);
    wrapper.appendChild(btnContainer);
  };
  
  renderTable();
  box.appendChild(wrapper);
}

// 3. Matrix MC (Single choice per row)
function renderMatrixMcConfigurator(q, box) {
  renderMatrixBaseConfigurator(q, box, false);
}

// 4. Matrix MR (Multiple response/checkboxes per row)
function renderMatrixMrConfigurator(q, box) {
  renderMatrixBaseConfigurator(q, box, true);
}

function renderMatrixBaseConfigurator(q, box, isMultiResponse) {
  if (!q.matrix) {
    q.matrix = {
      firstColumnHeader: '',
      columns: isMultiResponse ? ['', '', ''] : ['Indicated', 'Not Indicated'],
      rows: isMultiResponse ? [
        { text: '', correctIndices: [], correctIndex: 0 },
        { text: '', correctIndices: [], correctIndex: 0 }
      ] : [
        { text: '', correctIndex: 0, correctIndices: [0] },
        { text: '', correctIndex: 0, correctIndices: [0] }
      ]
    };
  }
  const m = q.matrix;
  if (!m.firstColumnHeader && isMultiResponse) {
    m.firstColumnHeader = '';
  }
  if (!m.columns || m.columns.length < 2) {
    m.columns = isMultiResponse ? ['', '', ''] : ['Indicated', 'Not Indicated'];
  }
  if (!m.rows || m.rows.length === 0) {
    m.rows = isMultiResponse ? [
      { text: '', correctIndex: 0, correctIndices: [] },
      { text: '', correctIndex: 0, correctIndices: [] }
    ] : [
      { text: '', correctIndex: 0, correctIndices: [0] },
      { text: '', correctIndex: 0, correctIndices: [0] }
    ];
  }

  const wrapper = document.createElement('div');
  wrapper.className = 'matrix-table-editor-wrapper';
  wrapper.style.marginTop = '12px';

  const renderTable = () => {
    wrapper.innerHTML = '';
    
    const tableContainer = document.createElement('div');
    tableContainer.style.overflowX = 'auto';
    
    const table = document.createElement('table');
    table.className = 'matrix-grid-designer-table';
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';
    table.style.marginBottom = '12px';
    
    // THEAD
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    // Generic default headers are cleared when the question type changes
    // (initializeQuestionTypeDefaults), not here: clearing on every render erased
    // headers such as "Findings" that authors chose on purpose.
    const h1Val = m.firstColumnHeader || '';

    // First column header input
    const thFirst = document.createElement('th');
    thFirst.style.padding = '8px';
    thFirst.style.minWidth = '180px';
    thFirst.innerHTML = `
      <input type="text" class="form-control matrix-first-header-input" style="font-weight:bold; font-size:12px; padding:6px;" value="${escapeHTML(h1Val)}" placeholder="Add text...">
    `;
    thFirst.querySelector('.matrix-first-header-input').addEventListener('input', (e) => {
      m.firstColumnHeader = e.target.value;
    });
    headerRow.appendChild(thFirst);
    
    // Additional column headers inputs
    m.columns.forEach((col, cIdx) => {
      const thCol = document.createElement('th');
      thCol.style.padding = '8px';
      thCol.style.textAlign = 'center';
      thCol.style.position = 'relative';
      thCol.style.minWidth = '120px';
      thCol.innerHTML = `
        <div style="display:flex; align-items:center; gap:4px; justify-content:center;">
          <input type="text" class="form-control matrix-col-header-input" style="font-size:12px; text-align:center; padding:6px;" value="${escapeHTML(col)}" placeholder="Add text...">
          ${m.columns.length > 2 ? `<button class="delete-col-btn" style="background:transparent; border:none; color:#ef4444; font-size:16px; cursor:pointer; padding:0 4px;">&times;</button>` : ''}
        </div>
      `;
      thCol.querySelector('.matrix-col-header-input').addEventListener('input', (e) => {
        m.columns[cIdx] = e.target.value;
      });
      if (m.columns.length > 2) {
        thCol.querySelector('.delete-col-btn').addEventListener('click', () => {
          m.columns.splice(cIdx, 1);
          // Shift correct indexes if needed
          m.rows.forEach(r => {
            if (isMultiResponse) {
              r.correctIndices = (r.correctIndices || []).filter(idx => idx !== cIdx).map(idx => idx > cIdx ? idx - 1 : idx);
            } else {
              if (r.correctIndex === cIdx) r.correctIndex = 0;
              else if (r.correctIndex > cIdx) r.correctIndex--;
            }
          });
          renderTable();
        });
      }
      headerRow.appendChild(thCol);
    });
    
    // Actions column header
    const thActions = document.createElement('th');
    thActions.style.width = '50px';
    thActions.style.padding = '8px';
    thActions.innerHTML = '';
    headerRow.appendChild(thActions);
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // TBODY
    const tbody = document.createElement('tbody');
    m.rows.forEach((r, rIdx) => {
      const tr = document.createElement('tr');
      
      // Clean generic row label strings to empty for placeholder behavior
      let rText = r.text || '';
      const genericRows = ['clear liquid diet', 'soapsuds enema', 'polyuria', 'weight gain', 'New Row 1', 'New Row 2'];
      if (genericRows.includes(rText)) {
        rText = '';
        r.text = '';
      }
      
      // Row Label Input
      const tdLabel = document.createElement('td');
      tdLabel.style.padding = '8px';
      tdLabel.innerHTML = `
        <input type="text" class="form-control matrix-row-label-input" style="font-size:12px; padding:6px;" value="${escapeHTML(rText)}" placeholder="Text...">
      `;
      tdLabel.querySelector('.matrix-row-label-input').addEventListener('input', (e) => {
        r.text = e.target.value;
      });
      tr.appendChild(tdLabel);
      
      // Correct indicator cells
      m.columns.forEach((col, cIdx) => {
        const tdCheck = document.createElement('td');
        tdCheck.style.padding = '8px';
        tdCheck.style.textAlign = 'center';
        
        const isChecked = isMultiResponse
          ? (r.correctIndices || []).includes(cIdx)
          : r.correctIndex === cIdx;
        
        tdCheck.innerHTML = `
          <input type="${isMultiResponse ? 'checkbox' : 'radio'}" name="matrix-row-radio-${rIdx}" ${isChecked ? 'checked' : ''} style="transform: scale(1.1); cursor:pointer;">
        `;
        tdCheck.querySelector('input').addEventListener('change', (e) => {
          if (isMultiResponse) {
            if (!r.correctIndices) r.correctIndices = [];
            if (e.target.checked) {
              r.correctIndices.push(cIdx);
            } else {
              r.correctIndices = r.correctIndices.filter(v => v !== cIdx);
            }
          } else {
            r.correctIndex = cIdx;
          }
        });
        tr.appendChild(tdCheck);
      });
      
      // Delete Row Button Cell
      const tdDel = document.createElement('td');
      tdDel.style.padding = '8px';
      tdDel.style.textAlign = 'center';
      tdDel.innerHTML = `
        <button class="delete-row-btn" style="background:transparent; border:none; color:#ef4444; font-size:18px; cursor:pointer; padding:0;">&times;</button>
      `;
      tdDel.querySelector('.delete-row-btn').addEventListener('click', () => {
        m.rows.splice(rIdx, 1);
        renderTable();
      });
      tr.appendChild(tdDel);
      
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    tableContainer.appendChild(table);
    wrapper.appendChild(tableContainer);
    
    // Bottom Action Buttons
    const btnContainer = document.createElement('div');
    btnContainer.style.display = 'flex';
    btnContainer.style.gap = '10px';
    btnContainer.style.marginTop = '10px';
    
    const addRowBtn = document.createElement('button');
    addRowBtn.className = 'btn btn-secondary btn-xs';
    addRowBtn.textContent = '+ Add Row';
    addRowBtn.addEventListener('click', () => {
      m.rows.push({ text: '', correctIndex: 0, correctIndices: [0] });
      renderTable();
    });
    btnContainer.appendChild(addRowBtn);
    
    const addColBtn = document.createElement('button');
    addColBtn.className = 'btn btn-secondary btn-xs';
    addColBtn.textContent = '+ Add Column';
    addColBtn.addEventListener('click', () => {
      m.columns.push('');
      renderTable();
    });
    btnContainer.appendChild(addColBtn);
    
    wrapper.appendChild(btnContainer);
  };
  
  renderTable();
  box.appendChild(wrapper);
}

// 5. Select N Configurator
function renderSelectNConfigurator(q, box) {
  renderOptionsBaseConfigurator(q, box, true, true);
}

// 7. Multiple Choice Configurator
function renderMultipleChoiceConfigurator(q, box) {
  renderOptionsBaseConfigurator(q, box, false, false);
}

// 11. Select All Configurator
function renderSataConfigurator(q, box) {
  renderOptionsBaseConfigurator(q, box, true, false);
}

function renderOptionsBaseConfigurator(q, box, isCheckbox, showNLimit) {
  const wrapper = document.createElement('div');
  if (showNLimit) {
    wrapper.innerHTML = `
      <div class="form-group" style="margin-bottom:16px;">
        <label>Select Exactly N Limit</label>
        <input type="number" id="selectN-limit-input" class="form-control" style="width:100px;" value="${q.limit || 3}">
      </div>
    `;
  }
  wrapper.innerHTML += `
    <div class="options-config-title">
      <span>Options List</span>
      <button id="add-option-btn" class="btn btn-text btn-xs">+ Add Option</button>
    </div>
    <div id="options-config-list"></div>
  `;
  box.appendChild(wrapper);
  
  if (showNLimit) {
    document.getElementById('selectN-limit-input').addEventListener('input', (e) => {
      q.limit = parseInt(e.target.value) || 3;
    });
  }
  
  const list = document.getElementById('options-config-list');
  const renderRows = () => {
    list.innerHTML = '';
    if (!q.options) q.options = [];
    
    q.options.forEach((opt, idx) => {
      const div = document.createElement('div');
      div.className = 'option-config-row';
      div.style.display = 'flex';
      div.style.flexDirection = 'column';
      div.style.gap = '8px';
      div.style.border = '1px solid #334155';
      div.style.padding = '8px';
      div.style.borderRadius = 'var(--radius-sm)';
      div.style.marginBottom = '8px';
      div.style.background = '#1e293b';
      
      const placeholderText = `Option ${String.fromCharCode(65 + idx)}`;
      
      let val = opt.text || '';
      const genericDefaults = [
        'Option A', 'Option B', 'Option C', 'Option D', 'Option E', 'Option F',
        'Option 1', 'Option 2', 'Option 3', 'Option 4'
      ];
      if (genericDefaults.includes(val)) {
        val = '';
        opt.text = '';
      }
      
      div.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px; width:100%;">
          <input type="${isCheckbox ? 'checkbox' : 'radio'}" name="correct-option-group" class="option-correct-toggle" ${opt.correct ? 'checked' : ''}>
          <input type="text" class="option-text-input form-control" style="flex-grow:1;" value="${escapeHTML(val)}" placeholder="${placeholderText}">
          <button class="btn-option-delete">&times;</button>
        </div>
        <div style="display:flex; align-items:center; gap:8px; width:100%;">
          <span style="font-size:11px; color:#94a3b8; flex-shrink:0;">Image URL:</span>
          <input type="text" class="option-image-input form-control" style="font-size:11px; padding:4px 8px; flex-grow:1; height:24px;" value="${escapeHTML(opt.imageUrl || '')}" placeholder="Option image URL or Base64 data...">
          <button class="btn btn-secondary btn-xs select-image-file-btn" style="font-size:10px; height:24px; padding:0 8px; flex-shrink:0;">Choose File</button>
          <input type="file" class="option-image-file-input" accept="image/*" style="display:none;">
        </div>
      `;
      
      div.querySelector('.option-text-input').addEventListener('input', (e) => {
        opt.text = e.target.value;
      });
      div.querySelector('.option-image-input').addEventListener('input', (e) => {
        opt.imageUrl = e.target.value;
      });
      
      const fileInput = div.querySelector('.option-image-file-input');
      const selectBtn = div.querySelector('.select-image-file-btn');
      const imgInput = div.querySelector('.option-image-input');
      
      selectBtn.addEventListener('click', () => {
        fileInput.click();
      });
      fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (evt) => {
          opt.imageUrl = evt.target.result;
          imgInput.value = evt.target.result;
          showToast("Image loaded from local computer.");
        };
        reader.readAsDataURL(file);
      });

      div.querySelector('.option-correct-toggle').addEventListener('change', (e) => {
        if (isCheckbox) {
          opt.correct = e.target.checked;
        } else {
          q.options.forEach((o, oi) => o.correct = oi === idx);
        }
      });
      div.querySelector('.btn-option-delete').addEventListener('click', () => {
        q.options.splice(idx, 1);
        renderRows();
      });
      
      list.appendChild(div);
    });
  };
  
  renderRows();
  
  document.getElementById('add-option-btn').addEventListener('click', () => {
    if (!q.options) q.options = [];
    q.options.push({ text: 'New Option', correct: false });
    renderRows();
  });
}

// 6. Bowtie Configurator
function renderBowtieConfigurator(q, box) {
  if (!q.bowtieActions) q.bowtieActions = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
  if (!q.bowtieConditions) q.bowtieConditions = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
  if (!q.bowtieParams) q.bowtieParams = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
  
  if (!q.bowtieLeftPlaceholder) q.bowtieLeftPlaceholder = '';
  if (!q.bowtieCenterPlaceholder) q.bowtieCenterPlaceholder = '';
  if (!q.bowtieRightPlaceholder) q.bowtieRightPlaceholder = '';
  
  if (!q.bowtieCol1Header) q.bowtieCol1Header = '';
  if (!q.bowtieCol2Header) q.bowtieCol2Header = '';
  if (!q.bowtieCol3Header) q.bowtieCol3Header = '';

  const wrapper = document.createElement('div');
  wrapper.style.display = 'flex';
  wrapper.style.flexDirection = 'column';
  wrapper.style.gap = '20px';

  wrapper.innerHTML = `
    <div style="background:#1e293b; padding:12px; border-radius:var(--radius-sm); border:1px solid #334155;">
      <h5 style="margin-top:0; margin-bottom:12px; color:white; font-size:13px; font-weight:600;">Bowtie Diagram Targets Placeholders</h5>
      <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px;">
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:10px; color:#94a3b8; margin-bottom:4px;">Left Targets (Actions)</label>
          <input type="text" id="bowtie-left-holder" class="form-control" style="font-size:11px; padding:4px;" value="${escapeHTML(q.bowtieLeftPlaceholder)}" placeholder="Action to Take">
        </div>
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:10px; color:#94a3b8; margin-bottom:4px;">Center Target (Condition)</label>
          <input type="text" id="bowtie-center-holder" class="form-control" style="font-size:11px; padding:4px;" value="${escapeHTML(q.bowtieCenterPlaceholder)}" placeholder="Condition Most Likely Experiencing">
        </div>
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:10px; color:#94a3b8; margin-bottom:4px;">Right Targets (Parameters)</label>
          <input type="text" id="bowtie-right-holder" class="form-control" style="font-size:11px; padding:4px;" value="${escapeHTML(q.bowtieRightPlaceholder)}" placeholder="Parameter to Monitor">
        </div>
      </div>
    </div>

    <div style="background:#1e293b; padding:12px; border-radius:var(--radius-sm); border:1px solid #334155;">
      <h5 style="margin-top:0; margin-bottom:12px; color:white; font-size:13px; font-weight:600;">Bowtie Table Configuration</h5>
      <p style="font-size:11px; color:#94a3b8; margin-top:-6px; margin-bottom:12px;">Mark the correct choices that should be dragged into the targets (exactly 2 in Col 1, 1 in Col 2, and 2 in Col 3).</p>
      
      <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:16px;">
        <!-- Column 1 -->
        <div style="display:flex; flex-direction:column; gap:8px;">
          <input type="text" id="bowtie-col1-header" class="form-control" style="font-weight:bold; text-align:center; font-size:12px;" value="${escapeHTML(q.bowtieCol1Header)}" placeholder="Actions to Take">
          <div id="bowtie-col1-list" style="display:flex; flex-direction:column; gap:6px;"></div>
          <button id="add-bowtie-col1-btn" class="btn btn-secondary btn-xs" style="margin-top:4px;">+ Add Choice</button>
        </div>
        
        <!-- Column 2 -->
        <div style="display:flex; flex-direction:column; gap:8px;">
          <input type="text" id="bowtie-col2-header" class="form-control" style="font-weight:bold; text-align:center; font-size:12px;" value="${escapeHTML(q.bowtieCol2Header)}" placeholder="Potential Conditions">
          <div id="bowtie-col2-list" style="display:flex; flex-direction:column; gap:6px;"></div>
          <button id="add-bowtie-col2-btn" class="btn btn-secondary btn-xs" style="margin-top:4px;">+ Add Choice</button>
        </div>
        
        <!-- Column 3 -->
        <div style="display:flex; flex-direction:column; gap:8px;">
          <input type="text" id="bowtie-col3-header" class="form-control" style="font-weight:bold; text-align:center; font-size:12px;" value="${escapeHTML(q.bowtieCol3Header)}" placeholder="Parameters to Monitor">
          <div id="bowtie-col3-list" style="display:flex; flex-direction:column; gap:6px;"></div>
          <button id="add-bowtie-col3-btn" class="btn btn-secondary btn-xs" style="margin-top:4px;">+ Add Choice</button>
        </div>
      </div>
    </div>
  `;
  
  box.appendChild(wrapper);

  // Bind placeholder inputs
  document.getElementById('bowtie-left-holder').addEventListener('input', (e) => q.bowtieLeftPlaceholder = e.target.value);
  document.getElementById('bowtie-center-holder').addEventListener('input', (e) => q.bowtieCenterPlaceholder = e.target.value);
  document.getElementById('bowtie-right-holder').addEventListener('input', (e) => q.bowtieRightPlaceholder = e.target.value);
  
  document.getElementById('bowtie-col1-header').addEventListener('input', (e) => q.bowtieCol1Header = e.target.value);
  document.getElementById('bowtie-col2-header').addEventListener('input', (e) => q.bowtieCol2Header = e.target.value);
  document.getElementById('bowtie-col3-header').addEventListener('input', (e) => q.bowtieCol3Header = e.target.value);

  // Helper to render rows inside each list
  const renderColList = (listId, array) => {
    const listEl = document.getElementById(listId);
    listEl.innerHTML = '';
    array.forEach((opt, idx) => {
      const row = document.createElement('div');
      row.className = 'option-config-row';
      row.style.gap = '4px';
      row.style.marginBottom = '2px';
      row.innerHTML = `
        <input type="checkbox" class="bowtie-correct-toggle" ${opt.correct ? 'checked' : ''} style="margin-right:2px;">
        <input type="text" class="form-control bowtie-input" style="font-size:11px; padding:2px 4px; height:24px;" value="${escapeHTML(opt.text)}" placeholder="Option ${idx + 1}">
        <button class="btn-option-delete" style="font-size:14px; padding:0 4px;">&times;</button>
      `;
      
      row.querySelector('.bowtie-input').addEventListener('input', (e) => {
        opt.text = e.target.value;
      });
      row.querySelector('.bowtie-correct-toggle').addEventListener('change', (e) => {
        opt.correct = e.target.checked;
      });
      row.querySelector('.btn-option-delete').addEventListener('click', () => {
        array.splice(idx, 1);
        renderColList(listId, array);
      });
      listEl.appendChild(row);
    });
  };

  const renderAll = () => {
    renderColList('bowtie-col1-list', q.bowtieActions);
    renderColList('bowtie-col2-list', q.bowtieConditions);
    renderColList('bowtie-col3-list', q.bowtieParams);
  };

  renderAll();

  document.getElementById('add-bowtie-col1-btn').addEventListener('click', () => {
    q.bowtieActions.push({ text: 'New Choice', correct: false });
    renderColList('bowtie-col1-list', q.bowtieActions);
  });
  document.getElementById('add-bowtie-col2-btn').addEventListener('click', () => {
    q.bowtieConditions.push({ text: 'New Choice', correct: false });
    renderColList('bowtie-col2-list', q.bowtieConditions);
  });
  document.getElementById('add-bowtie-col3-btn').addEventListener('click', () => {
    q.bowtieParams.push({ text: 'New Choice', correct: false });
    renderColList('bowtie-col3-list', q.bowtieParams);
  });
}

// 8. Fill-in-blank calculation Configurator
function renderFillBlankConfigurator(q, box) {
  const wrapper = document.createElement('div');
  wrapper.className = 'form-group';
  wrapper.innerHTML = `
    <div style="display: flex; gap: 12px; align-items: flex-end;">
      <div style="flex: 1;">
        <label for="fill-blank-correct-input">Correct Answer (Numeric value or word)</label>
        <input type="text" id="fill-blank-correct-input" class="form-control" value="${escapeHTML(q.correctAnswer || '')}" placeholder="Type answer...">
      </div>
      <div style="flex: 1;">
        <label for="fill-blank-unit-input">Unit</label>
        <input type="text" id="fill-blank-unit-input" class="form-control" value="${escapeHTML(q.unit || '')}" placeholder="Type Unit">
      </div>
    </div>
  `;
  box.appendChild(wrapper);
}

// 9. Hotspot Configurator
function renderHotspotConfigurator(q, box) {
  const wrapper = document.createElement('div');
  wrapper.innerHTML = `
    <div class="form-group" style="margin-bottom:12px;">
      <label for="hotspot-url-input">Hotspot Image URL</label>
      <input type="text" id="hotspot-url-input" class="form-control" value="${escapeHTML(q.imageUrl || '')}">
    </div>
    <div class="cloze-warning">Draw a box on the image below to set the correct coordinates.</div>
    <div style="text-align:center;">
      <div id="hotspot-editor-img-container" class="hotspot-image-container">
        <img id="hotspot-editor-img" class="hotspot-image" src="${escapeHTML(q.imageUrl || '')}" alt="Hotspot Image">
        <div id="hotspot-editor-box" class="hotspot-target-region" style="display:none;"></div>
      </div>
    </div>
  `;
  box.appendChild(wrapper);
  
  const imgInput = document.getElementById('hotspot-url-input');
  const imgEl = document.getElementById('hotspot-editor-img');
  const targetBox = document.getElementById('hotspot-editor-box');
  const imgContainer = document.getElementById('hotspot-editor-img-container');
  
  imgInput.addEventListener('change', (e) => {
    imgEl.src = e.target.value;
    q.imageUrl = e.target.value;
  });
  
  // Set current visual box
  const showSavedBox = () => {
    const r = q.rect;
    if (r) {
      targetBox.style.display = 'block';
      targetBox.style.left = Math.min(r.x1, r.x2) + '%';
      targetBox.style.top = Math.min(r.y1, r.y2) + '%';
      targetBox.style.width = Math.abs(r.x2 - r.x1) + '%';
      targetBox.style.height = Math.abs(r.y2 - r.y1) + '%';
    }
  };
  
  imgEl.onload = showSavedBox;
  showSavedBox();
  
  // Drawing logic
  let startX = 0, startY = 0, drawing = false;
  
  imgContainer.addEventListener('mousedown', (e) => {
    if (e.target !== imgEl && e.target !== targetBox) return;
    drawing = true;
    const rect = imgContainer.getBoundingClientRect();
    startX = ((e.clientX - rect.left) / rect.width) * 100;
    startY = ((e.clientY - rect.top) / rect.height) * 100;
    q.rect = { x1: startX, y1: startY, x2: startX, y2: startY };
    showSavedBox();
  });
  
  imgContainer.addEventListener('mousemove', (e) => {
    if (!drawing) return;
    const rect = imgContainer.getBoundingClientRect();
    const currentX = ((e.clientX - rect.left) / rect.width) * 100;
    const currentY = ((e.clientY - rect.top) / rect.height) * 100;
    
    q.rect.x2 = Math.min(100, Math.max(0, currentX));
    q.rect.y2 = Math.min(100, Math.max(0, currentY));
    showSavedBox();
  });
  
  window.addEventListener('mouseup', () => {
    drawing = false;
  });
}

// 10. Ordered Response Configurator
function renderOrderedResponseConfigurator(q, box) {
  const steps = q.orderedOptions || [];
  const wrapper = document.createElement('div');
  wrapper.innerHTML = `
    <div class="options-config-title">
      <span>Steps in CORRECT Order</span>
      <button id="add-order-opt-btn" class="btn btn-text btn-xs">+ Add Step</button>
    </div>
    <div id="ordered-items-config-list"></div>
  `;
  box.appendChild(wrapper);
  
  const list = document.getElementById('ordered-items-config-list');
  const renderSteps = () => {
    list.innerHTML = '';
    steps.forEach((step, idx) => {
      const div = document.createElement('div');
      div.className = 'option-config-row';
      div.innerHTML = `
        <span style="font-weight:bold; color:var(--nclex-sky); width:20px;">${idx + 1}.</span>
        <input type="text" class="form-control step-input-field" value="${escapeHTML(step)}">
        <button class="btn-option-delete">&times;</button>
      `;
      div.querySelector('.step-input-field').addEventListener('input', (e) => {
        steps[idx] = e.target.value;
      });
      div.querySelector('.btn-option-delete').addEventListener('click', () => {
        steps.splice(idx, 1);
        renderSteps();
      });
      list.appendChild(div);
    });
  };
  
  renderSteps();
  
  document.getElementById('add-order-opt-btn').addEventListener('click', () => {
    steps.push('Next instruction step');
    q.orderedOptions = steps;
    renderSteps();
  });
}

function renderHighlightConfigurator(q, box) {
  if (!q.highlightTabs) {
    q.highlightTabs = [
      { id: 'ht_' + Date.now(), title: "Nurses' Notes", content: q.highlightText || '' }
    ];
  }
  
  if (!highlightActiveTabId || !q.highlightTabs.find(t => t.id === highlightActiveTabId)) {
    highlightActiveTabId = q.highlightTabs[0].id;
  }
  
  const activeTab = q.highlightTabs.find(t => t.id === highlightActiveTabId);
  
  const wrapper = document.createElement('div');
  wrapper.className = 'highlight-tabs-editor-container';
  wrapper.innerHTML = `
    <div class="cloze-warning" style="margin-bottom: 12px;">
      Wrap phrases in curly braces like: <strong>{unstable vitals|correct}</strong> for correct findings, or <strong>{temperature of 98.6 F}</strong> for incorrect findings that are click-selectable.
    </div>
    
    <div class="tabs-editor-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
      <h5 style="margin:0;">Highlight Chart Tabs</h5>
      <button id="add-highlight-tab-btn" class="btn btn-text btn-xs">+ Add Tab</button>
    </div>
    
    <div id="highlight-editor-tabs-list" class="tabs-list-horizontal" style="display:flex; gap:4px; margin-bottom:8px; border-bottom:1px solid var(--border-color); padding-bottom:4px; overflow-x:auto;">
      ${q.highlightTabs.map(t => `
        <div class="tab-editor-item ${t.id === highlightActiveTabId ? 'active' : ''}" data-id="${t.id}" style="padding: 6px 12px; border: 1px solid var(--border-color); border-bottom: none; border-radius: 4px 4px 0 0; cursor: pointer; font-size:13px; font-weight:500;">
          <span>${escapeHTML(t.title)}</span>
        </div>
      `).join('')}
    </div>
    
    <div id="highlight-tab-content-editor" class="tab-content-editor-box" style="border: 1px solid var(--border-color); padding: 12px; border-radius: 4px; background: var(--background-secondary);">
      <div class="form-group no-margin">
        <label style="display:block; margin-bottom: 6px; font-weight: 500; font-size:13px;">Content for "${escapeHTML(activeTab.title)}"</label>
        <input type="text" id="highlight-tab-title-input" class="tab-title-rename" placeholder="Tab Title" value="${escapeHTML(activeTab.title)}" style="width:100%; padding:6px; border:1px solid var(--border-color); border-radius:4px; margin-bottom:10px; font-size:13px;">
        
        <div class="rich-editor-container" style="border:1px solid var(--border-color); border-radius:4px; overflow:hidden; background:#ffffff; margin-bottom:10px;">
          <div class="rich-editor-toolbar" style="display:flex; flex-wrap:wrap; gap:4px; padding:6px; border-bottom:1px solid var(--border-color); background:var(--background-primary);">
            <button type="button" class="toolbar-btn" data-cmd="bold" title="Bold"><b>B</b></button>
            <button type="button" class="toolbar-btn" data-cmd="superscript" title="Superscript">x<sup>2</sup></button>
            <button type="button" class="toolbar-btn" data-cmd="subscript" title="Subscript">x<sub>2</sub></button>
            <button type="button" class="toolbar-btn btn-symbol" data-symbol="&deg;" title="Degree Symbol">&deg;</button>
            <button type="button" class="toolbar-btn btn-symbol" data-symbol="&ge;" title="Greater Than or Equal to">&ge;</button>
            <button type="button" class="toolbar-btn btn-symbol" data-symbol="&le;" title="Less Than or Equal to">&le;</button>
            <button type="button" class="toolbar-btn" data-cmd="insertUnorderedList" title="Bullet List">• List</button>
            <button type="button" class="toolbar-btn" data-cmd="insertOrderedList" title="Numbered List">1. List</button>
            <button type="button" class="toolbar-btn table-insert-btn" title="Insert Table">
              <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" style="vertical-align: middle;"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>
              Table
            </button>
          </div>
          <div contenteditable="true" class="rich-text-editor" id="highlight-tab-text-input" placeholder="Enter chart text or tables here..." style="min-height: 150px; padding: 12px; outline: none; font-size:14px; line-height:1.5;">${activeTab.content || ''}</div>
        </div>
        
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <button id="delete-highlight-tab-btn" class="btn btn-danger btn-xs">Delete This Tab</button>
          <div>
            <label for="highlight-max-correct-input" style="font-size:12px; margin-right: 6px;">Max Correct (optional):</label>
            <input type="number" id="highlight-max-correct-input" class="form-control" style="width: 70px; display:inline-block; padding:4px;" min="1" value="${q.maxCorrectSelections || ''}">
          </div>
        </div>
      </div>
    </div>
  `;
  box.appendChild(wrapper);
  
  // Attach event listeners for highlight tabs editor
  const titleInput = document.getElementById('highlight-tab-title-input');
  titleInput.addEventListener('input', (e) => {
    activeTab.title = e.target.value;
    const tabHeader = document.querySelector(`#highlight-editor-tabs-list .tab-editor-item[data-id="${highlightActiveTabId}"] span`);
    if (tabHeader) tabHeader.textContent = e.target.value;
  });
  
  // Tab switching
  const tabItems = wrapper.querySelectorAll('#highlight-editor-tabs-list .tab-editor-item');
  tabItems.forEach(item => {
    item.addEventListener('click', () => {
      activeTab.content = document.getElementById('highlight-tab-text-input').innerHTML;
      highlightActiveTabId = item.getAttribute('data-id');
      renderDynamicQuestionConfigurator(q);
    });
  });
  
  // Add tab
  document.getElementById('add-highlight-tab-btn').addEventListener('click', () => {
    activeTab.content = document.getElementById('highlight-tab-text-input').innerHTML;
    const newId = 'ht_' + Date.now();
    q.highlightTabs.push({
      id: newId,
      title: 'New Tab',
      content: ''
    });
    highlightActiveTabId = newId;
    renderDynamicQuestionConfigurator(q);
  });
  
  // Delete tab
  document.getElementById('delete-highlight-tab-btn').addEventListener('click', () => {
    if (q.highlightTabs.length <= 1) {
      alert("Must keep at least one tab.");
      return;
    }
    if (confirm("Delete this tab?")) {
      const idx = q.highlightTabs.findIndex(t => t.id === highlightActiveTabId);
      q.highlightTabs.splice(idx, 1);
      highlightActiveTabId = q.highlightTabs[0].id;
      renderDynamicQuestionConfigurator(q);
    }
  });
}

// 14. Grouped Multiple Response Configurator
function renderGroupedMrConfigurator(q, box) {
  const groups = q.groupedRows || [];
  const wrapper = document.createElement('div');
  wrapper.innerHTML = `
    <div class="options-config-title">
      <span>Checkbox Groups</span>
      <button id="add-grouped-category-btn" class="btn btn-text btn-xs">+ Add Group</button>
    </div>
    <div id="grouped-categories-editor-container"></div>
  `;
  box.appendChild(wrapper);
  
  const container = document.getElementById('grouped-categories-editor-container');
  const renderGroups = () => {
    container.innerHTML = '';
    groups.forEach((g, gIdx) => {
      const card = document.createElement('div');
      card.className = 'cloze-dropdown-card';
      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
          <input type="text" class="form-control group-title-input" style="font-weight:bold; width:80%;" value="${escapeHTML(g.title)}" placeholder="Group Name (e.g. Pharmacological)">
          <button class="btn btn-danger btn-xs delete-group-btn">Delete Group</button>
        </div>
        <div class="options-config-title">
          <span>Options</span>
          <button class="btn btn-text btn-xs add-group-opt-btn">+ Add Option</button>
        </div>
        <div class="group-opts-list"></div>
      `;
      
      card.querySelector('.group-title-input').addEventListener('input', (e) => {
        g.title = e.target.value;
      });
      card.querySelector('.delete-group-btn').addEventListener('click', () => {
        groups.splice(gIdx, 1);
        renderGroups();
      });
      
      const optsList = card.querySelector('.group-opts-list');
      const renderGroupOptions = () => {
        optsList.innerHTML = '';
        g.options.forEach((opt, oIdx) => {
          const div = document.createElement('div');
          div.className = 'option-config-row';
          div.innerHTML = `
            <input type="checkbox" class="opt-correct-toggle" ${opt.correct ? 'checked' : ''}>
            <input type="text" class="form-control opt-text-input" style="font-size:12px; padding:6px;" value="${escapeHTML(opt.text)}">
            <button class="btn-option-delete">&times;</button>
          `;
          
          div.querySelector('.opt-text-input').addEventListener('input', (e) => {
            opt.text = e.target.value;
          });
          div.querySelector('.opt-correct-toggle').addEventListener('change', (e) => {
            opt.correct = e.target.checked;
          });
          div.querySelector('.btn-option-delete').addEventListener('click', () => {
            g.options.splice(oIdx, 1);
            renderGroupOptions();
          });
          optsList.appendChild(div);
        });
      };
      
      card.querySelector('.add-group-opt-btn').addEventListener('click', () => {
        g.options.push({ text: 'New Option', correct: false });
        renderGroupOptions();
      });
      
      renderGroupOptions();
      container.appendChild(card);
    });
  };
  
  renderGroups();
  
  document.getElementById('add-grouped-category-btn').addEventListener('click', () => {
    groups.push({
      title: 'New Group',
      options: [{ text: 'Correct action', correct: true }, { text: 'Incorrect action', correct: false }]
    });
    q.groupedRows = groups;
    renderGroups();
  });
}


/* ================= HIGH FIDELITY NCLEX PLAYER ENGINE ================= */
function initPlayerEvents() {
  document.getElementById('player-quit-btn').addEventListener('click', () => {
    if (confirm("Are you sure you want to quit the quiz? Your current progress will be lost.")) {
      switchView('student');
    }
  });

  // Question Navigator Button (Right-justified) and Drawer Overlay
  const navBtn = document.getElementById('player-nav-btn');
  if (navBtn) navBtn.addEventListener('click', () => toggleQuestionNavigator());

  const closeNavBtn = document.getElementById('close-question-nav-btn');
  if (closeNavBtn) closeNavBtn.addEventListener('click', () => toggleQuestionNavigator(false));

  const navBackdrop = document.getElementById('question-nav-drawer-backdrop');
  if (navBackdrop) navBackdrop.addEventListener('click', () => toggleQuestionNavigator(false));

  // Test Mode Submit Confirmation Modal
  const testModal = document.getElementById('test-submit-modal');
  const testCloseBtn = document.getElementById('test-submit-close-btn');
  const testCancelBtn = document.getElementById('test-submit-cancel-btn');
  const testConfirmBtn = document.getElementById('test-submit-confirm-btn');
  if (testCloseBtn) testCloseBtn.addEventListener('click', closeTestSubmitModal);
  if (testCancelBtn) testCancelBtn.addEventListener('click', closeTestSubmitModal);
  if (testConfirmBtn) testConfirmBtn.addEventListener('click', confirmTestSubmitAndAdvance);
  if (testModal) {
    testModal.addEventListener('click', (e) => {
      if (e.target === testModal) closeTestSubmitModal();
    });
  }

  document.getElementById('player-calc-btn').addEventListener('click', toggleCalculator);
  document.getElementById('close-calc-btn').addEventListener('click', toggleCalculator);

  document.getElementById('player-submit-btn').addEventListener('click', handlePlayerSubmit);
  document.getElementById('player-giveup-btn').addEventListener('click', handlePlayerGiveUp);

  const skipModal = document.getElementById('skip-question-modal');
  const skipNoBtn = document.getElementById('skip-modal-no-btn');
  const skipCloseBtn = document.getElementById('skip-modal-close-btn');
  const skipYesBtn = document.getElementById('skip-modal-yes-btn');

  if (skipNoBtn) skipNoBtn.addEventListener('click', closeSkipQuestionModal);
  if (skipCloseBtn) skipCloseBtn.addEventListener('click', closeSkipQuestionModal);
  if (skipYesBtn) skipYesBtn.addEventListener('click', confirmSkipQuestion);
  if (skipModal) {
    skipModal.addEventListener('click', (e) => {
      if (e.target === skipModal) closeSkipQuestionModal();
    });
  }

  document.getElementById('player-prev-btn').addEventListener('click', () => {
    if (sessionConfig.mode === 'test' && !sessionConfig.isRemediation) {
      return; // No backtracking in Test Mode
    }
    if (playerStepIndex > 0) {
      playerStepIndex--;
      renderPlayerStep(playerStepIndex);
    }
  });

  document.getElementById('player-next-btn').addEventListener('click', () => {
    // 1. In Remediation Mode: free browsing to next question
    if (sessionConfig.isRemediation) {
      if (playerStepIndex < currentCase.screens.length - 1) {
        playerStepIndex++;
        renderPlayerStep(playerStepIndex);
      } else {
        loadResultsView();
      }
      return;
    }

    // 2. In Test Mode: prompt confirmation or skip before advancing (irreversible)
    if (sessionConfig.mode === 'test') {
      const step = currentCase.screens[playerStepIndex];
      const hasAnswer = step ? hasSelectedAnyAnswer(step.question, playerStepIndex) : false;
      if (!hasAnswer) {
        showSkipQuestionModal();
        return;
      }
      showTestSubmitModal();
      return;
    }

    // 3. In Review Mode (Tutor): requires submitting before advancing
    const isSubmitted = submittedAnswers[playerStepIndex];
    if (!isSubmitted) {
      const step = currentCase.screens[playerStepIndex];
      const hasAnswer = step ? hasSelectedAnyAnswer(step.question, playerStepIndex) : false;
      if (!hasAnswer) {
        showSkipQuestionModal();
        return;
      }
      alert("Please submit your response first by clicking the Submit button.");
      return;
    }
    if (playerStepIndex < currentCase.screens.length - 1) {
      playerStepIndex++;
      renderPlayerStep(playerStepIndex);
    } else {
      loadResultsView();
    }
  });
}

function showTestSubmitModal() {
  const modal = document.getElementById('test-submit-modal');
  if (modal) modal.classList.remove('hidden');
}

function closeTestSubmitModal() {
  const modal = document.getElementById('test-submit-modal');
  if (modal) modal.classList.add('hidden');
}

function confirmTestSubmitAndAdvance() {
  closeTestSubmitModal();
  submittedAnswers[playerStepIndex] = true;
  evaluateStepScore(playerStepIndex);
  if (playerStepIndex < currentCase.screens.length - 1) {
    playerStepIndex++;
    renderPlayerStep(playerStepIndex);
  } else {
    loadResultsView();
  }
}

function toggleQuestionNavigator(forceState) {
  const drawer = document.getElementById('question-navigator-drawer');
  const backdrop = document.getElementById('question-nav-drawer-backdrop');
  if (!drawer) return;

  const shouldOpen = typeof forceState === 'boolean' ? forceState : drawer.classList.contains('hidden');
  if (shouldOpen) {
    renderQuestionNavigatorList();
    drawer.classList.remove('hidden');
    if (backdrop) backdrop.classList.remove('hidden');
  } else {
    drawer.classList.add('hidden');
    if (backdrop) backdrop.classList.add('hidden');
  }
}

function startPlayer(caseStudy, config) {
  migrateCaseTypes(caseStudy);
  currentCase = caseStudy;
  playerStepIndex = 0;
  playerActiveTabId = '';
  
  playerAnswers = {};
  submittedAnswers = {};
  playerScores = {};

  if (config) {
    sessionConfig = Object.assign({
      mode: 'review',
      isRemediation: false,
      allowBacktrack: config.mode !== 'test'
    }, config);
  } else {
    sessionConfig = {
      mode: 'review',
      isRemediation: false,
      allowBacktrack: true
    };
  }

  // In remediation review, mark all steps as submitted initially
  if (sessionConfig.isRemediation) {
    currentCase.screens.forEach((s, idx) => {
      submittedAnswers[idx] = true;
      if (!playerScores[idx]) evaluateStepScore(idx);
    });
  }
  
  const calc = document.getElementById('ti108-calculator');
  if (calc) calc.classList.add('hidden');
  closeSkipQuestionModal();
  closeTestSubmitModal();
  toggleQuestionNavigator(false);
  
  switchView('player');
  renderPlayerStep(0);
}

function renderPlayerStep(stepIdx) {
  playerStepIndex = stepIdx;
  const step = currentCase.screens[stepIdx];
  if (!step) return;
  
  document.getElementById('player-progress-text').textContent = `${stepIdx + 1} of ${currentCase.screens.length}`;
  document.getElementById('player-question-number-title').textContent = `Question ${stepIdx + 1}`;
  
  const isSubmitted = submittedAnswers[stepIdx] || sessionConfig.isRemediation;
  
  const statusEl = document.getElementById('player-question-status-text');
  statusEl.textContent = isSubmitted ? 'Complete' : 'Not complete';
  
  const isStepStandalone = currentCase.isStandalone || step.isStandalone;
  const screenLabel = document.getElementById('player-screen-label');
  if (isStepStandalone) {
    screenLabel.style.display = 'none';
  } else {
    screenLabel.style.display = 'block';
    screenLabel.textContent = `Case Study Screen ${stepIdx + 1} of ${currentCase.screens.length}`;
  }
  document.getElementById('player-intro-text').innerHTML = step.leftContent.intro || '';
  
  // Full-width adaptive layout for questions with no tabs
  const splitContainer = document.querySelector('.player-center-split');
  if (splitContainer) {
    const hasLeftContent = step.leftContent && step.leftContent.tabs && step.leftContent.tabs.length > 0 && step.question.type !== 'highlight';
    if (!hasLeftContent) {
      splitContainer.classList.add('full-width');
    } else {
      splitContainer.classList.remove('full-width');
    }
  }

  // Question Navigator button visibility: Hidden in active Test Mode, Visible in Review Mode & Remediation Review
  const navBtn = document.getElementById('player-nav-btn');
  if (navBtn) {
    if (sessionConfig.mode === 'test' && !sessionConfig.isRemediation) {
      navBtn.style.display = 'none';
    } else {
      navBtn.style.display = 'inline-flex';
    }
  }

  // Case Transition Banner (Shown when a case study begins)
  const caseBanner = document.getElementById('player-case-banner');
  const bannerText = document.getElementById('player-case-banner-text');
  if (caseBanner && bannerText) {
    const isNewCaseStart = !isStepStandalone && (stepIdx === 0 || currentCase.screens[stepIdx - 1]?.isStandalone || (currentCase.screens[stepIdx - 1]?.caseId && currentCase.screens[stepIdx - 1]?.caseId !== step.caseId));
    if (isNewCaseStart) {
      const caseName = step.caseTitle || currentCase.title || 'Unfolding Clinical Case';
      bannerText.innerHTML = `The following 6 questions refer to this clinical scenario: <strong>${caseName}</strong>.`;
      caseBanner.classList.remove('hidden');
    } else {
      caseBanner.classList.add('hidden');
    }
  }

  // Populate and show full-width meta header if in highlight question type
  const fullwidthHeader = document.getElementById('player-fullwidth-meta-header');
  if (fullwidthHeader) {
    if (step.question.type === 'highlight') {
      fullwidthHeader.classList.remove('hidden');
      document.getElementById('player-fullwidth-question-number-title').textContent = `Question ${stepIdx + 1}`;
      document.getElementById('player-fullwidth-question-status-text').textContent = isSubmitted ? 'Complete' : 'Not complete';
      
      const fwScreenLabel = document.getElementById('player-fullwidth-screen-label');
      if (fwScreenLabel) {
        if (isStepStandalone) {
          fwScreenLabel.style.display = 'none';
        } else {
          fwScreenLabel.style.display = 'block';
          fwScreenLabel.textContent = `Case Study Screen ${stepIdx + 1} of ${currentCase.screens.length}`;
        }
      }
    } else {
      fullwidthHeader.classList.add('hidden');
    }
  }

  renderPlayerTabs(step.leftContent.tabs);
  renderQuestionNavigatorList();
  
  const preambleEl = document.getElementById('player-question-preamble');
  if (preambleEl) {
    if (step.question.preamble && step.question.preamble.trim() && step.question.preamble.trim() !== '<br>') {
      preambleEl.innerHTML = step.question.preamble;
      preambleEl.classList.remove('hidden');
    } else {
      preambleEl.innerHTML = '';
      preambleEl.classList.add('hidden');
    }
  }
  
  // Render question image in player if present
  const imgContainer = document.getElementById('player-question-image-container');
  const playerImg = document.getElementById('player-question-image');
  if (imgContainer && playerImg) {
    if (step.question.questionImage) {
      playerImg.src = step.question.questionImage;
      imgContainer.classList.remove('hidden');
    } else {
      playerImg.src = '';
      imgContainer.classList.add('hidden');
    }
  }
  
  document.getElementById('player-question-stem').innerHTML = step.question.stem || '';
  
  renderPlayerAnswersBox(step.question, stepIdx);
  
  // Footer navigation buttons
  const prevBtn = document.getElementById('player-prev-btn');
  const nextBtn = document.getElementById('player-next-btn');

  // Previous button: strictly hidden in active Test Mode
  if (sessionConfig.mode === 'test' && !sessionConfig.isRemediation) {
    prevBtn.style.display = 'none';
  } else {
    prevBtn.style.display = 'inline-flex';
    prevBtn.disabled = stepIdx === 0;
  }

  // Next button label
  const isLast = (stepIdx === currentCase.screens.length - 1);
  if (sessionConfig.mode === 'test' && !sessionConfig.isRemediation) {
    nextBtn.innerHTML = isLast
      ? 'Finish Exam & Submit <svg viewBox="0 0 24 24" width="16" height="16" style="vertical-align: middle; fill: currentColor; margin-left: 6.5px; transform: rotate(180deg);"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>'
      : 'Submit & Next <svg viewBox="0 0 24 24" width="16" height="16" style="vertical-align: middle; fill: currentColor; margin-left: 6.5px; transform: rotate(180deg);"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>';
  } else {
    nextBtn.innerHTML = isLast
      ? 'Finish attempt <svg viewBox="0 0 24 24" width="16" height="16" style="vertical-align: middle; fill: currentColor; margin-left: 6.5px; transform: rotate(180deg);"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>'
      : 'Next <svg viewBox="0 0 24 24" width="16" height="16" style="vertical-align: middle; fill: currentColor; margin-left: 6.5px; transform: rotate(180deg);"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>';
  }
  
  const submitBtn = document.getElementById('player-submit-btn');
  const giveupBtn = document.getElementById('player-giveup-btn');
  
  if (sessionConfig.isRemediation) {
    // In remediation review, hide submit actions
    if (submitBtn) submitBtn.style.display = 'none';
    if (giveupBtn) giveupBtn.style.display = 'none';
  } else if (sessionConfig.mode === 'test') {
    // In test mode, submission happens on "Submit & Next" button
    if (submitBtn) submitBtn.style.display = 'none';
    if (giveupBtn) giveupBtn.style.display = 'none';
  } else {
    if (submitBtn) {
      submitBtn.style.display = '';
      submitBtn.disabled = isSubmitted;
    }
    if (giveupBtn) {
      giveupBtn.style.display = 'none';
      giveupBtn.disabled = isSubmitted;
    }
  }
  
  // Feedback card: only shown in Review Mode (after submit) or in Remediation Review
  const feedbackCard = document.getElementById('player-feedback-card');
  if (sessionConfig.isRemediation || (sessionConfig.mode === 'review' && isSubmitted)) {
    feedbackCard.classList.remove('hidden');
    displayPlayerFeedback(stepIdx);
  } else {
    feedbackCard.classList.add('hidden');
  }
}

function renderPlayerTabs(tabs) {
  const tabsBar = document.getElementById('player-chart-tabs');
  const contentBox = document.getElementById('player-chart-content');
  tabsBar.innerHTML = '';
  contentBox.innerHTML = '';
  
  if (!tabs || tabs.length === 0) {
    contentBox.innerHTML = '<p style="color:#9ca3af; font-style:italic;">No chart entries.</p>';
    return;
  }
  
  if (!playerActiveTabId || !tabs.find(t => t.id === playerActiveTabId)) {
    playerActiveTabId = tabs[0].id;
  }
  
  tabs.forEach(t => {
    const tabBtn = document.createElement('button');
    tabBtn.className = `patient-chart-tab ${t.id === playerActiveTabId ? 'active' : ''}`;
    tabBtn.textContent = t.title;
    tabBtn.addEventListener('click', () => {
      playerActiveTabId = t.id;
      renderPlayerTabs(tabs);
    });
    tabsBar.appendChild(tabBtn);
  });
  
  const activeTab = tabs.find(t => t.id === playerActiveTabId);
  contentBox.innerHTML = activeTab ? formatNursesNotes(activeTab.content, activeTab.title) : '';
}

function renderQuestionNavigatorList() {
  const drawerList = document.getElementById('question-nav-drawer-list');
  if (!drawerList || !currentCase || !currentCase.screens) return;
  drawerList.innerHTML = '';

  currentCase.screens.forEach((step, idx) => {
    const item = document.createElement('div');
    item.className = 'nav-drawer-item';
    if (idx === playerStepIndex) item.classList.add('active');

    const isSub = submittedAnswers[idx];
    if (isSub) item.classList.add('complete');

    // Title / Context label
    const typeLabel = (step.question.type || 'Question').toUpperCase().replace(/_/g, ' ');
    const isStepStandalone = currentCase.isStandalone || step.isStandalone;
    const contextLabel = isStepStandalone ? 'Stand-alone Question' : (step.caseTitle || currentCase.title || `Case Study Screen ${step.step || (idx + 1)}`);

    let badgeClass = 'badge-incomplete';
    let badgeText = 'Incomplete';

    if (sessionConfig.isRemediation) {
      const sc = playerScores[idx] || { score: 0, max: 1 };
      if (sc.score === sc.max) {
        badgeClass = 'badge-correct';
        badgeText = `✓ Correct (${sc.score}/${sc.max})`;
      } else if (sc.score > 0) {
        badgeClass = 'badge-partial';
        badgeText = `Partial (${sc.score}/${sc.max})`;
      } else {
        badgeClass = 'badge-incorrect';
        badgeText = `✗ Incorrect (0/${sc.max})`;
      }
    } else if (idx === playerStepIndex) {
      badgeClass = 'badge-current';
      badgeText = 'Current';
    } else if (isSub) {
      badgeClass = 'badge-complete';
      badgeText = 'Complete';
    }

    item.innerHTML = `
      <div class="nav-drawer-item-left">
        <div class="nav-drawer-item-num">${idx + 1}</div>
        <div class="nav-drawer-item-info">
          <span class="nav-drawer-item-title">${contextLabel}</span>
          <span class="nav-drawer-item-sub">Question ${idx + 1} &bull; ${typeLabel}</span>
        </div>
      </div>
      <span class="nav-drawer-item-badge ${badgeClass}">${badgeText}</span>
    `;

    item.addEventListener('click', () => {
      // In Review Mode or Remediation review, student can jump freely
      if (sessionConfig.mode === 'review' || sessionConfig.isRemediation) {
        renderPlayerStep(idx);
        toggleQuestionNavigator(false);
      } else {
        showToast("Backtracking is not permitted during Test Mode.", "info");
      }
    });

    drawerList.appendChild(item);
  });
}

/* ================= 17 PLAYER OPTIONS RENDERERS ================= */
function renderPlayerAnswersBox(q, stepIdx) {
  const box = document.getElementById('player-answer-box');
  if (!box) return;
  box.innerHTML = '';
  const isSubmitted = submittedAnswers[stepIdx];
  const userAnswers = playerAnswers[stepIdx];

  try {
    switch (q.type) {
      case 'dropdown_cloze':
      case 'cloze':
      case 'dyad':
      case 'triad':
        renderPlayerDropdownCloze(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'drag_drop_cloze':
        renderPlayerDragDropCloze(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'dropdown_table':
        renderPlayerDropdownTable(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'matrix_mc':
      case 'matrix':
        renderPlayerMatrixMc(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'matrix_mr':
        renderPlayerMatrixMr(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'select_n':
      case 'selectN':
        renderPlayerSelectN(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'bowtie':
        renderPlayerBowtie(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'multiple_choice':
      case 'single':
        renderPlayerMultipleChoice(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'fill_blank':
        renderPlayerFillBlank(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'hotspot':
        renderPlayerHotspot(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'ordered_response':
        renderPlayerOrderedResponse(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'select_all':
      case 'sata':
      case 'trend':
        renderPlayerSata(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'highlight':
      case 'highlight_2':
        renderPlayerHighlight(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'grouped_mr':
        renderPlayerGroupedMr(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      default:
        console.warn("Unknown question type:", q.type);
        box.innerHTML = `<div style="color:var(--accent-red); padding:16px; border:1px solid var(--accent-red); background-color:rgba(239, 68, 68, 0.05); border-radius:4px; font-size:13px;">
          <strong>Error:</strong> Unknown question type "${escapeHTML(q.type)}".
        </div>`;
    }
  } catch (err) {
    console.error("Error rendering player answers box:", err);
    box.innerHTML = `<div style="color:var(--accent-red); padding:16px; border:1px solid var(--accent-red); background-color:rgba(239, 68, 68, 0.05); border-radius:4px; font-size:13px;">
      <strong>Error rendering answer options:</strong> ${escapeHTML(err.message)}<br>
      <small style="display:block; margin-top:8px; opacity:0.8;">This could be due to legacy or corrupted case study data. Try recreating or editing the case study.</small>
    </div>`;
  }
}

// 1. Dropdown Cloze & Rationales (Dyad / Triad)
function renderPlayerDropdownCloze(q, stepIdx, box, isSubmitted, userAnswers) {
  const c = q.cloze || { text: '', dropdowns: [] };
  const container = document.createElement('div');
  container.className = 'cloze-sentence';
  
  let baseText = c.text || '';
  const regex = /\[\[d(?:r)?op(\d+)\]\]/gi;
  let lastIndex = 0;
  let match;
  
  const stateAnswers = userAnswers || {};
  const dropdowns = c.dropdowns || [];
  
  while ((match = regex.exec(baseText)) !== null) {
    const textSpan = document.createElement('span');
    textSpan.innerHTML = baseText.substring(lastIndex, match.index);
    container.appendChild(textSpan);
    const idx = parseInt(match[1]);
    const dd = dropdowns[idx];
    
    if (dd && dd.options) {
      const select = document.createElement('select');
      select.className = 'cloze-select';
      if (isSubmitted) select.disabled = true;
      
      const defOpt = document.createElement('option');
      defOpt.textContent = dd.placeholder || 'Select...';
      defOpt.value = '';
      select.appendChild(defOpt);
      
      const savedVal = stateAnswers[idx];
      dd.options.forEach((opt, oIdx) => {
        const oEl = document.createElement('option');
        oEl.textContent = opt.text || '';
        oEl.value = oIdx;
        if (savedVal !== undefined && parseInt(savedVal) === oIdx) {
          oEl.selected = true;
        }
        select.appendChild(oEl);
      });
      
      if (isSubmitted) {
        const correctIdx = dd.options.findIndex(o => o.correct);
        if (parseInt(savedVal) === correctIdx) {
          select.classList.add('show-correct');
        } else {
          select.classList.add('show-incorrect');
        }
      } else {
        select.addEventListener('change', (e) => {
          if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
          playerAnswers[stepIdx][idx] = e.target.value !== '' ? parseInt(e.target.value) : undefined;
        });
      }
      container.appendChild(select);
    } else {
      const fallback = document.createElement('span');
      fallback.textContent = `[drop${idx}]`;
      container.appendChild(fallback);
    }
    lastIndex = regex.lastIndex;
  }
  const endSpan = document.createElement('span');
  endSpan.innerHTML = baseText.substring(lastIndex);
  container.appendChild(endSpan);
  box.appendChild(container);
}

// 2. Drag and Drop Cloze
function renderPlayerDragDropCloze(q, stepIdx, box, isSubmitted, userAnswers) {
  const c = q.cloze || { text: '', dropdowns: [] };
  const container = document.createElement('div');
  container.className = 'cloze-sentence';
  
  const stateAnswers = userAnswers || {}; // { dropIdx: optionText }
  const dropdowns = c.dropdowns || [];
  
  let baseText = c.text || '';
  const regex = /\[\[d(?:r)?op(\d+)\]\]/gi;
  let lastIndex = 0;
  let match;
  
  while ((match = regex.exec(baseText)) !== null) {
    const textSpan = document.createElement('span');
    textSpan.innerHTML = baseText.substring(lastIndex, match.index);
    container.appendChild(textSpan);
    const idx = parseInt(match[1]);
    const dd = dropdowns[idx];
    
    if (dd) {
      const slot = document.createElement('div');
      slot.className = 'drag-blank-slot';
      
      const placedVal = stateAnswers[idx];
      if (placedVal) {
        slot.classList.add('occupied');
        slot.textContent = placedVal;
      } else {
        slot.textContent = `[Slot ${idx + 1}]`;
      }
      
      if (isSubmitted) {
        const correctText = dd.options ? (dd.options.find(o => o.correct)?.text || '') : '';
        if (placedVal === correctText) {
          slot.classList.add('show-correct');
        } else {
          slot.classList.add('show-incorrect');
        }
      } else {
        // Click blank to clear
        slot.addEventListener('click', () => {
          if (stateAnswers[idx]) {
            delete stateAnswers[idx];
            playerAnswers[stepIdx] = stateAnswers;
            renderPlayerStep(stepIdx);
          }
        });
      }
      container.appendChild(slot);
    }
    lastIndex = regex.lastIndex;
  }
  const endSpan = document.createElement('span');
  endSpan.innerHTML = baseText.substring(lastIndex);
  container.appendChild(endSpan);
  box.appendChild(container);
  
  // Options pool
  if (!isSubmitted) {
    const pool = document.createElement('div');
    pool.className = 'drag-options-pool';
    pool.innerHTML = '<span style="font-size:11px; width:100%; font-weight:700; color:#64748b; margin-bottom:4px;">Drag / Click a term to place in blank slots:</span>';
    
    // Aggregate options
    const allOptions = [];
    dropdowns.forEach(dd => {
      if (dd && dd.options) dd.options.forEach(o => allOptions.push(o.text));
    });
    const uniqueOptions = [...new Set(allOptions)];
    
    uniqueOptions.forEach(optText => {
      const isAlreadyPlaced = Object.values(stateAnswers).includes(optText);
      const token = document.createElement('div');
      token.className = `drag-option-token ${isAlreadyPlaced ? 'placed' : ''}`;
      token.textContent = optText;
      
      if (!isAlreadyPlaced) {
        token.addEventListener('click', () => {
          // Find first empty slot
          const targetIndex = dropdowns.findIndex((dd, i) => dd && !stateAnswers[i]);
          if (targetIndex !== -1) {
            if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
            playerAnswers[stepIdx][targetIndex] = optText;
            renderPlayerStep(stepIdx);
          }
        });
      }
      pool.appendChild(token);
    });
    box.appendChild(pool);
  }
}

// 3. Drop-Down Table
function renderPlayerDropdownTable(q, stepIdx, box, isSubmitted, userAnswers) {
  const rows = q.dropdownTableRows || [];
  const stateAnswers = userAnswers || {};
  const tbl = document.createElement('table');
  tbl.className = 'exam-matrix-table';
  
  const header1 = q.dropdownTableHeader1 || 'Category Findings';
  const header2 = q.dropdownTableHeader2 || 'Clinical Assessment Score / Selection';
  
  tbl.innerHTML = `
    <thead>
      <tr>
        <th>${escapeHTML(header1)}</th>
        <th>${escapeHTML(header2)}</th>
      </tr>
    </thead>
    <tbody></tbody>
  `;
  const tbody = tbl.querySelector('tbody');
  
  rows.forEach((row, rIdx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${escapeHTML(row.label)}</td>
      <td>
        <select class="cloze-select row-select-box" style="width:100%; max-width:260px;" ${isSubmitted ? 'disabled' : ''}>
          <option value="">${escapeHTML(row.placeholder || 'Select...')}</option>
        </select>
      </td>
    `;
    
    const select = tr.querySelector('.row-select-box');
    const savedVal = stateAnswers[rIdx];
    
    const rowOptions = row.options || [];
    rowOptions.forEach((opt, oIdx) => {
      const oEl = document.createElement('option');
      oEl.textContent = opt.text || '';
      oEl.value = oIdx;
      if (savedVal !== undefined && parseInt(savedVal) === oIdx) oEl.selected = true;
      select.appendChild(oEl);
    });
    
    if (isSubmitted) {
      const correctIdx = rowOptions.findIndex(o => o.correct);
      if (parseInt(savedVal) === correctIdx) {
        select.classList.add('show-correct');
      } else {
        select.classList.add('show-incorrect');
      }
    } else {
      select.addEventListener('change', (e) => {
        if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
        playerAnswers[stepIdx][rIdx] = e.target.value !== '' ? parseInt(e.target.value) : undefined;
      });
    }
    
    tbody.appendChild(tr);
  });
  box.appendChild(tbl);
}

// 4. Matrix MC (Single choice per row)
function renderPlayerMatrixMc(q, stepIdx, box, isSubmitted, userAnswers) {
  renderPlayerMatrixBase(q, stepIdx, box, isSubmitted, userAnswers, false);
}

// 13. Matrix MR (Multiple response checkboxes per row)
function renderPlayerMatrixMr(q, stepIdx, box, isSubmitted, userAnswers) {
  renderPlayerMatrixBase(q, stepIdx, box, isSubmitted, userAnswers, true);
}

function renderPlayerMatrixBase(q, stepIdx, box, isSubmitted, userAnswers, isMultiResponse) {
  const m = q.matrix || { columns: [], rows: [] };
  const columns = m.columns || [];
  const rows = m.rows || [];
  const tbl = document.createElement('table');
  tbl.className = isMultiResponse ? 'exam-matrix-table matrix-mr-table' : 'exam-matrix-table';
  
  let html = `<thead><tr><th>${escapeHTML(m.firstColumnHeader || (isMultiResponse ? 'Findings' : 'Column 1'))}</th>`;
  columns.forEach(col => { html += `<th>${escapeHTML(col)}</th>`; });
  html += `</tr></thead><tbody>`;
  
  const savedAnswers = userAnswers || {};
  
  rows.forEach((r, rIdx) => {
    html += `<tr><td>${escapeHTML(r.text)}</td>`;
    columns.forEach((col, cIdx) => {
      let isChecked = false;
      if (isMultiResponse) {
        isChecked = (savedAnswers[rIdx] || []).includes(cIdx);
      } else {
        isChecked = savedAnswers[rIdx] === cIdx;
      }
      
      let cellClass = '';
      if (isSubmitted) {
        const isCorrect = isMultiResponse
          ? (r.correctIndices || []).includes(cIdx)
          : r.correctIndex === cIdx;
        
        if (isCorrect) {
          cellClass = 'matrix-cell-correct';
        } else if (isChecked && !isCorrect) {
          cellClass = 'matrix-cell-incorrect';
        }
      }
      
      html += `<td class="${cellClass}">
        <input type="${isMultiResponse ? 'checkbox' : 'radio'}" name="player-matrix-row-${rIdx}" ${isChecked ? 'checked' : ''} ${isSubmitted ? 'disabled' : ''} data-row="${rIdx}" data-col="${cIdx}">
      </td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody>`;
  tbl.innerHTML = html;
  
  if (!isSubmitted) {
    tbl.querySelectorAll('input').forEach(input => {
      input.addEventListener('change', (e) => {
        const row = parseInt(e.target.dataset.row);
        const col = parseInt(e.target.dataset.col);
        if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
        
        if (isMultiResponse) {
          if (!playerAnswers[stepIdx][row]) playerAnswers[stepIdx][row] = [];
          if (e.target.checked) {
            playerAnswers[stepIdx][row].push(col);
          } else {
            playerAnswers[stepIdx][row] = playerAnswers[stepIdx][row].filter(v => v !== col);
          }
        } else {
          playerAnswers[stepIdx][row] = col;
        }
      });
    });
  }
  
  box.appendChild(tbl);
  
  const note = document.createElement('div');
  note.className = 'matrix-note';
  note.textContent = isMultiResponse 
    ? 'Note: Each column must have at least 1 response option selected.' 
    : 'Note: Each row must have only 1 response option selected.';
  box.appendChild(note);
}

// 5. Select N Response
function renderPlayerSelectN(q, stepIdx, box, isSubmitted, userAnswers) {
  const wrapper = document.createElement('div');
  const limit = q.limit || 3;
  wrapper.innerHTML = '';
  
  const savedVal = userAnswers || {};
  const options = q.options || [];
  
  options.forEach((opt, oIdx) => {
    const row = document.createElement('label');
    row.className = 'exam-option-row';
    const isChecked = savedVal[oIdx] === true;
    if (isChecked) row.classList.add('checked');
    
    if (isSubmitted) {
      if (opt.correct) row.classList.add('show-correct');
      else if (isChecked && !opt.correct) row.classList.add('show-incorrect');
    }
    
    row.innerHTML = `
      <input type="checkbox" name="selectN-group" ${isChecked ? 'checked' : ''} ${isSubmitted ? 'disabled' : ''}>
      <div style="display:flex; flex-direction:column; gap:6px; width:100%;">
        <span class="option-text-label">${oIdx + 1}. ${escapeHTML(opt.text)}</span>
        ${opt.imageUrl ? `<img src="${escapeHTML(opt.imageUrl)}" class="option-image" style="max-width:300px; max-height:200px; border-radius:4px; border:1px solid #e5e7eb; margin-top:4px;">` : ''}
      </div>
    `;
    
    if (!isSubmitted) {
      const input = row.querySelector('input');
      input.addEventListener('change', () => {
        const currentCount = Object.values(playerAnswers[stepIdx] || {}).filter(Boolean).length;
        if (input.checked && currentCount >= limit) {
          input.checked = false;
          alert(`You can only select up to ${limit} choices.`);
          return;
        }
        if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
        playerAnswers[stepIdx][oIdx] = input.checked;
        
        if (input.checked) row.classList.add('checked');
        else row.classList.remove('checked');
      });
    }
    wrapper.appendChild(row);
  });
  box.appendChild(wrapper);
}

// 6. Bowtie Player
function renderPlayerBowtie(q, stepIdx, box, isSubmitted, userAnswers) {
  const leftPH = q.bowtieLeftPlaceholder || 'Action to Take';
  const centerPH = q.bowtieCenterPlaceholder || 'Condition Most Likely Experiencing';
  const rightPH = q.bowtieRightPlaceholder || 'Parameter to Monitor';
  
  const col1Header = q.bowtieCol1Header || 'Actions to Take';
  const col2Header = q.bowtieCol2Header || 'Potential Conditions';
  const col3Header = q.bowtieCol3Header || 'Parameters to Monitor';

  const container = document.createElement('div');
  container.className = 'bowtie-container';
  container.style.display = 'flex';
  container.style.flexDirection = 'column';
  container.style.gap = '20px';
  container.style.width = '100%';

  const uA = userAnswers || {};
  const actions = q.bowtieActions || [];
  const conditions = q.bowtieConditions || [];
  const params = q.bowtieParams || [];

  let html = `
    <div class="bowtie-diagram-wrapper" style="display:flex; justify-content:space-between; align-items:center; position:relative; min-height:220px; padding:20px; background:#ffffff; border:0px; border-radius:var(--radius-md); box-shadow:none; user-select:none;">
      
      <svg style="position:absolute; top:20px; left:20px; width:calc(100% - 40px); height:calc(100% - 40px); pointer-events:none; stroke:#cbd5e1; stroke-width:0.5;" viewBox="0 0 100 100" preserveAspectRatio="none">
        <line x1="30" y1="22.2" x2="35" y2="50" />
        <line x1="30" y1="77.8" x2="35" y2="50" />
        <line x1="70" y1="22.2" x2="65" y2="50" />
        <line x1="70" y1="77.8" x2="65" y2="50" />
      </svg>

      <!-- Left Targets Column -->
      <div style="display:flex; flex-direction:column; justify-content:space-between; height:180px; width:30%; z-index:1;">
        <div id="bowtie-target-left1" class="bowtie-target-zone" data-col="1" style="background:#ecf5f4; border:1.5px solid #025287; border-radius:4px; height:80px; display:flex; align-items:center; justify-content:center; padding:8px; text-align:center; position:relative; transition:all 0.2s;">
          <span class="placeholder-text" style="color:#025287; font-size:13px; font-weight:500; opacity:0.6;">${escapeHTML(leftPH)}</span>
        </div>
        <div id="bowtie-target-left2" class="bowtie-target-zone" data-col="1" style="background:#ecf5f4; border:1.5px solid #025287; border-radius:4px; height:80px; display:flex; align-items:center; justify-content:center; padding:8px; text-align:center; position:relative; transition:all 0.2s;">
          <span class="placeholder-text" style="color:#025287; font-size:13px; font-weight:500; opacity:0.6;">${escapeHTML(leftPH)}</span>
        </div>
      </div>

      <!-- Center Target Column -->
      <div style="display:flex; flex-direction:column; justify-content:center; height:180px; width:30%; z-index:1;">
        <div id="bowtie-target-center" class="bowtie-target-zone" data-col="2" style="background:#bae6f2; border:1.5px solid #0891b2; border-radius:4px; height:80px; display:flex; align-items:center; justify-content:center; padding:8px; text-align:center; position:relative; transition:all 0.2s;">
          <span class="placeholder-text" style="color:#0891b2; font-size:13px; font-weight:500; opacity:0.6;">${escapeHTML(centerPH)}</span>
        </div>
      </div>

      <!-- Right Targets Column -->
      <div style="display:flex; flex-direction:column; justify-content:space-between; height:180px; width:30%; z-index:1;">
        <div id="bowtie-target-right1" class="bowtie-target-zone" data-col="3" style="background:#ecf0f5; border:1.5px solid #475569; border-radius:4px; height:80px; display:flex; align-items:center; justify-content:center; padding:8px; text-align:center; position:relative; transition:all 0.2s;">
          <span class="placeholder-text" style="color:#475569; font-size:13px; font-weight:500; opacity:0.6;">${escapeHTML(rightPH)}</span>
        </div>
        <div id="bowtie-target-right2" class="bowtie-target-zone" data-col="3" style="background:#ecf0f5; border:1.5px solid #475569; border-radius:4px; height:80px; display:flex; align-items:center; justify-content:center; padding:8px; text-align:center; position:relative; transition:all 0.2s;">
          <span class="placeholder-text" style="color:#475569; font-size:13px; font-weight:500; opacity:0.6;">${escapeHTML(rightPH)}</span>
        </div>
      </div>

    </div>
  `;

  html += `
    <div class="bowtie-table-wrapper" style="display:flex; gap:16px; width:100%; user-select:none;">
      
      <!-- Column 1 (Ingredients) -->
      <div style="flex:1; border:1.5px solid #000000; border-radius:4px; background:#ffffff; overflow:hidden; align-self: flex-start;">
        <div style="background:#e9f1f7; border-bottom:1.5px solid #000000; padding:10px; font-weight:bold; font-size:13px; text-align:center; color:#1e293b;">
          ${escapeHTML(col1Header)}
        </div>
        <div id="bowtie-table-col1" style="padding:8px; display:flex; flex-direction:column; gap:8px;"></div>
      </div>

      <!-- Column 2 (Orders) -->
      <div style="flex:1; border:1.5px solid #000000; border-radius:4px; background:#ffffff; overflow:hidden; align-self: flex-start;">
        <div style="background:#e9f1f7; border-bottom:1.5px solid #000000; padding:10px; font-weight:bold; font-size:13px; text-align:center; color:#1e293b;">
          ${escapeHTML(col2Header)}
        </div>
        <div id="bowtie-table-col2" style="padding:8px; display:flex; flex-direction:column; gap:8px;"></div>
      </div>

      <!-- Column 3 (Materials) -->
      <div style="flex:1; border:1.5px solid #000000; border-radius:4px; background:#ffffff; overflow:hidden; align-self: flex-start;">
        <div style="background:#e9f1f7; border-bottom:1.5px solid #000000; padding:10px; font-weight:bold; font-size:13px; text-align:center; color:#1e293b;">
          ${escapeHTML(col3Header)}
        </div>
        <div id="bowtie-table-col3" style="padding:8px; display:flex; flex-direction:column; gap:8px;"></div>
      </div>

    </div>
  `;

  container.innerHTML = html;
  box.appendChild(container);

  const placeItemInTarget = (col, idx, targetZone) => {
    const existingItem = targetZone.querySelector('.bowtie-drag-item');
    if (existingItem) {
      const origCol = parseInt(existingItem.dataset.col);
      const origIdx = parseInt(existingItem.dataset.idx);
      const homeSlot = container.querySelector(`.bowtie-home-slot[data-col="${origCol}"][data-idx="${origIdx}"]`);
      if (homeSlot) {
        homeSlot.appendChild(existingItem);
      }
    }
    
    const item = container.querySelector(`.bowtie-drag-item[data-col="${col}"][data-idx="${idx}"]`);
    if (item) {
      targetZone.appendChild(item);
      checkPlaceholderVisibility();
      saveState();
    }
  };

  const checkPlaceholderVisibility = () => {
    container.querySelectorAll('.bowtie-target-zone').forEach(zone => {
      const item = zone.querySelector('.bowtie-drag-item');
      const placeholder = zone.querySelector('.placeholder-text');
      if (placeholder) {
        placeholder.style.display = item ? 'none' : 'block';
      }
    });
  };

  const saveState = () => {
    if (isSubmitted) return;
    const a0Item = container.querySelector('#bowtie-target-left1 .bowtie-drag-item');
    const a1Item = container.querySelector('#bowtie-target-left2 .bowtie-drag-item');
    const condItem = container.querySelector('#bowtie-target-center .bowtie-drag-item');
    const p0Item = container.querySelector('#bowtie-target-right1 .bowtie-drag-item');
    const p1Item = container.querySelector('#bowtie-target-right2 .bowtie-drag-item');
    
    playerAnswers[stepIdx] = {
      action0: a0Item ? a0Item.textContent.trim() : '',
      action1: a1Item ? a1Item.textContent.trim() : '',
      condition: condItem ? condItem.textContent.trim() : '',
      param0: p0Item ? p0Item.textContent.trim() : '',
      param1: p1Item ? p1Item.textContent.trim() : ''
    };
  };

  const populateColumn = (colId, list, colNum, itemColor) => {
    const colList = container.querySelector(`#${colId}`);
    colList.innerHTML = '';
    list.forEach((opt, idx) => {
      const slot = document.createElement('div');
      slot.className = 'bowtie-home-slot';
      slot.dataset.col = colNum;
      slot.dataset.idx = idx;
      slot.style.height = '48px';
      slot.style.background = itemColor;
      slot.style.border = '1px solid #cbd5e1';
      slot.style.borderRadius = '4px';
      slot.style.display = 'flex';
      slot.style.alignItems = 'center';
      slot.style.justifyContent = 'center';
      slot.style.overflow = 'hidden';
      
      const item = document.createElement('div');
      item.className = 'bowtie-drag-item';
      item.draggable = !isSubmitted;
      item.dataset.col = colNum;
      item.dataset.idx = idx;
      item.textContent = opt.text;
      item.style.width = '100%';
      item.style.height = '100%';
      item.style.display = 'flex';
      item.style.alignItems = 'center';
      item.style.justifyContent = 'center';
      item.style.padding = '8px 12px';
      item.style.background = itemColor;
      item.style.color = '#0f172a';
      item.style.fontWeight = '500';
      item.style.fontSize = '12px';
      item.style.textAlign = 'center';
      item.style.cursor = isSubmitted ? 'default' : 'grab';
      item.style.transition = 'opacity 0.2s';

      if (!isSubmitted) {
        item.addEventListener('dragstart', (e) => {
          e.dataTransfer.setData('text/plain', JSON.stringify({ col: colNum, idx: idx }));
          item.style.opacity = '0.5';
        });
        item.addEventListener('dragend', () => {
          item.style.opacity = '1';
        });
        
        slot.addEventListener('dragover', (e) => {
          e.preventDefault();
        });
        slot.addEventListener('drop', (e) => {
          e.preventDefault();
          const data = JSON.parse(e.dataTransfer.getData('text/plain'));
          if (data.col === colNum && data.idx === idx) {
            const dragEl = container.querySelector(`.bowtie-drag-item[data-col="${data.col}"][data-idx="${data.idx}"]`);
            if (dragEl) {
              slot.appendChild(dragEl);
              checkPlaceholderVisibility();
              saveState();
            }
          }
        });
      }

      slot.appendChild(item);
      colList.appendChild(slot);
    });
  };

  populateColumn('bowtie-table-col1', actions, 1, '#ecf5f4');
  populateColumn('bowtie-table-col2', conditions, 2, '#bae6f2');
  populateColumn('bowtie-table-col3', params, 3, '#ecf0f5');

  if (!isSubmitted) {
    container.querySelectorAll('.bowtie-target-zone').forEach(zone => {
      zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.style.transform = 'scale(1.02)';
      });
      zone.addEventListener('dragleave', () => {
        zone.style.transform = 'none';
      });
      zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.style.transform = 'none';
        try {
          const data = JSON.parse(e.dataTransfer.getData('text/plain'));
          const targetCol = parseInt(zone.dataset.col);
          if (data.col !== targetCol) {
            showToast("Invalid placement! Option doesn't match this target type.", "error");
            return;
          }
          placeItemInTarget(data.col, data.idx, zone);
        } catch (err) {
          console.error(err);
        }
      });
    });
  }

  if (uA.action0) {
    const el = Array.from(container.querySelectorAll('.bowtie-drag-item[data-col="1"]')).find(item => item.textContent.trim() === uA.action0);
    if (el) placeItemInTarget(1, parseInt(el.dataset.idx), container.querySelector('#bowtie-target-left1'));
  }
  if (uA.action1) {
    const el = Array.from(container.querySelectorAll('.bowtie-drag-item[data-col="1"]')).find(item => item.textContent.trim() === uA.action1);
    if (el) placeItemInTarget(1, parseInt(el.dataset.idx), container.querySelector('#bowtie-target-left2'));
  }
  if (uA.condition) {
    const el = Array.from(container.querySelectorAll('.bowtie-drag-item[data-col="2"]')).find(item => item.textContent.trim() === uA.condition);
    if (el) placeItemInTarget(2, parseInt(el.dataset.idx), container.querySelector('#bowtie-target-center'));
  }
  if (uA.param0) {
    const el = Array.from(container.querySelectorAll('.bowtie-drag-item[data-col="3"]')).find(item => item.textContent.trim() === uA.param0);
    if (el) placeItemInTarget(3, parseInt(el.dataset.idx), container.querySelector('#bowtie-target-right1'));
  }
  if (uA.param1) {
    const el = Array.from(container.querySelectorAll('.bowtie-drag-item[data-col="3"]')).find(item => item.textContent.trim() === uA.param1);
    if (el) placeItemInTarget(3, parseInt(el.dataset.idx), container.querySelector('#bowtie-target-right2'));
  }

  if (isSubmitted) {
    const checkTarget = (targetEl, correctList) => {
      const item = targetEl.querySelector('.bowtie-drag-item');
      const val = item ? item.textContent.trim() : '';
      const correctTexts = correctList.filter(x => x.correct).map(x => x.text);
      if (val && correctTexts.includes(val)) {
        targetEl.style.border = '2px solid #22c55e';
        targetEl.style.boxShadow = '0 0 8px rgba(34, 197, 94, 0.4)';
      } else {
        targetEl.style.border = '2px solid #ef4444';
        targetEl.style.boxShadow = '0 0 8px rgba(239, 68, 68, 0.4)';
      }
    };
    checkTarget(container.querySelector('#bowtie-target-left1'), actions);
    checkTarget(container.querySelector('#bowtie-target-left2'), actions);
    checkTarget(container.querySelector('#bowtie-target-center'), conditions);
    checkTarget(container.querySelector('#bowtie-target-right1'), params);
    checkTarget(container.querySelector('#bowtie-target-right2'), params);
  }
}

// 7. Multiple Choice (Radio list)
function renderPlayerMultipleChoice(q, stepIdx, box, isSubmitted, userAnswers) {
  const wrapper = document.createElement('div');
  const savedVal = userAnswers || {};
  const options = q.options || [];
  
  options.forEach((opt, oIdx) => {
    const row = document.createElement('label');
    row.className = 'exam-option-row';
    const isChecked = savedVal[oIdx] === true;
    if (isChecked) row.classList.add('checked');
    
    if (isSubmitted) {
      if (opt.correct) row.classList.add('show-correct');
      else if (isChecked && !opt.correct) row.classList.add('show-incorrect');
    }
    
    row.innerHTML = `
      <input type="radio" name="single-mc" ${isChecked ? 'checked' : ''} ${isSubmitted ? 'disabled' : ''}>
      <div style="display:flex; flex-direction:column; gap:6px; width:100%;">
        <span class="option-text-label">${oIdx + 1}. ${escapeHTML(opt.text)}</span>
        ${opt.imageUrl ? `<img src="${escapeHTML(opt.imageUrl)}" class="option-image" style="max-width:300px; max-height:200px; border-radius:4px; border:1px solid #e5e7eb; margin-top:4px;">` : ''}
      </div>
    `;
    
    if (!isSubmitted) {
      row.querySelector('input').addEventListener('change', () => {
        playerAnswers[stepIdx] = { [oIdx]: true };
        wrapper.querySelectorAll('.exam-option-row').forEach(el => el.classList.remove('checked'));
        row.classList.add('checked');
      });
    }
    wrapper.appendChild(row);
  });
  box.appendChild(wrapper);
}

function renderPlayerFillBlank(q, stepIdx, box, isSubmitted, userAnswers) {
  const wrapper = document.createElement('div');
  wrapper.className = 'form-group';
  
  const val = userAnswers ? userAnswers.value : '';
  const unitText = q.unit ? ' ' + q.unit : '';
  
  wrapper.innerHTML = `
    <div style="display: inline-flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 500; margin: 16px 0; flex-wrap: nowrap;">
      <span style="white-space: nowrap;">Answer: </span>
      <input type="text" id="player-blank-input" class="form-control" 
        style="max-width:300px; width:220px; background-color:#f8fafc; border:1.5px solid #000000; color:#000000; display: inline-block; margin: 0; vertical-align: middle; border-radius: 0;" 
        value="${escapeHTML(val)}" ${isSubmitted ? 'disabled' : ''}>
      <span style="white-space: nowrap;">${escapeHTML(unitText)}</span>
    </div>
  `;
  
  if (isSubmitted) {
    const input = wrapper.querySelector('input');
    const correctVal = (q.correctAnswer || '').toString().trim().toLowerCase();
    const userVal = (val || '').toString().trim().toLowerCase();
    if (correctVal === userVal || parseFloat(correctVal) === parseFloat(userVal)) {
      input.style.borderColor = 'var(--accent-green)';
      input.style.backgroundColor = 'rgba(16, 185, 129, 0.08)';
    } else {
      input.style.borderColor = 'var(--accent-red)';
      input.style.backgroundColor = 'rgba(239, 68, 68, 0.08)';
    }
  } else {
    wrapper.querySelector('input').addEventListener('input', (e) => {
      playerAnswers[stepIdx] = { value: e.target.value };
    });
  }
  box.appendChild(wrapper);
}

// 9. Hotspot Player
function renderPlayerHotspot(q, stepIdx, box, isSubmitted, userAnswers) {
  const wrapper = document.createElement('div');
  wrapper.style.textAlign = 'center';
  
  const click = userAnswers || {}; // { x: val, y: val }
  
  wrapper.innerHTML = `
    <div id="hotspot-play-container" class="hotspot-image-container">
      <img id="hotspot-play-img" class="hotspot-image" src="${escapeHTML(q.imageUrl)}" alt="Hotspot Graphic">
      ${click.x !== undefined ? `<div class="hotspot-click-marker" style="left:${click.x}%; top:${click.y}%;"></div>` : ''}
      ${isSubmitted ? `<div class="hotspot-target-region" style="left:${Math.min(q.rect.x1, q.rect.x2)}%; top:${Math.min(q.rect.y1, q.rect.y2)}%; width:${Math.abs(q.rect.x2 - q.rect.x1)}%; height:${Math.abs(q.rect.y2 - q.rect.y1)}%;"></div>` : ''}
    </div>
  `;
  
  const container = wrapper.querySelector('#hotspot-play-container');
  if (!isSubmitted) {
    container.addEventListener('click', (e) => {
      const bounds = container.getBoundingClientRect();
      const clickX = ((e.clientX - bounds.left) / bounds.width) * 100;
      const clickY = ((e.clientY - bounds.top) / bounds.height) * 100;
      
      playerAnswers[stepIdx] = { x: clickX, y: clickY };
      
      // Place marker in DOM
      let marker = container.querySelector('.hotspot-click-marker');
      if (!marker) {
        marker = document.createElement('div');
        marker.className = 'hotspot-click-marker';
        container.appendChild(marker);
      }
      marker.style.left = clickX + '%';
      marker.style.top = clickY + '%';
    });
  }
  
  box.appendChild(wrapper);
}

// 10. Ordered Response Player
function renderPlayerOrderedResponse(q, stepIdx, box, isSubmitted, userAnswers) {
  const correctSequence = q.orderedOptions || [];
  const stateAnswers = userAnswers || { order: [] }; // { order: [items] }
  
  // Shuffled options list (only generated once or stored)
  if (!stateAnswers.shuffled) {
    stateAnswers.shuffled = [...correctSequence].sort(() => Math.random() - 0.5);
    // Remove items already placed in ordered box
    stateAnswers.shuffled = stateAnswers.shuffled.filter(item => !stateAnswers.order.includes(item));
  }
  
  const container = document.createElement('div');
  container.className = 'ordered-response-container';
  
  container.innerHTML = `
    <div>
      <div class="order-box-title">Unordered Options</div>
      <div id="order-left-box" class="order-box"></div>
    </div>
    <div class="order-actions-col">
      <button id="move-right-btn" class="btn-order-action" ${isSubmitted ? 'disabled' : ''}>&rarr;</button>
      <button id="move-left-btn" class="btn-order-action" ${isSubmitted ? 'disabled' : ''}>&larr;</button>
    </div>
    <div>
      <div class="order-box-title">Your Ordered Steps</div>
      <div id="order-right-box" class="order-box"></div>
    </div>
    <div class="order-actions-col" style="padding-left: 6px;">
      <button id="move-up-btn" class="btn-order-action" ${isSubmitted ? 'disabled' : ''}>&uarr;</button>
      <button id="move-down-btn" class="btn-order-action" ${isSubmitted ? 'disabled' : ''}>&darr;</button>
    </div>
  `;
  
  const leftBox = container.querySelector('#order-left-box');
  const rightBox = container.querySelector('#order-right-box');
  
  let selectedLeftItem = null;
  let selectedRightItem = null;
  
  const renderItemLists = () => {
    leftBox.innerHTML = '';
    rightBox.innerHTML = '';
    
    // Left Box Unordered
    stateAnswers.shuffled.forEach(item => {
      const el = document.createElement('div');
      el.className = `order-item ${selectedLeftItem === item ? 'selected' : ''}`;
      el.textContent = item;
      if (!isSubmitted) {
        el.addEventListener('click', () => {
          selectedLeftItem = item;
          selectedRightItem = null;
          renderItemLists();
        });
      }
      leftBox.appendChild(el);
    });
    
    // Right Box Ordered
    stateAnswers.order.forEach((item, idx) => {
      const el = document.createElement('div');
      el.className = `order-item ${selectedRightItem === item ? 'selected' : ''}`;
      el.innerHTML = `
        <span>${idx + 1}. ${escapeHTML(item)}</span>
      `;
      if (isSubmitted) {
        if (correctSequence[idx] === item) {
          el.style.borderColor = 'var(--accent-green)';
          el.style.backgroundColor = 'rgba(16, 185, 129, 0.05)';
        } else {
          el.style.borderColor = 'var(--accent-red)';
          el.style.backgroundColor = 'rgba(239, 68, 68, 0.05)';
        }
      } else {
        el.addEventListener('click', () => {
          selectedRightItem = item;
          selectedLeftItem = null;
          renderItemLists();
        });
      }
      rightBox.appendChild(el);
    });
  };
  
  renderItemLists();
  
  // Wire Action buttons
  if (!isSubmitted) {
    container.querySelector('#move-right-btn').addEventListener('click', () => {
      if (selectedLeftItem) {
        stateAnswers.order.push(selectedLeftItem);
        stateAnswers.shuffled = stateAnswers.shuffled.filter(x => x !== selectedLeftItem);
        selectedLeftItem = null;
        playerAnswers[stepIdx] = stateAnswers;
        renderItemLists();
      }
    });
    
    container.querySelector('#move-left-btn').addEventListener('click', () => {
      if (selectedRightItem) {
        stateAnswers.shuffled.push(selectedRightItem);
        stateAnswers.order = stateAnswers.order.filter(x => x !== selectedRightItem);
        selectedRightItem = null;
        playerAnswers[stepIdx] = stateAnswers;
        renderItemLists();
      }
    });
    
    container.querySelector('#move-up-btn').addEventListener('click', () => {
      if (selectedRightItem) {
        const idx = stateAnswers.order.indexOf(selectedRightItem);
        if (idx > 0) {
          // Swap up
          stateAnswers.order[idx] = stateAnswers.order[idx - 1];
          stateAnswers.order[idx - 1] = selectedRightItem;
          playerAnswers[stepIdx] = stateAnswers;
          renderItemLists();
        }
      }
    });
    
    container.querySelector('#move-down-btn').addEventListener('click', () => {
      if (selectedRightItem) {
        const idx = stateAnswers.order.indexOf(selectedRightItem);
        if (idx !== -1 && idx < stateAnswers.order.length - 1) {
          // Swap down
          stateAnswers.order[idx] = stateAnswers.order[idx + 1];
          stateAnswers.order[idx + 1] = selectedRightItem;
          playerAnswers[stepIdx] = stateAnswers;
          renderItemLists();
        }
      }
    });
  }
  
  box.appendChild(container);
}

// 11. Select All (SATA / Trend)
function renderPlayerSata(q, stepIdx, box, isSubmitted, userAnswers) {
  const wrapper = document.createElement('div');
  const savedVal = userAnswers || {};
  const options = q.options || [];
  
  options.forEach((opt, oIdx) => {
    const row = document.createElement('label');
    row.className = 'exam-option-row';
    const isChecked = savedVal[oIdx] === true;
    if (isChecked) row.classList.add('checked');
    
    if (isSubmitted) {
      if (opt.correct) row.classList.add('show-correct');
      else if (isChecked && !opt.correct) row.classList.add('show-incorrect');
    }
    
    row.innerHTML = `
      <input type="checkbox" ${isChecked ? 'checked' : ''} ${isSubmitted ? 'disabled' : ''}>
      <div style="display:flex; flex-direction:column; gap:6px; width:100%;">
        <span class="option-text-label">${oIdx + 1}. ${escapeHTML(opt.text)}</span>
        ${opt.imageUrl ? `<img src="${escapeHTML(opt.imageUrl)}" class="option-image" style="max-width:300px; max-height:200px; border-radius:4px; border:1px solid #e5e7eb; margin-top:4px;">` : ''}
      </div>
    `;
    
    if (!isSubmitted) {
      row.querySelector('input').addEventListener('change', (e) => {
        if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
        playerAnswers[stepIdx][oIdx] = e.target.checked;
        if (e.target.checked) row.classList.add('checked');
        else row.classList.remove('checked');
      });
    }
    wrapper.appendChild(row);
  });
  box.appendChild(wrapper);
}

// 12. Highlight Text/Table Player
function renderPlayerHighlight(q, stepIdx, box, isSubmitted, userAnswers) {
  const container = document.createElement('div');
  container.className = 'player-highlight-tabs-container';
  
  if (!q.highlightTabs) {
    q.highlightTabs = [
      { id: 'ht_' + Date.now(), title: "Nurses' Notes", content: q.highlightText || '' }
    ];
  }
  
  if (!playerHighlightActiveTabId || !q.highlightTabs.find(t => t.id === playerHighlightActiveTabId)) {
    playerHighlightActiveTabId = q.highlightTabs[0].id;
  }
  
  const activeTab = q.highlightTabs.find(t => t.id === playerHighlightActiveTabId);
  
  if (q.maxCorrectSelections) {
    const limitInfo = document.createElement('div');
    limitInfo.className = 'highlight-limit-info';
    limitInfo.style.marginBottom = '12px';
    limitInfo.style.fontSize = '13px';
    limitInfo.style.fontWeight = '700';
    limitInfo.style.color = '#025287';
    limitInfo.textContent = `Select ${q.maxCorrectSelections} correct findings.`;
    container.appendChild(limitInfo);
  }
  
  // Render tabs bar (always show, even if there's only 1 tab)
  const tabsBar = document.createElement('div');
  tabsBar.className = 'patient-chart-tabs-bar';
  q.highlightTabs.forEach(t => {
    const tabBtn = document.createElement('button');
    tabBtn.className = `patient-chart-tab ${t.id === playerHighlightActiveTabId ? 'active' : ''}`;
    tabBtn.textContent = t.title;
    tabBtn.addEventListener('click', () => {
      playerHighlightActiveTabId = t.id;
      box.innerHTML = '';
      renderPlayerHighlight(q, stepIdx, box, isSubmitted, userAnswers);
    });
    tabsBar.appendChild(tabBtn);
  });
  container.appendChild(tabsBar);
  
  // Calculate global index offset for the active tab's highlight items
  let globalHighlightIdx = 0;
  for (let i = 0; i < q.highlightTabs.indexOf(activeTab); i++) {
    const text = q.highlightTabs[i].content || '';
    const matches = text.match(/\{([^{|]+)(?:\|([^{}]+))?\}/g) || [];
    globalHighlightIdx += matches.length;
  }
  
  // Content container with border (uses patient-chart-content styling)
  const contentBox = document.createElement('div');
  contentBox.className = 'patient-chart-content';
  
  const passage = document.createElement('div');
  passage.className = 'highlight-passage';
  
  const rawText = activeTab.content || '';
  // Format nurses notes styling
  const formattedHtml = formatNursesNotes(rawText, activeTab.title);
  passage.innerHTML = formattedHtml;
  
  let currentLocalHIdx = 0;
  const savedAnswers = userAnswers || {};
  
  function processNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent;
      if (!text.includes('{')) return;
      
      const regex = /\{([^{|]+)(?:\|([^{}]+))?\}/g;
      const fragment = document.createDocumentFragment();
      let match;
      let lastIndex = 0;
      let hasMatch = false;
      
      while ((match = regex.exec(text)) !== null) {
        hasMatch = true;
        if (match.index > lastIndex) {
          fragment.appendChild(document.createTextNode(text.substring(lastIndex, match.index)));
        }
        
        const phrase = match[1];
        const isCorrect = match[2] === 'correct';
        const currentHIdx = globalHighlightIdx + (currentLocalHIdx++);
        
        const span = document.createElement('span');
        span.className = 'highlight-span';
        span.textContent = phrase;
        
        const isSelected = savedAnswers[currentHIdx] === true;
        if (isSelected) span.classList.add('selected');
        
        if (isSubmitted) {
          if (isCorrect) {
            span.classList.add('show-correct');
          } else if (isSelected) {
            span.classList.add('show-incorrect');
          }
        } else {
          span.addEventListener('click', () => {
            if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
            
            const state = !playerAnswers[stepIdx][currentHIdx];
            if (state && q.maxCorrectSelections) {
              const selectedCount = Object.values(playerAnswers[stepIdx]).filter(v => v === true).length;
              if (selectedCount >= q.maxCorrectSelections) {
                showToast(`You can only select up to ${q.maxCorrectSelections} findings.`, "error");
                return;
              }
            }
            
            playerAnswers[stepIdx][currentHIdx] = state;
            if (state) {
              span.classList.add('selected');
            } else {
              span.classList.remove('selected');
            }
          });
        }
        
        fragment.appendChild(span);
        lastIndex = regex.lastIndex;
      }
      
      if (hasMatch) {
        if (lastIndex < text.length) {
          fragment.appendChild(document.createTextNode(text.substring(lastIndex)));
        }
        node.parentNode.replaceChild(fragment, node);
      }
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      // Process children
      const children = Array.from(node.childNodes);
      children.forEach(child => processNode(child));
    }
  }
  
  processNode(passage);
  
  contentBox.appendChild(passage);
  container.appendChild(contentBox);
  box.appendChild(container);
}

// 14. Grouped Multiple Response Player
function renderPlayerGroupedMr(q, stepIdx, box, isSubmitted, userAnswers) {
  const groups = q.groupedRows || [];
  const container = document.createElement('div');
  
  const savedAnswers = userAnswers || {}; // { groupIdx: { oIdx: boolean } }
  
  groups.forEach((g, gIdx) => {
    const card = document.createElement('div');
    card.className = 'grouped-mr-category';
    
    card.innerHTML = `
      <div class="grouped-mr-category-title">${escapeHTML(g.title)}</div>
      <div class="grouped-mr-category-body"></div>
    `;
    const body = card.querySelector('.grouped-mr-category-body');
    const groupSavedVal = savedAnswers[gIdx] || {};
    const options = g.options || [];
    
    options.forEach((opt, oIdx) => {
      const row = document.createElement('label');
      row.className = 'exam-option-row';
      const isChecked = groupSavedVal[oIdx] === true;
      if (isChecked) row.classList.add('checked');
      
      if (isSubmitted) {
        if (opt.correct) row.classList.add('show-correct');
        else if (isChecked && !opt.correct) row.classList.add('show-incorrect');
      }
      
      row.innerHTML = `
        <input type="checkbox" ${isChecked ? 'checked' : ''} ${isSubmitted ? 'disabled' : ''}>
        <span class="option-text-label">${escapeHTML(opt.text)}</span>
      `;
      
      if (!isSubmitted) {
        row.querySelector('input').addEventListener('change', (e) => {
          if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
          if (!playerAnswers[stepIdx][gIdx]) playerAnswers[stepIdx][gIdx] = {};
          
          playerAnswers[stepIdx][gIdx][oIdx] = e.target.checked;
          if (e.target.checked) row.classList.add('checked');
          else row.classList.remove('checked');
        });
      }
      
      body.appendChild(row);
    });
    container.appendChild(card);
  });
  box.appendChild(container);
}


/* --- PLAYER GRADING SYSTEM (NGN STANDARDS) --- */
function evaluateStepScore(stepIdx) {
  const step = currentCase.screens[stepIdx];
  const q = step.question;
  const userAnswers = playerAnswers[stepIdx] || {};
  
  
  let score = 0;
  let maxScore = 0;
  
  switch (q.type) {
    // ================= 0/1 SCORING (No Penalties) =================
    case 'dropdown_cloze':
    case 'cloze':
    case 'drag_drop_cloze': {
      const c = q.cloze || { dropdowns: [] };
      const dropdowns = c.dropdowns || [];
      // Count indices where drop exists
      const activeDropdowns = dropdowns.filter(Boolean);
      maxScore = activeDropdowns.length;
      
      dropdowns.forEach((dd, idx) => {
        if (dd && dd.options) {
          const correctIdx = dd.options.findIndex(o => o.correct);
          const userVal = userAnswers[idx];
          // For drag drop, correct value is the exact text match
          if (q.type === 'drag_drop_cloze') {
            const correctText = dd.options.find(o => o.correct)?.text || '';
            if (userVal === correctText) score++;
          } else {
            if (userVal !== undefined && parseInt(userVal) === correctIdx) score++;
          }
        }
      });
      break;
    }
    case 'dropdown_table': {
      const rows = q.dropdownTableRows || [];
      maxScore = rows.length;
      rows.forEach((row, idx) => {
        const rowOptions = row.options || [];
        const correctIdx = rowOptions.findIndex(o => o.correct);
        const userVal = userAnswers[idx];
        if (userVal !== undefined && parseInt(userVal) === correctIdx) score++;
      });
      break;
    }
    case 'matrix_mc':
    case 'matrix': {
      const m = q.matrix || { rows: [] };
      const rows = m.rows || [];
      maxScore = rows.length;
      rows.forEach((r, idx) => {
        if (userAnswers[idx] === r.correctIndex) score++;
      });
      break;
    }
    case 'select_n':
    case 'selectN': {
      // 1 point per correct answer selected
      const limit = q.limit || 3;
      maxScore = limit;
      const options = q.options || [];
      options.forEach((opt, idx) => {
        if (opt.correct && userAnswers[idx] === true) score++;
      });
      score = Math.min(limit, score);
      break;
    }
    case 'bowtie': {
      // 5 slots, 1 point each
      maxScore = 5;
      const uA = userAnswers || {};
      
      const correctActions = (q.bowtieActions || []).filter(x => x.correct).map(x => x.text);
      const correctConditions = (q.bowtieConditions || []).filter(x => x.correct).map(x => x.text);
      const correctParams = (q.bowtieParams || []).filter(x => x.correct).map(x => x.text);
      
      // Actions
      const selActions = [uA['action0'], uA['action1']].filter(Boolean);
      selActions.forEach(act => {
        const cIdx = correctActions.indexOf(act);
        if (cIdx !== -1) {
          score++;
          correctActions.splice(cIdx, 1);
        }
      });
      
      // Condition
      if (uA['condition'] && correctConditions.includes(uA['condition'])) {
        score++;
      }
      
      // Params
      const selParams = [uA['param0'], uA['param1']].filter(Boolean);
      selParams.forEach(p => {
        const cIdx = correctParams.indexOf(p);
        if (cIdx !== -1) {
          score++;
          correctParams.splice(cIdx, 1);
        }
      });
      break;
    }
    case 'multiple_choice':
    case 'single': {
      maxScore = 1;
      const options = q.options || [];
      options.forEach((opt, idx) => {
        if (opt.correct && userAnswers[idx] === true) score = 1;
      });
      break;
    }
    case 'fill_blank': {
      maxScore = 1;
      const correctVal = (q.correctAnswer || '').toString().trim().toLowerCase();
      const userVal = (userAnswers.value || '').toString().trim().toLowerCase();
      if (correctVal === userVal || parseFloat(correctVal) === parseFloat(userVal)) {
        score = 1;
      }
      break;
    }
    case 'hotspot': {
      maxScore = 1;
      const r = q.rect || { x1: 0, y1: 0, x2: 100, y2: 100 };
      const ux = userAnswers.x;
      const uy = userAnswers.y;
      if (ux !== undefined && uy !== undefined) {
        const xMin = Math.min(r.x1, r.x2);
        const xMax = Math.max(r.x1, r.x2);
        const yMin = Math.min(r.y1, r.y2);
        const yMax = Math.max(r.y1, r.y2);
        if (ux >= xMin && ux <= xMax && uy >= yMin && uy <= yMax) score = 1;
      }
      break;
    }
    case 'ordered_response': {
      maxScore = 1;
      const correctSeq = q.orderedOptions || [];
      const userSeq = userAnswers.order || [];
      let allCorrect = correctSeq.length === userSeq.length;
      if (allCorrect) {
        for (let i = 0; i < correctSeq.length; i++) {
          if (correctSeq[i] !== userSeq[i]) {
            allCorrect = false;
            break;
          }
        }
      }
      score = allCorrect ? 1 : 0;
      break;
    }
    
    // ================= +/- SCORING (Penalty Deductions) =================
    case 'select_all':
    case 'sata':
    case 'trend': {
      let correctSel = 0;
      let incorrectSel = 0;
      const options = q.options || [];
      options.forEach((opt, idx) => {
        const isSelected = userAnswers[idx] === true;
        if (opt.correct) {
          maxScore++;
          if (isSelected) correctSel++;
        } else {
          if (isSelected) incorrectSel++;
        }
      });
      score = Math.max(0, correctSel - incorrectSel);
      break;
    }
    case 'highlight':
    case 'highlight_2': {
      let correctSel = 0;
      let incorrectSel = 0;
      
      const regex = /\{([^{|]+)(?:\|([^{}]+))?\}/g;
      let match;
      const highlights = [];
      
      if (q.highlightTabs) {
        q.highlightTabs.forEach(tab => {
          regex.lastIndex = 0;
          while ((match = regex.exec(tab.content || '')) !== null) {
            highlights.push({ text: match[1], correct: match[2] === 'correct' });
          }
        });
      } else {
        while ((match = regex.exec(q.highlightText || '')) !== null) {
          highlights.push({ text: match[1], correct: match[2] === 'correct' });
        }
      }
      
      highlights.forEach((h, idx) => {
        const isSelected = userAnswers[idx] === true;
        if (h.correct) {
          maxScore++;
          if (isSelected) correctSel++;
        } else {
          if (isSelected) incorrectSel++;
        }
      });
      score = Math.max(0, correctSel - incorrectSel);
      break;
    }
    case 'matrix_mr': {
      const m = q.matrix || { columns: [], rows: [] };
      let correctSel = 0;
      let incorrectSel = 0;
      const rows = m.rows || [];
      const columns = m.columns || [];
      
      rows.forEach((r, rIdx) => {
        const rowSel = userAnswers[rIdx] || [];
        columns.forEach((col, cIdx) => {
          const isCorrect = (r.correctIndices || []).includes(cIdx);
          const isChecked = rowSel.includes(cIdx);
          if (isCorrect) {
            maxScore++;
            if (isChecked) correctSel++;
          } else {
            if (isChecked) incorrectSel++;
          }
        });
      });
      score = Math.max(0, correctSel - incorrectSel);
      break;
    }
    case 'grouped_mr': {
      const groups = q.groupedRows || [];
      groups.forEach((g, gIdx) => {
        let gMax = 0;
        let gCorrect = 0;
        let gIncorrect = 0;
        const gAnswers = userAnswers[gIdx] || {};
        const options = g.options || [];
        
        options.forEach((opt, oIdx) => {
          const isSelected = gAnswers[oIdx] === true;
          if (opt.correct) {
            gMax++;
            if (isSelected) gCorrect++;
          } else {
            if (isSelected) gIncorrect++;
          }
        });
        
        maxScore += gMax;
        score += Math.max(0, gCorrect - gIncorrect); // category clamp min 0
      });
      break;
    }
    
    // ================= RATIONALE SCORING (All-or-Nothing) =================
    case 'dyad': {
      maxScore = 1;
      const c = q.cloze || { dropdowns: [] };
      const dropdowns = c.dropdowns || [];
      let dyadCorrect = dropdowns.filter(Boolean).length === 2;
      dropdowns.forEach((dd, idx) => {
        if (dd && dd.options) {
          const correctIdx = dd.options.findIndex(o => o.correct);
          if (parseInt(userAnswers[idx]) !== correctIdx) dyadCorrect = false;
        }
      });
      score = dyadCorrect ? 1 : 0;
      break;
    }
    case 'triad': {
      maxScore = 1;
      const c = q.cloze || { dropdowns: [] };
      const dropdowns = c.dropdowns || [];
      let triadCorrect = dropdowns.filter(Boolean).length === 3;
      dropdowns.forEach((dd, idx) => {
        if (dd && dd.options) {
          const correctIdx = dd.options.findIndex(o => o.correct);
          if (parseInt(userAnswers[idx]) !== correctIdx) triadCorrect = false;
        }
      });
      score = triadCorrect ? 1 : 0;
      break;
    }
  }
  
  playerScores[stepIdx] = { score, max: maxScore };
}

function hasSelectedAnyAnswer(q, stepIdx) {
  if (!q) return false;
  const userAnswers = playerAnswers[stepIdx];

  // 1. Check state object first
  if (userAnswers) {
    switch (q.type) {
      case 'dropdown_cloze':
      case 'cloze':
      case 'drag_drop_cloze':
      case 'dyad':
      case 'triad': {
        const hasVal = Object.values(userAnswers).some(v => v !== undefined && v !== null && v !== '');
        if (hasVal) return true;
        break;
      }
      case 'dropdown_table': {
        const hasVal = Object.values(userAnswers).some(v => v !== undefined && v !== null && v !== '');
        if (hasVal) return true;
        break;
      }
      case 'matrix_mc':
      case 'matrix': {
        const hasVal = Object.values(userAnswers).some(v => v !== undefined && v !== null && v !== '');
        if (hasVal) return true;
        break;
      }
      case 'select_n':
      case 'selectN':
      case 'multiple_choice':
      case 'single':
      case 'select_all':
      case 'sata':
      case 'trend':
      case 'highlight':
      case 'highlight_2': {
        const hasVal = Object.values(userAnswers).some(v => v === true);
        if (hasVal) return true;
        break;
      }
      case 'fill_blank': {
        if (userAnswers.value && userAnswers.value.toString().trim().length > 0) return true;
        break;
      }
      case 'hotspot': {
        if (userAnswers.x !== undefined && userAnswers.y !== undefined) return true;
        break;
      }
      case 'ordered_response': {
        if (Array.isArray(userAnswers.order) && userAnswers.order.length > 0) return true;
        break;
      }
      case 'bowtie': {
        if (userAnswers.action0 || userAnswers.action1 || userAnswers.condition || userAnswers.param0 || userAnswers.param1) return true;
        break;
      }
      case 'matrix_mr': {
        const hasVal = Object.values(userAnswers).some(arr => Array.isArray(arr) && arr.length > 0);
        if (hasVal) return true;
        break;
      }
      case 'grouped_mr': {
        const hasVal = Object.values(userAnswers).some(group => group && Object.values(group).some(v => v === true));
        if (hasVal) return true;
        break;
      }
      default: {
        const hasVal = Object.values(userAnswers).some(v => v !== undefined && v !== null && v !== false && v !== '');
        if (hasVal) return true;
      }
    }
  }


  return false;
}

function showSkipQuestionModal() {
  const modal = document.getElementById('skip-question-modal');
  if (modal) modal.classList.remove('hidden');
}

function closeSkipQuestionModal() {
  const modal = document.getElementById('skip-question-modal');
  if (modal) modal.classList.add('hidden');
}

function confirmSkipQuestion() {
  closeSkipQuestionModal();
  submittedAnswers[playerStepIndex] = true;
  evaluateStepScore(playerStepIndex);
  if (!playerScores[playerStepIndex]) {
    playerScores[playerStepIndex] = { score: 0, max: 1 };
  } else {
    playerScores[playerStepIndex].score = 0; // force zero points
  }

  if (sessionConfig.mode === 'test' && !sessionConfig.isRemediation) {
    if (playerStepIndex < currentCase.screens.length - 1) {
      playerStepIndex++;
      renderPlayerStep(playerStepIndex);
    } else {
      loadResultsView();
    }
  } else {
    renderPlayerStep(playerStepIndex);
  }
}

function handlePlayerSubmit() {
  const step = currentCase.screens[playerStepIndex];
  if (!step) return;

  const hasAnswer = hasSelectedAnyAnswer(step.question, playerStepIndex);
  if (!hasAnswer) {
    showSkipQuestionModal();
    return;
  }

  submittedAnswers[playerStepIndex] = true;
  evaluateStepScore(playerStepIndex);
  renderPlayerStep(playerStepIndex);
  // Response submitted toast removed per user request
}

function handlePlayerGiveUp() {
  submittedAnswers[playerStepIndex] = true;
  evaluateStepScore(playerStepIndex);
  playerScores[playerStepIndex].score = 0; // force zero points
  renderPlayerStep(playerStepIndex);
}

function displayPlayerFeedback(stepIdx) {
  const step = currentCase.screens[stepIdx];
  const res = playerScores[stepIdx] || { score: 0, max: 1 };
  
  const badge = document.getElementById('feedback-result-badge');
  const pointsEl = document.getElementById('feedback-score-display');
  const explText = document.getElementById('feedback-explanation-text');
  
  pointsEl.textContent = `Score: ${res.score} / ${res.max} point${res.max !== 1 ? 's' : ''}`;
  explText.innerHTML = step.question.explanation || 'No explanation rationale provided.';
  
  badge.className = 'feedback-badge';
  if (res.score === res.max) {
    badge.classList.add('correct');
    badge.textContent = 'Correct';
  } else if (res.score === 0) {
    badge.classList.add('incorrect');
    badge.textContent = 'Incorrect';
  } else {
    badge.classList.add('partial');
    badge.textContent = 'Partial Correct';
  }
}


/* ================= RESULTS VIEW (SCOREBOARD) ================= */
function initResultsEvents() {
  document.getElementById('results-retry-btn').addEventListener('click', () => {
    startPlayer(currentCase, { mode: sessionConfig.mode, isRemediation: false });
  });
  
  document.getElementById('results-dashboard-btn').addEventListener('click', () => {
    switchView('student');
  });

  const reviewAnswersBtn = document.getElementById('results-review-answers-btn');
  if (reviewAnswersBtn) {
    reviewAnswersBtn.addEventListener('click', () => {
      startRemediationReview(0);
    });
  }
}

function startRemediationReview(jumpIdx = 0) {
  sessionConfig.isRemediation = true;
  sessionConfig.allowBacktrack = true;
  currentCase.screens.forEach((s, idx) => {
    submittedAnswers[idx] = true;
    if (!playerScores[idx]) evaluateStepScore(idx);
  });
  switchView('player');
  renderPlayerStep(jumpIdx);
}

function loadResultsView() {
  currentCase.screens.forEach((s, idx) => {
    if (!submittedAnswers[idx]) {
      submittedAnswers[idx] = true;
      evaluateStepScore(idx);
      if (!playerScores[idx]) {
        playerScores[idx] = { score: 0, max: 1 };
      }
      playerScores[idx].score = 0; // auto zero if skipped
    }
  });
  
  let totalScore = 0;
  let totalMax = 0;
  
  Object.values(playerScores).forEach(s => {
    totalScore += s.score;
    totalMax += s.max;
  });
  
  const percent = totalMax > 0 ? Math.round((totalScore / totalMax) * 100) : 0;
  
  document.getElementById('results-case-title').textContent = currentCase.title;
  document.getElementById('results-score').textContent = `${totalScore} / ${totalMax}`;
  document.getElementById('results-percentage').textContent = `${percent}%`;
  
  const list = document.getElementById('results-breakdown-list');
  list.innerHTML = '';
  
  currentCase.screens.forEach((s, idx) => {
    const sc = playerScores[idx] || { score: 0, max: 1 };
    const typeLabel = (s.question.type || 'Question').toUpperCase().replace(/_/g, ' ');
    const isStepStandalone = currentCase.isStandalone || s.isStandalone;
    const contextLabel = isStepStandalone ? 'Stand-alone Question' : (s.caseTitle || currentCase.title || `Screen ${idx + 1}`);
    
    let badgeClass = 'incorrect';
    let badgeText = 'Incorrect';
    
    if (sc.score === sc.max) {
      badgeClass = 'correct';
      badgeText = 'Correct';
    } else if (sc.score > 0) {
      badgeClass = 'partial';
      badgeText = 'Partial';
    }
    
    const item = document.createElement('div');
    item.className = 'breakdown-item';
    item.style.cursor = 'pointer';
    item.title = 'Click to review question and clinical rationale';
    item.innerHTML = `
      <div class="breakdown-item-left">
        <span class="breakdown-badge ${badgeClass}">${badgeText}</span>
        <strong>Question ${idx + 1}</strong> (${contextLabel} &bull; ${typeLabel})
      </div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <span class="breakdown-score">${sc.score} / ${sc.max} pts</span>
        <span style="font-size: 11px; color: #38bdf8; font-weight: 500;">Review &rarr;</span>
      </div>
    `;
    item.addEventListener('click', () => {
      startRemediationReview(idx);
    });
    list.appendChild(item);
  });
  
  switchView('results');
}


function initCalculator() {
  const btns = document.querySelectorAll('.calc-btn');
  btns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const val = e.target.textContent.trim();
      const act = e.target.dataset.action;
      
      // Reset clear / mrc press counts if clicking a different action
      if (act !== 'clear') {
        clearPressCount = 0;
      }
      if (act !== 'mrc') {
        mrcPressCount = 0;
      }
      
      if (act === 'clear') {
        clearPressCount++;
        if (clearPressCount >= 2) {
          calcMemory = 0;
          clearPressCount = 0;
          showToast("Calculator memory cleared", "info");
        }
        calcInput = '0';
        calcPrevInput = null;
        calcOp = null;
        calcResetOnNext = false;
      } else if (act === 'sign') {
        if (calcInput !== '0' && calcInput !== 'Error') {
          calcInput = calcInput.startsWith('-') ? calcInput.slice(1) : '-' + calcInput;
        }
      } else if (act === 'sqrt') {
        let num = parseFloat(calcInput);
        if (num >= 0) {
          calcInput = Math.sqrt(num).toString().slice(0, 10);
        } else {
          calcInput = 'Error';
        }
        calcResetOnNext = true;
      } else if (act === 'percent') {
        let num = parseFloat(calcInput);
        calcInput = (num / 100).toString().slice(0, 10);
        calcResetOnNext = true;
      } else if (e.target.classList.contains('num-btn')) {
        if (calcInput === '0' || calcInput === 'Error' || calcResetOnNext) {
          calcInput = val;
          calcResetOnNext = false;
        } else {
          if (calcInput.length < 10) {
            if (val === '.' && calcInput.includes('.')) return;
            calcInput += val;
          }
        }
      } else if (e.target.classList.contains('op-btn')) {
        // Evaluate pending operation first (chaining support)
        if (calcPrevInput !== null && calcOp) {
          let curr = parseFloat(calcInput);
          let res = 0;
          switch (calcOp) {
            case 'add': res = calcPrevInput + curr; break;
            case 'subtract': res = calcPrevInput - curr; break;
            case 'multiply': res = calcPrevInput * curr; break;
            case 'divide': res = curr !== 0 ? calcPrevInput / curr : 'Error'; break;
          }
          calcInput = (res === 'Error') ? 'Error' : parseFloat(res.toFixed(8)).toString().slice(0, 10);
        }
        calcPrevInput = (calcInput === 'Error') ? null : parseFloat(calcInput);
        calcOp = act;
        calcResetOnNext = true;
      } else if (act === 'equals') {
        if (calcPrevInput !== null && calcOp) {
          let curr = parseFloat(calcInput);
          let res = 0;
          switch (calcOp) {
            case 'add': res = calcPrevInput + curr; break;
            case 'subtract': res = calcPrevInput - curr; break;
            case 'multiply': res = calcPrevInput * curr; break;
            case 'divide': res = curr !== 0 ? calcPrevInput / curr : 'Error'; break;
          }
          calcInput = (res === 'Error') ? 'Error' : parseFloat(res.toFixed(8)).toString().slice(0, 10);
          calcPrevInput = null;
          calcOp = null;
          calcResetOnNext = true;
        }
      } else if (e.target.classList.contains('mem-btn')) {
        if (act === 'mplus' || act === 'mminus') {
          // Evaluate pending operation first
          if (calcPrevInput !== null && calcOp) {
            let curr = parseFloat(calcInput);
            let res = 0;
            switch (calcOp) {
              case 'add': res = calcPrevInput + curr; break;
              case 'subtract': res = calcPrevInput - curr; break;
              case 'multiply': res = calcPrevInput * curr; break;
              case 'divide': res = curr !== 0 ? calcPrevInput / curr : 'Error'; break;
            }
            calcInput = (res === 'Error') ? 'Error' : parseFloat(res.toFixed(8)).toString().slice(0, 10);
            calcPrevInput = null;
            calcOp = null;
          }
          
          if (calcInput !== 'Error') {
            let num = parseFloat(calcInput);
            if (!isNaN(num)) {
              if (act === 'mplus') calcMemory += num;
              else if (act === 'mminus') calcMemory -= num;
            }
          }
          calcResetOnNext = true;
        } else if (act === 'mrc') {
          mrcPressCount++;
          if (mrcPressCount === 1) {
            calcInput = parseFloat(calcMemory.toFixed(8)).toString().slice(0, 10);
            calcResetOnNext = true;
          } else if (mrcPressCount >= 2) {
            calcMemory = 0;
            mrcPressCount = 0;
            showToast("Calculator memory cleared", "info");
          }
        }
      }
      
      updateCalculatorDisplay();
    });
  });

  document.addEventListener('keydown', (e) => {
    const calc = document.getElementById('ti108-calculator');
    if (!calc || calc.classList.contains('hidden')) return;

    // Ignore keypresses if focus is in an input or contenteditable element
    const activeEl = document.activeElement;
    if (activeEl && (
      activeEl.tagName === 'INPUT' || 
      activeEl.tagName === 'TEXTAREA' || 
      activeEl.contentEditable === 'true' || 
      activeEl.closest('[contenteditable="true"]')
    )) {
      return;
    }

    let btn = null;
    const key = e.key;

    if (key >= '0' && key <= '9') {
      btn = Array.from(calc.querySelectorAll('.num-btn')).find(b => b.textContent.trim() === key);
    } else if (key === '.') {
      btn = Array.from(calc.querySelectorAll('.num-btn')).find(b => b.textContent.trim() === '.');
    } else if (key === '+') {
      btn = calc.querySelector('[data-action="add"]');
    } else if (key === '-') {
      btn = calc.querySelector('[data-action="subtract"]');
    } else if (key === '*') {
      btn = calc.querySelector('[data-action="multiply"]');
    } else if (key === '/') {
      btn = calc.querySelector('[data-action="divide"]');
    } else if (key === '=' || key === 'Enter') {
      btn = calc.querySelector('[data-action="equals"]');
    } else if (key === 'Escape' || key === 'Backspace' || key.toLowerCase() === 'c') {
      btn = calc.querySelector('[data-action="clear"]');
    } else if (key === '%') {
      btn = calc.querySelector('[data-action="percent"]');
    } else if (key.toLowerCase() === 's') {
      btn = calc.querySelector('[data-action="sign"]');
    } else if (key.toLowerCase() === 'r') {
      btn = calc.querySelector('[data-action="sqrt"]');
    } else if (key.toLowerCase() === 'm') {
      btn = calc.querySelector('[data-action="mrc"]');
    } else if (key === '[') {
      btn = calc.querySelector('[data-action="mplus"]');
    } else if (key === ']') {
      btn = calc.querySelector('[data-action="mminus"]');
    }

    if (btn) {
      e.preventDefault();
      btn.click();
      btn.classList.add('active');
      setTimeout(() => btn.classList.remove('active'), 100);
    }
  });
}

function updateCalculatorDisplay() {
  const display = document.getElementById('calc-display');
  if (display) display.textContent = calcInput;
  
  const indicator = document.getElementById('calc-mem-indicator');
  if (indicator) {
    indicator.style.visibility = calcMemory !== 0 ? 'visible' : 'hidden';
  }
}

function toggleCalculator() {
  const calc = document.getElementById('ti108-calculator');
  if (calc.classList.contains('hidden')) {
    calc.classList.remove('hidden');
    calc.style.top = '50px';
    calc.style.left = '220px';
  } else {
    calc.classList.add('hidden');
  }
}

function makeCalculatorDraggable() {
  const calc = document.getElementById('ti108-calculator');
  const header = calc.querySelector('.calc-top-bar');
  
  if (!calc || !header) return;
  
  let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  
  header.addEventListener('mousedown', dragMouseDown);
  header.addEventListener('touchstart', dragTouchStart, { passive: false });
  
  function dragMouseDown(e) {
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.addEventListener('mouseup', closeDragElement);
    document.addEventListener('mousemove', elementDrag);
  }
  
  function dragTouchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    pos3 = touch.clientX;
    pos4 = touch.clientY;
    document.addEventListener('touchend', closeDragTouch);
    document.addEventListener('touchmove', elementTouchDrag, { passive: false });
  }
  
  function elementDrag(e) {
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    
    let finalTop = calc.offsetTop - pos2;
    let finalLeft = calc.offsetLeft - pos1;
    
    calc.style.top = Math.max(0, finalTop) + "px";
    calc.style.left = Math.max(0, finalLeft) + "px";
  }
  
  function elementTouchDrag(e) {
    e.preventDefault();
    const touch = e.touches[0];
    pos1 = pos3 - touch.clientX;
    pos2 = pos4 - touch.clientY;
    pos3 = touch.clientX;
    pos4 = touch.clientY;
    
    let finalTop = calc.offsetTop - pos2;
    let finalLeft = calc.offsetLeft - pos1;
    
    calc.style.top = Math.max(0, finalTop) + "px";
    calc.style.left = Math.max(0, finalLeft) + "px";
  }
  
  function closeDragElement() {
    document.removeEventListener('mouseup', closeDragElement);
    document.removeEventListener('mousemove', elementDrag);
  }
  
  function closeDragTouch() {
    document.removeEventListener('touchend', closeDragTouch);
    document.removeEventListener('touchmove', elementTouchDrag);
  }
}

/* ================= ESCAPING UTILITIES ================= */
function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, 
    tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag)
  );
}

function stripNursesNotesFormatting(html) {
  if (!html) return '';
  const temp = document.createElement('div');
  temp.innerHTML = html;
  
  temp.querySelectorAll('.nurse-note-row').forEach(row => {
    row.classList.remove('nurse-note-row');
    row.style.paddingLeft = '';
    row.style.textIndent = '';
  });
  
  temp.querySelectorAll('.nurse-note-time, .nurse-note-text').forEach(span => {
    const parent = span.parentNode;
    if (parent) {
      while (span.firstChild) {
        parent.insertBefore(span.firstChild, span);
      }
      parent.removeChild(span);
    }
  });
  
  return temp.innerHTML;
}

function formatNursesNotes(html, tabTitle) {
  if (!tabTitle || !/nurse|note|log|progress/i.test(tabTitle)) {
    return html;
  }
  if (!html) return '';

  const temp = document.createElement('div');
  temp.innerHTML = html;

  Array.from(temp.childNodes).forEach(child => {
    // Keep rows that already carry an authored time label such as "0800 (DOL 2)"
    // or "Postoperative Day 4"; re-detecting them would only recognize plain times.
    if (isAuthoredNoteRow(child)) return;

    let nodes = [child];
    if (child.nodeType === Node.ELEMENT_NODE) {
      const holder = document.createElement('div');
      holder.innerHTML = stripNursesNotesFormatting(child.outerHTML);
      nodes = Array.from(holder.childNodes);
      nodes.forEach(n => temp.insertBefore(n, child));
      temp.removeChild(child);
    }
    nodes.forEach(node => formatNoteNode(node, temp));
  });

  return temp.innerHTML;
}

// A note's time label: "0800", "08:00", or a time with a short qualifier such as "0800 (DOL 2)".
const NOTE_TIME_REGEX = /^\s*(\b\d{2}:?\d{2}\b(?:\s*\([^()<>]{1,60}\))?)\s*:\s*(.*)/is;

function isAuthoredNoteRow(node) {
  if (node.nodeType !== Node.ELEMENT_NODE || !node.classList.contains('nurse-note-row') || node.children.length !== 2) return false;
  const [time, text] = node.children;
  const label = time.textContent.replace(/ /g, ' ').trim();
  return time.classList.contains('nurse-note-time') && text.classList.contains('nurse-note-text') &&
    time.children.length === 0 && label.length > 0 && label.length <= 60;
}

function formatNoteNode(child, parent) {
  if (child.nodeType === Node.ELEMENT_NODE) {
    const tagName = child.tagName.toLowerCase();
    if (['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(tagName)) {
      // Strip any existing <b>/<strong> tags around time digits to clean up
      let innerHTML = child.innerHTML.replace(/<\/?(?:strong|b)>/g, '').trim();
      const match = innerHTML.match(NOTE_TIME_REGEX);

      if (match) {
        const rawTime = match[1];
        const restHtml = match[2].trim();
        child.className = 'nurse-note-row';
        child.innerHTML = `<span class="nurse-note-time">${rawTime}:</span><span class="nurse-note-text">${restHtml}</span>`;
      } else {
        child.classList.remove('nurse-note-row');
      }
    }
  } else if (child.nodeType === Node.TEXT_NODE && child.textContent.trim()) {
    const text = child.textContent.trim();
    const match = text.match(NOTE_TIME_REGEX);
    const newP = document.createElement('p');
    if (match) {
      const rawTime = match[1];
      const restText = match[2].trim();
      newP.className = 'nurse-note-row';
      newP.innerHTML = `<span class="nurse-note-time">${escapeHTML(rawTime)}:</span><span class="nurse-note-text">${escapeHTML(restText)}</span>`;
    } else {
      newP.textContent = text;
    }
    parent.replaceChild(newP, child);
  }
}

let selectedTableCellElement = null;

function setupTableInteractionMenu() {
  let menu = document.getElementById('table-interaction-menu');
  if (!menu) {
    menu = document.createElement('div');
    menu.id = 'table-interaction-menu';
    menu.style.position = 'absolute';
    menu.style.display = 'none';
    menu.style.zIndex = '10000';
    menu.style.background = '#1e293b';
    menu.style.border = '1px solid #475569';
    menu.style.borderRadius = 'var(--radius-md)';
    menu.style.padding = '6px';
    menu.style.boxShadow = 'var(--shadow-lg)';
    menu.style.gap = '4px';
    menu.style.flexDirection = 'column';
    menu.style.maxHeight = '180px';
    menu.style.overflowY = 'auto';
    menu.style.width = '160px';
    menu.innerHTML = `
      <button id="tbl-menu-add-row-below" class="btn btn-secondary btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">+ Add Row Below</button>
      <button id="tbl-menu-add-row-above" class="btn btn-secondary btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">+ Add Row Above</button>
      <button id="tbl-menu-delete-row" class="btn btn-danger btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">- Delete Row</button>
      <div style="border-top:1px solid #334155; margin:4px 0;"></div>
      <button id="tbl-menu-add-col-right" class="btn btn-secondary btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">+ Add Column Right</button>
      <button id="tbl-menu-add-col-left" class="btn btn-secondary btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">+ Add Column Left</button>
      <button id="tbl-menu-delete-col" class="btn btn-danger btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">- Delete Column</button>
    `;
    document.body.appendChild(menu);

    // Context Actions implementation
    menu.querySelector('#tbl-menu-add-row-below').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const row = selectedTableCellElement.closest('tr');
      const parent = row.parentNode;
      const colsCount = row.cells.length;
      
      const newRow = document.createElement('tr');
      for (let j = 0; j < colsCount; j++) {
        const newCell = document.createElement('td');
        newCell.setAttribute('placeholder', 'Cell');
        newCell.style.border = '1px solid #ccd8e0';
        newCell.style.padding = '8px';
        newCell.style.minWidth = '80px';
        newCell.style.background = 'white';
        newCell.style.color = '#1e293b';
        newRow.appendChild(newCell);
      }
      if (row.nextSibling) {
        parent.insertBefore(newRow, row.nextSibling);
      } else {
        parent.appendChild(newRow);
      }
      menu.style.display = 'none';
    });

    menu.querySelector('#tbl-menu-add-row-above').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const row = selectedTableCellElement.closest('tr');
      const parent = row.parentNode;
      const colsCount = row.cells.length;
      
      const newRow = document.createElement('tr');
      const isHeader = parent.tagName.toLowerCase() === 'thead';
      for (let j = 0; j < colsCount; j++) {
        const newCell = document.createElement(isHeader ? 'th' : 'td');
        if (isHeader) {
          newCell.setAttribute('placeholder', `Header ${j+1}`);
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.background = '#025287';
          newCell.style.color = 'white';
          newCell.style.fontWeight = '600';
          newCell.style.textAlign = 'left';
        } else {
          newCell.setAttribute('placeholder', 'Cell');
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.minWidth = '80px';
          newCell.style.background = 'white';
          newCell.style.color = '#1e293b';
        }
        newRow.appendChild(newCell);
      }
      parent.insertBefore(newRow, row);
      menu.style.display = 'none';
    });

    menu.querySelector('#tbl-menu-delete-row').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const row = selectedTableCellElement.closest('tr');
      const table = selectedTableCellElement.closest('table');
      if (table.querySelectorAll('tr').length > 1) {
        row.remove();
      }
      menu.style.display = 'none';
    });

    menu.querySelector('#tbl-menu-add-col-right').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const cellIndex = selectedTableCellElement.cellIndex;
      const table = selectedTableCellElement.closest('table');
      const rows = table.querySelectorAll('tr');
      
      rows.forEach(r => {
        const isHeader = r.closest('thead') !== null;
        const targetCell = r.cells[cellIndex];
        const newCell = document.createElement(isHeader ? 'th' : 'td');
        
        if (isHeader) {
          newCell.setAttribute('placeholder', 'Header');
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.background = '#025287';
          newCell.style.color = 'white';
          newCell.style.fontWeight = '600';
          newCell.style.textAlign = 'left';
        } else {
          newCell.setAttribute('placeholder', 'Cell');
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.minWidth = '80px';
          newCell.style.background = 'white';
          newCell.style.color = '#1e293b';
        }
        if (targetCell && targetCell.nextSibling) {
          r.insertBefore(newCell, targetCell.nextSibling);
        } else {
          r.appendChild(newCell);
        }
      });
      menu.style.display = 'none';
    });

    menu.querySelector('#tbl-menu-add-col-left').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const cellIndex = selectedTableCellElement.cellIndex;
      const table = selectedTableCellElement.closest('table');
      const rows = table.querySelectorAll('tr');
      
      rows.forEach(r => {
        const isHeader = r.closest('thead') !== null;
        const targetCell = r.cells[cellIndex];
        const newCell = document.createElement(isHeader ? 'th' : 'td');
        
        if (isHeader) {
          newCell.setAttribute('placeholder', 'Header');
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.background = '#025287';
          newCell.style.color = 'white';
          newCell.style.fontWeight = '600';
          newCell.style.textAlign = 'left';
        } else {
          newCell.setAttribute('placeholder', 'Cell');
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.minWidth = '80px';
          newCell.style.background = 'white';
          newCell.style.color = '#1e293b';
        }
        r.insertBefore(newCell, targetCell);
      });
      menu.style.display = 'none';
    });

    menu.querySelector('#tbl-menu-delete-col').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const cellIndex = selectedTableCellElement.cellIndex;
      const table = selectedTableCellElement.closest('table');
      const rows = table.querySelectorAll('tr');
      
      if (selectedTableCellElement.closest('tr').cells.length > 1) {
        rows.forEach(r => {
          if (r.cells[cellIndex]) {
            r.cells[cellIndex].remove();
          }
        });
      }
      menu.style.display = 'none';
    });
  }

  // Bind mousedown listener to table elements inside editor to position the menu
  document.addEventListener('mousedown', (e) => {
    // If click/mousedown is inside the menu itself, do nothing
    if (e.target.closest('#table-interaction-menu')) {
      return;
    }
    
    // Check if mousedown was inside a contenteditable rich-text cell
    const cell = e.target.closest('[contenteditable="true"] td, [contenteditable="true"] th');
    if (cell) {
      const rect = cell.getBoundingClientRect();
      const clickedX = e.clientX;
      const clickedY = e.clientY;
      const insideChevronX = (clickedX >= rect.right - 24 && clickedX <= rect.right);
      const insideChevronY = (clickedY >= rect.top && clickedY <= rect.top + 24);
      
      if (insideChevronX && insideChevronY) {
        if (menu.style.display === 'flex' && selectedTableCellElement === cell) {
          menu.style.display = 'none';
          selectedTableCellElement = null;
        } else {
          selectedTableCellElement = cell;
          menu.style.display = 'flex';
          
          const menuHeight = 180;
          const screenHeight = window.innerHeight;
          const offsetBelow = rect.bottom + menuHeight;
          
          if (offsetBelow > screenHeight && rect.top > menuHeight) {
            menu.style.top = `${rect.top + window.scrollY - menuHeight}px`;
          } else {
            menu.style.top = `${rect.bottom + window.scrollY}px`;
          }
          menu.style.left = `${rect.left + window.scrollX}px`;
        }
      } else {
        menu.style.display = 'none';
      }
    } else {
      menu.style.display = 'none';
    }
  });
}

// Run initializer on window load
if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', setupTableInteractionMenu);
} else {
  setupTableInteractionMenu();
}
