// NCLEX_Claude's Supabase tool. Talks to this copy's own project; the original
// app's database is only ever read (by `compare-original`), never written.
//
//   node tools/supabase.js ping              read-only: counts (daily keep-alive, so the free project is not paused)
//   node tools/supabase.js check             table exists, rows present, key can read/write
//   node tools/supabase.js compare-original  what changed on the original live site since this copy was made
//   node tools/supabase.js upload            cases-data.js -> this copy's database (verified)
//   node tools/supabase.js download          this copy's database -> cases-data.js
//
// Needs Node 18+ (global fetch).

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { execSync } = require('child_process');

const NEW_URL = 'https://wgnrcopjkylviiyllsgz.supabase.co';
const NEW_KEY = 'sb_publishable_yHZHAVA7OjJajQJfJ8zFAw_q2ld1l6M';
const ORIGINAL_URL = 'https://taprukpiubqsckahocaz.supabase.co';
const ORIGINAL_KEY = 'sb_publishable_V1u7recZMcdc2-DXhoMwoQ_BEVWej3g';
// The commit this copy was made from: the original app's data at that moment.
const COPY_BASE_COMMIT = 'a922452';

const REPO_DIR = path.dirname(__dirname);
const DATA_FILE = path.join(REPO_DIR, 'cases-data.js');

const headers = key => ({ apikey: key, Authorization: `Bearer ${key}` });

function parseBank(source) {
  const ctx = { window: {} };
  vm.runInNewContext(source, ctx);
  return { cases: ctx.window.NCLEX_CASES || [], standalone: ctx.window.NCLEX_STANDALONE || [] };
}

function bankToSource({ cases, standalone }) {
  return `window.NCLEX_CASES = ${JSON.stringify(cases, null, 2)};\n\nwindow.NCLEX_STANDALONE = ${JSON.stringify(standalone, null, 2)};\n`;
}

// Postgres jsonb does not keep object key order, so compare with keys sorted.
function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === 'object') {
    return Object.keys(value).sort().reduce((o, k) => { o[k] = canonical(value[k]); return o; }, {});
  }
  return value;
}
const same = (a, b) => JSON.stringify(canonical(a)) === JSON.stringify(canonical(b));

async function readBank(url, key) {
  const res = await fetch(`${url}/rest/v1/nclex_data?select=key,data`, { headers: headers(key) });
  if (!res.ok) throw new Error(`Reading ${url} failed: ${res.status} ${await res.text()}`);
  const rows = await res.json();
  const row = k => rows.find(r => r.key === k);
  return { rows, cases: row('cases') ? row('cases').data : null, standalone: row('standalone') ? row('standalone').data : null };
}

async function writeRow(key, data) {
  if (NEW_URL === ORIGINAL_URL) throw new Error('Refusing to write: the target is the original database.');
  const res = await fetch(`${NEW_URL}/rest/v1/nclex_data?key=eq.${key}`, {
    method: 'PATCH',
    headers: { ...headers(NEW_KEY), 'Content-Type': 'application/json', Prefer: 'return=representation' },
    body: JSON.stringify({ data })
  });
  const body = await res.text();
  if (!res.ok) throw new Error(`Writing '${key}' failed: ${res.status} ${body}`);
  if (JSON.parse(body).length !== 1) throw new Error(`Writing '${key}' changed no row. Was supabase/setup.sql run?`);
}

async function ping() {
  const bank = await readBank(NEW_URL, NEW_KEY);
  console.log(`OK: ${(bank.cases || []).length} case studies, ${(bank.standalone || []).length} stand-alone questions.`);
}

async function check() {
  const bank = await readBank(NEW_URL, NEW_KEY);
  console.log(`Rows: ${bank.rows.map(r => r.key).join(', ') || '(none)'}`);
  if (!Array.isArray(bank.cases) || !Array.isArray(bank.standalone)) {
    throw new Error("The 'cases' and 'standalone' rows are missing. Run supabase/setup.sql in the project's SQL Editor.");
  }
  console.log(`Currently holds ${bank.cases.length} case studies and ${bank.standalone.length} stand-alone questions.`);
  await writeRow('standalone', bank.standalone); // rewrite the same data: proves the key can update
  console.log('Read and write access: OK');
}

