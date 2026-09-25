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

// NCLEX_Claude's own Supabase project (not the original app's database).
const SUPABASE_URL = 'https://wgnrcopjkylviiyllsgz.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_yHZHAVA7OjJajQJfJ8zFAw_q2ld1l6M';
const USE_SUPABASE = true;

async function loadAllData() {
  // Try fetching from Supabase database
  let loadedFromSupabase = false;
  if (USE_SUPABASE) try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/nclex_data?select=*`, {
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
      }
    });
    if (response.ok) {
      const records = await response.json();
      const casesRecord = records.find(r => r.key === 'cases');
      const standaloneRecord = records.find(r => r.key === 'standalone');
      
      // An empty or missing bank means the database was never loaded (or was
      // wiped): use cases-data.js rather than showing, and later saving, nothing.
      if (casesRecord && Array.isArray(casesRecord.data) && casesRecord.data.length > 0) {
        caseStudies = casesRecord.data;
        caseStudies.forEach(migrateCaseTypes);
        standaloneQuestions = (standaloneRecord && Array.isArray(standaloneRecord.data)) ? standaloneRecord.data : [];
        standaloneQuestions.forEach(migrateCaseTypes);
        loadedFromSupabase = true;
        rememberBankSnapshot('cases', caseStudies, casesRecord.version);
        rememberBankSnapshot('standalone', standaloneQuestions, standaloneRecord ? standaloneRecord.version : null);
      } else {
        console.warn('Supabase returned no case studies, falling back to cases-data.js.');
      }
    } else {
      console.warn('Supabase fetch failed, falling back to local files/storage.', response.status);
    }
  } catch (err) {
    console.error('Error fetching from Supabase:', err);
  }

  // Fallback if Supabase fetch failed (or returned nothing)
  if (!loadedFromSupabase) {
    // Saving now would overwrite the database with this older fallback copy.
    if (USE_SUPABASE) isDatabaseUnavailable = true;
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

function refuseUnsafeSave() {
  if (isBankFiltered) {
    showToast('Saving is disabled on filtered links. Open the app without ?cases= or ?standalone= to edit.', 'error');
    return true;
  }
  if (isDatabaseUnavailable) {
    showToast('The database could not be reached when the page loaded, so saving is disabled to avoid overwriting newer questions. Reload the page and try again.', 'error');
    return true;
  }
  return false;
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

/* ---- Which items students can see ----
   Unfinished items (no question text, or an answer key that cannot score full marks) stay
   in the bank and in the authoring studio, but are left out of student sessions and links. */

function hasText(html) {
  return typeof html === 'string' && html.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim().length > 0;
}

// Why a screen is not ready for students, or '' when it is.
function screenProblem(q) {
  if (!q || !q.type) return 'no question';
  if (!hasText(q.stem)) return 'no question text';
  const options = q.options || [];
  const correct = options.filter(o => o.correct).length;
  switch (q.type) {
    case 'select_all': case 'trend':
      if (!correct) return 'no correct option';
      if (options.some(o => !hasText(o.text))) return 'blank option';
      return '';
    case 'multiple_choice':
      if (correct !== 1) return 'needs exactly one correct option';
      if (options.some(o => !hasText(o.text))) return 'blank option';
      return '';
    case 'select_n':
      if (!correct || correct !== (q.limit || 0)) return 'number of correct options does not match';
      if (options.some(o => !hasText(o.text))) return 'blank option';
      return '';
    case 'matrix_mc': case 'matrix_mr': {
      const m = q.matrix || {};
      if (!(m.rows || []).length || (m.rows || []).some(r => !hasText(r.text))) return 'blank matrix row';
      if ((m.columns || []).some(c => !hasText(c))) return 'blank matrix column';
      if (q.type === 'matrix_mc' && m.rows.some(r => !(r.correctIndex >= 0 && r.correctIndex < m.columns.length))) return 'matrix row without an answer';
      return '';
    }
    case 'dropdown_cloze': case 'drag_drop_cloze': case 'dyad': case 'triad': {
      const dropdowns = (q.cloze && q.cloze.dropdowns) || [];
      const blanks = ((q.cloze && q.cloze.text) || '').match(/\[\[d(?:r)?op\d+\]\]/gi) || [];
      if (!dropdowns.length || blanks.length !== dropdowns.length) return 'drop-downs do not match the sentence';
      if (dropdowns.some(d => (d.options || []).filter(o => o.correct).length !== 1)) return 'drop-down without exactly one answer';
      if (dropdowns.some(d => (d.options || []).some(o => !hasText(o.text)))) return 'blank drop-down option';
      return '';
    }
    case 'bowtie': {
      const count = list => (list || []).filter(x => x.correct && hasText(x.text)).length;
      if (count(q.bowtieActions) !== 2 || count(q.bowtieConditions) !== 1 || count(q.bowtieParams) !== 2) return 'bowtie answer key incomplete';
      return '';
    }
    case 'highlight': case 'highlight_2': {
      const passages = q.highlightTabs ? q.highlightTabs.map(t => t.content || '') : [q.highlightText || ''];
      return passages.some(p => /\|correct\}/.test(p)) ? '' : 'nothing marked to highlight';
    }
    case 'ordered_response':
      return (q.orderedOptions || []).filter(hasText).length >= 2 ? '' : 'fewer than two items to order';
    default:
      return '';
  }
}

function itemProblems(item) {
  if (!item || !Array.isArray(item.screens) || !item.screens.length) return ['no screens'];
  return item.screens.map((s, i) => { const p = screenProblem(s.question); return p ? `screen ${i + 1}: ${p}` : ''; }).filter(Boolean);
}

function isReadyForStudents(item) {
  return itemProblems(item).length === 0;
}

function studentCaseStudies() {
  return caseStudies.filter(isReadyForStudents);
}

function studentStandaloneQuestions() {
  return standaloneQuestions.filter(isReadyForStudents);
}

/* ---- Saving to the database ----
   Each row ('cases', 'standalone') holds a whole list and carries a version number that the
   database bumps on every save. A save only applies if the row is still at the version this
   page loaded; if another editor saved in the meantime, the latest list is fetched, this
   page's own additions, edits and deletions are applied on top of it, and the save is retried.
   Saving requires a signed-in administrator (see auth.js). */

// What this page last loaded or saved, per row: { version, items: Map(id -> JSON) }.
const bankSnapshots = { cases: null, standalone: null };

function rememberBankSnapshot(key, items, version) {
  bankSnapshots[key] = {
    version: (version === undefined ? null : version),
    items: new Map(items.map(item => [item.id, JSON.stringify(item)]))
  };
}

function bankList(key) {
  return key === 'cases' ? caseStudies : standaloneQuestions;
}

function setBankList(key, items) {
  if (key === 'cases') caseStudies = items;
  else standaloneQuestions = items;
}

async function fetchBankRow(key) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/nclex_data?key=eq.${key}&select=*`, {
    headers: { 'apikey': SUPABASE_ANON_KEY, 'Authorization': `Bearer ${SUPABASE_ANON_KEY}` }
  });
  if (!res.ok) throw new Error(`read failed: ${res.status}`);
  const [row] = await res.json();
  if (!row || !Array.isArray(row.data)) throw new Error('row missing');
  row.data.forEach(migrateCaseTypes);
  return { items: row.data, version: row.version === undefined ? null : row.version };
}

