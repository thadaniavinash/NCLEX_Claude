/* Tables in the authoring text boxes: building new tables (blank or from a template), the table
   toolbar shown under a text box's formatting toolbar while the cursor is in one of its table cells
   (insert/delete rows and columns next to the current cell, delete the table), Tab/Shift+Tab
   between cells, and the hint shown in an empty template cell. Nothing here writes to the content except the table edits
   themselves: the toolbar, the target outline and the hint are separate elements on top of the
   page, so they never end up in saved content. Students never see hints. */

const TABLE_HEADER_STYLE = 'border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;';
const TABLE_CELL_STYLE = 'border:1px solid #ccd8e0; padding:8px; min-width:80px; background:white; color:#1e293b;';

// Ready-made chart tables. Cells: string = content, { hint } = empty cell with an authoring hint.
const TABLE_TEMPLATES = {
  vitals: {
    label: 'Vital signs',
    tabTitle: 'Vital Signs',
    header: ['', { hint: 'Setting and time, e.g. Campus Clinic 1000' }],
    rows: [
      ['<b>T</b>', ''],
      ['<b>P</b>', ''],
      ['<b>RR</b>', ''],
      ['<b>BP</b>', ''],
      ['<b>Pulse Oximetry Reading (SpO<sub>2</sub>)</b>', '']
    ]
  },
  labs: {
    label: 'Laboratory results',
    tabTitle: 'Laboratory Results',
    header: ['Laboratory Test and Reference Range', { hint: 'Time, e.g. 0900' }],
    rows: Array.from({ length: 4 }, () => [{ hint: 'Test name, then Enter for the reference range' }, ''])
  }
};

function tableCellHTML(tag, cell) {
  const style = tag === 'th' ? TABLE_HEADER_STYLE : TABLE_CELL_STYLE;
  const hint = cell && typeof cell === 'object' ? ` placeholder="${escapeHTML(cell.hint)}"` : '';
  const content = typeof cell === 'string' ? cell : '';
  return `<${tag}${hint} style="${style}">${content}</${tag}>`;
}

function buildTableHTML(header, rows) {
  const head = `<thead><tr>${header.map(c => tableCellHTML('th', c)).join('')}</tr></thead>`;
  const body = `<tbody>${rows.map(r => `<tr>${r.map(c => tableCellHTML('td', c)).join('')}</tr>`).join('')}</tbody>`;
  return `<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">${head}${body}</table>`;
}

function blankTableHTML(rows, cols) {
  return buildTableHTML(Array(cols).fill(''), Array.from({ length: rows }, () => Array(cols).fill('')));
}

function templateTableHTML(key) {
  const t = TABLE_TEMPLATES[key];
  return buildTableHTML(t.header, t.rows);
}

// Inserts a table (HTML string) at the cursor in editorDiv, followed by an empty paragraph so
// the author can keep writing below it, and puts the cursor in the first cell.
function insertTableHTMLAtCursor(editorDiv, tableHTML) {
  editorDiv.focus();
  const holder = document.createElement('div');
  holder.innerHTML = tableHTML + '<p><br></p>';
  const table = holder.querySelector('table');
  const selection = window.getSelection();
  const range = selection.rangeCount ? selection.getRangeAt(0) : null;
  if (range && editorDiv.contains(range.commonAncestorContainer)) {
    range.deleteContents();
    const frag = document.createDocumentFragment();
    while (holder.firstChild) frag.appendChild(holder.firstChild);
    range.insertNode(frag);
  } else {
    while (holder.firstChild) editorDiv.appendChild(holder.firstChild);
  }
  // Start in the first cell to fill in (a template's first hinted cell), else the first cell.
  placeCaretInCell(table.querySelector('[placeholder]') || table.rows[0].cells[0]);
  notifyTableEdited(editorDiv);
}

function insertTableAtCursor(editorDiv, rows, cols) {
  insertTableHTMLAtCursor(editorDiv, blankTableHTML(rows, cols));
}

/* ---- Row and column editing ---- */

function placeCaretInCell(cell) {
  if (!cell) return;
  const range = document.createRange();
  range.selectNodeContents(cell);
  range.collapse(false);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
}

