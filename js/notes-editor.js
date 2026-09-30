/* Timed-entry editor for chart tabs in the authoring studio.

   Any chart tab without a table or list (Nurses' Notes, History and Physical, reports, orders, vital
   signs or results written as text) is edited as a list of entries, each with a time or date label
   ("0800", "0800 (DOL 2)", "Day 3 0800", "09/14 0800"), an optional title shown in bold on its own
   line above the time and note, and the note text. Tab moves from the label to the text, Enter starts
   the next entry. The entries are stored as the <p class="nurse-note-row"> markup the player already
   shows, each title as a bold paragraph "<p><b>Title</b></p>" just before its entry (the form older
   cases already use, e.g. "Emergency Department" above the first note), so no content changes.
   Tabs holding tables or lists, and any tab the author prefers, use the free-text editor; there T+
   puts a bold title line above the table or paragraph with the cursor. Deleting an entry takes a
   second click. */

const NOTE_LABEL_MAX = 60; // longest label the player keeps as an authored row (isAuthoredNoteRow)

let notesEditorState = null; // { tabId, rows: [{ time, title, html, showTitle }], dirty }
const notesModeChoice = {}; // tab id -> 'rows' | 'free' when the author picked one

function isNotesTabTitle(title) {
  return /nurse|note|log|progress/i.test(title || '');
}

// "<b>Title</b><br>note" -> { title, html: 'note' }; anything else has no title.
function splitNoteTitle(html) {
  const m = (html || '').match(/^\s*<(b|strong)>([^<]*)<\/\1>\s*<br\s*\/?>([\s\S]*)$/i);
  if (!m || !m[2].trim()) return { title: '', html: html || '' };
  const tmp = document.createElement('textarea');
  tmp.innerHTML = m[2];
  return { title: tmp.value.trim(), html: m[3] };
}

function noteRow(time, html, heading) {
  const { title, html: body } = splitNoteTitle(html);
  const t = heading || title;
  return { time, title: t, html: body, showTitle: !!t };
}

// A paragraph holding only bold text ("<p><b>Emergency Department</b></p>") is the title of the entry
// that follows it. Returns the title text, or ''.
function titleParagraphText(node) {
  if (!['p', 'div'].includes(node.tagName.toLowerCase()) || node.classList.contains('nurse-note-row')) return '';
  const kids = Array.from(node.childNodes).filter(n => !(n.nodeType === Node.TEXT_NODE && !n.textContent.trim()) && n.nodeName !== 'BR');
  if (kids.length !== 1 || !/^(B|STRONG)$/.test(kids[0].nodeName) || kids[0].children.length) return '';
  return kids[0].textContent.replace(/\u00a0/g, ' ').trim();
}

// Entries of a chart tab, or null when the content has something rows cannot hold (tables, lists…).
function parseNoteRows(html) {
  const doc = new DOMParser().parseFromString(`<div>${formatNursesNotes(html || '', "Nurses' Notes")}</div>`, 'text/html');
  const rows = [];
  let pendingTitle = '';
  const push = (time, html) => { rows.push(noteRow(time, html, pendingTitle)); pendingTitle = ''; };
  // A title with no entry after it stays a bold line of its own.
  const flushTitle = () => { if (pendingTitle) { rows.push(noteRow('', `<b>${escapeHTML(pendingTitle)}</b>`)); pendingTitle = ''; } };
  for (const node of Array.from(doc.body.firstChild.childNodes)) {
    if (node.nodeType === Node.TEXT_NODE) {
      if (node.textContent.trim()) push('', escapeHTML(node.textContent.trim()));
      continue;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) continue;
    const tag = node.tagName.toLowerCase();
    if (tag === 'br') continue;
    if (node.classList.contains('nurse-note-row')) {
      const time = node.querySelector('.nurse-note-time');
      const text = node.querySelector('.nurse-note-text');
      if (!time || !text) return null;
      push(time.textContent.replace(/ /g, ' ').replace(/:\s*$/, '').trim(), text.innerHTML);
      continue;
    }
    if (tag === 'p' || tag === 'div') {
      if (node.querySelector('table, ul, ol, img, p, div')) return null;
      if (!hasText(node.innerHTML)) continue;
      const title = titleParagraphText(node);
      if (title) { flushTitle(); pendingTitle = title; continue; }
      push('', node.innerHTML);
      continue;
    }
    return null; // table, list, heading, image…
  }
  flushTitle();
  return rows;
}

