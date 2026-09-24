// NCLEX NGN Case Study Studio - Server Configuration
const http = require('http');
const fs = require('fs');
const path = require('path');


const PORT = 3000;
const PUBLIC_DIR = __dirname;
const MAX_BODY_BYTES = 50 * 1024 * 1024; // the whole bank, including embedded images

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

// cases-data.js is the single source of question data. Write it to a temporary
// file first and rename, so a crash mid-write cannot leave a truncated bank.
function saveAllFiles(cases, standalone) {
  const jsContent = `window.NCLEX_CASES = ${JSON.stringify(cases, null, 2)};\n\nwindow.NCLEX_STANDALONE = ${JSON.stringify(standalone, null, 2)};\n`;
  const jsPath = path.join(PUBLIC_DIR, 'cases-data.js');
  const tmpPath = jsPath + '.tmp';
  fs.writeFileSync(tmpPath, jsContent, 'utf8');
  fs.renameSync(tmpPath, jsPath);
}

// Resolve a request path to a file inside PUBLIC_DIR, or null if it points
// outside it or into a hidden file or folder such as .git.
function resolvePublicPath(urlPath) {
  let decoded;
  try {
    decoded = decodeURIComponent(urlPath);
  } catch (e) {
    return null;
  }
  const filePath = path.resolve(PUBLIC_DIR, '.' + path.posix.normalize('/' + decoded));
  const relative = path.relative(PUBLIC_DIR, filePath);
  if (relative.startsWith('..') || path.isAbsolute(relative)) return null;
  if (relative.split(path.sep).some(part => part.startsWith('.'))) return null;
  return filePath;
}

const server = http.createServer((req, res) => {
  // Handle POST api save
  if (req.method === 'POST' && req.url === '/api/save') {
    let body = '';
    let tooLarge = false;
    req.on('data', chunk => {
      if (tooLarge) return;
      body += chunk.toString();
      if (body.length > MAX_BODY_BYTES) {
        tooLarge = true;
        res.writeHead(413, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: 'Request body too large.' }));
        req.destroy();
      }
    });

    req.on('end', () => {
      if (tooLarge) return;
      try {
        const data = JSON.parse(body);
        if (!Array.isArray(data.cases) || !Array.isArray(data.standalone)) {
          throw new Error("Request body must contain 'cases' and 'standalone' arrays.");
        }

        saveAllFiles(data.cases, data.standalone);

        console.log(`[NCLEX BACKEND] Saved ${data.cases.length} case studies and ${data.standalone.length} stand-alone questions to cases-data.js.`);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, message: 'Data saved successfully to cases-data.js!' }));
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
    let safeUrl = req.url.split('?')[0].split('#')[0];
    if (safeUrl === '/') {
      safeUrl = '/index.html';
    }

    const filePath = resolvePublicPath(safeUrl);
    if (!filePath) {
      res.writeHead(403, { 'Content-Type': 'text/plain' });
      res.end('403 Forbidden');
      return;
    }

    fs.stat(filePath, (err, stats) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
        return;
      }

      if (stats.isDirectory()) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('403 Forbidden');
        return;
      }

      const ext = path.extname(filePath).toLowerCase();
      const contentType = MIME_TYPES[ext] || 'application/octet-stream';

      res.writeHead(200, { 'Content-Type': contentType });

      // Stream file output
      const stream = fs.createReadStream(filePath);
      stream.on('error', () => {
        res.end();
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
  console.log('  All saves inside the editor will write directly to cases-data.js.');
});
