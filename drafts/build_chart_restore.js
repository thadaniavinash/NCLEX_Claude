// Builds drafts/chart_restore_patch.json: for every case study whose later screens show less of the
// chart than earlier ones, the screens' tab lists with everything carried forward (restoreChartContinuity
// in js/chart-continuity.js, run in the real app so the same code is used). Apply with the Supabase
// workflow's `patch` action; it refuses the whole patch if any tab list changed since cases-data.js
// was downloaded.
//
// Usage: serve the repo (python3 -m http.server 8765), then node drafts/build_chart_restore.js

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
let playwright;
try { playwright = require('playwright'); } catch {
  playwright = require(execSync('npm root -g').toString().trim() + '/playwright');
}

const REPO = path.dirname(__dirname);
const BASE = process.argv[2] || 'http://localhost:8765';
const raw = fs.readFileSync(path.join(REPO, 'cases-data.js'), 'utf8');
const m = raw.match(/^window\.NCLEX_CASES = ([\s\S]*);\n\nwindow\.NCLEX_STANDALONE = ([\s\S]*);\n$/);
if (!m) throw new Error('cases-data.js is not in the expected format');
const cases = JSON.parse(m[1]);

(async () => {
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage();
  await page.route(/supabase\.co|\/api\/save/, r => r.abort());
  await page.goto(`${BASE}/index.html?author=1&x=${Date.now()}`);
  await page.waitForFunction(() => typeof restoreChartContinuity === 'function');
  const result = await page.evaluate(cases => {
    const entries = [], summary = [];
    cases.forEach(c => {
      const before = chartContinuityProblems(c);
      if (!before.length) return;
      const fixed = JSON.parse(JSON.stringify(c));
      restoreChartContinuity(fixed);
      const after = chartContinuityProblems(fixed);
      fixed.screens.forEach((s, i) => {
        const was = c.screens[i].leftContent.tabs || [];
        if (JSON.stringify(was) !== JSON.stringify(s.leftContent.tabs)) {
          entries.push({ row: 'cases', id: c.id, path: ['screens', i, 'leftContent', 'tabs'], before: was, after: s.leftContent.tabs });
        }
      });
      summary.push({ id: c.id, title: c.title, gapsBefore: before.length, gapsAfter: after.map(describeChartProblem) });
    });
    return { entries, summary };
  }, cases);
  await browser.close();
  fs.writeFileSync(path.join(__dirname, 'chart_restore_patch.json'), JSON.stringify(result.entries, null, 1));
  result.summary.forEach(s => console.log(`${s.title} [${s.id}]: ${s.gapsBefore} gaps -> ${s.gapsAfter.length}${s.gapsAfter.length ? ' ' + JSON.stringify(s.gapsAfter) : ''}`));
  console.log(`${result.summary.length} cases, ${result.entries.length} screen tab lists changed -> drafts/chart_restore_patch.json`);
})();
