// NCLEX_Claude's Supabase tool. Talks to this copy's own project; the original
// app's database is only ever read (by `compare-original`), never written.
//
//   node tools/supabase.js ping              read-only: counts (daily keep-alive, so the free project is not paused)
//   node tools/supabase.js check             table exists, rows present, key can read/write
//   node tools/supabase.js compare-original  what changed on the original live site since this copy was made
//   node tools/supabase.js upload            cases-data.js -> this copy's database (verified)
//   node tools/supabase.js download          this copy's database -> cases-data.js
//   node tools/supabase.js add <file.json>   add one new case study or stand-alone question to the database
//
// Needs Node 18+ (global fetch). Writes use the SUPABASE_SECRET_KEY environment variable when
// it is set (required once supabase/002_admin_logins.sql restricts saving to admins); reads use
// the publishable key. When the table has a `version` column, every write only succeeds if
// nobody else saved in the meantime (and bumps the version, so open editors notice).

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

const WRITE_KEY = process.env.SUPABASE_SECRET_KEY || NEW_KEY;

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
  // select=* so this works both before and after the `version` column exists.
  const res = await fetch(`${url}/rest/v1/nclex_data?select=*`, { headers: headers(key) });
  if (!res.ok) throw new Error(`Reading ${url} failed: ${res.status} ${await res.text()}`);
  const rows = await res.json();
  const row = k => rows.find(r => r.key === k);
  const version = k => (row(k) && row(k).version !== undefined ? row(k).version : null);
  return {
    rows,
    cases: row('cases') ? row('cases').data : null,
    standalone: row('standalone') ? row('standalone').data : null,
    versions: { cases: version('cases'), standalone: version('standalone') }
  };
}

// expectedVersion: the version read before this write (null when the table has no version
// column). The write then only applies if the row is still at that version.
async function writeRow(key, data, expectedVersion = null) {
  if (NEW_URL === ORIGINAL_URL) throw new Error('Refusing to write: the target is the original database.');
  const versioned = expectedVersion !== null && expectedVersion !== undefined;
  const filter = versioned ? `&version=eq.${expectedVersion}` : '';
  const res = await fetch(`${NEW_URL}/rest/v1/nclex_data?key=eq.${key}${filter}`, {
    method: 'PATCH',
    headers: { ...headers(WRITE_KEY), 'Content-Type': 'application/json', Prefer: 'return=representation' },
    body: JSON.stringify(versioned ? { data, version: expectedVersion + 1 } : { data })
  });
  const body = await res.text();
  if (!res.ok) throw new Error(`Writing '${key}' failed: ${res.status} ${body}`);
  if (JSON.parse(body).length !== 1) {
    throw new Error(versioned
      ? `Writing '${key}' was refused: someone saved in the meantime, or this key may not save (set SUPABASE_SECRET_KEY). Nothing was changed.`
      : `Writing '${key}' changed no row: the rows are missing, or this key may not save (set SUPABASE_SECRET_KEY).`);
  }
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
  console.log(`Versions: cases=${bank.versions.cases}, standalone=${bank.versions.standalone} (null = no version column yet)`);
  // Rewrite the same data (version-checked): proves the write key can update.
  await writeRow('standalone', bank.standalone, bank.versions.standalone);
  console.log(`Read and write access with the ${process.env.SUPABASE_SECRET_KEY ? 'secret' : 'publishable'} key: OK`);
}

// Field-level differences between two versions of an item, with short excerpts.
function diffPaths(before, after, path = '', out = []) {
  if (same(before, after)) return out;
  const isObj = v => v && typeof v === 'object';
  if (isObj(before) && isObj(after)) {
    new Set([...Object.keys(before), ...Object.keys(after)]).forEach(k => diffPaths(before[k], after[k], `${path}.${k}`, out));
    return out;
  }
  const show = v => v === undefined ? '(missing)' : JSON.stringify(v);
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
  const current = await readBank(NEW_URL, NEW_KEY);
  for (const key of ['cases', 'standalone']) await writeRow(key, bank[key], current.versions[key]);
  const stored = await readBank(NEW_URL, NEW_KEY);
  const ok = same(stored.cases, bank.cases) && same(stored.standalone, bank.standalone);
  console.log(`Uploaded ${bank.cases.length} case studies and ${bank.standalone.length} stand-alone questions; ` +
              `read back ${ok ? 'identical' : 'DIFFERENT'}.`);
  if (!ok) throw new Error('The database does not match cases-data.js after upload.');
}

