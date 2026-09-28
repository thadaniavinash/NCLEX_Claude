/* My progress: each finished session's scores, kept only in this browser (localStorage), and the page
   that summarizes them. Nothing is sent anywhere; students can export the record to a file and import
   it on another device.

   Stored record (PROGRESS_STORAGE_KEY):
   { version: 1, sessions: [ { id, at (ISO), mode: 'review'|'test', title,
       questions: [ { item, kind: 'case'|'standalone', title, course, unit, screen, cj, type,
                      score, max, answered } ] } ] }
   `screen` is the question's position inside its item, `cj` the clinical judgment step (0-5) for
   case-study screens. Titles, course and unit are copied in so the record still reads well if the
   bank changes later. When student accounts arrive, these rows map one-to-one onto a results table. */

const PROGRESS_STORAGE_KEY = 'nclex_progress_v1';
const PROGRESS_MAX_SESSIONS = 500;
const REVISIT_LIMIT = { cases: 3, standalone: 30 }; // size of a "practise again" session

function emptyProgress() {
  return { version: 1, sessions: [] };
}

function loadProgress() {
  try {
    const raw = localStorage.getItem(PROGRESS_STORAGE_KEY);
    if (!raw) return emptyProgress();
    const data = JSON.parse(raw);
    if (!data || !Array.isArray(data.sessions)) return emptyProgress();
    return data;
  } catch (e) {
    return emptyProgress();
  }
}

// Returns false when the browser will not keep the data (private window, storage off or full).
function saveProgress(data) {
  data.sessions.sort((a, b) => String(a.at).localeCompare(String(b.at)));
  while (data.sessions.length > PROGRESS_MAX_SESSIONS) data.sessions.shift();
  for (;;) {
    try {
      localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(data));
      return true;
    } catch (e) {
      if (data.sessions.length <= 1) return false;
      data.sessions.shift(); // storage full: drop the oldest session and try again
    }
  }
}

function findBankItem(id) {
  return caseStudies.find(c => c.id === id) || standaloneQuestions.find(q => q.id === id) || null;
}

// "Unit 3 (Genetic and Developmental Disorders)" -> { num: 'Unit 3', name: 'Genetic and Developmental Disorders' }
function unitParts(unit) {
  const m = /^(Unit\s*\d+)\s*\((.*)\)\s*$/.exec(unit || '');
  if (m) return { num: m[1], name: m[2] };
  if (!unit || unit === 'Others') return { num: 'General practice', name: 'Not assigned to a unit' };
  return { num: unit, name: '' };
}

function courseUnitKey(course, unit) {
  return `${course || 'Others'}|${unit || 'Others'}`;
}

// Where each screen of the session that just finished came from.
function sessionScreenSources() {
  return currentCase.screens.map((s, idx) => {
    if (s.caseId) return { id: s.caseId, kind: 'case', screen: s.itemScreen ?? 0 };
    if (s.itemId) return { id: s.itemId, kind: 'standalone', screen: 0 };
    const kind = currentCase.isStandalone || String(currentCase.id).startsWith('standalone_') ? 'standalone' : 'case';
    return { id: currentCase.id, kind, screen: idx };
  });
}

function describeSession(questions) {
  const items = [...new Set(questions.map(q => q.item))];
  if (items.length === 1) return questions[0].title;
  const units = [...new Set(questions.map(q => courseUnitKey(q.course, q.unit)))];
  const labels = units.map(k => { const [course, unit] = k.split('|'); const u = unitParts(unit); return course === 'Others' ? u.num : `${course} ${u.num}`; });
  return labels.length <= 2 ? labels.join(', ') : `${labels.slice(0, 2).join(', ')} and ${labels.length - 2} more`;
}