// Structural edits bypass the browser's typing events, so tell the editor (unsaved-changes
// marker, live preview) that the content changed.
function notifyTableEdited(editor) {
  if (editor) editor.dispatchEvent(new Event('input', { bubbles: true }));
}

// An empty cell with the same tag and inline style as `model` (keeps a column's look).
function emptyCellLike(model, tag) {
  const cell = document.createElement(tag || (model ? model.tagName.toLowerCase() : 'td'));
  const style = model && model.getAttribute('style');
  cell.setAttribute('style', style || (cell.tagName === 'TH' ? TABLE_HEADER_STYLE : TABLE_CELL_STYLE));
  return cell;
}

function tableInsertRow(cell, below) {
  const row = cell.closest('tr');
  const table = row.closest('table');
  const inHead = row.parentElement.tagName === 'THEAD';
  let newRow;
  if (inHead && below) {
    // A row below the header row is a data row: first row of the body, styled like it.
    let body = table.tBodies[0];
    if (!body) { body = document.createElement('tbody'); table.appendChild(body); }
    const model = body.rows[0];
    newRow = document.createElement('tr');
    Array.from(row.cells).forEach((c, i) => newRow.appendChild(emptyCellLike(model && model.cells[i], model && model.cells[i] ? null : 'td')));
    body.insertBefore(newRow, body.firstChild);
  } else {
    newRow = document.createElement('tr');
    Array.from(row.cells).forEach(c => newRow.appendChild(emptyCellLike(c)));
    row.parentElement.insertBefore(newRow, below ? row.nextSibling : row);
  }
  return newRow.cells[Math.min(cell.cellIndex, newRow.cells.length - 1)];
}

function tableInsertColumn(cell, right) {
  const index = cell.cellIndex;
  const table = cell.closest('table');
  let target = null;
  Array.from(table.rows).forEach(r => {
    const ref = r.cells[Math.min(index, r.cells.length - 1)];
    const newCell = emptyCellLike(ref);
    if (!ref) r.appendChild(newCell);
    else r.insertBefore(newCell, right ? ref.nextSibling : ref);
    if (r === cell.parentElement) target = newCell;
  });
  return target;
}

// A new readings column for vital signs or results over time: after the last reading, before a
// trailing "Reference range" / "Normal range" / "Target" column. Returns its header cell (with a
// time hint), where the cursor goes.
function tableAddReading(table) {
  const header = table.rows[0];
  if (!header) return null;
  const cells = Array.from(header.cells);
  const last = cells[cells.length - 1];
  const refLast = cells.length > 2 && /reference|normal|target|expected|range/i.test(last.textContent);
  const index = refLast ? cells.length - 1 : cells.length; // insert position
  let headerCell = null;
  Array.from(table.rows).forEach(r => {
    const model = r.cells[Math.min(index, r.cells.length) - 1] || r.cells[0];
    const cell = emptyCellLike(model);
    if (r === header) { cell.setAttribute('placeholder', 'Time, e.g. 1400'); headerCell = cell; }
    if (index >= r.cells.length) r.appendChild(cell); else r.insertBefore(cell, r.cells[index]);
  });
  return headerCell;
}

// Returns the cell to move the cursor to, or null when the table was removed.
function tableDeleteRow(cell) {
  const row = cell.closest('tr');
  const table = row.closest('table');
  const rows = Array.from(table.rows);
  if (rows.length === 1) return tableDelete(table);
  const i = rows.indexOf(row);
  const next = rows[i + 1] || rows[i - 1];
  const section = row.parentElement;
  row.remove();
  if (!section.rows.length) section.remove();
  return next.cells[Math.min(cell.cellIndex, next.cells.length - 1)];
}

function tableDeleteColumn(cell) {
  const index = cell.cellIndex;
  const table = cell.closest('table');
  const row = cell.parentElement;
  if (row.cells.length === 1) return tableDelete(table);
  Array.from(table.rows).forEach(r => { if (r.cells[index]) r.cells[index].remove(); });
  return row.cells[Math.min(index, row.cells.length - 1)];
}

