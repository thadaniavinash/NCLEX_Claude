// Writes a PDF of every case study in one course unit from cases-data.js, screen by
// screen (chart, question, answer key, rationale). Reference copy for the author: the
// PDF is git-ignored, don't commit it (it holds the answer keys).
// Usage: node drafts/build_casebook_pdf.js "NURS 1017" 3 [--standalone] [output.pdf]
//   --standalone  also adds the unit's stand-alone questions after the case studies.
//   Default output: <Course>_Unit_<n>_Case_Studies.pdf in the current folder.
// The chart only grows from screen to screen, so screen 1 shows it in full and later
// screens show the tabs (matched by title; ids differ in older cases) and entries that are new or changed (the rest is listed by name).
const path = require('path');
const { execSync } = require('child_process');
let playwright;
try { playwright = require('playwright'); } catch {
  playwright = require(execSync('npm root -g').toString().trim() + '/playwright');
}
const ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const WITH_STANDALONE = args.includes('--standalone');
const [COURSE, UNIT, outArg] = args.filter(a => a !== '--standalone');
if (!COURSE || !/^\d+$/.test(UNIT || '')) {
  console.error('Usage: node drafts/build_casebook_pdf.js "NURS 1017" 3 [--standalone] [output.pdf]');
  process.exit(1);
}
const LABEL = `${COURSE} Unit ${UNIT} Case Studies`;
const OUT = path.resolve(outArg || `${COURSE.replace(/\s+/g, '_')}_Unit_${UNIT}_Case_Studies.pdf`);

const CSS = `
@page { size: Letter; margin: 16mm 15mm 18mm; }
* { box-sizing: border-box; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 10.5pt; color: #1e293b; line-height: 1.45; margin: 0; }
h1 { font-size: 22pt; color: #1e3a8a; margin: 0 0 6px; }
h2 { font-size: 16pt; color: #1e3a8a; margin: 0 0 4px; }
h3 { font-size: 12.5pt; color: #0f172a; margin: 18px 0 6px; padding: 6px 10px; background: #e0e7ff; border-left: 4px solid #1e3a8a; }
h4 { font-size: 10.5pt; text-transform: uppercase; letter-spacing: .04em; color: #475569; margin: 12px 0 4px; }
.cover { page-break-after: always; padding-top: 60px; }
.cover ol { font-size: 12pt; line-height: 1.9; }
.muted { color: #64748b; }
.case { page-break-before: always; }
.case-meta { color: #475569; margin-bottom: 8px; }
.screen { margin-top: 10px; }
.intro { font-style: italic; color: #334155; margin: 4px 0 8px; }
.tab { border: 1px solid #cbd5e1; border-radius: 4px; margin: 6px 0; }
.tab-title { background: #f1f5f9; font-weight: bold; padding: 4px 8px; border-bottom: 1px solid #cbd5e1; font-size: 10pt; }
.tab-title .tag { font-weight: normal; color: #64748b; font-size: 9pt; margin-left: 6px; }
.tab-body { padding: 6px 10px; }
.tab-body table { border-collapse: collapse; max-width: 100%; font-size: 9.5pt; }
.tab-body td, .tab-body th { border: 1px solid #94a3b8; padding: 3px 6px; vertical-align: top; }
.tab-body img { max-width: 100%; }
.nurse-note-row { display: flex; gap: 8px; margin: 4px 0; }
.nurse-note-time { font-weight: bold; white-space: nowrap; min-width: 48px; flex-shrink: 0; }
.unchanged { font-size: 9.5pt; color: #64748b; margin: 4px 0; }
.question { border: 1px solid #94a3b8; border-radius: 4px; padding: 8px 12px; margin-top: 10px; page-break-inside: avoid; }
.qtype { font-size: 9pt; color: #64748b; text-transform: uppercase; letter-spacing: .04em; }
.preamble { margin: 4px 0; color: #334155; }
.stem { font-weight: bold; margin: 4px 0 8px; }
ul.opts { list-style: none; padding: 0; margin: 0; }
ul.opts li { margin: 3px 0; padding-left: 26px; text-indent: -26px; }
.box { display: inline-block; width: 20px; font-weight: bold; text-indent: 0; }
.correct { color: #166534; font-weight: bold; }
.hl { text-decoration: underline dotted #64748b; }
.hl-correct { background: #bbf7d0; font-weight: bold; text-decoration: underline; }
table.matrix { border-collapse: collapse; width: 100%; font-size: 9.5pt; }
table.matrix th, table.matrix td { border: 1px solid #94a3b8; padding: 4px 6px; vertical-align: top; }
table.matrix th { background: #f1f5f9; }
table.matrix td.mark { text-align: center; width: 13%; }
.cloze-blank { border-bottom: 1px solid #1e293b; padding: 0 3px; }
.answer { background: #f0fdf4; border: 1px solid #86efac; border-radius: 4px; padding: 8px 12px; margin-top: 8px; }
.rationale { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 12px; margin-top: 8px; }
`;