// Called once when a session's results are shown. `answeredSteps[i]` says whether the student
// answered screen i (skipped screens count as 0 points).
function recordSessionProgress(answeredSteps) {
  if (!currentCase || !Array.isArray(currentCase.screens)) return false;
  const sources = sessionScreenSources();
  const questions = currentCase.screens.map((s, idx) => {
    const src = sources[idx];
    const item = findBankItem(src.id) || {};
    const sc = playerScores[idx] || { score: 0, max: 1 };
    return {
      item: src.id,
      kind: src.kind,
      title: item.title || s.caseTitle || currentCase.title || '',
      course: item.course || 'Others',
      unit: item.unit || item.topic || 'Others',
      screen: src.screen,
      cj: src.kind === 'case' && src.screen < CLINICAL_JUDGMENT_STEPS.length ? src.screen : null,
      type: (s.question && s.question.type) || '',
      score: sc.score,
      max: sc.max,
      answered: !!answeredSteps[idx]
    };
  });
  const data = loadProgress();
  data.sessions.push({
    id: 's_' + Date.now(),
    at: new Date().toISOString(),
    mode: sessionConfig.mode === 'test' ? 'test' : 'review',
    title: describeSession(questions),
    questions
  });
  return saveProgress(data);
}

/* ---- Summaries ---- */

function percentOf(score, max) {
  return max > 0 ? Math.round((score / max) * 100) : 0;
}

function summarizeProgress(data) {
  const sessions = data.sessions;
  const all = sessions.flatMap(s => s.questions.map(q => Object.assign({ at: s.at }, q)));
  const sum = list => list.reduce((acc, q) => { acc.score += q.score; acc.max += q.max; return acc; }, { score: 0, max: 0 });

  const byStep = CLINICAL_JUDGMENT_STEPS.map((label, i) => {
    const list = all.filter(q => q.cj === i);
    return Object.assign({ label, count: list.length }, sum(list));
  });

  const unitMap = new Map();
  all.forEach(q => {
    const key = courseUnitKey(q.course, q.unit);
    if (!unitMap.has(key)) unitMap.set(key, { key, course: q.course, unit: q.unit, count: 0, score: 0, max: 0, items: new Set() });
    const u = unitMap.get(key);
    u.count++; u.score += q.score; u.max += q.max; u.items.add(q.item);
  });
  const available = studentCaseStudies().concat(studentStandaloneQuestions());
  const byUnit = [...unitMap.values()].map(u => Object.assign(u, {
    available: available.filter(i => courseUnitKey(i.course, i.unit || i.topic) === u.key).length
  })).sort((a, b) => a.key.localeCompare(b.key, undefined, { numeric: true }));

  // Latest result per item: an item needs another look when its latest attempt lost points.
  const latest = new Map();
  sessions.forEach(s => {
    const perItem = new Map();
    s.questions.forEach(q => {
      if (!perItem.has(q.item)) perItem.set(q.item, { item: q.item, kind: q.kind, title: q.title, course: q.course, unit: q.unit, at: s.at, score: 0, max: 0 });
      const r = perItem.get(q.item); r.score += q.score; r.max += q.max;
    });
    perItem.forEach((r, id) => latest.set(id, r));
  });
  const revisit = [...latest.values()]
    .filter(r => r.score < r.max && findBankItem(r.item) && isReadyForStudents(findBankItem(r.item)))
    .sort((a, b) => percentOf(a.score, a.max) - percentOf(b.score, b.max));

  return {
    sessions: sessions.length,
    answered: all.filter(q => q.answered).length,
    totals: sum(all),
    practised: latest.size,
    available: available.length,
    byStep,
    byUnit,
    revisit,
    recent: sessions.slice(-8).reverse()
  };
}

/* ---- Page ---- */

function progressMeter(score, max, label) {
  const pct = percentOf(score, max);
  return `<span class="meter" role="img" aria-label="${escapeHTML(label)}: ${pct}%" title="${score} of ${max} points"><span class="meter-fill" style="width:${pct}%"></span></span>`;
}