function tableDelete(table) {
  const after = table.nextElementSibling;
  const editor = table.closest('[contenteditable="true"]');
  table.remove();
  if (after && editor && editor.contains(after)) placeCaretInCell(after);
  return null;
}

/* ---- Table toolbar (under the formatting toolbar of the text box being edited) ---- */

const TABLE_TOOLS_ACTIONS = [
  { group: 'Row' },
  { id: 'row-above', label: 'Above', title: 'Insert a row above this one', target: 'row' },
  { id: 'row-below', label: 'Below', title: 'Insert a row below this one', target: 'row' },
  { id: 'row-delete', label: 'Delete', title: 'Delete this row', target: 'row', danger: true },
  { group: 'Column' },
  { id: 'col-left', label: 'Left', title: 'Insert a column to the left of this one', target: 'col' },
  { id: 'col-right', label: 'Right', title: 'Insert a column to the right of this one', target: 'col' },
  { id: 'col-delete', label: 'Delete', title: 'Delete this column', target: 'col', danger: true },
  { group: '' },
  { id: 'add-reading', label: '+ Reading', title: 'Add a column for the next set of readings (before a Reference/Normal range column, if there is one), with its time header ready to fill', target: 'table' },
  { id: 'table-delete', label: 'Delete table', title: 'Delete the whole table', target: 'table', danger: true }
];

let tableToolsCell = null;
let tableToolsConfirmTimer = null;
let tableToolsPointerDown = false;

function currentEditableCell() {
  const sel = window.getSelection();
  if (!sel.rangeCount) return null;
  const node = sel.getRangeAt(0).startContainer;
  const el = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
  const cell = el && el.closest('td, th');
  const editor = cell && cell.closest('[contenteditable="true"]');
  // Only while that text box has focus (not when the selection is merely left there).
  return editor && editor.contains(document.activeElement) ? cell : null;
}

function ensureTableToolsElements() {
  let bar = document.getElementById('table-tools-bar');
  if (bar) return bar;
  bar = document.createElement('div');
  bar.id = 'table-tools-bar';
  bar.className = 'table-tools-bar hidden';
  bar.setAttribute('role', 'toolbar');
  bar.setAttribute('aria-label', 'Table');
  bar.innerHTML = TABLE_TOOLS_ACTIONS.map(a => 'group' in a
    ? `<span class="table-tools-group">${a.group}</span>`
    : `<button type="button" data-table-action="${a.id}" title="${a.title}" aria-label="${a.title}"${a.danger ? ' class="is-danger"' : ''}>${a.label}</button>`).join('');
  document.body.appendChild(bar); // moved under the current text box's toolbar when shown

  const outline = document.createElement('div');
  outline.id = 'table-tools-target';
  outline.className = 'table-tools-target hidden';
  document.body.appendChild(outline);

  const hint = document.createElement('div');
  hint.id = 'table-cell-hint';
  hint.className = 'table-cell-hint hidden';
  hint.setAttribute('aria-hidden', 'true');
  document.body.appendChild(hint);

  // Keep the cursor in the cell while using the toolbar.
  bar.addEventListener('mousedown', e => e.preventDefault());
  bar.addEventListener('click', e => {
    const btn = e.target.closest('[data-table-action]');
    if (btn) runTableAction(btn);
  });
  bar.addEventListener('mouseover', e => {
    const btn = e.target.closest('[data-table-action]');
    if (btn) showTableTarget(TABLE_TOOLS_ACTIONS.find(a => a.id === btn.dataset.tableAction).target);
  });
  bar.addEventListener('mouseleave', () => showTableTarget(null));
  return bar;
}