const TYPE_NAMES = {
  select_all: 'Multiple response (select all that apply)', matrix_mc: 'Matrix (multiple choice)',
  matrix_mr: 'Matrix (multiple response)', dropdown_cloze: 'Drop-down (cloze)', multiple_choice: 'Multiple choice',
  select_n: 'Multiple response (select N)', trend: 'Trend', dyad: 'Drop-down (dyad)', triad: 'Drop-down (triad)',
  drag_drop_cloze: 'Drag-and-drop (cloze)', highlight: 'Highlight', highlight_2: 'Highlight (chart)',
  ordered_response: 'Ordered response', bowtie: 'Bow-tie',
};
const STEPS = ['Recognize cues', 'Analyze cues', 'Prioritize hypotheses', 'Generate solutions', 'Take action', 'Evaluate outcomes'];

(async () => {
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage();
  await page.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>');
  await page.addScriptTag({ path: path.join(ROOT, 'cases-data.js') });
  const found = await page.evaluate(({ CSS, TYPE_NAMES, STEPS, COURSE, UNIT, LABEL, WITH_STANDALONE }) => {
    const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const inUnit = c => c.course === COURSE && new RegExp(`^Unit ${UNIT}\\b`).test(c.unit || '');
    const byTitle = (a, b) => a.title.localeCompare(b.title, undefined, { numeric: true });
    const cases = window.NCLEX_CASES.filter(inUnit).sort(byTitle);
    const standalone = WITH_STANDALONE ? (window.NCLEX_STANDALONE || []).filter(inUnit).sort(byTitle) : [];
    if (!cases.length && !standalone.length) return 0;
    // Top-level chart entries of a tab, compared by text so re-serialization doesn't count as a change.
    const blocks = html => {
      const d = document.createElement('div'); d.innerHTML = html || '';
      return [...d.childNodes].filter(n => n.nodeType === 1 || n.textContent.trim())
        .map(n => ({ html: n.nodeType === 1 ? n.outerHTML : esc(n.textContent), key: n.textContent.replace(/\s+/g, ' ').trim() + '|' + (n.querySelectorAll ? n.querySelectorAll('img').length : 0) }));
    };
    const tabBox = (title, tag, html) => `<div class="tab"><div class="tab-title">${esc(title)}${tag ? `<span class="tag">${tag}</span>` : ''}</div><div class="tab-body">${html}</div></div>`;

    const renderQuestion = q => {
      let body = '', answer = '';
      if (['select_all', 'multiple_choice', 'select_n', 'trend'].includes(q.type)) {
        const opts = q.options || [];
        body = `<ul class="opts">${opts.map((o, i) => `<li><span class="box">${i + 1}.</span>${esc(o.text)}</li>`).join('')}</ul>`;
        answer = `<ul class="opts">${opts.map((o, i) => o.correct ? `<li class="correct"><span class="box">✓</span>Option ${i + 1}: ${esc(o.text)}</li>` : '').join('')}</ul>`;
      } else if (q.type === 'matrix_mc' || q.type === 'matrix_mr') {
        const m = q.matrix, cols = m.columns || [];
        const table = withKey => `<table class="matrix"><tr><th>${esc(m.firstColumnHeader || '')}</th>${cols.map(c => `<th>${esc(c)}</th>`).join('')}</tr>${m.rows.map(r => {
          const right = q.type === 'matrix_mc' ? [r.correctIndex] : (r.correctIndices || []);
          return `<tr><td>${esc(r.text)}</td>${cols.map((_, ci) => `<td class="mark">${withKey ? (right.includes(ci) ? '<span class="correct">✓</span>' : '') : '○'}</td>`).join('')}</tr>`;
        }).join('')}</table>`;
        body = table(false); answer = table(true);
      } else if (['dropdown_cloze', 'drag_drop_cloze', 'dyad', 'triad'].includes(q.type)) {
        const cz = q.cloze, dd = cz.dropdowns || [];
        const sentence = withKey => cz.text.replace(/\[\[drop(\d+)\]\]/g, (_, n) => {
          const d = dd[+n]; if (!d) return '____';
          if (withKey) { const c = d.options.find(o => o.correct); return `<span class="correct">[${esc(c ? c.text : '?')}]</span>`; }
          return `<span class="cloze-blank">[Blank ${+n + 1}]</span>`;
        });
        if (q.type === 'drag_drop_cloze') {
          const pool = [...new Set(dd.flatMap(d => d.options.map(o => o.text)))];
          body = `<p>${sentence(false)}</p><p style="margin:4px 0 2px"><b>Word choices (drag into the blanks):</b></p><ul class="opts">${pool.map((t, j) => `<li><span class="box">${String.fromCharCode(97 + j)}.</span>${esc(t)}</li>`).join('')}</ul>`;
        } else body = `<p>${sentence(false)}</p>${dd.map((d, i) => `<p style="margin:4px 0 2px"><b>Blank ${i + 1} choices:</b></p><ul class="opts">${d.options.map((o, j) => `<li><span class="box">${String.fromCharCode(97 + j)}.</span>${esc(o.text)}</li>`).join('')}</ul>`).join('')}`;
        answer = `<p>${sentence(true)}</p>`;
      } else if (q.type === 'highlight' || q.type === 'highlight_2') {
        const srcs = q.highlightTabs && q.highlightTabs.length ? q.highlightTabs : [{ title: '', content: q.highlightText || '' }];
        const mark = (src, withKey) => {
          const h = /<[a-z]/i.test(src) ? src : esc(src).replace(/\n/g, '<br>');
          return h.replace(/\{([^{|}]+)(?:\|([^{}]+))?\}/g, (_, ph, flag) => withKey && flag === 'correct'
            ? `<span class="hl-correct">${ph}</span>` : `<span class="hl">${ph}</span>`);
        };
        const lim = q.maxCorrectSelections ? ` (students may select ${q.maxCorrectSelections})` : '';
        const tabs = withKey => srcs.map(t => tabBox(t.title || 'Passage', '', mark(t.content || '', withKey))).join('');
        body = `<p class="muted" style="font-size:9pt">Selectable phrases are underlined${lim}.</p>${tabs(false)}`;
        answer = `<p class="muted" style="font-size:9pt">Correct phrases are highlighted.</p>${tabs(true)}`;
      } else if (q.type === 'ordered_response') {
        const steps = q.orderedOptions || [];
        const shuffled = steps.map((t, i) => [t, (i * 7 + 3) % steps.length]).sort((a, b) => a[1] - b[1]).map(x => x[0]);
        body = `<p class="muted" style="font-size:9pt">The player shows these steps in a random order.</p><ul class="opts">${shuffled.map(t => `<li><span class="box">•</span>${esc(t)}</li>`).join('')}</ul>`;
        answer = `<ul class="opts">${steps.map((t, i) => `<li class="correct"><span class="box">${i + 1}.</span>${esc(t)}</li>`).join('')}</ul>`;
      } else if (q.type === 'bowtie') {
        const groups = [['Actions to take (2)', q.bowtieActions], ['Condition most likely experiencing (1)', q.bowtieConditions], ['Parameters to monitor (2)', q.bowtieParams]];
        body = groups.map(([t, l]) => `<p style="margin:6px 0 2px"><b>${t}</b></p><ul class="opts">${(l || []).map(o => `<li><span class="box">○</span>${esc(o.text)}</li>`).join('')}</ul>`).join('');
        answer = groups.map(([t, l]) => `<p style="margin:6px 0 2px"><b>${t}</b></p><ul class="opts">${(l || []).filter(o => o.correct).map(o => `<li class="correct"><span class="box">✓</span>${esc(o.text)}</li>`).join('')}</ul>`).join('');
      } else {
        body = `<p class="muted">(Question type ${esc(q.type)} is not laid out in this document.)</p>`;
      }
      return `<div class="question"><div class="qtype">${esc(TYPE_NAMES[q.type] || q.type)}</div>
        ${q.preamble ? `<div class="preamble">${q.preamble}</div>` : ''}<div class="stem">${q.stem || ''}</div>${body}</div>
        <div class="answer"><h4 style="margin-top:0">Answer key</h4>${answer}</div>
        ${q.explanation ? `<div class="rationale"><h4 style="margin-top:0">Rationale</h4>${q.explanation}</div>` : ''}`;
    };

    const all = [...cases, ...standalone];
    let html = `<div class="cover"><h1>${esc(LABEL)}</h1>
      <p class="muted">${esc(all[0].unit || '')}</p>
      <p>${cases.length} unfolding case ${cases.length === 1 ? 'study' : 'studies'}${standalone.length ? ` and ${standalone.length} stand-alone question${standalone.length === 1 ? '' : 's'}` : ''}, six screens each, following the NCSBN Clinical Judgment Measurement Model.
      Each screen shows the chart, the question as students see it, the answer key and the rationale. The chart only grows
      as a case unfolds: screen 1 shows it in full; later screens show the tabs and entries that are new or changed, and
      list the tabs that are unchanged.</p><ol>${all.map(c => `<li>${esc(c.title)}<br><span class="muted" style="font-size:10pt">${esc(c.description || '')}</span></li>`).join('')}</ol>
      <p class="muted" style="font-size:9pt">Source: question bank backup (cases-data.js), ${new Date().toISOString().slice(0, 10)}.</p></div>`;

    all.forEach(c => {
      html += `<section class="case"><h2>${esc(c.title)}</h2><div class="case-meta">${esc(c.description || '')}</div>`;
      let prev = {};
      c.screens.forEach((s, i) => {
        const lc = s.leftContent || {};
        const step = c.isStandalone ? '' : ` · ${esc(STEPS[(s.step || i + 1) - 1] || '')}`;
        html += `<div class="screen"><h3>${c.screens.length > 1 ? `Screen ${i + 1} of ${c.screens.length}` : 'Question'}${step}</h3>`;
        if (lc.intro) html += `<div class="intro">${lc.intro}</div>`;
        const unchanged = [], cur = {};
        (lc.tabs || []).forEach(t => {
          const b = blocks(t.content), name = (t.title || '').trim().toLowerCase(); cur[name] = b;
          const before = prev[name];
          if (!before) { html += tabBox(t.title, i ? 'new tab' : '', b.map(x => x.html).join('')); return; }
          const seen = new Set(before.map(x => x.key));
          const fresh = b.filter(x => !seen.has(x.key));
          if (!fresh.length) unchanged.push(t.title);
          else html += tabBox(t.title, 'new or updated entries', fresh.map(x => x.html).join(''));
        });
        if (unchanged.length) html += `<div class="unchanged">Unchanged from the previous screen: ${unchanged.map(esc).join(', ')}</div>`;
        prev = cur;
        html += renderQuestion(s.question || {}) + '</div>';
      });
      html += '</section>';
    });
    document.head.insertAdjacentHTML('beforeend', `<style>${CSS}</style>`);
    document.body.innerHTML = html;
    return all.length;
  }, { CSS, TYPE_NAMES, STEPS, COURSE, UNIT, LABEL, WITH_STANDALONE });
  if (!found) { console.error(`No items found for ${COURSE} Unit ${UNIT}.`); await browser.close(); process.exit(1); }
  await page.pdf({
    path: OUT, format: 'Letter', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `<div style="font-size:8px;width:100%;text-align:center;color:#64748b">${LABEL.replace(/[<&]/g, '')} · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>`,
  });
  await browser.close();
  console.log(`Wrote ${OUT} (${found} items)`);
})();
