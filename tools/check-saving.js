// Checks admin sign-in and database saving against a simulated Supabase that behaves like
// the real project after supabase/002_admin_logins.sql: anyone can read, only signed-in
// admins can save, every save bumps the row version, and saves at an old version are refused.
// Nothing leaves the machine: all Supabase requests are answered by the simulation.
//
// Usage: serve the repo (python3 -m http.server 8765), then node tools/check-saving.js

const { execSync } = require('child_process');
let playwright;
try { playwright = require('playwright'); } catch {
  playwright = require(execSync('npm root -g').toString().trim() + '/playwright');
}
const BASE = process.argv[2] || 'http://localhost:8765';

const ACCOUNTS = { 'admin@example.com': { password: 'right-password', token: 'admin-token', admin: true },
                   'student@example.com': { password: 'student-pass', token: 'student-token', admin: false } };

function makeDatabase() {
  const item = (id, title) => ({ id, title, course: 'NURS 1017', unit: 'Unit 1 (Introduction to Pathophysiology)',
    topic: 'Unit 1 (Introduction to Pathophysiology)', disorder: 'Unit 1 (Introduction to Pathophysiology)', description: '',
    screens: [{ step: 1, leftContent: { intro: '', tabs: [] },
      question: { type: 'multiple_choice', stem: 'Q?', explanation: 'R', options: [{ text: 'A', correct: true }, { text: 'B', correct: false }, { text: 'C', correct: false }, { text: 'D', correct: false }] } }] });
  return { rows: { cases: { version: 5, data: [item('c1', 'Case One'), item('c2', 'Case Two'), item('c3', 'Case Three')] },
                   standalone: { version: 2, data: [] } }, patches: 0 };
}

async function simulate(route, dbState) {
  const req = route.request();
  const url = new URL(req.url());
  const auth = (req.headers()['authorization'] || '').replace('Bearer ', '');
  const json = (status, body) => route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(body) });
  const account = Object.values(ACCOUNTS).find(a => a.token === auth);

  if (url.pathname === '/auth/v1/token') {
    const body = JSON.parse(req.postData() || '{}');
    if (url.searchParams.get('grant_type') === 'refresh_token') return json(400, { error: 'invalid' });
    const acct = ACCOUNTS[body.email];
    if (!acct || acct.password !== body.password) return json(400, { error_description: 'Invalid login credentials' });
    return json(200, { access_token: acct.token, refresh_token: 'r', expires_in: 3600, user: { email: body.email } });
  }
  if (url.pathname === '/auth/v1/logout') return route.fulfill({ status: 204, body: '' });
  if (url.pathname === '/rest/v1/rpc/is_nclex_admin') return json(200, !!(account && account.admin));
  if (url.pathname === '/rest/v1/nclex_data') {
    const key = (url.searchParams.get('key') || '').replace('eq.', '');
    if (req.method() === 'GET') {
      const rows = Object.entries(dbState.rows).filter(([k]) => !key || k === key)
        .map(([k, r]) => ({ key: k, data: JSON.parse(JSON.stringify(r.data)), version: r.version }));
      return json(200, rows);
    }
    if (req.method() === 'PATCH') {
      const row = dbState.rows[key];
      const wantVersion = url.searchParams.get('version');
      const allowed = account && account.admin; // row level security: admins only
      if (!allowed || (wantVersion && Number(wantVersion.replace('eq.', '')) !== row.version)) return json(200, []);
      row.data = JSON.parse(req.postData()).data;
      row.version += 1;
      dbState.patches += 1;
      return json(200, [{ key, data: row.data, version: row.version }]);
    }
  }
  return route.abort();
}

