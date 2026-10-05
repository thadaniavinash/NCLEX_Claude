/* Studio only: "Share with students" for one case study or stand-alone question. Gives two links, one
   for Practice (feedback and rationale after each question) and one for Exam conditions (&mode=test:
   no going back, results at the end), each with Copy and a QR code to show on the projector.

   Links always point at the published app (STUDENT_SITE_URL in js/state.js) and open the item even when
   it is hidden from the student portal (draft or unfinished): main.js opens any item named in a link.
   Students see nothing of this; the dialog is reached from the Question bank and the editor. */

let shareDialogItem = null;
let shareQrMode = null;

function studentSiteBase() {
  const { hostname, origin, pathname } = window.location;
  return hostname.endsWith('github.io') ? origin + pathname : STUDENT_SITE_URL;
}

function studentLink(item, mode) {
  const param = item.isStandalone ? 'standalone' : 'case';
  return `${studentSiteBase()}?${param}=${encodeURIComponent(item.id)}${mode === 'test' ? '&mode=test' : ''}`;
}

// The QR library is only needed here, so it loads the first time a code is shown.
let qrLibraryPromise = null;
function loadQrLibrary() {
  if (typeof qrcode === 'function') return Promise.resolve();
  if (!qrLibraryPromise) {
    qrLibraryPromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'js/vendor/qrcode.js';
      script.onload = resolve;
      script.onerror = () => { qrLibraryPromise = null; reject(new Error('QR library failed to load')); };
      document.head.appendChild(script);
    });
  }
  return qrLibraryPromise;
}

const SHARE_MODES = [
  { mode: 'review', name: 'Practice', badge: 'Recommended for class',
    text: 'After each question students see whether they were right and the rationale. They can go back.' },
  { mode: 'test', name: 'Exam', badge: 'Before a midterm or final',
    text: 'Like the NCLEX: no going back and no feedback until the end, then results and rationales.' }
];

function shareStatusHTML(item, fromEditor) {
  const notes = [];
  const problems = itemProblems(item).filter(p => p !== 'marked as draft');
  if (problems.length) {
    notes.push({ tone: 'warn', text: `Not finished: ${problems.slice(0, 3).join('; ')}${problems.length > 3 ? `; and ${problems.length - 3} more` : ''}. Students who open the link will meet these problems.` });
  }
  if (fromEditor && typeof editorDirty !== 'undefined' && editorDirty) {
    notes.push({ tone: 'warn', text: 'You have unsaved changes. Students get the last saved version, so save first.' });
  }
  if (isDatabaseUnavailable) {
    notes.push({ tone: 'warn', text: 'The database could not be reached, so this is the backup copy. The link works for items saved in the database.' });
  }
  notes.push(isReadyForStudents(item)
    ? { tone: 'info', text: 'Also listed in the student portal (Practise page).' }
    : { tone: 'info', text: 'Hidden from the student portal. Only students with the link can open it.' });
  return notes.map(n => `<p class="share-note ${n.tone}">${escapeHTML(n.text)}</p>`).join('');
}