function runTableAction(btn) {
  const cell = tableToolsCell;
  if (!cell || !cell.isConnected) return;
  const editor = cell.closest('[contenteditable="true"]');
  const action = btn.dataset.tableAction;
  // Every delete asks for a second click: what it removes cannot be brought back.
  if (/-delete$/.test(action) && !btn.classList.contains('is-confirming')) {
    resetTableDeleteButton();
    btn.classList.add('is-confirming');
    btn.textContent = action === 'table-delete' ? 'Click again to delete' : 'Click again';
    clearTimeout(tableToolsConfirmTimer);
    tableToolsConfirmTimer = setTimeout(() => resetTableDeleteButton(), 3000);
    return;
  }
  const next = {
    'row-above': () => tableInsertRow(cell, false),
    'row-below': () => tableInsertRow(cell, true),
    'row-delete': () => tableDeleteRow(cell),
    'col-left': () => tableInsertColumn(cell, false),
    'col-right': () => tableInsertColumn(cell, true),
    'col-delete': () => tableDeleteColumn(cell),
    'add-reading': () => tableAddReading(cell.closest('table')),
    'table-delete': () => tableDelete(cell.closest('table'))
  }[action]();
  resetTableDeleteButton();
  if (editor) editor.focus();
  if (next) placeCaretInCell(next);
  notifyTableEdited(editor);
  updateTableTools();
  if (next) showTableTarget(TABLE_TOOLS_ACTIONS.find(a => a.id === action).target);
}

function resetTableDeleteButton() {
  clearTimeout(tableToolsConfirmTimer);
  document.querySelectorAll('#table-tools-bar .is-confirming').forEach(btn => {
    btn.classList.remove('is-confirming');
    btn.textContent = TABLE_TOOLS_ACTIONS.find(a => a.id === btn.dataset.tableAction).label;
  });
}

// Outlines the row, column or table the hovered toolbar button will change.
function showTableTarget(kind) {
  const outline = document.getElementById('table-tools-target');
  if (!outline) return;
  const cell = tableToolsCell;
  if (!kind || !cell || !cell.isConnected) { outline.classList.add('hidden'); return; }
  const table = cell.closest('table');
  const tableRect = table.getBoundingClientRect();
  let rect;
  if (kind === 'row') {
    const r = cell.parentElement.getBoundingClientRect();
    rect = { left: tableRect.left, top: r.top, width: tableRect.width, height: r.height };
  } else if (kind === 'col') {
    const c = cell.getBoundingClientRect();
    rect = { left: c.left, top: tableRect.top, width: c.width, height: tableRect.height };
  } else {
    rect = tableRect;
  }
  Object.assign(outline.style, { left: `${rect.left}px`, top: `${rect.top}px`, width: `${rect.width}px`, height: `${rect.height}px` });
  outline.classList.remove('hidden');
}

// The bar sits as a second row under the text box's formatting toolbar while the cursor is in a
// table, so it never covers the table. It is outside the editable area, so it is never saved.
function updateTableTools() {
  if (tableToolsPointerDown) return; // wait for mouseup, so the layout does not move mid-click
  const bar = ensureTableToolsElements();
  const cell = currentEditableCell();
  if (cell !== tableToolsCell) resetTableDeleteButton();
  tableToolsCell = cell;
  if (!cell) {
    bar.classList.add('hidden');
    showTableTarget(null);
    updateTableCellHint(null);
    return;
  }
  const editor = cell.closest('[contenteditable="true"]');
  const container = editor.closest('.rich-editor-container');
  const anchor = container && container.querySelector(':scope > .rich-editor-toolbar');
  if (anchor && anchor.nextElementSibling !== bar) anchor.after(bar);
  else if (!anchor && editor.previousElementSibling !== bar) editor.before(bar);
  bar.classList.remove('hidden');
  updateTableCellHint(cell);
}

// Template cells carry an authoring hint (placeholder attribute), shown only in the editor, only
// in the cell with the cursor, and only while it is empty. The generic "Cell" / "Header 1" labels
// older tables carry are not shown.
function updateTableCellHint(cell) {
  const hint = document.getElementById('table-cell-hint');
  if (!hint) return;
  const text = cell && (cell.getAttribute('placeholder') || '').trim();
  if (!text || /^(cell|header(\s*\d+)?)$/i.test(text) || cell.textContent.trim()) {
    hint.classList.add('hidden');
    return;
  }
  const rect = cell.getBoundingClientRect();
  const cs = getComputedStyle(cell);
  hint.textContent = text;
  hint.classList.toggle('on-header', cell.tagName === 'TH');
  Object.assign(hint.style, {
    left: `${rect.left + parseFloat(cs.paddingLeft) + 2}px`,
    top: `${rect.top + parseFloat(cs.paddingTop)}px`,
    maxWidth: `${Math.max(40, rect.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - 4)}px`
  });
  hint.classList.remove('hidden');
}