function formatSessionDate(iso) {
  const d = new Date(iso);
  if (isNaN(d)) return '';
  const today = new Date();
  const sameDay = d.toDateString() === today.toDateString();
  const yesterday = new Date(today); yesterday.setDate(today.getDate() - 1);
  const time = d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  if (sameDay) return `Today, ${time}`;
  if (d.toDateString() === yesterday.toDateString()) return `Yesterday, ${time}`;
  return d.toLocaleDateString([], { day: 'numeric', month: 'short', year: d.getFullYear() === today.getFullYear() ? undefined : 'numeric' });
}

function unitLabelHTML(course, unit) {
  const u = unitParts(unit);
  const head = course === 'Others' ? u.num : `${escapeHTML(course)} · ${escapeHTML(u.num)}`;
  return `<span class="unit-label"><strong>${head}</strong>${u.name ? `<span>${escapeHTML(u.name)}</span>` : ''}</span>`;
}

const PROGRESS_PRIVACY_TEXT = 'Your results are saved only in this browser on this device. They are not sent to your instructor or anyone else. Clearing your browsing data or using a private window removes them; use Export to keep a copy or to move them to another device.';

function renderProgressView() {
  const box = document.getElementById('progress-content');
  if (!box) return;
  const data = loadProgress();
  const privacy = `<div class="app-notice" role="note"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg><p>${PROGRESS_PRIVACY_TEXT}</p></div>`;
  const dataPanel = `
    <section class="app-card" aria-labelledby="progress-data-title">
      <h2 id="progress-data-title" class="app-card-title">Your data</h2>
      <p class="app-card-sub">Move your progress to another browser or device with a file, or start again.</p>
      <div class="app-actions">
        <button type="button" class="app-btn" id="progress-export-btn" ${data.sessions.length ? '' : 'disabled'}>Export to a file</button>
        <button type="button" class="app-btn" id="progress-import-btn">Import from a file</button>
        <button type="button" class="app-btn danger" id="progress-clear-btn" ${data.sessions.length ? '' : 'disabled'}>Delete my progress</button>
        <input type="file" id="progress-import-input" accept="application/json,.json" class="hidden">
      </div>
      <div id="progress-clear-confirm" class="app-confirm hidden" role="alertdialog" aria-labelledby="progress-clear-q">
        <p id="progress-clear-q">Delete all ${data.sessions.length} session${data.sessions.length === 1 ? '' : 's'} from this browser? This cannot be undone.</p>
        <button type="button" class="app-btn danger" id="progress-clear-yes">Delete</button>
        <button type="button" class="app-btn" id="progress-clear-no">Keep</button>
      </div>
      <p id="progress-data-message" class="app-card-sub" role="status"></p>
    </section>`;

  if (!data.sessions.length) {
    box.innerHTML = `${privacy}
      <section class="app-card app-empty">
        <svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        <h2>No results yet</h2>
        <p>Finish a practice session and your scores appear here, by unit and by clinical judgment step.</p>
        <button type="button" class="app-btn primary" data-goto="student">Start practising</button>
      </section>
      ${dataPanel}`;
    return;
  }

  const sum = summarizeProgress(data);
  const tiles = [
    { label: 'Average score', value: `${percentOf(sum.totals.score, sum.totals.max)}%`, sub: `${sum.totals.score} of ${sum.totals.max} points` },
    { label: 'Questions answered', value: sum.answered, sub: `in ${sum.sessions} session${sum.sessions === 1 ? '' : 's'}` },
    { label: 'Items practised', value: sum.practised, sub: `of ${sum.available} case studies and questions` },
    { label: 'To revisit', value: sum.revisit.length, sub: sum.revisit.length ? 'lost points last time' : 'nothing outstanding' }
  ];

  const stepRows = sum.byStep.map(s => s.count ? `
      <tr><th scope="row">${escapeHTML(s.label)}</th>
        <td class="num">${percentOf(s.score, s.max)}%</td>
        <td class="bar">${progressMeter(s.score, s.max, s.label)}</td>
        <td class="num muted">${s.count}</td></tr>` : `
      <tr class="is-empty"><th scope="row">${escapeHTML(s.label)}</th><td class="num">–</td><td class="bar"><span class="meter"></span></td><td class="num muted">0</td></tr>`).join('');

  const unitRows = sum.byUnit.map(u => `
      <tr><th scope="row">${unitLabelHTML(u.course, u.unit)}</th>
        <td class="num">${percentOf(u.score, u.max)}%</td>
        <td class="bar">${progressMeter(u.score, u.max, unitParts(u.unit).num)}</td>
        <td class="num muted">${u.items.size}${u.available ? ` / ${u.available}` : ''}</td></tr>`).join('');

  const revisitRows = sum.revisit.slice(0, 12).map(r => `
      <li class="app-list-row">
        <span class="app-list-main"><strong>${escapeHTML(r.title)}</strong>
          <span class="muted"><span class="kind-tag${r.kind === 'case' ? ' case' : ''}">${r.kind === 'case' ? 'Case study' : 'Stand-alone'}</span> ${escapeHTML(unitParts(r.unit).num)} · ${formatSessionDate(r.at)}</span></span>
        <span class="app-list-score">${percentOf(r.score, r.max)}%</span>
        <button type="button" class="app-btn small" data-practise-item="${escapeHTML(r.item)}">Practise</button>
      </li>`).join('');

  const recentRows = sum.recent.map(s => {
    const t = s.questions.reduce((a, q) => { a.score += q.score; a.max += q.max; return a; }, { score: 0, max: 0 });
    return `
      <li class="app-list-row">
        <span class="app-list-main"><strong>${escapeHTML(s.title || 'Practice session')}</strong>
          <span class="muted">${formatSessionDate(s.at)} · ${s.questions.length} question${s.questions.length === 1 ? '' : 's'} · ${s.mode === 'test' ? 'Test mode' : 'Review mode'}</span></span>
        <span class="app-list-score">${percentOf(t.score, t.max)}%</span>
      </li>`;
  }).join('');

  box.innerHTML = `${privacy}
    <div class="stat-grid">${tiles.map(t => `
      <div class="stat-tile"><span class="stat-label">${t.label}</span><span class="stat-value">${t.value}</span><span class="stat-sub">${t.sub}</span></div>`).join('')}
    </div>

    <div class="app-grid-2">
      <section class="app-card" aria-labelledby="progress-steps-title">
        <h2 id="progress-steps-title" class="app-card-title">By clinical judgment step</h2>
        <p class="app-card-sub">Case study questions only; each case works through the six steps in order.</p>
        <table class="meter-table">
          <thead><tr><th scope="col">Step</th><th scope="col" class="num">Score</th><th scope="col"><span class="visually-hidden">Bar</span></th><th scope="col" class="num">Qs</th></tr></thead>
          <tbody>${stepRows}</tbody>
        </table>
      </section>

      <section class="app-card" aria-labelledby="progress-units-title">
        <h2 id="progress-units-title" class="app-card-title">By unit</h2>
        <p class="app-card-sub">Items practised out of those available in each unit.</p>
        <table class="meter-table">
          <thead><tr><th scope="col">Unit</th><th scope="col" class="num">Score</th><th scope="col"><span class="visually-hidden">Bar</span></th><th scope="col" class="num">Items</th></tr></thead>
          <tbody>${unitRows}</tbody>
        </table>
      </section>
    </div>

    <div class="app-grid-2">
      <section class="app-card" aria-labelledby="progress-revisit-title">
        <div class="app-card-head">
          <div><h2 id="progress-revisit-title" class="app-card-title">To revisit</h2>
          <p class="app-card-sub">Items where you lost points the last time you did them.</p></div>
          ${sum.revisit.length ? '<button type="button" class="app-btn primary small" id="progress-revisit-all-btn">Practise these again</button>' : ''}
        </div>
        ${sum.revisit.length ? `<ul class="app-list">${revisitRows}</ul>${sum.revisit.length > 12 ? `<p class="app-card-sub">and ${sum.revisit.length - 12} more.</p>` : ''}` : '<p class="app-card-sub">Nothing to revisit: you scored full marks on the latest attempt of everything you have practised.</p>'}
      </section>

      <section class="app-card" aria-labelledby="progress-recent-title">
        <h2 id="progress-recent-title" class="app-card-title">Recent sessions</h2>
        <ul class="app-list">${recentRows}</ul>
      </section>
    </div>

    ${dataPanel}`;
}

