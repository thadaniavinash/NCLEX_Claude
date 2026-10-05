/* Results view (scoreboard) and remediation review. */

/* ================= RESULTS VIEW (SCOREBOARD) ================= */
function initResultsEvents() {
  document.getElementById('results-retry-btn').addEventListener('click', () => {
    const { mode, source, attemptKey, attemptItems } = sessionConfig;
    if (attemptKey) clearAttempt(attemptKey);
    startPlayer(currentCase, { mode, isRemediation: false, source, attemptKey, attemptItems });
  });
  
  document.getElementById('results-dashboard-btn').addEventListener('click', leaveSession);
  document.getElementById('results-progress-btn').addEventListener('click', () => switchView('progress'));

  const reviewAnswersBtn = document.getElementById('results-review-answers-btn');
  if (reviewAnswersBtn) {
    reviewAnswersBtn.addEventListener('click', () => {
      startRemediationReview(0);
    });
  }
}

// Where a session returns to: the question bank when the author launched it from the studio, a
// "paused" page for a case study opened from a shared link (its answers stay saved for later),
// otherwise the student portal.
function leaveSession() {
  if (sessionConfig.source === 'studio') { switchView('dashboard'); return; }
  if (sessionConfig.source === 'link' && !sessionConfig.progressRecorded) { showPausedLinkSession(); return; }
  switchView('student');
}

function showPausedLinkSession() {
  saveCurrentAttempt();
  const item = currentCase;
  const mode = sessionConfig.mode;
  const saved = getAttempt(sessionConfig.attemptKey);
  document.getElementById('paused-title').textContent = item.title || 'Case study';
  document.getElementById('paused-text').textContent = saved && answeredCount(saved)
    ? `You answered ${answeredCount(saved)} of ${saved.total} questions. Your answers are saved on this device: continue now, or open the same link later.`
    : 'You have not answered any questions yet. Open the same link later, or start now.';
  document.getElementById('paused-continue-btn').onclick = () => {
    const again = getAttempt(linkAttemptKey(item, mode));
    startPlayer(item, Object.assign({}, sessionConfig, { isRemediation: false, progressRecorded: false, progressSaved: false }));
    if (again) applyAttempt(again);
  };
  document.getElementById('paused-restart-btn').onclick = () => {
    clearAttempt(linkAttemptKey(item, mode));
    startPlayer(item, Object.assign({}, sessionConfig, { isRemediation: false, progressRecorded: false, progressSaved: false }));
  };
  switchView('paused');
}

function startRemediationReview(jumpIdx = 0) {
  sessionConfig.isRemediation = true;
  sessionConfig.allowBacktrack = true;
  currentCase.screens.forEach((s, idx) => {
    submittedAnswers[idx] = true;
    if (!playerScores[idx]) evaluateStepScore(idx);
  });
  playerMobilePaneStep = null;
  switchView('player');
  renderPlayerStep(jumpIdx);
}