function openShareDialog(item, opts = {}) {
  closeShareDialog();
  shareDialogItem = item;
  shareQrMode = null;
  const kind = item.isStandalone ? 'Stand-alone question' : 'Case study';
  const backdrop = document.createElement('div');
  backdrop.id = 'share-dialog';
  backdrop.className = 'share-backdrop';
  backdrop.innerHTML = `
    <div class="share-dialog" role="dialog" aria-modal="true" aria-labelledby="share-title">
      <div class="share-head">
        <div>
          <h2 id="share-title">Share with students</h2>
          <p class="share-item"><strong>${escapeHTML(item.title || 'Untitled')}</strong> · ${kind}</p>
        </div>
        <button type="button" class="share-close" data-share-close aria-label="Close">&times;</button>
      </div>
      <div class="share-notes">${shareStatusHTML(item, opts.fromEditor)}</div>
      <div class="share-options">
        ${SHARE_MODES.map(m => `
          <section class="share-option" data-share-mode="${m.mode}">
            <div class="share-option-head"><strong>${m.name}</strong><span class="share-badge">${m.badge}</span></div>
            <p>${m.text}</p>
            <div class="share-link-row">
              <input type="text" readonly value="${escapeHTML(studentLink(item, m.mode))}" aria-label="${m.name} link" id="share-link-${m.mode}">
              <button type="button" class="app-btn primary small" data-share-copy="${m.mode}">Copy</button>
            </div>
            <button type="button" class="share-qr-btn" data-share-qr="${m.mode}" aria-pressed="false">Show QR code</button>
          </section>`).join('')}
      </div>
      <div class="share-qr hidden" id="share-qr">
        <div class="share-qr-code" id="share-qr-code"></div>
        <div class="share-qr-side">
          <p id="share-qr-caption"></p>
          <button type="button" class="app-btn small" data-share-qr-large aria-pressed="false">Larger for the projector</button>
        </div>
      </div>
      <p class="share-foot">Each student's answers are saved on their own device, so a refresh or a closed tab does not lose them. Nothing is sent to you.</p>
    </div>`;
  document.body.appendChild(backdrop);
  backdrop.addEventListener('click', onShareDialogClick);
  backdrop.querySelector('[data-share-copy="review"]').focus();
}

function closeShareDialog() {
  const d = document.getElementById('share-dialog');
  if (d) d.remove();
  shareDialogItem = null;
}

async function copyShareLink(mode, button) {
  const input = document.getElementById(`share-link-${mode}`);
  let copied = false;
  try {
    await navigator.clipboard.writeText(input.value);
    copied = true;
  } catch (e) {
    input.focus();
    input.select();
    try { copied = document.execCommand('copy'); } catch (err) { copied = false; }
  }
  button.textContent = copied ? 'Copied' : 'Select and copy';
  setTimeout(() => { if (button.isConnected) button.textContent = 'Copy'; }, 2000);
}

async function showShareQr(mode) {
  const panel = document.getElementById('share-qr');
  document.querySelectorAll('[data-share-qr]').forEach(b => {
    const on = b.dataset.shareQr === mode && shareQrMode !== mode;
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    b.textContent = on ? 'Hide QR code' : 'Show QR code';
  });
  if (shareQrMode === mode) { shareQrMode = null; panel.classList.add('hidden'); return; }
  shareQrMode = mode;
  const url = studentLink(shareDialogItem, mode);
  const name = SHARE_MODES.find(m => m.mode === mode).name;
  const box = document.getElementById('share-qr-code');
  panel.classList.remove('hidden');
  box.textContent = 'Loading…';
  try {
    await loadQrLibrary();
    const qr = qrcode(0, 'M');
    qr.addData(url);
    qr.make();
    box.innerHTML = qr.createSvgTag({ cellSize: 4, margin: 16, scalable: true, title: `QR code for the ${name} link` });
  } catch (e) {
    box.textContent = 'The QR code could not be made. Copy the link instead.';
  }
  document.getElementById('share-qr-caption').innerHTML =
    `<strong>${name} link</strong><br>Students scan it with their phone camera. It opens ${escapeHTML(shareDialogItem.title || 'the item')}${mode === 'test' ? ' under exam conditions' : ''}.`;
}

function onShareDialogClick(e) {
  const t = e.target;
  if (t.id === 'share-dialog' || t.closest('[data-share-close]')) { closeShareDialog(); return; }
  const copy = t.closest('[data-share-copy]');
  if (copy) { copyShareLink(copy.dataset.shareCopy, copy); return; }
  const qr = t.closest('[data-share-qr]');
  if (qr) { showShareQr(qr.dataset.shareQr); return; }
  const large = t.closest('[data-share-qr-large]');
  if (large) {
    const on = document.getElementById('share-qr').classList.toggle('large');
    large.setAttribute('aria-pressed', on ? 'true' : 'false');
    large.textContent = on ? 'Smaller' : 'Larger for the projector';
    return;
  }
  if (t.matches('input[readonly]')) t.select();
}

function initShareDialog() {
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && document.getElementById('share-dialog')) closeShareDialog();
  });
}
