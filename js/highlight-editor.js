/* Authoring for Highlight Text/Table questions (`highlight`, `highlight_2`).

   The passage is stored as HTML with the highlightable phrases written as {phrase|correct} (a
   correct answer) or {phrase} (a distractor). In the editor the braces are never typed or shown:
   phrases are marked by selecting text (or clicking in a table cell) and choosing Correct answer /
   Distractor / Unmark, and appear as coloured <mark class="hl-mark"> elements that are turned back
   into braces on save. A `highlight` question is edited in the left column (where students see it);
   a `highlight_2` passage sits in the question designer and can be copied from a chart tab.
   Opening and saving without changes keeps the stored content exactly as it was. */

const HL_PHRASE_RE = /\{([^{|]+)(?:\|([^{}]+))?\}/g;

let highlightEditorState = null; // { q, tabId, loadedHTML, originalContent }
const highlightAutoLimit = new WeakSet(); // questions whose limit follows the number of correct phrases (not saved)

// Stored passage -> editor HTML: Nurses' Notes laid out as timed entries, phrases as marks.
function highlightToEditorHTML(content, title) {
  const tpl = document.createElement('template');
  tpl.innerHTML = formatNursesNotes(content || '', title || '');
  const walk = node => {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent;
      if (!text.includes('{')) return;
      HL_PHRASE_RE.lastIndex = 0;
      const frag = document.createDocumentFragment();
      let last = 0, m, hit = false;
      while ((m = HL_PHRASE_RE.exec(text))) {
        hit = true;
        if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)));
        const mark = document.createElement('mark');
        mark.className = `hl-mark ${m[2] === 'correct' ? 'hl-correct' : 'hl-option'}`;
        mark.textContent = m[1];
        frag.appendChild(mark);
        last = HL_PHRASE_RE.lastIndex;
      }
      if (!hit) return;
      if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
      node.replaceWith(frag);
    } else {
      Array.from(node.childNodes).forEach(walk);
    }
  };
  walk(tpl.content);
  return tpl.innerHTML;
}

// Editor HTML -> stored passage: marks become {phrase|correct} / {phrase}.
function highlightFromEditorHTML(html) {
  const tpl = document.createElement('template');
  tpl.innerHTML = html || '';
  tpl.content.querySelectorAll('mark.hl-mark').forEach(mark => {
    const text = mark.textContent.replace(/[{}|]/g, '').replace(/\s+/g, ' ').trim();
    if (!text) { mark.remove(); return; }
    mark.replaceWith(document.createTextNode(`{${text}${mark.classList.contains('hl-correct') ? '|correct' : ''}}`));
  });
  return tpl.innerHTML;
}

function highlightPassageEl() {
  return document.getElementById('highlight-tab-text-input');
}

// Writes the passage being edited (and the other settings) back into the question.
function highlightEditorFlush(q) {
  const st = highlightEditorState;
  const el = highlightPassageEl();
  if (!st || !el || st.q !== q || !q.highlightTabs) return;
  const tab = q.highlightTabs.find(t => t.id === st.tabId);
  if (!tab) return;
  const titleEl = document.getElementById('highlight-tab-title-input');
  if (titleEl) tab.title = titleEl.value;
  const now = highlightFromEditorHTML(el.innerHTML);
  tab.content = now === st.loadedHTML ? st.originalContent : now;
  applyHighlightLimit(q);
}

// "Students select": the same number as the correct phrases (kept in step), no limit, or a number.
function highlightLimitMode(q) {
  const correct = highlightPhrases(q).filter(p => p.correct).length;
  const max = q.maxCorrectSelections;
  if (max === undefined || max === null || max === '') return highlightAutoLimit.has(q) ? 'auto' : 'none';
  return Number(max) === correct ? 'auto' : 'custom';
}

function applyHighlightLimit(q) {
  const mode = document.getElementById('highlight-limit-mode');
  const input = document.getElementById('highlight-max-correct-input');
  if (!mode) return;
  const correct = highlightPhrases(q).filter(p => p.correct).length;
  if (mode.value === 'auto') q.maxCorrectSelections = correct || null;
  else if (mode.value === 'custom') q.maxCorrectSelections = parseInt(input.value, 10) || null;
  else if (q.maxCorrectSelections !== undefined) q.maxCorrectSelections = null;
}

