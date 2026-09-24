/* Results view (scoreboard) and remediation review. */

/* ================= RESULTS VIEW (SCOREBOARD) ================= */
function initResultsEvents() {
  document.getElementById('results-retry-btn').addEventListener('click', () => {
    startPlayer(currentCase, { mode: sessionConfig.mode, isRemediation: false });
  });
  
  document.getElementById('results-dashboard-btn').addEventListener('click', () => {
    switchView('student');
  });

  const reviewAnswersBtn = document.getElementById('results-review-answers-btn');
  if (reviewAnswersBtn) {
    reviewAnswersBtn.addEventListener('click', () => {
      startRemediationReview(0);
    });
  }
}

function startRemediationReview(jumpIdx = 0) {
  sessionConfig.isRemediation = true;
  sessionConfig.allowBacktrack = true;
  currentCase.screens.forEach((s, idx) => {
    submittedAnswers[idx] = true;
    if (!playerScores[idx]) evaluateStepScore(idx);
  });
  switchView('player');
  renderPlayerStep(jumpIdx);
}

function loadResultsView() {
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
  document.getElementById('results-score').textContent = `${totalScore} / ${totalMax}`;
  document.getElementById('results-percentage').textContent = `${percent}%`;
  
  const list = document.getElementById('results-breakdown-list');
  list.innerHTML = '';
  
  currentCase.screens.forEach((s, idx) => {
    const sc = playerScores[idx] || { score: 0, max: 1 };
    const typeLabel = (s.question.type || 'Question').toUpperCase().replace(/_/g, ' ');
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
    
    const item = document.createElement('div');
    item.className = 'breakdown-item';
    item.style.cursor = 'pointer';
    item.title = 'Click to review question and clinical rationale';
    item.innerHTML = `
      <div class="breakdown-item-left">
        <span class="breakdown-badge ${badgeClass}">${badgeText}</span>
        <strong>Question ${idx + 1}</strong> (${contextLabel} &bull; ${typeLabel})
      </div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <span class="breakdown-score">${sc.score} / ${sc.max} pts</span>
        <span style="font-size: 11px; color: #38bdf8; font-weight: 500;">Review &rarr;</span>
      </div>
    `;
    item.addEventListener('click', () => {
      startRemediationReview(idx);
    });
    list.appendChild(item);
  });
  
  switchView('results');
}
