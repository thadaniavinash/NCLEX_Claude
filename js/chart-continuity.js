/* Chart continuity for case studies: the chart only grows as a case unfolds. A tab on one screen
   is on every later screen, and entries (notes, paragraphs, tables) shown on one screen are never
   taken away on a later one.

   The editor enforces this as the author edits (applyChartTabEdit, carryNewTabForward,
   removeTabFromScreens), and chartContinuityProblems / restoreChartContinuity find and repair gaps
   in items written before the rule existed. Only edits the author makes are carried; opening and
   saving without changes alters nothing. Tabs are matched by id (screens copy tabs with their ids),
   falling back to the title. */

function chartBlockKey(node) {
  const text = (node.textContent || '').replace(/\s+/g, ' ').trim();
  if (!text) return '';
  return node.nodeName === 'TABLE' ? `table:${text}` : text;
}

// Top-level pieces of a tab's content that carry text: note rows, paragraphs, lists, tables.
function chartBlocks(root) {
  return Array.from(root.childNodes)
    .map(node => ({ node, key: chartBlockKey(node) }))
    .filter(b => b.key);
}

function parseChartHTML(html) {
  const tpl = document.createElement('template');
  tpl.innerHTML = html || '';
  return tpl.content;
}

function chartFragmentHTML(fragment) {
  const div = document.createElement('div');
  div.appendChild(fragment.cloneNode(true));
  return div.innerHTML;
}

// The same tab on another screen: same id, or (for items whose screens were copied without ids)
// the same title, but never a tab whose id belongs to a different tab of `ownTabs`.
function findChartTab(tabs, tab, ownTabs) {
  const list = tabs || [];
  const byId = list.find(t => t.id === tab.id);
  if (byId) return byId;
  const taken = new Set((ownTabs || []).map(t => t.id));
  return list.find(t => t.title === tab.title && !taken.has(t.id));
}

// Longest-common-subsequence diff of two key lists -> [{ op: 'same'|'del'|'ins', a, b }].
function diffChartKeys(a, b) {
  const n = a.length, m = b.length;
  const lcs = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(0));
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      lcs[i][j] = a[i] === b[j] ? lcs[i + 1][j + 1] + 1 : Math.max(lcs[i + 1][j], lcs[i][j + 1]);
    }
  }
  const ops = [];
  let i = 0, j = 0;
  while (i < n || j < m) {
    if (i < n && j < m && a[i] === b[j]) { ops.push({ op: 'same', a: i++, b: j++ }); }
    else if (j < m && (i >= n || lcs[i][j + 1] >= lcs[i + 1][j])) { ops.push({ op: 'ins', b: j++ }); }
    else { ops.push({ op: 'del', a: i++ }); }
  }
  return ops;
}

function chartNoteLabel(node) {
  const label = node.querySelector && node.querySelector('.nurse-note-time');
  return label ? label.textContent.trim() : null;
}

function sameChartEntry(a, b) {
  if (a.nodeName !== b.nodeName) return false;
  return chartNoteLabel(a) === chartNoteLabel(b);
}

// Turns a diff into changes: replacements (an entry edited in place), insertions (with the key of
// the entry they follow) and deletions.
function chartChanges(oldBlocks, newBlocks) {
  const ops = diffChartKeys(oldBlocks.map(b => b.key), newBlocks.map(b => b.key));
  const changes = [];
  let lastKey = null; // key of the latest block in the new content, to anchor insertions
  for (let k = 0; k < ops.length;) {
    if (ops[k].op === 'same') { lastKey = newBlocks[ops[k].b].key; k++; continue; }
    const dels = [], ins = [];
    while (k < ops.length && ops[k].op !== 'same') {
      if (ops[k].op === 'del') dels.push(oldBlocks[ops[k].a]); else ins.push(newBlocks[ops[k].b]);
      k++;
    }
    // Pair a deleted entry with an inserted one as an edit only when they are the same kind of entry
    // (a note with the same time label, a table for a table, ...); otherwise it is a removal plus
    // an addition, so an old entry cannot quietly be overwritten by a new one.
    let pairs = 0;
    while (pairs < dels.length && pairs < ins.length && sameChartEntry(dels[pairs].node, ins[pairs].node)) pairs++;
    for (let p = 0; p < pairs; p++) changes.push({ type: 'replace', from: dels[p], to: ins[p], after: lastKey });
    let anchor = pairs ? ins[pairs - 1].key : lastKey;
    for (let p = pairs; p < ins.length; p++) { changes.push({ type: 'insert', block: ins[p], after: anchor }); anchor = ins[p].key; }
    for (let p = pairs; p < dels.length; p++) changes.push({ type: 'delete', block: dels[p], after: lastKey });
    if (ins.length) lastKey = ins[ins.length - 1].key;
  }
  return changes;
}

