// NCLEX NGN Case Study Studio - Server Configuration
const http = require('http');
const fs = require('fs');
const path = require('path');


const PORT = 3000;
const PUBLIC_DIR = __dirname;

// Helper to determine content type from file extension
const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

function saveAllFiles(cases, standalone) {
  // 1. cases-data.js
  const jsContent = `window.NCLEX_CASES = ${JSON.stringify(cases, null, 2)};\n\nwindow.NCLEX_STANDALONE = ${JSON.stringify(standalone, null, 2)};\n`;
  const jsPath = path.join(PUBLIC_DIR, 'cases-data.js');
  fs.writeFileSync(jsPath, jsContent, 'utf8');

  // 2. cases.json
  const casesJsonPath = path.join(PUBLIC_DIR, 'cases.json');
  fs.writeFileSync(casesJsonPath, JSON.stringify(cases, null, 2), 'utf8');

  // 3. standalone.json
  const standaloneJsonPath = path.join(PUBLIC_DIR, 'standalone.json');
  fs.writeFileSync(standaloneJsonPath, JSON.stringify(standalone, null, 2), 'utf8');

  // 4. Individual json files in json/ folder
  const jsonDir = path.join(PUBLIC_DIR, 'json');
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

  // 5. Desktop backup mirror is disabled in NCLEX_Claude: that folder belongs
  // to the original app, and this experimental copy must not overwrite it.
  const desktopDir = path.join('C:', 'Users', 'thada', 'Desktop', 'Antigravity', 'NCLEX Application');
  const MIRROR_TO_ORIGINAL_DESKTOP_BACKUP = false;
  if (MIRROR_TO_ORIGINAL_DESKTOP_BACKUP && fs.existsSync(desktopDir)) {
    try {
      fs.writeFileSync(path.join(desktopDir, 'cases-data.js'), jsContent, 'utf8');
      fs.writeFileSync(path.join(desktopDir, 'cases.json'), JSON.stringify(cases, null, 2), 'utf8');
      fs.writeFileSync(path.join(desktopDir, 'standalone.json'), JSON.stringify(standalone, null, 2), 'utf8');
      const desktopJsonDir = path.join(desktopDir, 'json');
      if (!fs.existsSync(desktopJsonDir)) fs.mkdirSync(desktopJsonDir, { recursive: true });
      for (const c of cases) {
        const slug = (c.title || 'case').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 30);
        fs.writeFileSync(path.join(desktopJsonDir, `${c.id}_${slug}.json`), JSON.stringify(c, null, 2), 'utf8');
      }
      for (const s of standalone) {
        const slug = (s.title || 'standalone').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 30);
        fs.writeFileSync(path.join(desktopJsonDir, `${s.id}_${slug}.json`), JSON.stringify(s, null, 2), 'utf8');
      }
    } catch (e) {
      console.warn('[NCLEX BACKEND] Desktop mirror error:', e.message);
    }
  }
}

const server = http.createServer((req, res) => {
  // Handle POST api save
  if (req.method === 'POST' && req.url === '/api/save') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        if (!data.cases || !data.standalone) {
          throw new Error("Missing 'cases' or 'standalone' property in request body.");
        }
        
        saveAllFiles(data.cases, data.standalone);
        
        console.log(`[NCLEX BACKEND] Directly wrote updates to cases-data.js, cases.json, standalone.json, and json/ folder.`);
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, message: 'Data saved successfully to disk and json/ folder!' }));
      } catch (err) {
        console.error('[NCLEX BACKEND] Save error:', err.message);
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      }
    });
    return;
  }

  // Handle static file serving (GET requests)
  if (req.method === 'GET') {
    // Prevent directory traversal
    let safeUrl = req.url.split('?')[0].split('#')[0];
    if (safeUrl === '/') {
      safeUrl = '/index.html';
    }

    const filePath = path.join(PUBLIC_DIR, safeUrl);
    
    // Check if path is actually inside the repo folder
    if (!filePath.startsWith(PUBLIC_DIR)) {
      res.writeHead(403, { 'Content-Type': 'text/plain' });
      res.end('403 Forbidden');
      return;
    }

    fs.exists(filePath, (exists) => {
      if (!exists) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
        return;
      }

      // Check if directory
      if (fs.statSync(filePath).isDirectory()) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('403 Forbidden');
        return;
      }

      const ext = path.extname(filePath).toLowerCase();
      const contentType = MIME_TYPES[ext] || 'application/octet-stream';

      res.writeHead(200, { 'Content-Type': contentType });
      
      // Stream file output
      const stream = fs.createReadStream(filePath);
      stream.on('error', (err) => {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('500 Internal Server Error');
      });
      stream.pipe(res);
    });
    return;
  }

  // Fallback for other HTTP methods
  res.writeHead(405, { 'Content-Type': 'text/plain' });
  res.end('405 Method Not Allowed');
});

server.listen(PORT, () => {
  console.log('================================================================');
  console.log(`  NCLEX NGN Case Study Studio is running at:`);
  console.log(`  http://localhost:${PORT}`);
  console.log('================================================================');
  console.log('  Press Ctrl+C in this terminal window to stop the server.');
  console.log('  All saves inside the editor will write directly to your disk.');
});
