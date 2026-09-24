// Script to migrate existing cases-data.js content into Supabase

// Disabled in NCLEX_Claude: this experimental copy must not overwrite the
// original app's live Supabase data. Remove this guard only after pointing
// the URL and key below at a Supabase project dedicated to this copy.
console.error('upload-to-supabase.js is disabled in NCLEX_Claude to protect the original app\'s database.');
process.exit(1);
const fs = require('fs');
const path = require('path');
const https = require('https');

// Define global.window to evaluate the cases-data.js file
global.window = {};
require('./cases-data.js');

const cases = global.window.NCLEX_CASES || [];
const standalone = global.window.NCLEX_STANDALONE || [];

console.log(`Read ${cases.length} cases and ${standalone.length} standalone questions from cases-data.js.`);

const supabaseUrl = 'https://taprukpiubqsckahocaz.supabase.co';
const apiKey = 'sb_publishable_V1u7recZMcdc2-DXhoMwoQ_BEVWej3g';

function uploadData(key, payload) {
  return new Promise((resolve, reject) => {
    const url = `${supabaseUrl}/rest/v1/nclex_data?key=eq.${key}`;
    const requestData = JSON.stringify({ data: payload });

    const parsedUrl = new URL(url);
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'apikey': apiKey,
        'Authorization': `Bearer ${apiKey}`,
        'Prefer': 'return=representation'
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          console.log(`Successfully uploaded ${key} data to Supabase (Status: ${res.statusCode})`);
          resolve(body);
        } else {
          reject(new Error(`Failed to upload ${key}. Status: ${res.statusCode}, Body: ${body}`));
        }
      });
    });

    req.on('error', (err) => reject(err));
    req.write(requestData);
    req.end();
  });
}

async function runMigration() {
  try {
    console.log('Migrating cases data...');
    await uploadData('cases', cases);

    console.log('Migrating standalone questions data...');
    await uploadData('standalone', standalone);

    console.log('Migration completed successfully!');
  } catch (err) {
    console.error('Migration failed:', err);
    process.exit(1);
  }
}

runMigration();
