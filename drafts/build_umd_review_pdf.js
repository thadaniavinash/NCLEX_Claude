// Builds drafts/UMD_Case_Studies_Review_Tasks.pdf: the author's to-do list for the University of Maryland case
// studies converted from the Maryland Next Gen NCLEX Test Bank Project (CS2-CS21): how to review and publish,
// per case what to check (changed or questionable content), and each item's answer key at a glance.
// Reads drafts/umd_review/CS<nn>.json (written by the build_umd_cs<n>.py generators) and the items from
// cases-data.js (falling back to the draft JSON files).
// Usage: node drafts/build_umd_review_pdf.js
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.join(__dirname, '..');
const OUT = path.join(__dirname, 'UMD_Case_Studies_Review_Tasks.pdf');

global.window = {};
require(path.join(ROOT, 'cases-data.js'));
const bankItems = new Map([...(window.NCLEX_CASES || []), ...(window.NCLEX_STANDALONE || [])].map(x => [x.id, x]));

const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// Question HTML -> short plain text (keeps sub/superscripts readable).
const plain = html => String(html || '')
  .replace(/<br\s*\/?>/gi, ' ').replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&rsquo;/g, '’').replace(/&lsquo;/g, '‘').replace(/&ldquo;/g, '“')
  .replace(/&rdquo;/g, '”').replace(/&ndash;/g, '–').replace(/&mdash;/g, '—').replace(/&times;/g, '×')
  .replace(/&deg;/g, '°').replace(/&minus;/g, '−').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();

const TYPE_NAMES = {
  select_all: 'Select all that apply', multiple_choice: 'Multiple choice', select_n: 'Select N', trend: 'Trend',
  matrix_mc: 'Matrix (one per row)', matrix_mr: 'Matrix (multiple per row)', dropdown_cloze: 'Drop-down cloze',
  drag_drop_cloze: 'Drag and drop', dyad: 'Dyad', triad: 'Triad', highlight: 'Highlight (passage left)',
  highlight_2: 'Highlight', bowtie: 'Bow-tie', ordered_response: 'Ordered response',
};

function answerKey(q) {
  const ok = list => (list || []).filter(o => o.correct).map(o => plain(o.text));
  switch (q.type) {
    case 'select_all': case 'multiple_choice': case 'select_n': case 'trend':
      return ok(q.options).map(t => '✓ ' + t);
    case 'matrix_mc': case 'matrix_mr': {
      const cols = q.matrix.columns.map(plain);
      return q.matrix.rows.map(r => {
        const idx = q.type === 'matrix_mr' ? (r.correctIndices || []) : [r.correctIndex];
        return `${plain(r.text)} → ${idx.map(i => cols[i]).join(', ')}`;
      });
    }
    case 'dropdown_cloze': case 'drag_drop_cloze': case 'dyad': case 'triad': {
      const c = q.cloze;
      let text = plain(c.text.replace(/\[\[drop(\d+)\]\]/g, (m, i) => {
        const d = c.dropdowns[+i];
        return `[${d ? ok(d.options).join(' / ') : '?'}]`;
      }));
      const out = [text];
      if (c.scoreGroups && c.scoreGroups.length) out.push('(Scored as a pair: 1 point only if both blanks are correct.)');
      return out;
    }
    case 'highlight': case 'highlight_2': {
      const out = [];
      for (const t of q.highlightTabs || []) {
        for (const m of String(t.content).matchAll(/\{([^{}|]+)\|correct\}/g)) out.push('✓ ' + plain(m[1]));
      }
      return out;
    }
    case 'bowtie':
      return [`Condition: ${ok(q.bowtieConditions).join(', ')}`, `Actions: ${ok(q.bowtieActions).join('; ')}`,
        `Parameters: ${ok(q.bowtieParams).join('; ')}`];
    case 'ordered_response':
      return (q.orderedOptions || []).map((o, i) => `${i + 1}. ${plain(o.text || o)}`);
    default:
      return ['(answer key not summarized)'];
  }
}

function loadItem(entry) {
  if (bankItems.has(entry.id)) return { item: bankItems.get(entry.id), inBank: true };
  return { item: JSON.parse(fs.readFileSync(path.join(ROOT, entry.file), 'utf8')), inBank: false };
}