(async () => {
  const browser = await playwright.chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  const dbState = makeDatabase();
  const errors = [];
  let failures = 0;
  const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${detail ? ` - ${detail}` : ''}`); if (!ok) failures++; };

  await page.route(/wgnrcopjkylviiyllsgz\.supabase\.co/, r => simulate(r, dbState));
  await page.route(/taprukpiubqsckahocaz/, r => { errors.push('contacted the original database'); r.abort(); });
  page.on('pageerror', e => errors.push(e.message));
  page.on('dialog', d => d.accept());
  const load = async () => { await page.goto(`${BASE}/index.html?author=1&x=${Date.now()}`); await page.waitForFunction(() => typeof caseStudies !== 'undefined' && caseStudies.length > 0); };
  const lastToast = () => page.evaluate(() => [...document.querySelectorAll('.toast')].map(t => t.textContent.trim()).pop() || '');
  const signIn = async (email, password) => {
    await page.click('#admin-login-btn');
    await page.fill('#login-username', email);
    await page.fill('#login-password', password);
    await page.click('#admin-login-form button[type="submit"]');
    await page.waitForTimeout(300);
    return page.evaluate(() => ({ admin: isAdminLoggedIn, error: document.getElementById('login-error-msg').classList.contains('hidden') ? '' : document.getElementById('login-error-msg').textContent.trim() }));
  };
  const editTitle = (id, title) => page.evaluate(([id, title]) => { caseStudies.find(c => c.id === id).title = title; }, [id, title]);
  const save = async () => { await page.evaluate(() => saveCasesToStorage()); await page.waitForTimeout(200); return lastToast(); };

  await load();
  check('loads the bank from the database', await page.evaluate(() => caseStudies.length) === 3);

  await editTitle('c1', 'Signed-out edit');
  let toast = await save();
  check('signed out: save refused', dbState.patches === 0 && /log in as an administrator/i.test(toast), toast);

  let r = await signIn('admin@example.com', 'wrong');
  check('wrong password: rejected with a message', !r.admin && /incorrect email or password/i.test(r.error), r.error);
  await page.click('#login-cancel-btn');

  r = await signIn('student@example.com', 'student-pass');
  check('non-admin account: rejected', !r.admin && /not an administrator/i.test(r.error), r.error);
  await page.click('#login-cancel-btn');

  r = await signIn('admin@example.com', 'right-password');
  check('admin account: signed in', r.admin, r.error);
  toast = await save();
  check('admin: save reaches the database', dbState.patches === 1 && dbState.rows.cases.version === 6 &&
        dbState.rows.cases.data[0].title === 'Signed-out edit', toast);

  // Another editor saves a different case in the meantime.
  dbState.rows.cases.data[1].title = 'Changed by another editor';
  dbState.rows.cases.version += 1;
  await editTitle('c3', 'Changed on this page');
  toast = await save();
  const titles = dbState.rows.cases.data.map(c => c.title);
  check('simultaneous edits to different cases: both kept', titles.includes('Changed by another editor') && titles.includes('Changed on this page'), toast);
  check('page shows the other editor\'s change after merging', (await page.evaluate(() => caseStudies.map(c => c.title))).includes('Changed by another editor'));

  // Both edit the same case.
  dbState.rows.cases.data[0].title = 'Their version';
  dbState.rows.cases.version += 1;
  await editTitle('c1', 'My version');
  toast = await save();
  check('same case edited by both: saved, editor warned', dbState.rows.cases.data[0].title === 'My version' && /also changed/i.test(toast), toast);

  // Deleting a case while someone else edits another one.
  dbState.rows.cases.data[2].title = 'Edited elsewhere again';
  dbState.rows.cases.version += 1;
  await page.evaluate(() => { caseStudies = caseStudies.filter(c => c.id !== 'c2'); });
  await save();
  const ids = dbState.rows.cases.data.map(c => c.id);
  check('deletion merged with another editor\'s change', !ids.includes('c2') && dbState.rows.cases.data.find(c => c.id === 'c3').title === 'Edited elsewhere again');

  await load();
  check('sign-in survives a page reload', await page.evaluate(() => isAdminLoggedIn));

  await page.click('#admin-logout-btn');
  await page.waitForTimeout(200);
  const before = dbState.patches;
  await editTitle('c1', 'After sign-out');
  toast = await save();
  check('after signing out: save refused', dbState.patches === before, toast);

  check('no page errors and the original database was never contacted', errors.length === 0, errors.join('; '));
  await browser.close();
  console.log(failures ? `\n${failures} check(s) failed.` : '\nAll saving checks passed.');
  process.exit(failures ? 1 : 0);
})();
