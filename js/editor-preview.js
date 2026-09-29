/* Live preview in the authoring editor.

   The panel holds the real player in an iframe (index.html?preview=1), so the screen looks exactly as
   students will see it and the editor's own state is never touched. The editor sends the item with the
   current screen's unsaved edits; "With answers" fills in the answer key and submits it, which shows
   the score, the answer markers and the rationale. A checklist above the preview lists what still keeps
   the screen from students and content conventions worth fixing. */

const PREVIEW_WIDTH = 820; // the player renders at this width (its desktop layout) and is scaled to fit

let previewMode = 'student';
let previewTimer = null;
let previewFrameReady = false;

/* ---- Editor side ---- */

function isPreviewOpen() {
  const panel = document.getElementById('editor-preview-panel');
  return !!panel && !panel.classList.contains('hidden');
}

function togglePreview(force) {
  const panel = document.getElementById('editor-preview-panel');
  const view = document.getElementById('editor-view');
  const btn = document.getElementById('editor-preview-btn');
  const open = typeof force === 'boolean' ? force : !isPreviewOpen();
  panel.classList.toggle('hidden', !open);
  view.classList.toggle('with-preview', open);
  if (btn) btn.setAttribute('aria-pressed', open ? 'true' : 'false');
  if (!open) return;
  const frame = document.getElementById('editor-preview-frame');
  if (!frame.dataset.loaded) {
    frame.dataset.loaded = '1';
    previewFrameReady = false;
    frame.src = `${window.location.pathname}?preview=1`;
  }
  fitPreviewFrame();
  schedulePreviewUpdate(0);
}

function fitPreviewFrame() {
  const body = document.getElementById('editor-preview-body');
  const frame = document.getElementById('editor-preview-frame');
  if (!body || !frame || !isPreviewOpen()) return;
  const scale = Math.min(1, body.clientWidth / PREVIEW_WIDTH);
  frame.style.width = `${PREVIEW_WIDTH}px`;
  frame.style.height = `${body.clientHeight / scale}px`;
  frame.style.transform = `scale(${scale})`;
}

// The item as it would be saved now: the current screen's text boxes and chart tab are read from the
// page without touching them (saving would move the cursor while the author types).
function buildPreviewItem() {
  const item = JSON.parse(JSON.stringify(currentCase));
  const step = item.screens[currentStepIndex];
  if (!step) return item;
  const html = id => { const el = document.getElementById(id); return el ? el.innerHTML : ''; };
  step.leftContent.intro = html('step-intro-input');
  step.question.preamble = html('question-preamble-input');
  step.question.stem = html('question-stem-input');
  step.question.explanation = html('question-explanation-input');
  const tab = step.leftContent.tabs.find(t => t.id === activeTabId);
  if (tab) {
    tab.title = document.getElementById('tab-title-input').value;
    const raw = notesEditorState && notesEditorState.dirty ? serializeNoteRows(notesEditorState.rows) : html('tab-text-input');
    tab.content = formatNursesNotes(raw, tab.title);
  }
  if ((step.question.type === 'highlight' || step.question.type === 'highlight_2') && step.question.highlightTabs) {
    const hTab = step.question.highlightTabs.find(t => t.id === highlightActiveTabId);
    const el = document.getElementById('highlight-tab-text-input');
    if (hTab && el) hTab.content = highlightFromEditorHTML(el.innerHTML);
  }
  return item;
}

function schedulePreviewUpdate(delay = 500) {
  if (!isPreviewOpen()) return;
  clearTimeout(previewTimer);
  previewTimer = setTimeout(sendPreview, delay);
}

function sendPreview() {
  if (!isPreviewOpen() || !currentCase) return;
  const item = buildPreviewItem();
  renderPreviewChecks(item);
  const label = document.getElementById('preview-screen-label');
  if (label) label.textContent = item.isStandalone ? '' : `Screen ${currentStepIndex + 1} of ${item.screens.length}`;
  const frame = document.getElementById('editor-preview-frame');
  if (previewFrameReady && frame.contentWindow) {
    frame.contentWindow.postMessage({ nclexPreview: true, item, step: currentStepIndex, mode: previewMode }, window.location.origin);
  }
}

// What still keeps this screen from students, and content conventions worth fixing.
function previewChecks(item) {
  const step = item.screens[currentStepIndex];
  const q = step.question || {};
  const list = [];
  const problem = screenProblem(q);
  if (problem) list.push({ level: 'block', text: `Hidden from students: ${problem}.` });
  if (item.draft === true) list.push({ level: 'block', text: 'Marked as a draft (hidden from students).' });
  const options = q.options || [];
  if (['select_all', 'trend', 'multiple_choice', 'select_n'].includes(q.type) && options.length > 1 && options[0].correct) {
    list.push({ level: 'warn', text: 'Option 1 is a correct answer. Shuffle the options (and relabel any "(Option N)" in the rationale).' });
  }
  const dropdowns = (q.cloze && q.cloze.dropdowns) || [];
  dropdowns.forEach((dd, i) => {
    const opts = (dd && dd.options) || [];
    if (opts.length > 1 && opts[0].correct) list.push({ level: 'warn', text: `Drop-down ${i + 1}: the correct choice is listed first.` });
  });
  if (!hasText(q.explanation)) list.push({ level: 'warn', text: 'No rationale yet; students see "No explanation rationale provided."' });
  const tabs = step.leftContent.tabs || [];
  if (q.type !== 'highlight' && tabs.length && tabs.every(t => !hasText(t.content))) list.push({ level: 'warn', text: 'The chart tabs are empty.' });
  if (q.type === 'highlight' || q.type === 'highlight_2') highlightWarnings(q).forEach(w => list.push({ level: 'warn', text: w }));
  const otherProblems = item.screens.filter((s, i) => i !== currentStepIndex && screenProblem(s.question)).length;
  if (otherProblems) list.push({ level: 'info', text: `${otherProblems} other screen${otherProblems === 1 ? '' : 's'} still need work before students can see this ${item.isStandalone ? 'question' : 'case'}.` });
  return list;
}

