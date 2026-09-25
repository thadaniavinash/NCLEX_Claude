/* Shared constants and application state, plus IndexedDB browser storage. */

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
// True when the database is enabled but could not be read, so the app fell back
// to cases-data.js. Saving would overwrite newer database content, so it is refused.
let isDatabaseUnavailable = false;
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
// Set by restoreAdminSession() / signInAdmin() in auth.js once a Supabase admin session is confirmed.
let isAdminLoggedIn = false;

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