function insertChartNodeAfter(root, node, afterKey) {
  let clone = node.cloneNode(true);
  if (clone.nodeType === Node.TEXT_NODE) {
    // Loose text would merge with its neighbours: give it its own paragraph.
    const p = document.createElement('p');
    p.appendChild(clone);
    clone = p;
  }
  const anchor = afterKey != null ? chartBlocks(root).find(b => b.key === afterKey) : null;
  if (anchor) anchor.node.after(clone);
  else if (afterKey == null) root.insertBefore(clone, root.firstChild);
  else {
    // The anchor is not on this screen: add at the end, before trailing empty paragraphs.
    let tail = root.lastChild;
    while (tail && !chartBlockKey(tail) && tail.previousSibling) tail = tail.previousSibling;
    if (tail && chartBlockKey(tail)) tail.after(clone); else root.appendChild(clone);
  }
}

// Called when the author saves a chart tab on screen `stepIdx`. Carries the edit to every later
// screen, keeps entries inherited from the previous screen (puts back any that were removed) and
// returns what happened so the editor can say so. `tab` already holds the new title and content.
function applyChartTabEdit(item, stepIdx, tab, oldContent, oldTitle) {
  const result = { restored: 0, carried: 0 };
  if (!item || item.isStandalone || !item.screens) return result;
  const screens = item.screens;
  const ownTabs = screens[stepIdx].leftContent.tabs;
  const prevTab = stepIdx > 0 ? findChartTab(screens[stepIdx - 1].leftContent.tabs, { id: tab.id, title: oldTitle }, ownTabs) : null;
  const inherited = new Set(prevTab ? chartBlocks(parseChartHTML(prevTab.content)).map(b => b.key) : []);

  const oldRoot = parseChartHTML(oldContent);
  const newRoot = parseChartHTML(tab.content);
  const changes = oldContent === tab.content ? [] : chartChanges(chartBlocks(oldRoot), chartBlocks(newRoot));

  // Inherited entries cannot be deleted here: put them back where they were.
  changes.filter(c => c.type === 'delete' && inherited.has(c.block.key)).forEach(c => {
    insertChartNodeAfter(newRoot, c.block.node, c.after);
    result.restored++;
  });
  if (result.restored) tab.content = chartFragmentHTML(newRoot);

  const carried = changes.filter(c => !(c.type === 'delete' && inherited.has(c.block.key)));
  // Nothing the author changed (the editor may still have tidied the markup): leave later screens alone.
  if (!carried.length && oldTitle === tab.title) return result;
  for (let s = stepIdx + 1; s < screens.length; s++) {
    const tabs = screens[s].leftContent.tabs = screens[s].leftContent.tabs || [];
    const later = findChartTab(tabs, { id: tab.id, title: oldTitle }, screens[s - 1].leftContent.tabs);
    if (!later) {
      tabs.push({ id: tab.id, title: tab.title, content: tab.content });
      result.carried++;
      continue;
    }
    let touched = false;
    if (oldTitle !== tab.title && later.title === oldTitle) { later.title = tab.title; touched = true; }
    if (carried.length) {
      const root = parseChartHTML(later.content);
      carried.forEach(c => {
        const blocks = chartBlocks(root);
        if (c.type === 'replace') {
          const hit = blocks.find(b => b.key === c.from.key);
          if (hit) { hit.node.replaceWith(c.to.node.cloneNode(true)); touched = true; }
          else if (!blocks.some(b => b.key === c.to.key)) { insertChartNodeAfter(root, c.to.node, c.after); touched = true; }
        } else if (c.type === 'insert') {
          if (!blocks.some(b => b.key === c.block.key)) { insertChartNodeAfter(root, c.block.node, c.after); touched = true; }
        } else if (c.type === 'delete') {
          const hit = blocks.find(b => b.key === c.block.key);
          if (hit) { hit.node.remove(); touched = true; }
        }
      });
      if (touched) later.content = chartFragmentHTML(root);
    }
    if (touched) result.carried++;
  }
  return result;
}

// A tab added on screen `stepIdx` is added (same id, same content) to every later screen.
function carryNewTabForward(item, stepIdx, tab) {
  if (!item || item.isStandalone) return 0;
  let added = 0;
  for (let s = stepIdx + 1; s < item.screens.length; s++) {
    const tabs = item.screens[s].leftContent.tabs = item.screens[s].leftContent.tabs || [];
    if (!tabs.some(t => t.id === tab.id)) { tabs.push({ id: tab.id, title: tab.title, content: tab.content }); added++; }
  }
  return added;
}