function serializeNoteRows(rows) {
  return rows
    .filter(r => r.time.trim() || (r.title || '').trim() || hasText(r.html))
    .map(r => {
      const title = (r.title || '').trim();
      const html = r.html.replace(/(<br\s*\/?>\s*)+$/i, '');
      const heading = title ? `<p><b>${escapeHTML(title)}</b></p>` : '';
      const label = r.time.trim().replace(/:\s*$/, '');
      if (!label && !hasText(html)) return heading;
      return heading + (label
        ? `<p class="nurse-note-row"><span class="nurse-note-time">${escapeHTML(label)}:</span><span class="nurse-note-text">${html}</span></p>`
        : `<p>${html}</p>`);
    })
    .join('');
}

/* ---- Showing the right editor for the active tab ---- */

function notesEditorElements() {
  return {
    bar: document.getElementById('notes-mode-bar'),
    rowsBox: document.getElementById('notes-row-editor'),
    free: document.getElementById('tab-text-input'),
    tableBtn: document.querySelector('#tab-content-editor .table-insert-btn')
  };
}

// Called whenever a tab is shown (or its title changes). Picks entries mode for notes tabs whose
// content fits it, unless the author chose free text for this tab.
function notesEditorOpen(tab, preferredMode) {
  const { bar, rowsBox, free, tableBtn } = notesEditorElements();
  if (!bar || !rowsBox || !free) return;
  // Every tab can use timed entries; tabs with tables or lists stay in free text.
  const eligible = !!tab;
  const rows = eligible ? parseNoteRows(free.innerHTML) : null;
  const mode = eligible && rows && preferredMode !== 'free' ? 'rows' : 'free';

  bar.classList.toggle('hidden', !eligible);
  if (eligible) {
    bar.querySelectorAll('[data-notes-mode]').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.notesMode === mode);
      btn.setAttribute('aria-pressed', btn.dataset.notesMode === mode ? 'true' : 'false');
    });
    const rowsBtn = bar.querySelector('[data-notes-mode="rows"]');
    rowsBtn.disabled = !rows;
    rowsBtn.title = rows ? 'One entry per time or date' : 'This tab has a table or list; edit it as free text';
    bar.querySelector('.notes-mode-hint').textContent = mode === 'rows'
      ? 'Tab moves to the note, Enter adds the next entry, Shift+Enter starts a new line in a note. T+ in the toolbar adds a bold title above the current entry.'
      : (rows ? 'Start a line with a time and press Tab (or type "0800:") to make it a timed entry.'
              : 'This tab contains a table or list, so it is edited as free text. T+ in the toolbar adds a bold title above the table or paragraph with the cursor.');
  }

  if (mode === 'rows') {
    notesEditorState = { tabId: tab.id, rows: rows.length ? rows : [noteRow('', '')], dirty: false };
    free.classList.add('hidden');
    rowsBox.classList.remove('hidden');
    if (tableBtn) tableBtn.classList.remove('hidden'); // a table switches the tab to free text (tableInsertTarget)
    noteToolsEntryIndex = 0;
    showNoteTools(true);
    renderNoteRows();
  } else {
    notesEditorState = null;
    showNoteTools('free');
    free.classList.remove('hidden');
    rowsBox.classList.add('hidden');
    rowsBox.innerHTML = '';
    if (tableBtn) tableBtn.classList.remove('hidden');
  }
}