// Problems worth fixing, for the line under the passage and the preview checklist.
function highlightWarnings(q) {
  const phrases = highlightPhrases(q);
  const correct = phrases.filter(p => p.correct).length;
  const list = [];
  if (!phrases.length) list.push('Nothing is marked yet: select words in the passage and mark them.');
  else if (!correct) list.push('No phrase is marked as a correct answer.');
  else if (correct === phrases.length && phrases.length > 1) list.push('Every phrase is a correct answer; add distractors so students have to choose.');
  const stray = (q.highlightTabs || []).some(t => /[{}]/.test((t.content || '').replace(HL_PHRASE_RE, '').replace(/<[^>]*>/g, '')));
  if (stray) list.push('The passage has a stray { or } that is not part of a marked phrase; remove it.');
  const max = Number(q.maxCorrectSelections);
  if (max && correct && max < correct) list.push(`Students may select only ${max}, but ${correct} phrases are correct.`);
  return list;
}

function renderHighlightSummary(q) {
  const box = document.getElementById('highlight-summary');
  if (!box) return;
  const phrases = highlightPhrases(q);
  const correct = phrases.filter(p => p.correct).length;
  const warnings = highlightWarnings(q);
  box.innerHTML = `<div class="hl-counts"><span class="hl-count"><strong>${phrases.length}</strong> highlightable phrase${phrases.length === 1 ? '' : 's'}</span>`
    + `<span class="hl-count hl-count-correct"><strong>${correct}</strong> correct</span>`
    + `<span class="hl-count hl-count-option"><strong>${phrases.length - correct}</strong> distractor${phrases.length - correct === 1 ? '' : 's'}</span></div>`
    + warnings.map(w => `<p class="hl-warning">${escapeHTML(w)}</p>`).join('');
  const auto = document.querySelector('#highlight-limit-mode option[value="auto"]');
  if (auto) auto.textContent = `Same as the correct phrases (${correct})`;
}

function highlightNotice(text) {
  const box = document.getElementById('highlight-mark-notice');
  if (!box) return;
  box.textContent = text;
  box.classList.toggle('hidden', !text);
}

/* ---- Marking ---- */

const HL_BLOCK_SELECTOR = 'p, div, li, ul, ol, table, tbody, thead, tr, td, th, br';

function highlightMarkAt(node) {
  const el = node && (node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement);
  return el ? el.closest('mark.hl-mark') : null;
}

function setMarkKind(mark, kind) {
  if (kind === 'none') { mark.replaceWith(...mark.childNodes); return; }
  mark.classList.toggle('hl-correct', kind === 'correct');
  mark.classList.toggle('hl-option', kind !== 'correct');
}

function newMark(kind, text) {
  const mark = document.createElement('mark');
  mark.className = `hl-mark ${kind === 'correct' ? 'hl-correct' : 'hl-option'}`;
  mark.textContent = text;
  return mark;
}