// Field-level differences between two versions of an item, with short excerpts.
function diffPaths(before, after, path = '', out = []) {
  if (same(before, after)) return out;
  const isObj = v => v && typeof v === 'object';
  if (isObj(before) && isObj(after)) {
    new Set([...Object.keys(before), ...Object.keys(after)]).forEach(k => diffPaths(before[k], after[k], `${path}.${k}`, out));
    return out;
  }
  const show = v => v === undefined ? '(missing)' : JSON.stringify(v).slice(0, 300);
  out.push(`${path}\n        was: ${show(before)}\n        now: ${show(after)}`);
  return out;
}

function describeChanges(label, base, live) {
  const byId = list => new Map(list.map(x => [x.id, x]));
  const b = byId(base), l = byId(live);
  const added = live.filter(x => !b.has(x.id));
  const removed = base.filter(x => !l.has(x.id));
  const edited = live.filter(x => b.has(x.id) && !same(b.get(x.id), x));
  console.log(`\n${label}: ${base.length} when copied, ${live.length} on the live site now`);
  added.forEach(x => console.log(`  + added:   ${x.title} [${x.id}]`));
  edited.forEach(x => {
    console.log(`  ~ edited:  ${x.title} [${x.id}]`);
    diffPaths(b.get(x.id), x).forEach(d => console.log(`      ${d}`));
  });
  removed.forEach(x => console.log(`  - removed: ${x.title} [${x.id}]`));
  if (!added.length && !edited.length && !removed.length) console.log('  no changes');
  return added.length + edited.length + removed.length;
}

async function compareOriginal() {
  const base = parseBank(execSync(`git -C "${REPO_DIR}" show ${COPY_BASE_COMMIT}:cases-data.js`, { maxBuffer: 64 * 1024 * 1024 }).toString());
  const live = await readBank(ORIGINAL_URL, ORIGINAL_KEY); // GET only
  const n = describeChanges('Case studies', base.cases, live.cases || []) +
            describeChanges('Stand-alone questions', base.standalone, live.standalone || []);
  console.log(n ? `\n${n} item(s) changed on the original live site since this copy was made.` :
                  '\nThe original live site has not changed since this copy was made.');
}

async function upload() {
  const bank = parseBank(fs.readFileSync(DATA_FILE, 'utf8'));
  if (!bank.cases.length) throw new Error('cases-data.js has no case studies; refusing to upload an empty bank.');
  for (const key of ['cases', 'standalone']) await writeRow(key, bank[key]);
  const stored = await readBank(NEW_URL, NEW_KEY);
  const ok = same(stored.cases, bank.cases) && same(stored.standalone, bank.standalone);
  console.log(`Uploaded ${bank.cases.length} case studies and ${bank.standalone.length} stand-alone questions; ` +
              `read back ${ok ? 'identical' : 'DIFFERENT'}.`);
  if (!ok) throw new Error('The database does not match cases-data.js after upload.');
}

async function download() {
  const bank = await readBank(NEW_URL, NEW_KEY);
  if (!Array.isArray(bank.cases) || !bank.cases.length) throw new Error('The database has no case studies; refusing to overwrite cases-data.js.');
  const tmp = DATA_FILE + '.tmp';
  fs.writeFileSync(tmp, bankToSource(bank), 'utf8');
  fs.renameSync(tmp, DATA_FILE);
  console.log(`Saved ${bank.cases.length} case studies and ${bank.standalone.length} stand-alone questions to cases-data.js.`);
}

const commands = { ping, check, 'compare-original': compareOriginal, upload, download };
const command = commands[process.argv[2]];
if (!command) {
  console.error(`Usage: node tools/supabase.js <${Object.keys(commands).join('|')}>`);
  process.exit(1);
}
command().catch(err => { console.error('ERROR: ' + err.message); process.exit(1); });