// Writes the entries back into the free-text editor, which saveActiveTabContent reads. Untouched
// entries leave the tab's HTML exactly as it was.
function notesEditorFlush() {
  if (!notesEditorState || !notesEditorState.dirty) return;
  const { free } = notesEditorElements();
  free.innerHTML = serializeNoteRows(notesEditorState.rows);
  notesEditorState.dirty = false;
}

function switchNotesMode(mode) {
  const tab = currentCase && currentCase.screens[currentStepIndex].leftContent.tabs.find(t => t.id === activeTabId);
  if (!tab) return;
  if (mode) notesModeChoice[tab.id] = mode;
  notesEditorFlush();
  const title = document.getElementById('tab-title-input').value;
  notesEditorOpen(Object.assign({}, tab, { title }), mode);
  // In free text, timed entries read as plain "0800: text" lines; saving turns them back into entries.
  const { free } = notesEditorElements();
  if (mode === 'free' && isNotesTabTitle(title)) free.innerHTML = stripNursesNotesFormatting(free.innerHTML);
}

/* ---- The entry list ---- */

function renderNoteRows(focusIndex, focusField) {
  const { rowsBox } = notesEditorElements();
  const state = notesEditorState;
  rowsBox.innerHTML = '';
  state.rows.forEach((row, i) => {
    const el = document.createElement('div');
    el.className = 'note-entry';
    el.innerHTML = `
      <input type="text" class="note-entry-title ${row.showTitle ? '' : 'hidden'}" placeholder="Title (optional), shown in bold above the time and note" aria-label="Title for entry ${i + 1}" value="${escapeHTML(row.title || '')}">
      <input type="text" class="note-entry-time" maxlength="${NOTE_LABEL_MAX}" placeholder="0800" aria-label="Time or date of entry ${i + 1}" value="${escapeHTML(row.time)}">
      <div class="note-entry-body">
        <div class="note-entry-text rich-text-editor" contenteditable="true" role="textbox" aria-multiline="true" aria-label="Note for entry ${i + 1}" placeholder="Note…"></div>
        <p class="note-entry-warn hidden" role="status"></p>
      </div>
      <div class="note-entry-actions">
        <button type="button" class="note-entry-btn danger" data-act="delete" tabindex="-1" title="Delete entry" aria-label="Delete entry ${i + 1}">&times;</button>
      </div>`;
    const timeInput = el.querySelector('.note-entry-time');
    // The time box is only as wide as its label ("0800" is short; "0800 (DOL 2)" grows).
    const fitTime = () => { timeInput.style.width = `${Math.min(18, Math.max(6, timeInput.value.length + 2))}ch`; };
    fitTime();
    timeInput.addEventListener('input', fitTime);
    const titleInput = el.querySelector('.note-entry-title');
    const text = el.querySelector('.note-entry-text');
    text.innerHTML = row.html;
    titleInput.addEventListener('input', () => { row.title = titleInput.value; state.dirty = true; });
    titleInput.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); timeInput.focus(); } });

    timeInput.addEventListener('input', () => { row.time = timeInput.value; state.dirty = true; updateNoteTimeHints(); });
    timeInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') { e.preventDefault(); placeCaretAtEnd(text); }
      else if (e.altKey && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) { e.preventDefault(); moveNoteRow(i, e.key === 'ArrowUp' ? -1 : 1, 'time'); }
    });
    text.addEventListener('input', () => { row.html = text.innerHTML; state.dirty = true; });
    text.addEventListener('keydown', e => {
      if (e.key === 'Enter' && e.shiftKey) {
        e.preventDefault();
        richCommand('insertLineBreak');
      } else if (e.key === 'Enter') {
        e.preventDefault();
        row.html = text.innerHTML;
        state.rows.splice(i + 1, 0, noteRow('', ''));
        state.dirty = true;
        renderNoteRows(i + 1, 'time');
      } else if (e.key === 'Backspace' && !hasText(text.innerHTML) && !row.time.trim() && !(row.title || '').trim() && state.rows.length > 1) {
        e.preventDefault();
        state.rows.splice(i, 1);
        state.dirty = true;
        renderNoteRows(Math.max(0, i - 1), 'text');
      } else if (e.altKey && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) {
        e.preventDefault();
        row.html = text.innerHTML;
        moveNoteRow(i, e.key === 'ArrowUp' ? -1 : 1, 'text');
      }
    });
    el.querySelectorAll('.note-entry-btn').forEach(btn => btn.addEventListener('click', () => {
      row.html = text.innerHTML;
      if (btn.dataset.act === 'title') {
        row.showTitle = !row.showTitle;
        if (!row.showTitle && row.title) { row.title = ''; state.dirty = true; }
        renderNoteRows();
        const input = rowsBox.querySelectorAll('.note-entry')[i].querySelector('.note-entry-title');
        if (row.showTitle) input.focus();
        return;
      }
      if (btn.dataset.act === 'delete') {
        // An entry cannot be brought back once saved, so deleting takes a second click.
        const empty = !row.time.trim() && !(row.title || '').trim() && !hasText(row.html);
        if (!empty && !btn.classList.contains('is-confirming')) {
          rowsBox.querySelectorAll('.note-entry-btn.is-confirming').forEach(resetNoteDeleteButton);
          btn.classList.add('is-confirming');
          btn.textContent = 'Delete?';
          btn.title = 'Click again to delete this entry. An entry deleted on the screen where it first appears is also removed from the later screens.';
          clearTimeout(btn.confirmTimer);
          btn.confirmTimer = setTimeout(() => resetNoteDeleteButton(btn), 3000);
          return;
        }
        state.rows.splice(i, 1);
        if (!state.rows.length) state.rows.push(noteRow('', ''));
        state.dirty = true;
        renderNoteRows(Math.min(i, state.rows.length - 1), 'time');
      } else {
        moveNoteRow(i, btn.dataset.act === 'up' ? -1 : 1, 'time');
      }
    }));
    rowsBox.appendChild(el);
  });

  updateNoteTimeHints();

  const add = document.createElement('button');
  add.type = 'button';
  add.className = 'note-entry-add';
  add.textContent = '+ Add entry';
  add.addEventListener('click', () => {
    state.rows.push(noteRow('', ''));
    state.dirty = true;
    renderNoteRows(state.rows.length - 1, 'time');
  });
  rowsBox.appendChild(add);

  if (typeof focusIndex === 'number') {
    const entry = rowsBox.querySelectorAll('.note-entry')[focusIndex];
    if (entry) {
      if (focusField === 'text') placeCaretAtEnd(entry.querySelector('.note-entry-text'));
      else entry.querySelector('.note-entry-time').focus();
    }
  }
}