/* ---- Keyboard: Tab / Shift+Tab between cells, Tab in the last cell adds a row, Enter = line break ---- */

/* ---- Laboratory results: reference range filled in from LAB_REFERENCE_RANGES (js/lab-ranges.js) ---- */

function isLabTable(table) {
  const first = table && table.rows[0] && table.rows[0].cells[0];
  return !!first && /laboratory|lab test|reference range/i.test(first.textContent);
}

// When the author leaves the first cell of a lab-table row holding only a test name that is in the
// list, the name is set in bold and the reference range goes on the next line ("<b>Potassium</b><br>
// 3.5–5.0 mmol/L"), as in the existing charts. Anything else in the cell is left alone.
function fillLabReferenceRange(cell) {
  if (!cell || cell.cellIndex !== 0 || cell.tagName !== 'TD' || typeof findLabReference !== 'function') return false;
  const table = cell.closest('table');
  if (!isLabTable(table)) return false;
  if (cell.querySelector('br') && cell.innerText.trim().split('\n').filter(Boolean).length > 1) return false;
  const name = cell.textContent.replace(/\s+/g, ' ').trim();
  const ref = name && findLabReference(name);
  if (!ref) return false;
  cell.innerHTML = `<b>${escapeHTML(name)}</b><br>${escapeHTML(ref.range)}`; // the author's wording, MCC's range
  notifyTableEdited(cell.closest('[contenteditable="true"]'));
  return true;
}

let labCellWithCursor = null;
function trackLabCell() {
  const cell = currentEditableCell();
  if (labCellWithCursor && labCellWithCursor !== cell && labCellWithCursor.isConnected) fillLabReferenceRange(labCellWithCursor);
  labCellWithCursor = cell && cell.cellIndex === 0 && isLabTable(cell.closest('table')) ? cell : null;
}

function handleTableKeydown(e) {
  if (e.key !== 'Tab' && e.key !== 'Enter') return;
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const cell = currentEditableCell();
  if (!cell) return;
  if (e.key === 'Enter') {
    // One cell holds one entry; Enter starts a new line inside it (as in the existing charts).
    if (e.shiftKey) return;
    e.preventDefault();
    e.stopPropagation();
    richCommand('insertLineBreak');
    return;
  }
  e.preventDefault();
  e.stopPropagation(); // not the free-text notes Tab handler
  fillLabReferenceRange(cell); // leaving a lab test name: add its reference range
  const table = cell.closest('table');
  const cells = Array.from(table.querySelectorAll('th, td')).filter(c => c.closest('table') === table);
  const i = cells.indexOf(cell);
  let next = cells[i + (e.shiftKey ? -1 : 1)];
  if (!next && !e.shiftKey) {
    const row = table.rows[table.rows.length - 1];
    next = tableInsertRow(row.cells[0], true);
    notifyTableEdited(cell.closest('[contenteditable="true"]'));
  }
  if (next) placeCaretInCell(next);
  updateTableTools();
}

function initTableTools() {
  ensureTableToolsElements();
  document.addEventListener('selectionchange', updateTableTools);
  document.addEventListener('selectionchange', trackLabCell);
  document.addEventListener('focusout', () => setTimeout(trackLabCell, 0));
  document.addEventListener('input', () => updateTableTools());
  document.addEventListener('keydown', handleTableKeydown, true);
  document.addEventListener('focusout', () => setTimeout(updateTableTools, 0));
  document.addEventListener('mousedown', e => { if (!e.target.closest('#table-tools-bar')) tableToolsPointerDown = true; }, true);
  document.addEventListener('mouseup', () => { tableToolsPointerDown = false; setTimeout(updateTableTools, 0); }, true);
  // The hint and the target outline are drawn over the page, so follow scrolling.
  const reposition = () => { if (tableToolsCell) { updateTableCellHint(tableToolsCell); showTableTarget(null); } };
  window.addEventListener('scroll', reposition, true);
  window.addEventListener('resize', reposition);
}
