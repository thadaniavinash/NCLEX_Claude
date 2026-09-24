// One-time copy of the original app's data into NCLEX_Claude's own Supabase project.
// The original database is only READ (GET); every write goes to the new project.
//
// Usage: node copy-from-original-supabase.js <NEW_SUPABASE_URL> <NEW_PUBLISHABLE_KEY>
// Run supabase/setup.sql in the new project first.

const ORIGINAL_URL = 'https://taprukpiubqsckahocaz.supabase.co';
const ORIGINAL_KEY = 'sb_publishable_V1u7recZMcdc2-DXhoMwoQ_BEVWej3g';

const [newUrl, newKey] = process.argv.slice(2);
if (!newUrl || !newKey) {
  console.error('Usage: node copy-from-original-supabase.js <NEW_SUPABASE_URL> <NEW_PUBLISHABLE_KEY>');
  process.exit(1);
}
if (newUrl.replace(/\/+$/, '') === ORIGINAL_URL) {
  console.error('Refusing to run: the destination is the original database.');
  process.exit(1);
}

const headers = key => ({ apikey: key, Authorization: `Bearer ${key}` });

async function main() {
  const res = await fetch(`${ORIGINAL_URL}/rest/v1/nclex_data?select=key,data`, { headers: headers(ORIGINAL_KEY) });
  if (!res.ok) throw new Error(`Reading original failed: ${res.status} ${await res.text()}`);
  const records = await res.json();

  for (const key of ['cases', 'standalone']) {
    const rec = records.find(r => r.key === key);
    if (!rec || !Array.isArray(rec.data)) throw new Error(`Original has no '${key}' row`);

    const put = await fetch(`${newUrl}/rest/v1/nclex_data?key=eq.${key}`, {
      method: 'PATCH',
      headers: { ...headers(newKey), 'Content-Type': 'application/json', Prefer: 'return=representation' },
      body: JSON.stringify({ data: rec.data })
    });
    const written = put.ok ? await put.json() : null;
    if (!put.ok || !written.length) {
      throw new Error(`Writing '${key}' to new project failed (${put.status}). Did you run supabase/setup.sql?`);
    }

    const check = await fetch(`${newUrl}/rest/v1/nclex_data?key=eq.${key}&select=data`, { headers: headers(newKey) });
    const [{ data }] = await check.json();
    const same = JSON.stringify(data) === JSON.stringify(rec.data);
    console.log(`${key}: copied ${rec.data.length} items, verified ${same ? 'identical' : 'MISMATCH'}`);
    if (!same) process.exit(1);
  }
}

main().catch(e => { console.error(e.message); process.exit(1); });