function resetNoteDeleteButton(btn) {
  clearTimeout(btn.confirmTimer);
  btn.classList.remove('is-confirming');
  btn.innerHTML = '&times;';
  btn.title = 'Delete entry';
}

function moveNoteRow(i, delta, focusField) {
  const rows = notesEditorState.rows;
  const j = i + delta;
  if (j < 0 || j >= rows.length) return;
  [rows[i], rows[j]] = [rows[j], rows[i]];
  notesEditorState.dirty = true;
  renderNoteRows(j, focusField);
}

function placeCaretAtEnd(el) {
  el.focus();
  const range = document.createRange();
  range.selectNodeContents(el);
  range.collapse(false);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
}

/* ---- Free-text mode: Tab after a time label makes it a timed entry ---- */

// In the free-text editor of a notes tab, a line that so far holds only a time or date label
// ("1430", "0800 (DOL 2)", "Day 3 0800") gets ": " on Tab, which saving turns into a timed entry.
// Anywhere else Tab inserts spaces as before.
function handleFreeTextNotesTab(e) {
  if (e.key !== 'Tab') return;
  e.preventDefault();
  const title = document.getElementById('tab-title-input').value;
  const sel = window.getSelection();
  if (isNotesTabTitle(title) && sel.rangeCount) {
    const range = sel.getRangeAt(0);
    const block = (range.startContainer.nodeType === Node.ELEMENT_NODE ? range.startContainer : range.startContainer.parentElement)
      .closest('p, div:not(.rich-text-editor)');
    const lineText = (block && e.currentTarget.contains(block) ? block.textContent : range.startContainer.textContent || '').replace(/ /g, ' ');
    if (new RegExp(String.raw`^\s*` + NOTE_LABEL_SOURCE + String.raw`\s*$`, 'i').test(lineText)) {
      richCommand('insertText', ': ');
      return;
    }
  }
  richCommand('insertHTML', '&nbsp;&nbsp;&nbsp;&nbsp;');
}

