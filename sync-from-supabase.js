// Script to pull latest cases and standalone questions from Supabase
// and save directly to cases-data.js, cases.json, standalone.json, the json/ folder, and Desktop backup.

// Disabled in NCLEX_Claude: this pulls from the original app's database and would
// overwrite the fixes made to cases-data.js in this repository. It will be
// re-pointed at NCLEX_Claude's own Supabase project once that exists.
console.error('sync-from-supabase.js is disabled in NCLEX_Claude until it is pointed at this copy\'s own database.');
process.exit(1);

const fs = require('fs');
const path = require('path');
const https = require('https');

const SUPABASE_URL = 'https://taprukpiubqsckahocaz.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_V1u7recZMcdc2-DXhoMwoQ_BEVWej3g';

const REPO_DIR = __dirname;
const DESKTOP_DIR = path.join('C:', 'Users', 'thada', 'Desktop', 'Antigravity', 'NCLEX Application');
const E_DRIVE_DIR = path.join('E:', 'NCLEX_NGN_Antigravity');

function fetchTableData() {
  return new Promise((resolve, reject) => {
    const url = new URL(`${SUPABASE_URL}/rest/v1/nclex_data?select=key,data`);
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: 'GET',
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(body));
          } catch (e) {
            reject(new Error("Failed to parse JSON response from Supabase: " + e.message));
          }
        } else {
          reject(new Error(`Failed to fetch data from Supabase. Status: ${res.statusCode}, Body: ${body}`));
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function runSync() {
  console.log('================================================================');
  console.log('  NCLEX STUDIO - SYNCING FROM CLOUD (SUPABASE) TO LOCAL DISK');
  console.log('================================================================');

  try {
    const records = await fetchTableData();
    const casesRecord = records.find(r => r.key === 'cases');
    const standaloneRecord = records.find(r => r.key === 'standalone');

    const cases = (casesRecord && casesRecord.data) ? casesRecord.data : [];
    const standalone = (standaloneRecord && standaloneRecord.data) ? standaloneRecord.data : [];

    console.log(`[INFO] Received ${cases.length} case studies and ${standalone.length} standalone questions from Supabase.`);

    // 1. Write cases-data.js
    const jsContent = `window.NCLEX_CASES = ${JSON.stringify(cases, null, 2)};\n\nwindow.NCLEX_STANDALONE = ${JSON.stringify(standalone, null, 2)};\n`;
    fs.writeFileSync(path.join(REPO_DIR, 'cases-data.js'), jsContent, 'utf8');
    console.log(`[OK] Updated cases-data.js`);

    // 2. Write cases.json and standalone.json
    fs.writeFileSync(path.join(REPO_DIR, 'cases.json'), JSON.stringify(cases, null, 2), 'utf8');
    fs.writeFileSync(path.join(REPO_DIR, 'standalone.json'), JSON.stringify(standalone, null, 2), 'utf8');
    console.log(`[OK] Updated cases.json and standalone.json`);

    // 3. Write individual JSON files in json/ folder
    const jsonDir = path.join(REPO_DIR, 'json');
    if (!fs.existsSync(jsonDir)) {
      fs.mkdirSync(jsonDir, { recursive: true });
    }
    for (const c of cases) {
      const slug = (c.title || 'case').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 30);
      fs.writeFileSync(path.join(jsonDir, `${c.id}_${slug}.json`), JSON.stringify(c, null, 2), 'utf8');
    }
    for (const s of standalone) {
      const slug = (s.title || 'standalone').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 30);
      fs.writeFileSync(path.join(jsonDir, `${s.id}_${slug}.json`), JSON.stringify(s, null, 2), 'utf8');
    }
    console.log(`[OK] Updated all files in json/ directory.`);

    // 4. Mirror to Desktop backup
    if (fs.existsSync(DESKTOP_DIR)) {
      try {
        fs.writeFileSync(path.join(DESKTOP_DIR, 'cases-data.js'), jsContent, 'utf8');
        fs.writeFileSync(path.join(DESKTOP_DIR, 'cases.json'), JSON.stringify(cases, null, 2), 'utf8');
        fs.writeFileSync(path.join(DESKTOP_DIR, 'standalone.json'), JSON.stringify(standalone, null, 2), 'utf8');
        const desktopJsonDir = path.join(DESKTOP_DIR, 'json');
        if (!fs.existsSync(desktopJsonDir)) fs.mkdirSync(desktopJsonDir, { recursive: true });
        for (const c of cases) {
          const slug = (c.title || 'case').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 30);
          fs.writeFileSync(path.join(desktopJsonDir, `${c.id}_${slug}.json`), JSON.stringify(c, null, 2), 'utf8');
        }
        for (const s of standalone) {
          const slug = (s.title || 'standalone').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 30);
          fs.writeFileSync(path.join(desktopJsonDir, `${s.id}_${slug}.json`), JSON.stringify(s, null, 2), 'utf8');
        }
        console.log(`[OK] Mirrored to Desktop folder: ${DESKTOP_DIR}`);
      } catch (e) {
        console.warn(`[WARN] Could not mirror to Desktop folder: ${e.message}`);
      }
    }

    // 5. Mirror to E: drive backup
    if (fs.existsSync('E:\\')) {
      try {
        if (!fs.existsSync(E_DRIVE_DIR)) fs.mkdirSync(E_DRIVE_DIR, { recursive: true });
        fs.writeFileSync(path.join(E_DRIVE_DIR, 'cases-data.js'), jsContent, 'utf8');
        fs.writeFileSync(path.join(E_DRIVE_DIR, 'cases.json'), JSON.stringify(cases, null, 2), 'utf8');
        fs.writeFileSync(path.join(E_DRIVE_DIR, 'standalone.json'), JSON.stringify(standalone, null, 2), 'utf8');
        const eJsonDir = path.join(E_DRIVE_DIR, 'json');
        if (!fs.existsSync(eJsonDir)) fs.mkdirSync(eJsonDir, { recursive: true });
        for (const c of cases) {
          const slug = (c.title || 'case').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 30);
          fs.writeFileSync(path.join(eJsonDir, `${c.id}_${slug}.json`), JSON.stringify(c, null, 2), 'utf8');
        }
        for (const s of standalone) {
          const slug = (s.title || 'standalone').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 30);
          fs.writeFileSync(path.join(eJsonDir, `${s.id}_${slug}.json`), JSON.stringify(s, null, 2), 'utf8');
        }
        console.log(`[OK] Mirrored to E: drive folder: ${E_DRIVE_DIR}`);
      } catch (e) {
        console.warn(`[WARN] Could not mirror to E: drive folder: ${e.message}`);
      }
    }

    console.log('\n================================================================');
    console.log('  SUCCESS! All cloud data is safely saved to your local disk.');
    console.log('================================================================');
  } catch (err) {
    console.error('\n[ERROR] Sync failed:', err.message);
    process.exit(1);
  }
}

runSync();
