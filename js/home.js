/* Home: the student's first page (#home-view). A dashboard in the style of paid question banks:
   continue an unfinished session, open a case study or question by code or link (js/short-codes.js),
   quick starts (only while the question bank is open to this visitor), and this device's progress.

   Everything here comes from this browser (js/attempts.js, js/progress.js); nothing is sent anywhere.
   When student accounts exist, the same panels can show the account's data instead. */

function homePortalOpen() {
  return studentPortalOpenForViewer();
}

function renderHomeView() {
  const progress = loadProgress();
  const attempts = resumableAttempts();
  const returning = progress.sessions.length > 0 || attempts.length > 0;
  const open = homePortalOpen();

  document.getElementById('home-title').textContent = returning ? 'Welcome back' : 'Welcome';
  document.getElementById('home-sub').textContent = open
    ? 'Pick up where you left off, open what your instructor shared, or start a new practice session.'
    : 'Your instructor shares case studies and questions with a code or a link. The full question bank opens later.';
  renderAuthorPreviewNote(document.getElementById('home-preview-note'));

  renderHomeContinue(attempts);
  renderHomeQuickStart(open);
  renderHomeDevice(progress);
  renderPractiseNavState();
}

// The author trying out the practice site: what is different for them, and the way back to the studio.
function renderAuthorPreviewNote(el) {
  if (!el) return;
  const on = isAuthorPreview();
  el.classList.toggle('hidden', !on);
  if (!on) { el.innerHTML = ''; return; }
  el.innerHTML = `<span><strong>Preview as a student.</strong> You are ${isAdminLoggedIn ? 'signed in as the author' : 'on your own computer'}, so nothing you do here is kept: sessions and progress last only until you close this tab.${STUDENT_PORTAL_OPEN ? '' : ' Students see this site without Practise until you open the question bank.'}</span>`;
}

// The sidebar's Practise entry says when it is not open yet.
function renderPractiseNavState() {
  const open = homePortalOpen();
  const tag = document.getElementById('nav-practise-tag');
  const nav = document.getElementById('nav-practise');
  if (tag) tag.classList.toggle('hidden', open);
  if (nav) {
    if (open) nav.removeAttribute('aria-disabled'); else nav.setAttribute('aria-disabled', 'true');
    nav.title = open ? '' : 'Opens when your instructor opens the question bank';
  }
}

function renderHomeContinue(attempts) {
  const box = document.getElementById('home-continue');
  const list = document.getElementById('home-continue-list');
  const shown = attempts.slice(0, 3);
  box.classList.toggle('hidden', !shown.length);
  list.innerHTML = shown.map((a, i) => {
    const items = attemptBankItems(a) || [];
    const n = answeredCount(a);
    const pct = Math.round(n / Math.max(1, a.total) * 100);
    const one = items.length === 1 ? items[0] : null;
    const kind = !one ? 'Session' : (one.isStandalone ? 'Question' : 'Case study');
    const title = one ? (one.title || 'Untitled') : `${items.length} items`;
    const where = one && one.course && one.course !== 'Others' ? `${one.course} · ${unitParts(one.unit || one.topic).num}` : '';
    return `
      <div class="home-continue-row">
        <div class="home-ring" style="--pct:${pct}" aria-hidden="true"><span>${n}/${a.total}</span></div>
        <div class="home-continue-main">
          <div class="home-continue-meta"><span class="home-kind">${kind}</span>${escapeHTML([where, a.mode === 'test' ? 'Exam conditions' : 'Practice'].filter(Boolean).join(' · '))}</div>
          <strong>${escapeHTML(title)}</strong>
          <span class="muted">${n} of ${a.total} answered · saved ${escapeHTML(relativeTime(a.savedAt))}</span>
        </div>
        <button type="button" class="app-btn ${i === 0 ? 'primary' : ''}" data-home-resume="${escapeHTML(a.key)}">Continue</button>
      </div>`;
  }).join('');
}

function renderHomeQuickStart(open) {
  document.querySelectorAll('#home-quick [data-quick]').forEach(b => { b.disabled = !open; });
  document.getElementById('home-quick-note').classList.toggle('hidden', open);
}