function initNotesEditor() {
  const rowsBox = document.getElementById('notes-row-editor');
  if (rowsBox) {
    rowsBox.addEventListener('paste', handleNoteRowsPaste);
    rowsBox.addEventListener('focusin', e => {
      const entry = e.target.closest('.note-entry');
      if (entry) noteToolsEntryIndex = Array.from(rowsBox.querySelectorAll('.note-entry')).indexOf(entry);
    });
  }
  const bar = document.getElementById('notes-mode-bar');
  if (bar) bar.querySelectorAll('[data-notes-mode]').forEach(btn => btn.addEventListener('click', () => switchNotesMode(btn.dataset.notesMode)));
  const title = document.getElementById('tab-title-input');
  if (title) title.addEventListener('change', () => switchNotesMode(notesModeChoice[activeTabId]));
}

// The Table button in timed-entry mode: a table cannot sit inside one entry, so the tab switches to
// free text (every entry kept) and the cursor goes after the entry that had it (or to the end).
// Returns the free-text editor to insert into.
function tableInsertTarget(editor) {
  if (!editor || !editor.classList.contains('note-entry-text') || !notesEditorState) return editor;
  const entries = Array.from(document.querySelectorAll('#notes-row-editor .note-entry-text'));
  const index = entries.indexOf(editor);
  const kept = notesEditorState.rows.slice(0, index + 1)
    .filter(r => r.time.trim() || (r.title || '').trim() || hasText(r.html)).length;
  notesEditorState.dirty = true;
  switchNotesMode('free');
  const { free } = notesEditorElements();
  free.focus();
  const blocks = Array.from(free.childNodes).filter(n => n.nodeType === Node.ELEMENT_NODE || n.textContent.trim());
  const range = document.createRange();
  const anchor = index >= 0 && kept > 0 ? blocks[kept - 1] : null;
  if (anchor) range.setStartAfter(anchor); else { range.selectNodeContents(free); range.collapse(false); }
  range.collapse(true);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  return free;
}

/* ---- Time checks: an entry earlier than the one above gets a gentle warning ---- */

// "1430" -> { day: null, minutes: 870 }; "Day 3 0800", "0800 (DOL 2)", "POD 2", "09/14 0800" carry a day.
function noteLabelParts(label) {
  const text = (label || '').trim();
  if (!text) return null;
  let day = null;
  const d = text.match(/\b(Day|POD|DOL|Post-?op(?:erative)?\s+day)\s*(\d{1,3})/i);
  const date = text.match(/\b(\d{1,2})\/(\d{1,2})(?:\/(\d{2,4}))?/);
  if (d) day = { kind: d[1].toUpperCase().replace(/\s+/g, ''), n: Number(d[2]) };
  else if (date) day = { kind: 'DATE', n: Number(date[3] || 0) * 10000 + Number(date[1]) * 100 + Number(date[2]) };
  const withoutDate = date ? text.replace(date[0], '') : text;
  const t = withoutDate.match(/\b(\d{2}):?(\d{2})\b(?!\d)/);
  const minutes = t && Number(t[1]) < 24 && Number(t[2]) < 60 ? Number(t[1]) * 60 + Number(t[2]) : null;
  return { day, minutes };
}

