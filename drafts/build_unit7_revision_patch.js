// Builds drafts/unit7_cases2-6_revision_patch.json: replaces description, authorReview and screens of NURS 1017 Unit 7
// Case Studies 2-6 with the nursing-focused revision (2 Nov 2026). "before" values come from cases-data.js (the database
// backup), so the workflow's patch refuses to run if the author has edited these items in the studio since.
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
global.window = {}; require(path.join(root, 'cases-data.js'));
const out = [];
for (const n of [2, 3, 4, 5, 6]) {
  const id = `case_178241000000${n}`;
  const file = fs.readdirSync(__dirname).find(f => f.startsWith(id + '_') && f.endsWith('.json'));
  const next = JSON.parse(fs.readFileSync(path.join(__dirname, file), 'utf8'));
  const cur = window.NCLEX_CASES.find(c => c.id === id);
  if (!cur) throw new Error(`${id} not in cases-data.js`);
  for (const key of ['description', 'authorReview', 'screens']) {
    if (JSON.stringify(cur[key]) !== JSON.stringify(next[key])) out.push({ row: 'cases', id, path: [key], before: cur[key] ?? null, after: next[key] });
  }
}
fs.writeFileSync(path.join(__dirname, 'unit7_cases2-6_revision_patch.json'), JSON.stringify(out, null, 1));
console.log(`wrote ${out.length} field changes`);