function loadResultsView() {
  // Screens the student answered themselves (the rest are scored 0 below).
  const answeredSteps = currentCase.screens.map((s, idx) => !!submittedAnswers[idx]);
  currentCase.screens.forEach((s, idx) => {
    if (!submittedAnswers[idx]) {
      submittedAnswers[idx] = true;
      evaluateStepScore(idx);
      if (!playerScores[idx]) {
        playerScores[idx] = { score: 0, max: 1 };
      }
      playerScores[idx].score = 0; // auto zero if skipped
    }
  });
  
  let totalScore = 0;
  let totalMax = 0;
  
  Object.values(playerScores).forEach(s => {
    totalScore += s.score;
    totalMax += s.max;
  });
  
  const percent = totalMax > 0 ? Math.round((totalScore / totalMax) * 100) : 0;
  
  document.getElementById('results-case-title').textContent = currentCase.title;
  // Heading and icon match how the session went, instead of always celebrating.
  const outcome = percent >= 80
    ? { tone: 'good', heading: 'Great work!', message: 'Review the rationales to lock in what you got right.',
        icon: '<svg viewBox="0 0 24 24" width="40" height="40" stroke="currentColor" stroke-width="2" fill="none"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>' }
    : percent >= 50
      ? { tone: 'fair', heading: 'Session complete', message: 'Good progress. Review the questions you missed to see where points were lost.',
          icon: '<svg viewBox="0 0 24 24" width="40" height="40" stroke="currentColor" stroke-width="2" fill="none"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>' }
      : { tone: 'low', heading: 'Session complete', message: 'This topic needs more practice. Work through the rationales, then try these questions again.',
          icon: '<svg viewBox="0 0 24 24" width="40" height="40" stroke="currentColor" stroke-width="2" fill="none"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>' };
  const iconEl = document.getElementById('results-icon');
  if (iconEl) { iconEl.innerHTML = outcome.icon; iconEl.dataset.tone = outcome.tone; }
  document.getElementById('results-heading').textContent = outcome.heading;
  document.getElementById('results-message').textContent = outcome.message;
  document.getElementById('results-score').textContent = `${totalScore} / ${totalMax}`;
  document.getElementById('results-percentage').textContent = `${percent}%`;
  
  const list = document.getElementById('results-breakdown-list');
  list.innerHTML = '';
  
  currentCase.screens.forEach((s, idx) => {
    const sc = playerScores[idx] || { score: 0, max: 1 };
    const typeLabel = getQuestionTypeLabel(s.question.type || '') || 'Question';
    const isStepStandalone = currentCase.isStandalone || s.isStandalone;
    const contextLabel = isStepStandalone ? 'Stand-alone Question' : (s.caseTitle || currentCase.title || `Screen ${idx + 1}`);
    
    let badgeClass = 'incorrect';
    let badgeText = 'Incorrect';
    
    if (sc.score === sc.max) {
      badgeClass = 'correct';
      badgeText = 'Correct';
    } else if (sc.score > 0) {
      badgeClass = 'partial';
      badgeText = 'Partial';
    }
    
    const item = document.createElement('button');
    item.type = 'button';
    item.className = 'breakdown-item';
    item.title = 'Review this question and its rationale';
    item.innerHTML = `
      <span class="breakdown-badge ${badgeClass}">${badgeText}</span>
      <span class="breakdown-item-main">
        <strong>Question ${idx + 1}</strong>
        <span class="breakdown-context">${escapeHTML(contextLabel)} &bull; ${escapeHTML(typeLabel)}</span>
      </span>
      <span class="breakdown-score">${sc.score} / ${sc.max} pts</span>
      <span class="breakdown-review">Review &rarr;</span>
    `;
    item.addEventListener('click', () => {
      startRemediationReview(idx);
    });
    list.appendChild(item);
  });
  
  // Kept in this browser for My progress (once per session, not again after reviewing answers).
  const fromStudio = sessionConfig.source === 'studio';
  if (!fromStudio && !sessionConfig.progressRecorded) {
    sessionConfig.progressRecorded = true;
    sessionConfig.progressSaved = recordSessionProgress(answeredSteps);
    clearAttempt(sessionConfig.attemptKey); // finished: nothing left to continue
  }
  const note = document.getElementById('results-progress-note');
  if (note) {
    note.classList.toggle('hidden', fromStudio);
    note.dataset.tone = sessionConfig.progressSaved ? 'ok' : 'warn';
    note.textContent = sessionConfig.progressSaved
      ? 'Saved to My progress in this browser.'
      : 'This result could not be saved to My progress: this browser is not keeping site data (for example in a private window).';
  }
  const progressBtn = document.getElementById('results-progress-btn');
  if (progressBtn) progressBtn.classList.toggle('hidden', fromStudio);
  // A case study opened from a shared link ends here (no way into the rest of the bank from it).
  const backBtn = document.getElementById('results-dashboard-btn');
  if (backBtn) {
    backBtn.textContent = fromStudio ? 'Back to Question bank' : 'Back to Practise';
    backBtn.classList.toggle('hidden', sessionConfig.source === 'link');
  }
  const retryBtn = document.getElementById('results-retry-btn');
  if (retryBtn) retryBtn.textContent = sessionConfig.source === 'link' ? 'Try again' : 'Retry These Questions';

  switchView('results');
}