// True when entry b is clearly earlier than entry a (same kind of day, or no days at all).
function noteLabelEarlier(a, b) {
  if (!a || !b) return false;
  if (a.day && b.day) {
    if (a.day.kind !== b.day.kind) return false;
    if (b.day.n !== a.day.n) return b.day.n < a.day.n;
  } else if (a.day || b.day) {
    return false;
  }
  return a.minutes != null && b.minutes != null && b.minutes < a.minutes;
}

function updateNoteTimeHints() {
  const state = notesEditorState;
  const { rowsBox } = notesEditorElements();
  if (!state || !rowsBox) return;
  const entries = rowsBox.querySelectorAll('.note-entry');
  let prev = null; // the last entry above with a time
  state.rows.forEach((row, i) => {
    const el = entries[i];
    if (!el) return;
    const warn = el.querySelector('.note-entry-warn');
    const input = el.querySelector('.note-entry-time');
    input.placeholder = prev ? `after ${prev.label}` : '0800';
    const parts = noteLabelParts(row.time);
    const earlier = parts && prev && noteLabelEarlier(prev.parts, parts);
    warn.textContent = earlier
      ? `This is earlier than ${prev.label} above. Entries read top to bottom in time order; if it is the next day, add the day (for example "Day 2 ${row.time.trim()}").`
      : '';
    warn.classList.toggle('hidden', !earlier);
    if (parts) prev = { label: row.time.trim(), parts };
  });
}

/* ---- Paste many entries: "0800 text" lines become one entry each ---- */

function handleNoteRowsPaste(e) {
  const state = notesEditorState;
  const field = e.target.closest && e.target.closest('.note-entry-text, .note-entry-time');
  if (!state || !field) return;
  const text = (e.clipboardData && e.clipboardData.getData('text/plain')) || '';
  const lines = text.split(/\r?\n/).map(l => l.replace(/\u00a0/g, ' ').trim()).filter(Boolean);
  const labelRe = new RegExp('^(' + NOTE_LABEL_SOURCE + ')\\s*(?:[:\\-\u2013\u2014]\\s*|\\s+)(.+)$', 'i');
  if (lines.filter(l => labelRe.test(l)).length < 2) return; // an ordinary paste
  e.preventDefault();
  e.stopPropagation();
  const pasted = [];
  lines.forEach(line => {
    const m = line.match(labelRe);
    if (m) pasted.push(noteRow(m[1].trim(), escapeHTML(m[2].trim())));
    else if (pasted.length) pasted[pasted.length - 1].html += `<br>${escapeHTML(line)}`;
    else pasted.push(noteRow('', escapeHTML(line)));
  });
  const { rowsBox } = notesEditorElements();
  const entries = Array.from(rowsBox.querySelectorAll('.note-entry'));
  const index = entries.indexOf(field.closest('.note-entry'));
  // Keep what was typed in the current entry, then put the pasted entries after it (or in its place if empty).
  const current = state.rows[index];
  if (current) {
    current.html = entries[index].querySelector('.note-entry-text').innerHTML;
    current.time = entries[index].querySelector('.note-entry-time').value;
  }
  const empty = current && !current.time.trim() && !(current.title || '').trim() && !hasText(current.html);
  state.rows.splice(empty ? index : index + 1, empty ? 1 : 0, ...pasted);
  state.dirty = true;
  renderNoteRows((empty ? index : index + 1) + pasted.length - 1, 'text');
  showToast(`Pasted ${pasted.length} entries.`);
}

/* ---- Entry tools in the tab's formatting toolbar: Title, Move up, Move down ----
   They act on the entry that has (or last had) the cursor, so each entry row keeps only its
   delete button and the note gets the width. */

let noteToolsEntryIndex = 0;

