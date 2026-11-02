// Review PDF for draft case studies: for each item, every screen as the student sees it, then answered with the key and rationale.
// Usage: serve a copy of the app whose cases-data.js includes the drafts (Supabase is blocked here), then
//   node drafts/build_unit7_review_pdf.js <base url> <out.pdf> <case id> [case id ...]
const { execSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
let pw; try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const check = fs.readFileSync(path.join(__dirname, '..', 'tools', 'check.js'), 'utf8');
const answerKeySrc = check.slice(check.indexOf('function answerKey'), check.indexOf('(async () =>'));

(async () => {
  const [base, out, ...ids] = process.argv.slice(2);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'review-'));
  const b = await pw.chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  await p.route(/supabase\.co|\/api\/save/, r => r.abort());
  await p.goto(`${base}/index.html?author=1`);
  await p.waitForFunction(() => typeof caseStudies !== 'undefined' && caseStudies.length > 0);
  await p.evaluate(src => { window.answerKey = eval('(' + src + ')'); }, answerKeySrc.replace(/^function answerKey/, 'function'));
  let html = '<html><body style="font-family:Arial;margin:0">';
  for (const id of ids) {
    const info = await p.evaluate(id => {
      const item = caseStudies.find(c => c.id === id);
      startPlayer(item, { mode: 'review', isRemediation: false, allowBacktrack: true });
      return { title: item.title, description: item.description, n: item.screens.length, problems: itemProblems(item) };
    }, id);
    html += `<div style="page-break-after:always;padding:40px"><h1>${info.title}</h1><p>${info.description}</p>` +
      `<p>Readiness problems: ${info.problems.length ? info.problems.join('; ') : 'none'}</p></div>`;
    for (let i = 0; i < info.n; i++) {
      const shots = [];
      for (const answered of [false, true]) {
        const res = await p.evaluate(({ id, i, answered }) => {
          const item = caseStudies.find(c => c.id === id);
          const q = item.screens[i].question;
          if (answered) { playerAnswers[i] = answerKey(q); evaluateStepScore(i); } else { delete playerAnswers[i]; delete playerScores[i]; }
          renderPlayerStep(i);
          document.querySelectorAll('#player-view *').forEach(el => { if (el.scrollTop) el.scrollTop = 0; });
          const s = playerScores[i];
          return s ? `${s.score}/${s.max}` : '';
        }, { id, i, answered });
        const f = path.join(tmp, `${id}_${i}_${answered ? 'a' : 'q'}.jpg`);
        await p.waitForTimeout(150);
        await p.screenshot({ path: f, type: 'jpeg', quality: 80 });
        shots.push({ f, res });
      }
      for (const s of shots) {
        html += `<div style="page-break-after:always;padding:0"><div style="font-size:13px;margin:4px 0">${info.title}, screen ${i + 1}` +
          `${s.res ? ` (answer key, score ${s.res})` : ''}</div><img style="display:block;margin:auto;max-width:100%;max-height:178mm" src="data:image/jpeg;base64,${fs.readFileSync(s.f).toString('base64')}"></div>`;
      }
    }
  }
  html += '</body></html>';
  const q = await b.newPage();
  await q.setContent(html, { waitUntil: 'load' });
  await q.pdf({ path: out, format: 'A4', landscape: true, printBackground: true, margin: { top: '8mm', bottom: '8mm', left: '8mm', right: '8mm' } });
  await b.close();
  console.log('wrote', out);
})();