// Apply this page's changes (relative to its snapshot) on top of the latest saved list.
// Returns the merged list and the titles of items that both sides had changed.
function mergeBankChanges(snapshot, localItems, latestItems) {
  const localById = new Map(localItems.map(item => [item.id, item]));
  const deletedHere = [...snapshot.items.keys()].filter(id => !localById.has(id));
  const changedHere = localItems.filter(item => snapshot.items.get(item.id) !== JSON.stringify(item));
  const conflicts = [];

  const merged = latestItems.filter(item => !deletedHere.includes(item.id));
  changedHere.forEach(item => {
    const i = merged.findIndex(other => other.id === item.id);
    if (i === -1) {
      merged.push(item);
    } else {
      const before = snapshot.items.get(item.id);
      if (before !== undefined && before !== JSON.stringify(merged[i])) conflicts.push(item.title || item.id);
      merged[i] = item; // this page's version wins, and the editor is told
    }
  });
  return { merged, conflicts };
}

// PATCH one row. Returns { status: 'saved' | 'conflict' | 'denied' | 'error', version }.
async function patchBankRow(key, items, expectedVersion, token) {
  const versioned = expectedVersion !== null;
  const res = await fetch(`${SUPABASE_URL}/rest/v1/nclex_data?key=eq.${key}${versioned ? `&version=eq.${expectedVersion}` : ''}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'apikey': SUPABASE_ANON_KEY,
      'Authorization': `Bearer ${token}`,
      'Prefer': 'return=representation'
    },
    body: JSON.stringify({ data: items })
  });
  if (res.status === 401 || res.status === 403) return { status: 'denied' };
  if (!res.ok) return { status: 'error' };
  const rows = await res.json();
  if (rows.length === 1) return { status: 'saved', version: rows[0].version === undefined ? null : rows[0].version };
  // No row updated: either someone saved first (version moved on) or this account may not save.
  if (!versioned) return { status: 'denied' };
  const latest = await fetchBankRow(key);
  return { status: latest.version !== expectedVersion ? 'conflict' : 'denied' };
}

async function saveBankRowToDatabase(key) {
  const token = await getAdminAccessToken();
  if (!token) return { ok: false, reason: 'signed-out' };
  let items = bankList(key);
  let expectedVersion = bankSnapshots[key] ? bankSnapshots[key].version : null;
  const conflicts = [];
  let merged = false;

  for (let attempt = 0; attempt < 3; attempt++) {
    const result = await patchBankRow(key, items, expectedVersion, token);
    if (result.status === 'saved') {
      setBankList(key, items);
      rememberBankSnapshot(key, items, result.version);
      return { ok: true, merged, conflicts };
    }
    if (result.status !== 'conflict') return { ok: false, reason: result.status };
    const latest = await fetchBankRow(key);
    const mergeResult = mergeBankChanges(bankSnapshots[key], bankList(key), latest.items);
    items = mergeResult.merged;
    expectedVersion = latest.version;
    mergeResult.conflicts.forEach(title => { if (!conflicts.includes(title)) conflicts.push(title); });
    merged = true;
  }
  return { ok: false, reason: 'busy' };
}

function showSaveResult(savedToLocalServer, dbResult) {
  if (dbResult && dbResult.ok) {
    if (dbResult.conflicts.length) {
      showToast(`Saved. Someone else had also changed ${dbResult.conflicts.join(', ')}; your version replaced theirs.`, 'warning');
    } else if (dbResult.merged) {
      showToast('Saved. Changes another editor made since you opened the page were kept as well.');
      if (typeof renderDashboard === 'function') renderDashboard();
    } else {
      showToast('Changes saved to cloud database.');
    }
    return;
  }
  const reason = dbResult && dbResult.reason;
  if (reason === 'signed-out') {
    showToast(savedToLocalServer ? 'Saved to cases-data.js on your hard drive. Log in as an administrator to also save to the database.'
                                 : 'Not saved: log in as an administrator to save changes.', 'error');
  } else if (reason === 'denied') {
    showToast('Not saved: this account is not allowed to save. Log in again as an administrator.', 'error');
  } else if (reason === 'busy') {
    showToast('Not saved: other editors are saving right now. Wait a moment and save again.', 'error');
  } else if (reason) {
    showToast('Not saved: the database could not be reached. Your changes are still on this page; try saving again.', 'error');
  } else if (savedToLocalServer) {
    showToast('Saved directly to cases-data.js on your hard drive!');
  } else {
    showToast('Not saved permanently: no database is connected, so this change will be lost when the page reloads.', 'warning');
  }
}

async function saveBankToStorage(key) {
  if (refuseUnsafeSave()) return;
  // 1. IndexedDB / localStorage copy in this browser
  const storeName = key === 'cases' ? 'case_studies' : 'standalone_questions';
  if (db) {
    bankList(key).forEach(item => putInStore(storeName, item));
  } else {
    try {
      localStorage.setItem(key === 'cases' ? 'nclex_cases' : 'nclex_standalone', JSON.stringify(bankList(key)));
    } catch (e) {
      console.warn("localStorage is blocked:", e);
    }
  }

  // 2. Direct save to Local Server if running locally
  const savedToLocalServer = await saveToLocalBackend(caseStudies, standaloneQuestions);

  // 3. The database
  let dbResult = null;
  if (USE_SUPABASE) {
    try {
      dbResult = await saveBankRowToDatabase(key);
    } catch (err) {
      console.error(`Error saving ${key} to Supabase:`, err);
      dbResult = { ok: false, reason: 'error' };
    }
  }

  showSaveResult(savedToLocalServer, dbResult);
}

function saveCasesToStorage() {
  return saveBankToStorage('cases');
}

function saveStandaloneToStorage() {
  return saveBankToStorage('standalone');
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