function renderHomeDevice(progress) {
  const box = document.getElementById('home-device');
  const link = document.getElementById('home-progress-link');
  if (!progress.sessions.length) {
    link.classList.add('hidden');
    box.innerHTML = `
      <div class="home-empty">
        <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        <p><strong>Your results will appear here</strong> after your first case study or question: your score for each of the six clinical judgment steps, and what to practise again.</p>
        <p class="muted">${isAuthorPreview() ? 'Preview: they are kept in this tab only and cleared when you close it.' : 'They are kept in this browser only. Nothing is sent to your instructor or anyone else.'}</p>
      </div>`;
    return;
  }
  link.classList.remove('hidden');
  const s = summarizeProgress(progress);
  const steps = s.byStep.map(st => `
    <div class="home-step">
      <span>${escapeHTML(st.label)}</span>
      ${st.max ? progressMeter(st.score, st.max, st.label) : '<span class="meter" aria-hidden="true"></span>'}
      <em>${st.max ? `${percentOf(st.score, st.max)}%` : '—'}</em>
    </div>`).join('');
  box.innerHTML = `
    <div class="home-stats">
      <div><span class="home-stat-value">${s.sessions}</span><span class="home-stat-label">session${s.sessions === 1 ? '' : 's'}</span></div>
      <div><span class="home-stat-value">${percentOf(s.totals.score, s.totals.max)}%</span><span class="home-stat-label">average score</span></div>
      <div><span class="home-stat-value">${s.answered}</span><span class="home-stat-label">questions answered</span></div>
    </div>
    <h3 class="home-sub-title">By clinical judgment step <span class="muted">(case studies)</span></h3>
    <div class="home-steps">${steps}</div>
    ${s.revisit.length ? `<p class="home-revisit"><strong>${s.revisit.length}</strong> ${s.revisit.length === 1 ? 'item' : 'items'} to practise again in My progress.</p>` : ''}
    <div class="home-keep">
      <p>${isAuthorPreview() ? 'Preview: these results are cleared when you close this tab.' : 'Results stay in this browser. Export them to keep a copy or to move them to another device.'}</p>
      <button type="button" class="app-btn small" id="home-export-btn">Export</button>
    </div>`;
}

function homeOpenMode() {
  const checked = document.querySelector('input[name="home-open-mode"]:checked');
  return checked && checked.value === 'test' ? 'test' : 'review';
}

function showHomeOpenMessage(text) {
  const msg = document.getElementById('home-open-msg');
  msg.textContent = text;
  msg.classList.toggle('hidden', !text);
  document.getElementById('home-open-input').setAttribute('aria-invalid', text ? 'true' : 'false');
}

function openFromHome() {
  const input = document.getElementById('home-open-input');
  const text = input.value.trim();
  if (!text) { showHomeOpenMessage('Type a code such as C-7KD4M, or paste the link your instructor shared.'); input.focus(); return; }
  const req = parseOpenRequest(text);
  if (req.unknown.length) {
    const what = req.unknown.map(u => u.length > 40 ? `${u.slice(0, 40)}…` : u).join(', ');
    showHomeOpenMessage(req.unknown.length === 1 && !/[?=/]/.test(req.unknown[0])
      ? `No case study or question has the code ${what}. Check it with your instructor. Codes start with C (case study) or Q (question) and never use the letters O, I or L.`
      : `This does not match any case study or question: ${what}. Check it with your instructor.`);
    input.focus();
    return;
  }
  showHomeOpenMessage('');
  const mode = req.mode || homeOpenMode();
  input.value = '';
  if (req.items.length === 1) {
    startLinkSession(req.items[0], mode);
  } else {
    startCompiledSession(req.items.filter(i => !isStandaloneItem(i)), req.items.filter(isStandaloneItem), mode);
  }
}

function startQuickSession(kind) {
  if (!homePortalOpen()) return;
  if (kind === 'build') { switchView('student'); return; }
  if (kind === 'case') {
    const pool = studentCaseStudies();
    if (!pool.length) { showToast('No case studies are available yet.', 'warning'); return; }
    startCompiledSession([shuffleArray(pool.slice())[0]], [], 'review');
  } else {
    const pool = studentStandaloneQuestions();
    if (!pool.length) { showToast('No stand-alone questions are available yet.', 'warning'); return; }
    startCompiledSession([], shuffleArray(pool.slice()).slice(0, 10), 'review');
  }
}

function initHome() {
  document.getElementById('home-open-form').addEventListener('submit', e => { e.preventDefault(); openFromHome(); });
  document.getElementById('home-open-input').addEventListener('input', () => showHomeOpenMessage(''));
  const view = document.getElementById('home-view');
  view.addEventListener('click', e => {
    const resume = e.target.closest('[data-home-resume]');
    if (resume) {
      const saved = getAttempt(resume.dataset.homeResume);
      if (!saved || !resumeSavedAttempt(saved)) { showToast('This session can no longer be continued: its questions have changed.', 'warning'); renderHomeView(); }
      return;
    }
    const quick = e.target.closest('[data-quick]');
    if (quick) { startQuickSession(quick.dataset.quick); return; }
    if (e.target.closest('#home-export-btn')) exportProgress();
  });
  const pausedHome = document.getElementById('paused-home-btn');
  if (pausedHome) pausedHome.addEventListener('click', () => switchView('home'));
}
