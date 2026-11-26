// Builds the MCC range patch for the NCLEX bank. Runs inside the app page (cases-data.js loaded).
// Output: { changes: [{row,id,path,before,after,edits:[...]}], flags: [...], stats }
const {chromium} = require('playwright');
const fs = require('fs');
const OUT = process.argv[2];

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.route(/supabase\.co/, r => r.abort());
  await p.goto('http://localhost:8766/');
  await p.waitForTimeout(4000);
  const BLOCK = fs.existsSync(OUT + '/block.json') ? JSON.parse(fs.readFileSync(OUT + '/block.json', 'utf8')) : [];
  const res = await p.evaluate((BLOCK) => {
    const blocked = new Set(BLOCK);
    const MONO = /^(Potassium|Sodium|Chloride|Bicarbonate)/; // mEq/L = mmol/L for these
    const lines = el => cellTextForUnits(el).split('\n').map(x => x.trim()).filter(Boolean);
    const norm = s => s.replace(/&sup9;/g, '⁹').replace(/\s+/g, '').replace(/[-–−]/g, '–').replace(/x10/gi, '×10').replace(/μ/g, 'µ').toLowerCase();
    const unitEq = u => (u || '').replace(/μ/g, 'µ').replace(/mcmol/g, 'µmol').replace(/^seconds?$/i, 's').replace(/^mm\/hr$/, 'mm/h')
      .replace(/^U\/L$/, 'IU/L').replace(/^mOsm\/kg$/, 'mmol/kg').replace(/x\s*10/g, '×10').replace(/\s+/g, '').toLowerCase();
    const num = s => parseFloat(String(s).replace(/,/g, ''));
    // "Female: 115–155 g/L; Male: 125–170 g/L" → [{sex, lo, hi, unit}]
    function parseRange(text, name) {
      const t = text.replace(/&sup9;/g, '⁹');
      if (/newborn|age |child|years|see |rise|siadh|borderline|hour-specific|point-of-care|capillary/i.test(t)) return null;
      const parts = t.split(/;|(?=\b(?:Male|Female)\s*:)/i).map(x => x.trim()).filter(Boolean);
      const out = [];
      for (const part of parts) {
        const sm = part.match(/^(Male|Female)\s*:\s*/i);
        const sex = sm ? sm[1][0].toUpperCase() : null;
        const body = sm ? part.slice(sm[0].length) : part;
        let m;
        const unitOf = rest => (rest || '').replace(/\(.*$/, '').trim();
        if ((m = body.match(/^([\d.,]+)\s*%?\s*[–\-−]\s*([\d.,]+)\s*(.*)$/))) out.push({ sex, lo: num(m[1]), hi: num(m[2]), unit: unitOf(m[3]) || (/%/.test(body) ? '%' : '') });
        else if ((m = body.match(/^(?:<|≤|less than)\s*([\d.,]+)\s*(.*)$/i))) out.push({ sex, lo: -Infinity, hi: num(m[1]), strictHi: /^</.test(body) || /less/i.test(body), unit: unitOf(m[2]) });
        else if ((m = body.match(/^(?:>|≥)\s*([\d.,]+)\s*(.*)$/))) out.push({ sex, lo: num(m[1]), hi: Infinity, strictLo: /^>/.test(body), unit: unitOf(m[2]) });
        else return null;
      }
      return out.length ? out : null;
    }
    const cls = (v, r) => (v < r.lo || (r.strictLo && v === r.lo)) ? 'L' : (v > r.hi || (r.strictHi && v === r.hi)) ? 'H' : 'N';
    const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    const changes = [], flags = [], fine = [];
    const items = [...caseStudies.map(c => ['cases', c]), ...standaloneQuestions.map(c => ['standalone', c])];
    const PEDS = new Set(["case_1782370000001", "case_1782370000003", "case_1782390000002", "case_1782370000004", "case_1786060000002", "case_1782370000005", "case_1782370000006", "case_1786010000010", "standalone_1783030000001", "standalone_1783030000002", "standalone_1783030000003", "standalone_1783030000007", "standalone_1783030000009", "standalone_1783050000002", "standalone_1784060000006", "standalone_1784060000007", "standalone_1790300000001", "standalone_1790300000006", "standalone_1790300000047", "standalone_1790300000055"]); // MCC ranges are for adults: newborn and child cases keep their own
    for (const [row, c] of items) (c.screens || []).forEach((s, si) => {
      if (PEDS.has(c.id)) return;
      const tabs = [];
      ((s.leftContent && s.leftContent.tabs) || []).forEach((t, ti) => tabs.push([['screens', si, 'leftContent', 'tabs', ti, 'content'], t]));
      ((s.question && s.question.highlightTabs) || []).forEach((t, ti) => tabs.push([['screens', si, 'question', 'highlightTabs', ti, 'content'], t]));
      for (const [path, t] of tabs) {
        const raw = t.content || '';
        if (!/<table/i.test(raw)) continue;
        const d = document.createElement('div'); d.innerHTML = raw;
        const allTds = Array.from(d.querySelectorAll('td'));
        if (d.querySelectorAll('table table').length) continue; // nested tables: skip (none expected)
        const tdEdits = []; // {tdIndex, mode:'afterFirstBr'|'whole', html}
        d.querySelectorAll('table').forEach(tb => {
          if (!(isLabTable(tb) || hasRangeColumn(tb))) return;
          const hdr = tb.rows[0]; let rc = -1;
          for (let i = 1; hdr && i < hdr.cells.length; i++) if (isRangeHeader(hdr.cells[i])) rc = i;
          const names = Array.from(tb.rows).slice(1).map(r => r.cells[0] ? (lines(r.cells[0].querySelector('b,strong') || r.cells[0])[0] || '') : '');
          const arterialTable = names.some(n => /arterial|^pa?co2|^pa?o2|^ph\b/i.test(n));
          Array.from(tb.rows).slice(1).forEach(r => {
            const c0 = r.cells[0]; if (!c0 || c0.tagName !== 'TD') return;
            const bold = c0.querySelector('b,strong');
            const name = (lines(bold || c0)[0] || '').replace(/\s+/g, ' ');
            let ref = findLabReference(name) || findLabReferenceLoose(name);
            if (!ref && /^bicarbonate/i.test(name)) ref = LAB_REFERENCE_RANGES.find(x => x.name === (arterialTable ? 'Bicarbonate (HCO₃), arterial blood' : 'Bicarbonate (HCO₃)'));
            if (!ref) return;
            const rangeCell = rc > 0 ? r.cells[rc] : null;
            const oldRange = rangeCell ? lines(rangeCell).join(' ') : lines(c0).slice(1).join(' ');
            const where = { row, id: c.id, title: c.title, draft: !!c.draft, tab: t.title, screen: si + 1, test: name, old: oldRange, mcc: ref.range, mccName: ref.name };
            if (!oldRange) { fine.push({ ...where, why: 'no range shown' }); return; }
            if (norm(oldRange) === norm(ref.range)) { fine.push({ ...where, why: 'matches MCC' }); return; }
            if (blocked.has(c.id + '|' + ref.name)) { flags.push({ ...where, why: 'left as written to stay the same as another screen of this case, where it is flagged' }); return; }
            const newP = parseRange(ref.range, ref.name), oldP = parseRange(oldRange, name);
            // one sex shown, exactly MCC's value for that sex
            if (oldP && newP && oldP.length === 1 && oldP[0].sex) {
              const same = newP.find(x => x.sex === oldP[0].sex);
              const seg = ref.range.split(';').map(x => x.trim()).find(x => x[0].toUpperCase() === oldP[0].sex);
              if (same && seg && norm(oldRange) === norm(seg)) { fine.push({ ...where, why: 'matches MCC for the sex shown' }); return; }
            }
            if (!oldP || !newP) { flags.push({ ...where, why: 'special range (age group, note or format): left as written' }); return; }
            // units
            const ou = unitEq(oldP[0].unit), nu = unitEq(newP[0].unit);
            let unitSwap = null;
            if (ou && nu && ou !== nu) {
              if (ou === 'meq/l' && nu === 'mmol/l' && MONO.test(ref.name)) unitSwap = ['mEq/L', 'mmol/L'];
              else { flags.push({ ...where, why: `different units (${oldP[0].unit} vs ${newP[0].unit}): left as written` }); return; }
            }
            // results keep the same low/normal/high reading?
            const values = Array.from(r.cells).slice(1).filter((x, i) => i + 1 !== rc)
              .map(x => x.textContent.trim()).filter(Boolean).map(v => ({ text: v, n: num((v.match(/[<>≤≥]?\s*([\d][\d,]*\.?\d*)/) || [])[1]) })).filter(v => !isNaN(v.n));
            const sexes = oldP.some(x => x.sex) ? oldP.map(x => x.sex) : [null];
            let changed = [];
            for (const v of values) for (const sx of sexes) {
              const o = oldP.find(x => x.sex === sx) || oldP[0];
              const nList = sx ? newP.filter(x => x.sex === sx) : newP;
              for (const nn of (nList.length ? nList : newP)) if (cls(v.n, o) !== cls(v.n, nn)) changed.push(`${v.text}: ${cls(v.n, o)}→${cls(v.n, nn)}${nn.sex ? ' (' + nn.sex + ')' : ''}`);
            }
            if (changed.length) {
              // Allowed only when no question text in this item mentions the test (stems, options, rationales,
              // cloze, matrix rows) and the table is not itself a highlight passage: then the result is background.
              const qText = (c.screens || []).map(sc => JSON.stringify(sc.question || {})).join(' ').replace(/<[^>]+>/g, ' ').toLowerCase();
              const words = [ref.name, ...(ref.aliases || []), name].map(w => w.toLowerCase().replace(/\(.*?\)|,.*$/g, '').trim()).filter(w => w.length > 2);
              const abbrs = [ref.name, name].map(w => (w.match(/\(([^)]{2,})\)/) || [])[1]).filter(Boolean).map(w => w.toLowerCase());
              const mentioned = words.some(w => qText.includes(w)) || abbrs.some(a => new RegExp('\\b' + a.replace(/[^a-z0-9]/g, '.') + '\\b').test(qText));
              if (mentioned || path[2] === 'question') { flags.push({ ...where, why: 'a result would change reading (L/N/H) and the questions use this test: left as written', results: [...new Set(changed)] }); return; }
              where.readingChange = [...new Set(changed)];
            }
            // keep the sex shown if the chart shows one sex only
            let newText = ref.range;
            if (oldP.length === 1 && oldP[0].sex) { const seg = ref.range.split(';').map(x => x.trim()).find(x => x[0].toUpperCase() === oldP[0].sex); if (seg) newText = seg; }
            tdEdits.push({ td: allTds.indexOf(rangeCell || c0), mode: rangeCell ? 'whole' : 'afterFirstBr', html: esc(newText), unitSwap, resultTds: unitSwap ? Array.from(r.cells).slice(1).filter((x, i) => i + 1 !== rc).map(x => allTds.indexOf(x)) : [], where });
          });
        });
        if (!tdEdits.length) continue;
        // Apply as string edits on the raw HTML: locate the n-th <td ...>...</td> in document order.
        const tdRe = /<td\b[^>]*>([\s\S]*?)<\/td>/gi;
        const spans = []; let m;
        while ((m = tdRe.exec(raw))) spans.push({ start: m.index + m[0].indexOf('>') + 1, end: m.index + m[0].length - 5, inner: m[1] });
        if (spans.length !== allTds.length) { tdEdits.forEach(e => flags.push({ ...e.where, why: 'table markup could not be edited safely: left as written' })); continue; }
        let out = raw; const ops = [];
        for (const e of tdEdits) {
          const sp = spans[e.td];
          if (e.mode === 'whole') ops.push({ start: sp.start, end: sp.end, text: e.html });
          else {
            const br = sp.inner.search(/<br\s*\/?>/i);
            if (br < 0) { flags.push({ ...e.where, why: 'range not on its own line: left as written' }); continue; }
            const brEnd = sp.inner.slice(br).match(/<br\s*\/?>/i)[0].length + br;
            // the range is everything after the first line break; a closing </b> after it stays
            const rest = sp.inner.slice(brEnd);
            const close = rest.match(/(<\/(?:b|strong)>)\s*$/i);
            ops.push({ start: sp.start + brEnd, end: sp.end - (close ? close[0].length : 0), text: e.html });
          }
          for (const ti of e.resultTds) { const rs = spans[ti]; if (rs && /mEq\/L/.test(rs.inner)) ops.push({ start: rs.start, end: rs.end, text: rs.inner.replace(/mEq\/L/g, 'mmol/L') }); }
          changes.push({ ...e.where, now: e.html.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&'), unitSwap: !!e.unitSwap });
        }
        ops.sort((a, b2) => b2.start - a.start).forEach(o => { out = out.slice(0, o.start) + o.text + out.slice(o.end); });
        if (out !== raw) changes.push({ patch: { row, id: c.id, path, before: raw, after: out } });
      }
    });
    return { changes, flags, fine };
  }, BLOCK);
  fs.writeFileSync(OUT + '/plan.json', JSON.stringify(res, null, 1));
  const rows = res.changes.filter(x => !x.patch), patches = res.changes.filter(x => x.patch);
  console.log('rows to change', rows.length, '| tab fields to patch', patches.length, '| already fine', res.fine.length, '| flagged', res.flags.length);
  await b.close();
})();