/* ---- Actions ---- */

function practiseItemsAgain(ids) {
  const items = ids.map(findBankItem).filter(i => i && isReadyForStudents(i));
  const cases = items.filter(i => !i.isStandalone).slice(0, REVISIT_LIMIT.cases);
  const singles = items.filter(i => i.isStandalone).slice(0, REVISIT_LIMIT.standalone);
  if (!cases.length && !singles.length) {
    showToast('These items are no longer available to practise.', 'error');
    return;
  }
  startCompiledSession(cases, singles, 'review');
}

function exportProgress() {
  const data = loadProgress();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `nclex-progress-${new Date().toISOString().slice(0, 10)}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

// Adds the file's sessions to this browser's (sessions already here are not duplicated).
function importProgressFile(file) {
  const reader = new FileReader();
  reader.onload = () => {
    let incoming;
    try {
      incoming = JSON.parse(reader.result);
    } catch (e) {
      incoming = null;
    }
    const valid = incoming && Array.isArray(incoming.sessions) && incoming.sessions.every(s => s && s.id && Array.isArray(s.questions));
    if (!valid) {
      renderProgressView();
      setProgressMessage('That file is not a progress export from this site.');
      return;
    }
    const data = loadProgress();
    const known = new Set(data.sessions.map(s => s.id));
    const added = incoming.sessions.filter(s => !known.has(s.id));
    data.sessions.push(...added);
    const ok = saveProgress(data);
    renderProgressView();
    setProgressMessage(!ok ? 'This browser is not keeping site data, so the import could not be saved.'
      : added.length ? `Imported ${added.length} session${added.length === 1 ? '' : 's'}.` : 'Those sessions are already here.');
  };
  reader.readAsText(file);
}

function setProgressMessage(text) {
  const el = document.getElementById('progress-data-message');
  if (el) el.textContent = text;
}

function initProgressEvents() {
  const view = document.getElementById('progress-view');
  if (!view) return;
  view.addEventListener('click', e => {
    const t = e.target;
    const goto = t.closest('[data-goto]');
    if (goto) { switchView(goto.dataset.goto); return; }
    const one = t.closest('[data-practise-item]');
    if (one) { practiseItemsAgain([one.dataset.practiseItem]); return; }
    if (t.closest('#progress-revisit-all-btn')) {
      practiseItemsAgain(summarizeProgress(loadProgress()).revisit.map(r => r.item));
      return;
    }
    if (t.closest('#progress-export-btn')) { exportProgress(); return; }
    if (t.closest('#progress-import-btn')) { document.getElementById('progress-import-input').click(); return; }
    if (t.closest('#progress-clear-btn')) {
      document.getElementById('progress-clear-confirm').classList.remove('hidden');
      document.getElementById('progress-clear-no').focus();
      return;
    }
    if (t.closest('#progress-clear-no')) { document.getElementById('progress-clear-confirm').classList.add('hidden'); return; }
    if (t.closest('#progress-clear-yes')) {
      try { localStorage.removeItem(PROGRESS_STORAGE_KEY); } catch (err) { /* nothing stored */ }
      renderProgressView();
      setProgressMessage('Your progress was deleted from this browser.');
    }
  });
  view.addEventListener('change', e => {
    if (e.target.id === 'progress-import-input' && e.target.files && e.target.files[0]) {
      importProgressFile(e.target.files[0]);
      e.target.value = '';
    }
  });
}
