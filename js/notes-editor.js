/* Timed-entry editor for chart tabs in the authoring studio.

   Any chart tab without a table or list (Nurses' Notes, History and Physical, reports, orders, vital
   signs or results written as text) is edited as a list of entries, each with a time or date label
   ("0800", "0800 (DOL 2)", "Day 3 0800", "09/14 0800"), an optional title shown in bold above the
   note, and the note text. Tab moves from the label to the text, Enter starts the next entry. The
   entries are stored as the <p class="nurse-note-row"> markup the player already shows (the title as
   "<b>Title</b><br>" at the start of the note), so no content changes. Tabs holding tables or lists,
   and any tab the author prefers, use the free-text editor. */

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

function noteRow(time, html) {
  const { title, html: body } = splitNoteTitle(html);
  return { time, title, html: body, showTitle: !!title };
}

// Entries of a chart tab, or null when the content has something rows cannot hold (tables, lists…).
function parseNoteRows(html) {
  const doc = new DOMParser().parseFromString(`<div>${formatNursesNotes(html || '', "Nurses' Notes")}</div>`, 'text/html');
  const rows = [];
  for (const node of Array.from(doc.body.firstChild.childNodes)) {
    if (node.nodeType === Node.TEXT_NODE) {
      if (node.textContent.trim()) rows.push(noteRow('', escapeHTML(node.textContent.trim())));
      continue;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) continue;
    const tag = node.tagName.toLowerCase();
    if (tag === 'br') continue;
    if (node.classList.contains('nurse-note-row')) {
      const time = node.querySelector('.nurse-note-time');
      const text = node.querySelector('.nurse-note-text');
      if (!time || !text) return null;
      rows.push(noteRow(time.textContent.replace(/ /g, ' ').replace(/:\s*$/, '').trim(), text.innerHTML));
      continue;
    }
    if (tag === 'p' || tag === 'div') {
      if (node.querySelector('table, ul, ol, img, p, div')) return null;
      if (!hasText(node.innerHTML)) continue;
      rows.push(noteRow('', node.innerHTML));
      continue;
    }
    return null; // table, list, heading, image…
  }
  return rows;
}

function serializeNoteRows(rows) {
  return rows
    .filter(r => r.time.trim() || (r.title || '').trim() || hasText(r.html))
    .map(r => {
      const title = (r.title || '').trim();
      const body = r.html.replace(/(<br\s*\/?>\s*)+$/i, '');
      const html = title ? `<b>${escapeHTML(title)}</b><br>${body}` : body;
      const label = r.time.trim().replace(/:\s*$/, '');
      return label
        ? `<p class="nurse-note-row"><span class="nurse-note-time">${escapeHTML(label)}:</span><span class="nurse-note-text">${html}</span></p>`
        : `<p>${html}</p>`;
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
      ? 'Tab moves to the note, Enter adds the next entry, Shift+Enter starts a new line in a note. +T adds a bold title above a note.'
      : (rows ? 'Start a line with a time and press Tab (or type "0800:") to make it a timed entry.'
              : 'This tab contains a table or list, so it is edited as free text.');
  }

  if (mode === 'rows') {
    notesEditorState = { tabId: tab.id, rows: rows.length ? rows : [noteRow('', '')], dirty: false };
    free.classList.add('hidden');
    rowsBox.classList.remove('hidden');
    if (tableBtn) tableBtn.classList.remove('hidden'); // a table switches the tab to free text (tableInsertTarget)
    renderNoteRows();
  } else {
    notesEditorState = null;
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
      <input type="text" class="note-entry-time" maxlength="${NOTE_LABEL_MAX}" placeholder="0800" aria-label="Time or date of entry ${i + 1}" value="${escapeHTML(row.time)}">
      <div class="note-entry-body">
        <input type="text" class="note-entry-title ${row.showTitle ? '' : 'hidden'}" placeholder="Title (optional), shown in bold above the note" aria-label="Title for entry ${i + 1}" value="${escapeHTML(row.title || '')}">
        <div class="note-entry-text rich-text-editor" contenteditable="true" role="textbox" aria-multiline="true" aria-label="Note for entry ${i + 1}" placeholder="Note…"></div>
      </div>
      <div class="note-entry-actions">
        <button type="button" class="note-entry-btn note-entry-title-btn" data-act="title" tabindex="-1" title="${row.showTitle ? 'Remove the title' : 'Add a title above this note'}" aria-label="${row.showTitle ? 'Remove the title of' : 'Add a title to'} entry ${i + 1}">${row.showTitle ? '&minus;T' : '+T'}</button>
        <button type="button" class="note-entry-btn" data-act="up" tabindex="-1" title="Move up (Alt+↑)" aria-label="Move entry ${i + 1} up" ${i === 0 ? 'disabled' : ''}>&uarr;</button>
        <button type="button" class="note-entry-btn" data-act="down" tabindex="-1" title="Move down (Alt+↓)" aria-label="Move entry ${i + 1} down" ${i === state.rows.length - 1 ? 'disabled' : ''}>&darr;</button>
        <button type="button" class="note-entry-btn danger" data-act="delete" tabindex="-1" title="Delete entry" aria-label="Delete entry ${i + 1}">&times;</button>
      </div>`;
    const timeInput = el.querySelector('.note-entry-time');
    const titleInput = el.querySelector('.note-entry-title');
    const text = el.querySelector('.note-entry-text');
    text.innerHTML = row.html;
    titleInput.addEventListener('input', () => { row.title = titleInput.value; state.dirty = true; });
    titleInput.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); placeCaretAtEnd(text); } });

    timeInput.addEventListener('input', () => { row.time = timeInput.value; state.dirty = true; });
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
      } else if (e.key === 'Backspace' && !hasText(text.innerHTML) && !row.time.trim() && state.rows.length > 1) {
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
