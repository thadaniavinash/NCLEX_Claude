/* Unfinished sessions, kept in this browser so a refresh, a closed tab or a laptop going to sleep does
   not lose a student's answers.

   A session is saved while the student works (after answers and moves, and when the page is hidden)
   and removed when its results are shown. Two kinds are kept (ATTEMPT_STORAGE_KEY):
   - link sessions (a case study or question opened from a link the author shared), one per item and
     mode, key "link:<id>:<mode>". Reopening the link offers "Continue where you left off?".
   - the latest session started from the Practise page, key "portal"; the Practise page shows a
     "Continue your session" banner.
   Only item ids are stored (not question content). A saved session is dropped when one of its items
   has been edited since (its `updatedAt` or number of screens differ), so answers never land on
   changed questions. Sessions started from the studio or the editor preview are never saved. */

const ATTEMPT_STORAGE_KEY = 'nclex_attempts_v1';
const ATTEMPT_MAX_LINK = 20; // link sessions kept (oldest dropped)

function loadAttempts() {
  try {
    const data = JSON.parse(localStorage.getItem(ATTEMPT_STORAGE_KEY) || '{}');
    return data && typeof data === 'object' ? data : {};
  } catch (e) {
    return {};
  }
}

function storeAttempts(data) {
  const links = Object.values(data).filter(a => a.key.startsWith('link:'))
    .sort((a, b) => String(b.savedAt).localeCompare(String(a.savedAt)));
  links.slice(ATTEMPT_MAX_LINK).forEach(a => { delete data[a.key]; });
  try {
    localStorage.setItem(ATTEMPT_STORAGE_KEY, JSON.stringify(data));
    return true;
  } catch (e) {
    return false;
  }
}

function itemFingerprint(item) {
  return `${item.updatedAt || ''}|${(item.screens || []).length}`;
}

function linkAttemptKey(item, mode) {
  return `link:${item.id}:${mode === 'test' ? 'test' : 'review'}`;
}

function getAttempt(key) {
  return loadAttempts()[key] || null;
}

function clearAttempt(key) {
  if (!key) return;
  const data = loadAttempts();
  if (data[key]) {
    delete data[key];
    storeAttempts(data);
  }
}

function answeredCount(attempt) {
  return Object.values(attempt.submitted || {}).filter(Boolean).length;
}

// Saves the running session (called often; cheap when nothing is running).
function saveCurrentAttempt() {
  const key = sessionConfig && sessionConfig.attemptKey;
  if (!key || sessionConfig.isRemediation || sessionConfig.progressRecorded || !currentCase) return;
  const refs = sessionConfig.attemptItems || [];
  const data = loadAttempts();
  data[key] = {
    key,
    savedAt: new Date().toISOString(),
    mode: sessionConfig.mode === 'test' ? 'test' : 'review',
    title: currentCase.title || '',
    items: refs,
    step: playerStepIndex,
    total: currentCase.screens.length,
    answers: playerAnswers,
    submitted: submittedAnswers,
    scores: playerScores
  };
  storeAttempts(data);
}

let attemptSaveTimer = null;
function scheduleAttemptSave() {
  clearTimeout(attemptSaveTimer);
  attemptSaveTimer = setTimeout(saveCurrentAttempt, 400);
}

// The bank items a saved session refers to, in order; null when one is gone or has changed.
function attemptBankItems(attempt) {
  const items = (attempt.items || []).map(ref => {
    const item = findBankItem(ref.id);
    return item && itemFingerprint(item) === ref.fp ? item : null;
  });
  return items.length && items.every(Boolean) ? items : null;
}

// Puts the saved answers back into the player that was just started for the same items.
function applyAttempt(attempt) {
  playerAnswers = attempt.answers || {};
  submittedAnswers = attempt.submitted || {};
  playerScores = attempt.scores || {};
  const step = Math.min(Math.max(0, attempt.step || 0), currentCase.screens.length - 1);
  playerMobilePaneStep = null;
  renderPlayerStep(step);
}

/* ---- Link sessions ---- */

// Opens an item from a shared link (?case= / ?standalone=, optional &mode=test). Hidden items open too:
// the author decides who gets the link. Offers to continue a saved attempt.
function startLinkSession(item, mode) {
  const config = { mode, isRemediation: false, allowBacktrack: mode !== 'test', source: 'link' };
  const key = linkAttemptKey(item, mode);
  startPlayer(item, Object.assign(config, { attemptKey: key, attemptItems: [{ id: item.id, fp: itemFingerprint(item) }] }));
  const saved = getAttempt(key);
  if (!saved) return;
  if (!attemptBankItems(saved)) { clearAttempt(key); return; } // edited since: start fresh
  if (answeredCount(saved) === 0 && !saved.step) return;
  showResumeModal(saved, () => applyAttempt(saved), () => { clearAttempt(key); });
}

function showResumeModal(attempt, onContinue, onStartOver) {
  const modal = document.getElementById('resume-modal');
  if (!modal) return;
  const n = answeredCount(attempt);
  document.getElementById('resume-modal-text').textContent =
    `You answered ${n} of ${attempt.total} question${attempt.total === 1 ? '' : 's'} on this device (last saved ${relativeTime(attempt.savedAt)}).`;
  modal.classList.remove('hidden');
  const yes = document.getElementById('resume-modal-continue-btn');
  const no = document.getElementById('resume-modal-restart-btn');
  const close = () => { modal.classList.add('hidden'); yes.onclick = null; no.onclick = null; };
  yes.onclick = () => { close(); onContinue(); };
  no.onclick = () => { close(); onStartOver(); };
  yes.focus();
}

/* ---- Practise page banner ---- */

function renderPortalResume() {
  const box = document.getElementById('portal-resume');
  if (!box) return;
  const saved = getAttempt('portal');
  const items = saved && attemptBankItems(saved);
  if (saved && !items) clearAttempt('portal');
  if (!items) { box.classList.add('hidden'); box.innerHTML = ''; return; }
  const n = answeredCount(saved);
  const pct = Math.round(n / Math.max(1, saved.total) * 100);
  box.innerHTML = `
    <div class="portal-resume-text">
      <strong>Continue your ${saved.mode === 'test' ? 'exam' : 'practice'} session</strong>
      <span>${n} of ${saved.total} questions answered · saved ${escapeHTML(relativeTime(saved.savedAt))}</span>
      <span class="meter" aria-hidden="true"><span class="meter-fill" style="width:${pct}%"></span></span>
    </div>
    <button type="button" class="app-btn primary" id="portal-resume-continue">Continue</button>
    <button type="button" class="app-btn" id="portal-resume-discard">Discard</button>`;
  box.classList.remove('hidden');
  document.getElementById('portal-resume-continue').addEventListener('click', () => {
    const cases = items.filter(i => !i.isStandalone);
    const singles = items.filter(i => i.isStandalone);
    startCompiledSession(cases, singles, saved.mode);
    applyAttempt(saved);
  });
  document.getElementById('portal-resume-discard').addEventListener('click', () => {
    clearAttempt('portal');
    renderPortalResume();
  });
}

function initAttemptSaving() {
  const view = document.getElementById('player-view');
  if (!view) return;
  // Answers are kept in playerAnswers by many handlers (clicks, selects, drag and drop): save shortly
  // after any of them, and straight away when the page is hidden, closed or reloaded.
  ['click', 'change', 'input', 'drop', 'dragend', 'pointerup', 'keyup'].forEach(type =>
    view.addEventListener(type, scheduleAttemptSave, true));
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') saveCurrentAttempt(); });
  window.addEventListener('pagehide', saveCurrentAttempt);
}
