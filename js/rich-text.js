/* Authoring text boxes (.rich-text-editor): one place for editing commands, clean paste, keyboard
   shortcuts, the expanded writing view and the table size picker. The toolbar itself is wired in
   initRichTextEditors (js/session-builder.js). */

// Every formatting command goes through here, so replacing the browser's (deprecated but still
// universally supported) document.execCommand later is a change in one function.
function richCommand(command, value = null) {
  return document.execCommand(command, false, value);
}

/* ---- Clean paste ---- */

const PASTE_BLOCK_TAGS = new Set(['p', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'th', 'td']);
const PASTE_INLINE_TAGS = new Set(['b', 'strong', 'i', 'em', 'u', 'sup', 'sub', 'br']);

// Keeps the structure of pasted text (bold, italics, underline, sub/superscript, line breaks,
// paragraphs, lists, tables) and drops everything else: fonts, colours, sizes, classes, links,
// images and Word's markup. `inlineOnly` (for single-line fields such as a note entry) also turns
// paragraphs and list items into line breaks.
function cleanPastedHtml(html, inlineOnly) {
  const tpl = document.createElement('template');
  tpl.innerHTML = html.replace(/<!--[\s\S]*?-->/g, '');
  const out = document.createElement('div');

  const walk = (node, parent) => {
    node.childNodes.forEach(child => {
      if (child.nodeType === Node.TEXT_NODE) {
        parent.appendChild(document.createTextNode(child.textContent.replace(/\s+/g, ' ')));
        return;
      }
      if (child.nodeType !== Node.ELEMENT_NODE) return;
      let tag = child.tagName.toLowerCase();
      if (['style', 'script', 'meta', 'link', 'title', 'xml', 'img', 'svg'].includes(tag) || tag.includes(':')) return;
      if (tag === 'div' || /^h[1-6]$/.test(tag)) tag = 'p';
      // Word and Google Docs express bold/italic as styles on spans.
      const style = (child.getAttribute('style') || '').toLowerCase();
      if (tag === 'span' && /font-weight:\s*(bold|[6-9]00)/.test(style)) tag = 'b';
      else if (tag === 'span' && /font-style:\s*italic/.test(style)) tag = 'i';

      if (inlineOnly && PASTE_BLOCK_TAGS.has(tag)) {
        walk(child, parent);
        if (['p', 'li', 'tr'].includes(tag)) parent.appendChild(document.createElement('br'));
        else if (['td', 'th'].includes(tag)) parent.appendChild(document.createTextNode(' '));
        return;
      }
      if (PASTE_BLOCK_TAGS.has(tag) || PASTE_INLINE_TAGS.has(tag)) {
        const el = document.createElement(tag);
        if ((tag === 'td' || tag === 'th') && child.getAttribute('colspan')) el.setAttribute('colspan', child.getAttribute('colspan'));
        if ((tag === 'td' || tag === 'th') && child.getAttribute('rowspan')) el.setAttribute('rowspan', child.getAttribute('rowspan'));
        if (tag === 'table') el.className = 'nclex-editor-table';
        parent.appendChild(el);
        walk(child, el);
        return;
      }
      walk(child, parent); // span, font, a, … keep only their text
    });
  };
  walk(tpl.content, out);
  out.querySelectorAll('p, li').forEach(el => { if (!el.textContent.trim() && !el.querySelector('br, table')) el.remove(); });
  return out.innerHTML.replace(/(<br>\s*)+$/, '').trim();
}

function plainTextToHtml(text) {
  return escapeHTML(text.replace(/\r\n?/g, '\n').trim()).replace(/\n/g, '<br>');
}

function handleRichPaste(e) {
  const editor = e.target.closest && e.target.closest('.rich-text-editor');
  if (!editor) return;
  e.preventDefault();
  const data = e.clipboardData || window.clipboardData;
  const html = data.getData('text/html');
  const inlineOnly = editor.classList.contains('note-entry-text');
  const clean = html ? cleanPastedHtml(html, inlineOnly) : plainTextToHtml(data.getData('text/plain'));
  if (clean) richCommand('insertHTML', clean);
}

/* ---- Keyboard shortcuts ---- */

const RICH_SHORTCUTS = {
  '.': 'superscript',
  ',': 'subscript',
  '7': 'insertOrderedList',
  '8': 'insertUnorderedList'
};

// Ctrl/Cmd+B, I and U are the browser's own. Added: Ctrl+. superscript, Ctrl+, subscript,
// Ctrl+Shift+7 numbered list, Ctrl+Shift+8 bullets, Esc closes the expanded view.
function handleRichKeydown(e) {
  const editor = e.target.closest && e.target.closest('.rich-text-editor');
  if (!editor) return;
  if (e.key === 'Escape') {
    const container = editor.closest('.rich-editor-container.is-expanded');
    if (container) { e.preventDefault(); toggleExpandedEditor(container, false); }
    return;
  }
  if (!(e.ctrlKey || e.metaKey) || e.altKey) return;
  const listKey = e.shiftKey && (e.code === 'Digit7' || e.code === 'Digit8') ? e.code.slice(-1) : null;
  const command = listKey ? RICH_SHORTCUTS[listKey] : (!e.shiftKey ? RICH_SHORTCUTS[e.key] : null);
  if (!command) return;
  if (editor.classList.contains('note-entry-text') && command.includes('List')) return; // entries hold one note, no lists
  e.preventDefault();
  richCommand(command);
  if (typeof updateToolbarStates === 'function') updateToolbarStates(editor);
}