function ensureNoteTools() {
  const toolbar = document.querySelector('#tab-content-editor .rich-editor-toolbar');
  if (!toolbar || toolbar.querySelector('.note-tool')) return toolbar;
  const tools = [
    ['title', '<b>T</b>+', 'Title: show or hide a bold title above the note of the current entry'],
    ['up', '&uarr;', 'Move the current entry up (Alt+↑)'],
    ['down', '&darr;', 'Move the current entry down (Alt+↓)']
  ];
  const sep = document.createElement('span');
  sep.className = 'note-tool toolbar-sep';
  const expand = toolbar.querySelector('.toolbar-expand-btn');
  toolbar.insertBefore(sep, expand);
  tools.forEach(([act, html, title]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'toolbar-btn note-tool';
    b.dataset.noteAct = act;
    b.innerHTML = html;
    b.title = title;
    b.setAttribute('aria-label', title.split(':')[0]);
    toolbar.insertBefore(b, expand);
  });
  return toolbar;
}

// show: true (timed entries: T+, ↑, ↓), 'free' (free text: only T+, which adds a title line) or false.
function showNoteTools(show) {
  const toolbar = ensureNoteTools();
  if (!toolbar) return;
  toolbar.querySelectorAll('.note-tool').forEach(el => {
    const visible = show === true || (show === 'free' && (el.dataset.noteAct === 'title' || el.classList.contains('toolbar-sep')));
    el.classList.toggle('hidden', !visible);
  });
  const t = toolbar.querySelector('[data-note-act="title"]');
  if (t) t.title = show === 'free'
    ? 'Title: add a bold title line above the table or paragraph with the cursor'
    : 'Title: show or hide a bold title above the time and note of the current entry';
}

// Free text (tabs with tables): puts "<p><b>Title</b></p>" above the top-level block with the cursor
// (or above the first table) and selects the word so typing replaces it.
let freeTextLastRange = null;
document.addEventListener('selectionchange', () => {
  const free = document.getElementById('tab-text-input');
  const sel = window.getSelection();
  if (free && sel.rangeCount && free.contains(sel.getRangeAt(0).startContainer)) freeTextLastRange = sel.getRangeAt(0).cloneRange();
});

function insertFreeTextTitle() {
  const free = document.getElementById('tab-text-input');
  if (!free) return;
  let block = null;
  if (freeTextLastRange && free.contains(freeTextLastRange.startContainer)) {
    block = freeTextLastRange.startContainer;
    while (block && block.parentNode !== free) block = block.parentNode;
  }
  if (!block) block = Array.from(free.children).find(el => el.matches('table') || el.querySelector('table')) || free.firstChild;
  const p = document.createElement('p');
  const b = document.createElement('b');
  b.textContent = 'Title';
  p.appendChild(b);
  free.insertBefore(p, block && block.parentNode === free ? block : free.firstChild);
  free.focus();
  const range = document.createRange();
  range.selectNodeContents(b);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  free.dispatchEvent(new Event('input', { bubbles: true }));
}

function noteToolbarAction(act) {
  if (!notesEditorState) { if (act === 'title') insertFreeTextTitle(); return; }
  const state = notesEditorState;
  const { rowsBox } = notesEditorElements();
  if (!state || !rowsBox) return;
  const entries = rowsBox.querySelectorAll('.note-entry');
  const i = Math.min(noteToolsEntryIndex, state.rows.length - 1);
  const row = state.rows[i];
  if (!row || !entries[i]) return;
  row.html = entries[i].querySelector('.note-entry-text').innerHTML;
  if (act === 'title') {
    row.showTitle = !row.showTitle;
    if (!row.showTitle && row.title) { row.title = ''; state.dirty = true; }
    renderNoteRows();
    const entry = rowsBox.querySelectorAll('.note-entry')[i];
    if (row.showTitle) entry.querySelector('.note-entry-title').focus();
    else placeCaretAtEnd(entry.querySelector('.note-entry-text'));
  } else {
    moveNoteRow(i, act === 'up' ? -1 : 1, 'text');
    noteToolsEntryIndex = Math.max(0, Math.min(state.rows.length - 1, i + (act === 'up' ? -1 : 1)));
  }
}