// kind: 'correct', 'option' (distractor) or 'none' (unmark).
function markHighlightSelection(kind) {
  const el = highlightPassageEl();
  const sel = window.getSelection();
  if (!el || !sel.rangeCount || !el.contains(sel.getRangeAt(0).commonAncestorContainer)) {
    highlightNotice('Click in the passage first: select the words students should be able to highlight.');
    return;
  }
  highlightNotice('');
  const range = sel.getRangeAt(0);
  const inMark = highlightMarkAt(range.startContainer);

  if (range.collapsed) {
    if (inMark) { setMarkKind(inMark, kind); return highlightEdited(); }
    const cell = (range.startContainer.nodeType === Node.ELEMENT_NODE ? range.startContainer : range.startContainer.parentElement).closest('td, th');
    if (cell && el.contains(cell)) {
      // A click in a table cell marks the whole cell.
      if (kind === 'none') { cell.querySelectorAll('mark.hl-mark').forEach(m => m.replaceWith(...m.childNodes)); return highlightEdited(); }
      const text = cell.innerText.replace(/\s+/g, ' ').trim();
      if (!text) return highlightNotice('This cell is empty.');
      cell.textContent = '';
      cell.appendChild(newMark(kind, text));
      return highlightEdited();
    }
    return highlightNotice(kind === 'none' ? 'Click inside a marked phrase to unmark it.' : 'Select the words to mark (or click in a table cell to mark the whole cell).');
  }

  // Unmark every phrase the selection touches.
  if (kind === 'none') {
    Array.from(el.querySelectorAll('mark.hl-mark')).filter(m => range.intersectsNode(m)).forEach(m => m.replaceWith(...m.childNodes));
    return highlightEdited();
  }

  // Selecting inside one marked phrase changes that phrase.
  if (inMark && inMark === highlightMarkAt(range.endContainer)) { setMarkKind(inMark, kind); return highlightEdited(); }

  const fragment = range.cloneContents();
  if (fragment.querySelector(HL_BLOCK_SELECTOR)) {
    return highlightNotice('A phrase has to stay within one line or one table cell. Select less, or mark each part separately.');
  }
  // Trim spaces at either end so the mark covers only the words.
  const raw = range.toString();
  const text = raw.replace(/\s+/g, ' ').trim();
  if (!text) return;
  const lead = raw.match(/^\s*/)[0], trail = raw.match(/\s*$/)[0];
  range.deleteContents();
  const frag = document.createDocumentFragment();
  if (lead) frag.appendChild(document.createTextNode(' '));
  const mark = newMark(kind, text);
  frag.appendChild(mark);
  if (trail) frag.appendChild(document.createTextNode(' '));
  range.insertNode(frag);
  // Marks the selection overlapped are merged into the new one.
  el.querySelectorAll('mark.hl-mark mark.hl-mark').forEach(m => m.replaceWith(...m.childNodes));
  sel.removeAllRanges();
  const after = document.createRange();
  after.setStartAfter(mark);
  after.collapse(true);
  sel.addRange(after);
  highlightEdited();
}

function highlightEdited() {
  const q = highlightEditorState && highlightEditorState.q;
  if (!q) return;
  highlightEditorFlush(q);
  renderHighlightSummary(q);
  updateHighlightMarkButtons();
  const el = highlightPassageEl();
  if (el) el.dispatchEvent(new Event('input', { bubbles: true })); // unsaved-changes marker, preview
}

// The mark buttons show the kind of the phrase the cursor is in.
function updateHighlightMarkButtons() {
  const bar = document.getElementById('highlight-mark-bar');
  const el = highlightPassageEl();
  if (!bar || !el) return;
  const sel = window.getSelection();
  const mark = sel.rangeCount && el.contains(sel.anchorNode) ? highlightMarkAt(sel.anchorNode) : null;
  const kind = mark ? (mark.classList.contains('hl-correct') ? 'correct' : 'option') : '';
  bar.querySelectorAll('[data-hl-mark]').forEach(b => b.classList.toggle('active', b.dataset.hlMark === kind));
}

/* ---- The configurator ---- */