/* ---- Expanded writing view ---- */

let expandedBackdrop = null;

function toggleExpandedEditor(container, force) {
  const expand = typeof force === 'boolean' ? force : !container.classList.contains('is-expanded');
  document.querySelectorAll('.rich-editor-container.is-expanded').forEach(c => { if (c !== container) c.classList.remove('is-expanded'); });
  container.classList.toggle('is-expanded', expand);
  const btn = container.querySelector('.toolbar-expand-btn');
  if (btn) {
    btn.textContent = expand ? 'Done' : 'Expand';
    btn.setAttribute('aria-pressed', expand ? 'true' : 'false');
  }
  if (!expandedBackdrop) {
    expandedBackdrop = document.createElement('div');
    expandedBackdrop.className = 'rich-expand-backdrop';
    expandedBackdrop.addEventListener('click', () => {
      document.querySelectorAll('.rich-editor-container.is-expanded').forEach(c => toggleExpandedEditor(c, false));
    });
    document.body.appendChild(expandedBackdrop);
  }
  expandedBackdrop.classList.toggle('visible', expand);
  if (expand) {
    const editor = Array.from(container.querySelectorAll('.rich-text-editor')).find(el => el.offsetParent !== null);
    if (editor) editor.focus();
  }
}

function addExpandButtons() {
  document.querySelectorAll('.rich-editor-toolbar').forEach(toolbar => {
    if (toolbar.querySelector('.toolbar-expand-btn')) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'toolbar-btn toolbar-expand-btn';
    btn.textContent = 'Expand';
    btn.title = 'Write in a larger box (Esc to return)';
    btn.setAttribute('aria-pressed', 'false');
    toolbar.appendChild(btn);
  });
}

/* ---- Table size picker ---- */

function openTableSizePicker(button, editor) {
  closeTableSizePicker();
  const savedRange = (() => { const sel = window.getSelection(); return sel.rangeCount && editor.contains(sel.getRangeAt(0).commonAncestorContainer) ? sel.getRangeAt(0).cloneRange() : null; })();
  const picker = document.createElement('div');
  picker.id = 'table-size-picker';
  picker.className = 'table-size-picker';
  picker.setAttribute('role', 'dialog');
  picker.setAttribute('aria-label', 'Table size');
  const MAX = 8;
  let cells = '';
  for (let r = 1; r <= MAX; r++) for (let c = 1; c <= MAX; c++) cells += `<button type="button" data-r="${r}" data-c="${c}" aria-label="${r} rows by ${c} columns"></button>`;
  picker.innerHTML = `<div class="table-size-grid" style="grid-template-columns: repeat(${MAX}, 18px)">${cells}</div><div class="table-size-label">Header row + 2 rows × 2 columns</div>`;
  document.body.appendChild(picker);
  const rect = button.getBoundingClientRect();
  picker.style.top = `${rect.bottom + 4}px`;
  picker.style.left = `${Math.min(rect.left, window.innerWidth - picker.offsetWidth - 8)}px`;

  const label = picker.querySelector('.table-size-label');
  const show = (r, c) => {
    picker.querySelectorAll('button').forEach(b => b.classList.toggle('on', +b.dataset.r <= r && +b.dataset.c <= c));
    label.textContent = `Header row + ${r} row${r === 1 ? '' : 's'} × ${c} column${c === 1 ? '' : 's'}`;
  };
  picker.addEventListener('mouseover', e => { const b = e.target.closest('button'); if (b) show(+b.dataset.r, +b.dataset.c); });
  picker.addEventListener('focusin', e => { const b = e.target.closest('button'); if (b) show(+b.dataset.r, +b.dataset.c); });
  picker.addEventListener('mousedown', e => e.preventDefault());
  picker.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    editor.focus();
    if (savedRange) { const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(savedRange); }
    insertTableAtCursor(editor, +b.dataset.r, +b.dataset.c);
    closeTableSizePicker();
  });
  show(2, 2);
  picker.querySelector('button[data-r="2"][data-c="2"]').focus();
}

function closeTableSizePicker() {
  const picker = document.getElementById('table-size-picker');
  if (picker) picker.remove();
}

document.addEventListener('mousedown', e => {
  if (!e.target.closest('#table-size-picker') && !e.target.closest('.table-insert-btn')) closeTableSizePicker();
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeTableSizePicker(); });

function initRichTextExtras() {
  addExpandButtons();
  document.addEventListener('paste', handleRichPaste);
  document.addEventListener('keydown', handleRichKeydown);
  document.body.addEventListener('click', e => {
    const btn = e.target.closest('.toolbar-expand-btn');
    if (btn) { e.preventDefault(); toggleExpandedEditor(btn.closest('.rich-editor-container')); }
  });
  // Tooltips name the shortcuts
  const tips = { bold: 'Bold (Ctrl+B)', superscript: 'Superscript (Ctrl+.)', subscript: 'Subscript (Ctrl+,)',
    insertUnorderedList: 'Bullet list (Ctrl+Shift+8)', insertOrderedList: 'Numbered list (Ctrl+Shift+7)' };
  document.querySelectorAll('.rich-editor-toolbar .toolbar-btn[data-cmd]').forEach(btn => {
    if (tips[btn.dataset.cmd]) btn.title = tips[btn.dataset.cmd];
  });
}