async function download() {
  const bank = await readBank(NEW_URL, NEW_KEY);
  if (!Array.isArray(bank.cases) || !bank.cases.length) throw new Error('The database has no case studies; refusing to overwrite cases-data.js.');
  // Postgres reorders the keys inside each item. Keep the repo's copy of every item that
  // has not really changed, so the file's diff shows only real edits.
  const local = parseBank(fs.readFileSync(DATA_FILE, 'utf8'));
  let changed = 0;
  // Edited items: put keys back in the repo's order, so the diff shows only the edit.
  const orderLike = (value, model) => {
    if (Array.isArray(value)) return value.map((v, i) => orderLike(v, Array.isArray(model) ? model[i] : undefined));
    if (!value || typeof value !== 'object') return value;
    const reference = model && typeof model === 'object' && !Array.isArray(model) ? Object.keys(model) : [];
    const keys = [...reference.filter(k => k in value), ...Object.keys(value).filter(k => !reference.includes(k))];
    return keys.reduce((o, k) => { o[k] = orderLike(value[k], model ? model[k] : undefined); return o; }, {});
  };
  const keepOrder = (dbItems, localItems) => {
    const byId = new Map(localItems.map(x => [x.id, x]));
    return dbItems.map(x => {
      const mine = byId.get(x.id);
      if (mine && same(mine, x)) return mine;
      changed++;
      return orderLike(x, mine);
    });
  };
  const merged = { cases: keepOrder(bank.cases, local.cases), standalone: keepOrder(bank.standalone || [], local.standalone) };
  const dbIds = new Set([...merged.cases, ...merged.standalone].map(x => x.id));
  const removed = [...local.cases, ...local.standalone].filter(x => !dbIds.has(x.id)).length;
  const tmp = DATA_FILE + '.tmp';
  fs.writeFileSync(tmp, bankToSource(merged), 'utf8');
  fs.renameSync(tmp, DATA_FILE);
  console.log(`Saved ${merged.cases.length} case studies and ${merged.standalone.length} stand-alone questions to cases-data.js ` +
              `(${changed} added or edited in the database, ${removed} removed).`);
}

async function add() {
  const files = process.argv.slice(3);
  if (!files.length) throw new Error('Usage: node tools/supabase.js add <item.json> [more.json ...]');
  const bank = await readBank(NEW_URL, NEW_KEY);
  if (!Array.isArray(bank.cases) || !Array.isArray(bank.standalone)) throw new Error('The database rows are missing.');
  const touched = new Set();
  for (const file of files) {
    const item = JSON.parse(fs.readFileSync(path.resolve(REPO_DIR, file), 'utf8'));
    if (!item.id || !Array.isArray(item.screens) || !item.screens.length) throw new Error(`${file} is not a case study or stand-alone question.`);
    if ([...bank.cases, ...bank.standalone].some(x => x.id === item.id)) throw new Error(`${item.id} is already in the database; not added.`);
    const key = item.isStandalone ? 'standalone' : 'cases';
    bank[key].push(item);
    touched.add(key);
    console.log(`Adding ${item.title} [${item.id}] to ${key}.`);
  }
  for (const key of touched) await writeRow(key, bank[key], bank.versions[key]);
  console.log(`Database now holds ${bank.cases.length} case studies and ${bank.standalone.length} stand-alone questions.`);
}

const commands = { ping, check, 'compare-original': compareOriginal, upload, download, add };
const command = commands[process.argv[2]];
if (!command) {
  console.error(`Usage: node tools/supabase.js <${Object.keys(commands).join('|')}>`);
  process.exit(1);
}
command().catch(err => { console.error('ERROR: ' + err.message); process.exit(1); });