function authorOf(item) {
  const fn = plain(item.screens[0].question.footnote || '');
  const m = fn.match(/case study(?:, stand-alone [\w-]+)? \((.*?), (?:January|February|March|April|May|June|July|August|September|October|November|December) \d/);
  return m ? m[1] : '';
}

const reviews = fs.readdirSync(path.join(__dirname, 'umd_review')).filter(f => /^CS\d+\.json$/.test(f)).sort()
  .map(f => JSON.parse(fs.readFileSync(path.join(__dirname, 'umd_review', f), 'utf8')));

let totalNotes = 0;
const overviewRows = [];
const sections = reviews.map(r => {
  const loaded = r.items.map(loadItem);
  const main = loaded[0].item;
  const author = authorOf(main);
  totalNotes += r.notes.length;
  const status = loaded.every(l => l.inBank)
    ? (loaded.some(l => l.item.draft) ? 'In the bank, hidden (draft)' : 'In the bank, visible to students')
    : 'Not yet in the bank';
  overviewRows.push(`<tr><td><b>CS${r.cs}</b></td><td>${esc(r.topic)}</td><td>${loaded.length === 1 ? 'Case study'
    : 'Case study + ' + esc(loaded.slice(1).map(l => l.item.title.replace(/^University of Maryland - CS\d+ /, '')).join(', '))}</td>
    <td class="num">${r.notes.length}</td><td>${esc(status)}</td></tr>`);
  const items = loaded.map(({ item }) => {
    const screens = item.screens.map((s, i) => {
      const q = s.question;
      const key = answerKey(q).map(k => `<li>${esc(k)}</li>`).join('');
      const label = item.isStandalone ? 'Question' : `Screen ${i + 1}`;
      return `<div class="screen"><div class="sh"><b>${label}</b> · ${esc(TYPE_NAMES[q.type] || q.type)}${q.limit ? ` (${q.limit})` : ''}</div>
        <div class="stem">${esc(plain(q.stem))}</div><ul class="key">${key}</ul></div>`;
    }).join('');
    return `<div class="item"><h3>${esc(item.title)} <span class="id">${esc(item.id)}</span></h3>${screens}</div>`;
  }).join('');
  const notes = r.notes.map(n => `<li><span class="box"></span><span>${esc(n.replace(/->/g, "→"))}</span></li>`).join('');
  return `<section class="case">
    <h2>University of Maryland - CS${r.cs}: ${esc(r.topic)}</h2>
    <div class="meta">Source: “${esc(r.source)}” (medical-surgical)${author ? ` · Author: ${esc(author)}` : ''} · ${esc(status)}</div>
    <h4>What to review</h4><ul class="todo">${notes}
      <li><span class="box"></span><span>Read the whole case in the studio preview (With answers) and check the rationales; then publish it (see page 1).</span></li></ul>
    <h4>Answer key at a glance</h4>${items}</section>`;
});

const today = new Date().toLocaleDateString('en-CA', { year: 'numeric', month: 'long', day: 'numeric' });
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
  @page { size: Letter; margin: 16mm 15mm 16mm 15mm; }
  body { font-family: "Inter", "Segoe UI", Arial, sans-serif; color: #1e293b; font-size: 10pt; line-height: 1.4; }
  h1 { font-size: 20pt; margin: 0 0 4px; color: #025287; }
  h2 { font-size: 14pt; margin: 0 0 2px; color: #025287; border-bottom: 2px solid #025287; padding-bottom: 3px; }
  h3 { font-size: 10.5pt; margin: 10px 0 4px; } h4 { font-size: 10.5pt; margin: 10px 0 4px; color: #334155; }
  .id { font-weight: 400; color: #64748b; font-size: 8.5pt; }
  .sub { color: #475569; margin-bottom: 14px; }
  .meta { color: #475569; font-size: 9pt; margin-bottom: 6px; }
  .case { page-break-before: always; }
  ol.steps li, ul.plain li { margin-bottom: 4px; }
  ul.todo { list-style: none; padding: 0; margin: 0; }
  ul.todo li { display: flex; gap: 8px; margin-bottom: 5px; page-break-inside: avoid; }
  .box { flex: 0 0 11px; height: 11px; border: 1.3px solid #334155; border-radius: 2px; margin-top: 2px; }
  table { border-collapse: collapse; width: 100%; font-size: 9pt; }
  th, td { border: 1px solid #cbd5e1; padding: 4px 6px; text-align: left; vertical-align: top; }
  th { background: #e2e8f0; } td.num { text-align: center; }
  .screen { border: 1px solid #e2e8f0; border-radius: 4px; padding: 5px 8px; margin-bottom: 5px; page-break-inside: avoid; }
  .sh { font-size: 9pt; color: #025287; } .stem { font-size: 9pt; color: #334155; margin: 2px 0; }
  ul.key { margin: 2px 0 0; padding-left: 16px; font-size: 9pt; } ul.key li { margin: 0; }
  .note { background: #f1f5f9; border-left: 3px solid #025287; padding: 6px 10px; margin: 10px 0; }
</style></head><body>
<h1>University of Maryland case studies: your review tasks</h1>
<div class="sub">NCLEX NGN Case Study Studio · ${esc(today)} · ${reviews.length} case studies (CS2–CS21) ·
  ${totalNotes} review points</div>

<p>These case studies were converted from the medical-surgical faculty case studies of the Maryland Next Gen NCLEX Test
Bank Project (University of Maryland School of Nursing,
nursing.umaryland.edu/mnwc/initiatives/nextgen-nclex/nextgen-nclex-library/). Asthma is CS1 (already in NURS 1021 Unit 3).
Every screen carries an acknowledgment of the source and author. All of them are in the question bank under
<b>Others</b>, <b>hidden from students</b> until you publish them.</p>

<div class="note"><b>What I checked for each item:</b> every screen renders in the player and scores full marks with its
answer key; the readiness check finds nothing missing (except the draft flag); the chart never loses a tab or an entry from
one screen to the next; opening and saving in the editor changes nothing.</div>

<h4>How to review and publish a case</h4>
<ol class="steps">
  <li>Open the studio (<b>?author=1</b>), sign in, and go to <b>Question bank</b>. Set the status filter to <b>Hidden from students</b> or search for
    “University of Maryland”.</li>
  <li>Open the case and go through the items for that case in this document (tick each box). Use <b>Preview</b> with
    <b>With answers</b> to read each screen as a student sees it.</li>
  <li>Make any changes in the editor and save (the chart carries changes forward to later screens).</li>
  <li>If you want the case in a course unit instead of <b>Others</b>, change the Course and Unit chips.</li>
  <li>Publish: click the <b>Ready for students</b> chip → <b>Show to students</b> (or ⋯ → Show to students in the question bank).
    Do the same for its stand-alone trend or bow-tie.</li>
</ol>

<h4>Changes made to every case</h4>
<ul class="plain">
  <li>Laboratory values are in SI units (Canada). The author’s reference ranges were converted, not replaced, so each
    question keys exactly as written. Blood gases stay in mm Hg (as MCC prints them). Temperatures are shown in °C with °F.</li>
  <li>Answer options were reordered where a correct answer was listed first. Where a source’s answer key was missing or
    unreadable, the key was taken from its rationale; this is flagged in that case.</li>
  <li>Clear errors (doses, units, lab values that contradict the question) were corrected and are listed below. Content that is
    debatable was kept as the author wrote it and flagged for your decision.</li>
  <li>Each source’s stand-alone trend or bow-tie was added as its own stand-alone question, unless it repeated screen 6.</li>
</ul>

<h4>Overview</h4>
<table><tr><th>Case</th><th>Topic</th><th>Items</th><th>Review points</th><th>Status</th></tr>${overviewRows.join('')}</table>
${sections.join('')}
</body></html>`;

if (process.env.UMD_HTML) fs.writeFileSync(process.env.UMD_HTML, html); // for visual checks

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  await page.pdf({ path: OUT, format: 'Letter', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;color:#64748b;width:100%;text-align:center;">University of Maryland case studies: review tasks · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
    margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' } });
  await browser.close();
  console.log('wrote', path.relative(ROOT, OUT), `(${reviews.length} cases, ${totalNotes} review points)`);
})();