// The earliest screen (index) showing this tab, following the chain of screens that have it.
function chartTabFirstScreen(item, stepIdx, tab) {
  let first = stepIdx;
  while (first > 0 && findChartTab(item.screens[first - 1].leftContent.tabs, tab, item.screens[first].leftContent.tabs)) first--;
  return first;
}

// Deletes a tab from screen `stepIdx` and all later screens. Only allowed on the screen where the
// tab first appears; returns the number of screens changed.
function removeTabFromScreens(item, stepIdx, tab) {
  let removed = 0;
  const last = item.isStandalone ? stepIdx : item.screens.length - 1;
  for (let s = stepIdx; s <= last; s++) {
    const tabs = item.screens[s].leftContent.tabs || [];
    const i = tabs.findIndex(t => t.id === tab.id); // by id only: never another tab that shares the title
    if (i >= 0) { tabs.splice(i, 1); removed++; }
  }
  return removed;
}

/* ---- Gaps in existing items ---- */

// Every text value of a tab's tables, and every non-table entry, to compare screens.
function chartFacts(html) {
  const root = parseChartHTML(html);
  const entries = new Set(), cells = new Set();
  chartBlocks(root).forEach(b => {
    if (b.node.nodeName === 'TABLE') {
      b.node.querySelectorAll('th, td').forEach(c => { const t = c.textContent.replace(/\s+/g, ' ').trim(); if (t) cells.add(t); });
    } else {
      entries.add(b.key);
    }
  });
  const text = chartBlocks(root).filter(b => b.node.nodeName !== 'TABLE').map(b => b.key).join(' ');
  return { entries, cells, text };
}

// [{ screen (1-based), tab, missingTab?, entries, cells }] where a screen shows less than the one before.
function chartContinuityProblems(item) {
  const problems = [];
  if (!item || item.isStandalone || !item.screens) return problems;
  for (let s = 1; s < item.screens.length; s++) {
    const prevTabs = item.screens[s - 1].leftContent.tabs || [];
    const tabs = item.screens[s].leftContent.tabs || [];
    prevTabs.forEach(pt => {
      const t = findChartTab(tabs, pt, prevTabs);
      if (!t) { problems.push({ screen: s + 1, tab: pt.title, missingTab: true, entries: 0, cells: 0 }); return; }
      const before = chartFacts(pt.content), now = chartFacts(t.content);
      const entries = [...before.entries].filter(e => !now.text.includes(e)).length;
      const cells = [...before.cells].filter(c => !now.cells.has(c)).length;
      if (entries || cells) problems.push({ screen: s + 1, tab: pt.title, missingTab: false, entries, cells });
    });
  }
  return problems;
}

function describeChartProblem(p) {
  if (p.missingTab) return `Screen ${p.screen} is missing the "${p.tab}" tab from screen ${p.screen - 1}.`;
  const parts = [];
  if (p.entries) parts.push(`${p.entries} entr${p.entries === 1 ? 'y' : 'ies'}`);
  if (p.cells) parts.push(`${p.cells} table value${p.cells === 1 ? '' : 's'}`);
  return `Screen ${p.screen}, "${p.tab}": ${parts.join(' and ')} from screen ${p.screen - 1} ${p.entries + p.cells === 1 ? 'is' : 'are'} missing.`;
}

// Carries everything forward screen by screen: missing tabs are copied, missing entries are put back
// after the entry they followed, and a table that changed (e.g. a vital signs table with a new
// column) is kept, with the previous screen's version added only when the tab has no table left.
// Returns the number of tabs changed.
function restoreChartContinuity(item) {
  let changed = 0;
  if (!item || item.isStandalone || !item.screens) return changed;
  for (let s = 1; s < item.screens.length; s++) {
    const prevTabs = item.screens[s - 1].leftContent.tabs || [];
    const tabs = item.screens[s].leftContent.tabs = item.screens[s].leftContent.tabs || [];
    prevTabs.forEach((pt, index) => {
      const t = findChartTab(tabs, pt, prevTabs);
      if (!t) {
        tabs.splice(Math.min(index, tabs.length), 0, { id: pt.id, title: pt.title, content: pt.content });
        changed++;
        return;
      }
      const root = parseChartHTML(t.content);
      const have = new Set(chartBlocks(root).map(b => b.key));
      const text = chartFacts(t.content).text;
      const hasTable = !!root.querySelector('table');
      let after = null, touched = false;
      chartBlocks(parseChartHTML(pt.content)).forEach(b => {
        const isTable = b.node.nodeName === 'TABLE';
        const present = isTable ? (have.has(b.key) || hasTable) : (have.has(b.key) || text.includes(b.key));
        if (!present) {
          insertChartNodeAfter(root, b.node, after);
          have.add(b.key);
          touched = true;
        }
        after = b.key;
      });
      if (touched) { t.content = chartFragmentHTML(root); changed++; }
    });
  }
  return changed;
}
