// Regression check for the NCLEX app. Loads the real app in headless Chromium
// (network calls to Supabase and /api/save are blocked, so nothing is written
// anywhere), then for every case study and stand-alone question:
//   1. renders each screen in the player and checks drop-down questions show
//      one <select> per blank,
//   2. fills in the answer key and checks the screen scores full marks,
//   3. opens it in the authoring editor, saves each screen without edits, and
//      reports anything the editor changed.
//
// Usage: serve the repo (e.g. `python3 -m http.server 8765`) then
//   node tools/check.js [http://localhost:8765]
// Needs Playwright (preinstalled in Claude Code cloud sessions).

const { execSync } = require('child_process');
let playwright;
try { playwright = require('playwright'); } catch {
  playwright = require(execSync('npm root -g').toString().trim() + '/playwright');
}

const BASE = process.argv[2] || 'http://localhost:8765';

// Unfinished items that are intentionally left as they are for now. Their
// answer-key failures are reported separately instead of failing the check.
const KNOWN_INCOMPLETE = ['case_1789753289436', 'case_1781285254218', 'case_1789577787012', 'standalone_1782309032227'];

// Answer key -> the player's answer format, per question type.
function answerKey(q) {
  const a = {};
  switch (q.type) {
    case 'select_all': case 'trend': case 'multiple_choice': case 'select_n':
      (q.options || []).forEach((o, i) => { if (o.correct) a[i] = true; }); break;
    case 'matrix_mc':
      q.matrix.rows.forEach((r, i) => { a[i] = r.correctIndex; }); break;
    case 'matrix_mr':
      q.matrix.rows.forEach((r, i) => { a[i] = [...(r.correctIndices || [])]; }); break;
    case 'dropdown_cloze': case 'dyad': case 'triad':
      (q.cloze.dropdowns || []).forEach((d, i) => { a[i] = d.options.findIndex(o => o.correct); }); break;
    case 'ordered_response':
      a.order = [...(q.orderedOptions || [])]; break;
    case 'highlight': case 'highlight_2': {
      const re = /\{([^{|]+)(?:\|([^{}]+))?\}/g; let m, i = 0;
      const sources = q.highlightTabs ? q.highlightTabs.map(t => t.content || '') : [q.highlightText || ''];
      sources.forEach(src => { re.lastIndex = 0; while ((m = re.exec(src))) { if (m[2] === 'correct') a[i] = true; i++; } });
      break;
    }
    case 'bowtie': {
      const pick = (list) => (list || []).filter(x => x.correct).map(x => x.text);
      const [a0, a1] = pick(q.bowtieActions), [p0, p1] = pick(q.bowtieParams);
      Object.assign(a, { action0: a0, action1: a1, condition: pick(q.bowtieConditions)[0], param0: p0, param1: p1 });
      break;
    }
    default: return null;
  }
  return a;
}

(async () => {
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const pageErrors = [];
  await page.route(/supabase\.co|\/api\/save/, r => r.abort());
  page.on('pageerror', e => pageErrors.push(e.message));
  page.on('dialog', d => d.accept());
  await page.goto(`${BASE}/index.html?author=1&nocache=${Date.now()}`);
  await page.waitForFunction(() => typeof caseStudies !== 'undefined' && caseStudies.length > 0, null, { timeout: 15000 });

  const results = await page.evaluate(`(${async (answerKeySrc) => {
    const answerKey = eval('(' + answerKeySrc + ')');
    window.saveCasesToStorage = async () => {}; window.saveStandaloneToStorage = async () => {};
    const items = [...caseStudies, ...standaloneQuestions];
    const failures = [], editorChanges = [], skipped = {};
    let screens = 0;

    for (const item of items) {
      const original = JSON.stringify(item);
      startPlayer(item, { mode: 'review', isRemediation: false, allowBacktrack: true });
      item.screens.forEach((screen, i) => {
        screens++;
        const q = screen.question || {};
        const where = `${item.title} [${item.id}] screen ${i + 1} (${q.type})`;
        renderPlayerStep(i);
        if (['dropdown_cloze', 'dyad', 'triad'].includes(q.type)) {
          const shown = document.querySelectorAll('#player-view select.cloze-select').length;
          const expected = (q.cloze && q.cloze.dropdowns || []).length;
          if (shown !== expected || expected === 0) failures.push(`${where}: shows ${shown} drop-downs, expected ${expected || 'at least 1'}`);
        }
        const key = answerKey(q);
        if (!key) { skipped[q.type] = (skipped[q.type] || 0) + 1; return; }
        playerAnswers[i] = key;
        evaluateStepScore(i);
        const s = playerScores[i];
        if (!s || s.max === 0 || s.score !== s.max) failures.push(`${where}: answer key scores ${s ? s.score : '?'}/${s ? s.max : '?'}`);
      });
      if (JSON.stringify(item) !== original) failures.push(`${item.title} [${item.id}]: the player modified the item`);

      const copy = JSON.parse(original);
      startEditor(copy);
      for (let i = 0; i < copy.screens.length; i++) { renderEditorStep(i); currentStepIndex = i; saveCurrentStepData(false, true); }
      const before = JSON.parse(original);
      const diff = [];
      // Ignore changes that render identically: HTML re-serialization (e.g. & -> &amp;)
      // and a missing field saved as an empty string.
      const tmp = document.createElement('div');
      const norm = v => { if (v === undefined || v === null) return ''; if (typeof v !== 'string') return v; tmp.innerHTML = v; return tmp.innerHTML; };
      (function walk(a, b, path) {
        if (JSON.stringify(a) === JSON.stringify(b) || (typeof (a ?? '') === 'string' && typeof (b ?? '') === 'string' && norm(a) === norm(b))) return;
        if (a && b && typeof a === 'object' && typeof b === 'object') {
          new Set([...Object.keys(a), ...Object.keys(b)]).forEach(k => walk(a[k], b[k], path + '.' + k));
        } else diff.push(path);
      })(before, copy, '');
      if (diff.length) editorChanges.push(`${item.title} [${item.id}]: ${diff.slice(0, 4).join(', ')}${diff.length > 4 ? ` (+${diff.length - 4} more)` : ''}`);
    }
    return { items: items.length, screens, failures, editorChanges, skipped };
  }})(${JSON.stringify(answerKey.toString())})`);

  console.log(`Checked ${results.items} items, ${results.screens} screens.`);
  if (Object.keys(results.skipped).length) console.log('No answer-key check for types:', JSON.stringify(results.skipped));
  console.log(`\nEditor open-and-save changed ${results.editorChanges.length} items${results.editorChanges.length ? ':' : '.'}`);
  results.editorChanges.forEach(c => console.log('  ~ ' + c));
  console.log(`\nPage errors: ${pageErrors.length}`);
  pageErrors.forEach(e => console.log('  ! ' + e));
  const known = results.failures.filter(f => KNOWN_INCOMPLETE.some(id => f.includes(`[${id}]`)));
  const failures = results.failures.filter(f => !known.includes(f));
  console.log(`\nKnown incomplete items: ${known.length}`);
  known.forEach(f => console.log('  - ' + f));
  console.log(`\nFailures: ${failures.length}`);
  failures.forEach(f => console.log('  x ' + f));
  await browser.close();
  process.exit(failures.length || pageErrors.length ? 1 : 0);
})();
