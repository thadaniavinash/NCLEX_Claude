/* Question bank data: content sanitizing, format migrations, loading and saving. */

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