function renderPreviewChecks(item) {
  const box = document.getElementById('preview-checks');
  if (!box) return;
  const list = previewChecks(item);
  const blocking = list.some(c => c.level === 'block');
  const head = blocking ? '' : `<li class="preview-check ok">&#10003; This screen is ready for students.</li>`;
  box.innerHTML = head + list.map(c => `<li class="preview-check ${c.level}">${c.level === 'block' ? '&#9888;' : c.level === 'warn' ? '!' : 'i'} ${escapeHTML(c.text)}</li>`).join('');
}

function initEditorPreview() {
  const btn = document.getElementById('editor-preview-btn');
  if (!btn) return;
  btn.addEventListener('click', () => togglePreview());
  document.getElementById('editor-preview-close').addEventListener('click', () => togglePreview(false));
  document.querySelectorAll('[data-preview-mode]').forEach(b => b.addEventListener('click', () => {
    previewMode = b.dataset.previewMode;
    document.querySelectorAll('[data-preview-mode]').forEach(x => {
      x.classList.toggle('active', x === b);
      x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
    });
    schedulePreviewUpdate(0);
  }));
  // Any edit in the editor refreshes the preview shortly after typing stops.
  const view = document.getElementById('editor-view');
  ['input', 'change'].forEach(type => view.addEventListener(type, e => {
    if (!e.target.closest('#editor-preview-panel')) schedulePreviewUpdate();
  }));
  view.addEventListener('click', e => {
    if (e.target.closest('button') && !e.target.closest('#editor-preview-panel')) schedulePreviewUpdate(300);
  });
  window.addEventListener('resize', fitPreviewFrame);
  window.addEventListener('message', e => {
    if (e.origin !== window.location.origin || !e.data || !e.data.nclexPreviewReady) return;
    previewFrameReady = true;
    schedulePreviewUpdate(0);
  });
}

/* ---- Inside the preview frame ---- */

// The answer key in the player's answer format, per question type (as in tools/check.js).
function previewAnswerKey(q) {
  const a = {};
  switch (q.type) {
    case 'select_all': case 'trend': case 'multiple_choice': case 'select_n':
      (q.options || []).forEach((o, i) => { if (o.correct) a[i] = true; }); break;
    case 'matrix_mc':
      ((q.matrix || {}).rows || []).forEach((r, i) => { a[i] = r.correctIndex; }); break;
    case 'matrix_mr':
      ((q.matrix || {}).rows || []).forEach((r, i) => { a[i] = [...(r.correctIndices || [])]; }); break;
    case 'dropdown_cloze': case 'dyad': case 'triad':
      ((q.cloze || {}).dropdowns || []).forEach((d, i) => { a[i] = ((d && d.options) || []).findIndex(o => o.correct); }); break;
    case 'drag_drop_cloze':
      ((q.cloze || {}).dropdowns || []).forEach((d, i) => { const o = ((d && d.options) || []).find(x => x.correct); if (o) a[i] = o.text; }); break;
    case 'ordered_response':
      a.order = [...(q.orderedOptions || [])]; break;
    case 'highlight': case 'highlight_2':
      highlightPhrases(q).forEach((h, i) => { if (h.correct) a[i] = true; }); break;
    case 'bowtie': {
      const pick = list => (list || []).filter(x => x.correct).map(x => x.text);
      const [a0, a1] = pick(q.bowtieActions), [p0, p1] = pick(q.bowtieParams);
      Object.assign(a, { action0: a0, action1: a1, condition: pick(q.bowtieConditions)[0], param0: p0, param1: p1 });
      break;
    }
    case 'fill_blank':
      a.value = q.correctAnswer || ''; break;
  }
  return a;
}

function initPreviewFrame() {
  document.body.classList.add('preview-frame');
  initPlayerEvents();
  initCalculator();
  makeCalculatorDraggable();
  window.addEventListener('message', e => {
    if (e.origin !== window.location.origin || !e.data || !e.data.nclexPreview) return;
    const { item, step, mode } = e.data;
    const keepTab = playerActiveTabId;
    startPlayer(item, { mode: 'review', isRemediation: false, allowBacktrack: true, source: 'studio' });
    playerActiveTabId = keepTab; // stay on the chart tab the author was looking at
    if (mode === 'key') {
      playerAnswers[step] = previewAnswerKey(item.screens[step].question || {});
      submittedAnswers[step] = true;
      evaluateStepScore(step);
    }
    renderPlayerStep(step);
  });
  window.parent.postMessage({ nclexPreviewReady: true }, window.location.origin);
}