function renderHighlightConfigurator(q, box) {
  if (!q.highlightTabs || !q.highlightTabs.length) {
    q.highlightTabs = [{ id: 'ht_' + Date.now(), title: "Nurses' Notes", content: q.highlightText || '' }];
  }
  if (!highlightActiveTabId || !q.highlightTabs.find(t => t.id === highlightActiveTabId)) highlightActiveTabId = q.highlightTabs[0].id;
  const activeTab = q.highlightTabs.find(t => t.id === highlightActiveTabId);
  if (!highlightPhrases(q).length && q.maxCorrectSelections == null) highlightAutoLimit.add(q); // new question: limit follows the key

  // `highlight`: the passage is edited in the left column, where students see it.
  const leftHost = document.getElementById('highlight-passage-host');
  if (leftHost) leftHost.innerHTML = '';
  let host = box;
  if (q.type === 'highlight' && leftHost) {
    host = leftHost;
    box.insertAdjacentHTML('beforeend', `<div class="hl-where-note">The passage for this question is on the left, where students see it. Select words there and mark them as correct answers or distractors.</div>`);
  }

  const step = currentCase && currentCase.screens[currentStepIndex];
  const chartTabs = (step && step.leftContent && step.leftContent.tabs) || [];
  const mode = highlightLimitMode(q);

  const wrapper = document.createElement('div');
  wrapper.className = 'highlight-tabs-editor-container';
  wrapper.innerHTML = `
    <div class="tabs-editor-header">
      <h5>Passage students highlight</h5>
      <div class="hl-header-actions">
        ${chartTabs.length ? `<select id="highlight-copy-select" class="hl-copy-select" aria-label="Copy a chart tab into the passage">
          <option value="">Copy from a chart tab…</option>
          ${chartTabs.map(t => `<option value="${escapeHTML(t.id)}">${escapeHTML(t.title)}</option>`).join('')}
        </select>` : ''}
        <button id="add-highlight-tab-btn" type="button" class="btn btn-text btn-xs">+ Add tab</button>
      </div>
    </div>
    <div id="highlight-editor-tabs-list" class="tabs-list-horizontal">
      ${q.highlightTabs.map(t => `<div class="tab-editor-item ${t.id === highlightActiveTabId ? 'active' : ''}" data-id="${escapeHTML(t.id)}"><span>${escapeHTML(t.title)}</span></div>`).join('')}
    </div>
    <div class="tab-content-editor-box">
      <input type="text" id="highlight-tab-title-input" class="tab-title-rename" placeholder="Tab title" aria-label="Tab title" value="${escapeHTML(activeTab.title)}">
      <div id="highlight-mark-bar" class="hl-mark-bar" role="toolbar" aria-label="Mark phrases">
        <span class="hl-mark-label">Mark the selection as</span>
        <button type="button" data-hl-mark="correct" class="hl-mark-btn hl-mark-btn-correct" title="Students should highlight this">&#10003; Correct answer</button>
        <button type="button" data-hl-mark="option" class="hl-mark-btn hl-mark-btn-option" title="Highlightable, but not a correct answer">Distractor</button>
        <button type="button" data-hl-mark="none" class="hl-mark-btn" title="Not highlightable">Unmark</button>
        <span class="hl-mark-hint">Select words, or click in a table cell to mark the whole cell. Click a marked phrase to change it.</span>
      </div>
      <div id="highlight-mark-notice" class="hl-mark-notice hidden" role="status"></div>
      <div class="rich-editor-container">
        <div class="rich-editor-toolbar">
          <button type="button" class="toolbar-btn" data-cmd="bold" title="Bold"><b>B</b></button>
          <button type="button" class="toolbar-btn" data-cmd="superscript" title="Superscript">x<sup>2</sup></button>
          <button type="button" class="toolbar-btn" data-cmd="subscript" title="Subscript">x<sub>2</sub></button>
          <button type="button" class="toolbar-btn btn-symbol" data-symbol="&deg;" title="Degree Symbol">&deg;</button>
          <button type="button" class="toolbar-btn btn-symbol" data-symbol="&ge;" title="Greater Than or Equal to">&ge;</button>
          <button type="button" class="toolbar-btn btn-symbol" data-symbol="&le;" title="Less Than or Equal to">&le;</button>
          <button type="button" class="toolbar-btn" data-cmd="insertUnorderedList" title="Bullet List">&bull; List</button>
          <button type="button" class="toolbar-btn" data-cmd="insertOrderedList" title="Numbered List">1. List</button>
          <button type="button" class="toolbar-btn table-insert-btn" title="Insert Table">
            <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" style="vertical-align: middle;"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>
            Table
          </button>
        </div>
        <div contenteditable="true" class="rich-text-editor hl-passage" id="highlight-tab-text-input" placeholder="Paste or type the chart text or table here, or copy it from a chart tab above."></div>
      </div>
      <div id="highlight-summary" class="hl-summary" aria-live="polite"></div>
      <div class="hl-footer">
        <button id="delete-highlight-tab-btn" type="button" class="btn btn-danger btn-xs">Delete this tab</button>
        <label class="hl-limit">Students may select
          <select id="highlight-limit-mode">
            <option value="auto">Same as the correct phrases</option>
            <option value="none">No limit</option>
            <option value="custom">A set number</option>
          </select>
          <input type="number" id="highlight-max-correct-input" min="1" aria-label="Number students may select" value="${mode === 'custom' ? escapeHTML(String(q.maxCorrectSelections)) : ''}" class="${mode === 'custom' ? '' : 'hidden'}">
        </label>
      </div>
    </div>`;
  host.appendChild(wrapper);

  const el = highlightPassageEl();
  el.innerHTML = highlightToEditorHTML(activeTab.content, activeTab.title);
  highlightEditorState = { q, tabId: activeTab.id, loadedHTML: highlightFromEditorHTML(el.innerHTML), originalContent: activeTab.content || '' };
  document.getElementById('highlight-limit-mode').value = mode;
  renderHighlightSummary(q);

  const switchTo = id => { highlightEditorFlush(q); highlightActiveTabId = id; renderDynamicQuestionConfigurator(q); };

  document.getElementById('highlight-tab-title-input').addEventListener('input', e => {
    const head = wrapper.querySelector(`.tab-editor-item[data-id="${CSS.escape(activeTab.id)}"] span`);
    if (head) head.textContent = e.target.value;
  });
  wrapper.querySelectorAll('#highlight-editor-tabs-list .tab-editor-item').forEach(item => item.addEventListener('click', () => switchTo(item.dataset.id)));

  document.getElementById('add-highlight-tab-btn').addEventListener('click', () => {
    highlightEditorFlush(q);
    const id = 'ht_' + Date.now();
    q.highlightTabs.push({ id, title: 'New Tab', content: '' });
    switchTo(id);
  });

  const copySelect = document.getElementById('highlight-copy-select');
  if (copySelect) copySelect.addEventListener('change', () => {
    const src = chartTabs.find(t => t.id === copySelect.value);
    if (!src) return;
    highlightEditorFlush(q);
    const current = q.highlightTabs.find(t => t.id === highlightActiveTabId);
    const empty = !current.content || !current.content.replace(/<[^>]*>|&nbsp;/g, '').trim();
    let target = current.id;
    if (empty) { current.title = src.title; current.content = src.content; }
    else {
      target = 'ht_' + Date.now();
      q.highlightTabs.push({ id: target, title: src.title, content: src.content });
    }
    highlightEditorState = null; // already flushed: don't write the old editor over the copy
    highlightActiveTabId = target;
    renderDynamicQuestionConfigurator(q);
    highlightEdited();
    showToast(`Copied "${src.title}" into the passage. Now mark the phrases.`);
  });

  const delBtn = document.getElementById('delete-highlight-tab-btn');
  delBtn.addEventListener('click', () => {
    if (q.highlightTabs.length <= 1) return highlightNotice('The passage needs at least one tab.');
    if (!delBtn.classList.contains('is-confirming')) {
      delBtn.classList.add('is-confirming');
      delBtn.textContent = 'Click again to delete this tab';
      setTimeout(() => { delBtn.classList.remove('is-confirming'); delBtn.textContent = 'Delete this tab'; }, 4000);
      return;
    }
    q.highlightTabs = q.highlightTabs.filter(t => t.id !== highlightActiveTabId);
    highlightEditorState = null;
    highlightActiveTabId = q.highlightTabs[0].id;
    renderDynamicQuestionConfigurator(q);
    renderHighlightSummary(q);
  });

  const bar = document.getElementById('highlight-mark-bar');
  bar.addEventListener('mousedown', e => { if (e.target.closest('[data-hl-mark]')) e.preventDefault(); }); // keep the selection
  bar.addEventListener('click', e => { const b = e.target.closest('[data-hl-mark]'); if (b) markHighlightSelection(b.dataset.hlMark); });

  let timer = null;
  el.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(() => { highlightEditorFlush(q); renderHighlightSummary(q); }, 250); });
  el.addEventListener('click', updateHighlightMarkButtons);
  el.addEventListener('keyup', updateHighlightMarkButtons);

  const modeSel = document.getElementById('highlight-limit-mode');
  const maxInput = document.getElementById('highlight-max-correct-input');
  modeSel.addEventListener('change', () => {
    maxInput.classList.toggle('hidden', modeSel.value !== 'custom');
    if (modeSel.value === 'custom' && !maxInput.value) maxInput.value = highlightPhrases(q).filter(p => p.correct).length || 1;
    if (modeSel.value === 'auto') highlightAutoLimit.add(q); else highlightAutoLimit.delete(q);
    applyHighlightLimit(q);
    renderHighlightSummary(q);
  });
  maxInput.addEventListener('input', () => { applyHighlightLimit(q); renderHighlightSummary(q); });
}
