/* Scoring of each question type, answer checks, submit/skip handling and rationale feedback. */

/* --- PLAYER GRADING SYSTEM (NGN STANDARDS) --- */
function evaluateStepScore(stepIdx) {
  const step = currentCase.screens[stepIdx];
  const q = step.question;
  const userAnswers = playerAnswers[stepIdx] || {};
  
  
  let score = 0;
  let maxScore = 0;
  
  switch (q.type) {
    // ================= 0/1 SCORING (No Penalties) =================
    case 'dropdown_cloze':
    case 'cloze':
    case 'drag_drop_cloze': {
      const c = q.cloze || { dropdowns: [] };
      const dropdowns = c.dropdowns || [];
      // Count indices where drop exists
      const activeDropdowns = dropdowns.filter(Boolean);
      maxScore = activeDropdowns.length;
      
      dropdowns.forEach((dd, idx) => {
        if (dd && dd.options) {
          const correctIdx = dd.options.findIndex(o => o.correct);
          const userVal = userAnswers[idx];
          // For drag drop, correct value is the exact text match
          if (q.type === 'drag_drop_cloze') {
            const correctText = dd.options.find(o => o.correct)?.text || '';
            if (userVal === correctText) score++;
          } else {
            if (userVal !== undefined && parseInt(userVal) === correctIdx) score++;
          }
        }
      });
      break;
    }
    case 'dropdown_table': {
      const rows = q.dropdownTableRows || [];
      maxScore = rows.length;
      rows.forEach((row, idx) => {
        const rowOptions = row.options || [];
        const correctIdx = rowOptions.findIndex(o => o.correct);
        const userVal = userAnswers[idx];
        if (userVal !== undefined && parseInt(userVal) === correctIdx) score++;
      });
      break;
    }
    case 'matrix_mc':
    case 'matrix': {
      const m = q.matrix || { rows: [] };
      const rows = m.rows || [];
      maxScore = rows.length;
      rows.forEach((r, idx) => {
        if (userAnswers[idx] === r.correctIndex) score++;
      });
      break;
    }
    case 'select_n':
    case 'selectN': {
      // 1 point per correct answer selected
      const limit = q.limit || 3;
      maxScore = limit;
      const options = q.options || [];
      options.forEach((opt, idx) => {
        if (opt.correct && userAnswers[idx] === true) score++;
      });
      score = Math.min(limit, score);
      break;
    }
    case 'bowtie': {
      // 5 slots, 1 point each
      maxScore = 5;
      const uA = userAnswers || {};
      
      const correctActions = (q.bowtieActions || []).filter(x => x.correct).map(x => x.text);
      const correctConditions = (q.bowtieConditions || []).filter(x => x.correct).map(x => x.text);
      const correctParams = (q.bowtieParams || []).filter(x => x.correct).map(x => x.text);
      
      // Actions
      const selActions = [uA['action0'], uA['action1']].filter(Boolean);
      selActions.forEach(act => {
        const cIdx = correctActions.indexOf(act);
        if (cIdx !== -1) {
          score++;
          correctActions.splice(cIdx, 1);
        }
      });
      
      // Condition
      if (uA['condition'] && correctConditions.includes(uA['condition'])) {
        score++;
      }
      
      // Params
      const selParams = [uA['param0'], uA['param1']].filter(Boolean);
      selParams.forEach(p => {
        const cIdx = correctParams.indexOf(p);
        if (cIdx !== -1) {
          score++;
          correctParams.splice(cIdx, 1);
        }
      });
      break;
    }
    case 'multiple_choice':
    case 'single': {
      maxScore = 1;
      const options = q.options || [];
      options.forEach((opt, idx) => {
        if (opt.correct && userAnswers[idx] === true) score = 1;
      });
      break;
    }
    case 'fill_blank': {
      maxScore = 1;
      const correctVal = (q.correctAnswer || '').toString().trim().toLowerCase();
      const userVal = (userAnswers.value || '').toString().trim().toLowerCase();
      if (correctVal === userVal || parseFloat(correctVal) === parseFloat(userVal)) {
        score = 1;
      }
      break;
    }
    case 'hotspot': {
      maxScore = 1;
      const r = q.rect || { x1: 0, y1: 0, x2: 100, y2: 100 };
      const ux = userAnswers.x;
      const uy = userAnswers.y;
      if (ux !== undefined && uy !== undefined) {
        const xMin = Math.min(r.x1, r.x2);
        const xMax = Math.max(r.x1, r.x2);
        const yMin = Math.min(r.y1, r.y2);
        const yMax = Math.max(r.y1, r.y2);
        if (ux >= xMin && ux <= xMax && uy >= yMin && uy <= yMax) score = 1;
      }
      break;
    }
    case 'ordered_response': {
      maxScore = 1;
      const correctSeq = q.orderedOptions || [];
      const userSeq = userAnswers.order || [];
      let allCorrect = correctSeq.length === userSeq.length;
      if (allCorrect) {
        for (let i = 0; i < correctSeq.length; i++) {
          if (correctSeq[i] !== userSeq[i]) {
            allCorrect = false;
            break;
          }
        }
      }
      score = allCorrect ? 1 : 0;
      break;
    }
    
    // ================= +/- SCORING (Penalty Deductions) =================
    case 'select_all':
    case 'sata':
    case 'trend': {
      let correctSel = 0;
      let incorrectSel = 0;
      const options = q.options || [];
      options.forEach((opt, idx) => {
        const isSelected = userAnswers[idx] === true;
        if (opt.correct) {
          maxScore++;
          if (isSelected) correctSel++;
        } else {
          if (isSelected) incorrectSel++;
        }
      });
      score = Math.max(0, correctSel - incorrectSel);
      break;
    }
    case 'highlight':
    case 'highlight_2': {
      let correctSel = 0;
      let incorrectSel = 0;
      
      const regex = /\{([^{|]+)(?:\|([^{}]+))?\}/g;
      let match;
      const highlights = [];
      
      if (q.highlightTabs) {
        q.highlightTabs.forEach(tab => {
          regex.lastIndex = 0;
          while ((match = regex.exec(tab.content || '')) !== null) {
            highlights.push({ text: match[1], correct: match[2] === 'correct' });
          }
        });
      } else {
        while ((match = regex.exec(q.highlightText || '')) !== null) {
          highlights.push({ text: match[1], correct: match[2] === 'correct' });
        }
      }
      
      highlights.forEach((h, idx) => {
        const isSelected = userAnswers[idx] === true;
        if (h.correct) {
          maxScore++;
          if (isSelected) correctSel++;
        } else {
          if (isSelected) incorrectSel++;
        }
      });
      score = Math.max(0, correctSel - incorrectSel);
      break;
    }
    case 'matrix_mr': {
      const m = q.matrix || { columns: [], rows: [] };
      let correctSel = 0;
      let incorrectSel = 0;
      const rows = m.rows || [];
      const columns = m.columns || [];
      
      rows.forEach((r, rIdx) => {
        const rowSel = userAnswers[rIdx] || [];
        columns.forEach((col, cIdx) => {
          const isCorrect = (r.correctIndices || []).includes(cIdx);
          const isChecked = rowSel.includes(cIdx);
          if (isCorrect) {
            maxScore++;
            if (isChecked) correctSel++;
          } else {
            if (isChecked) incorrectSel++;
          }
        });
      });
      score = Math.max(0, correctSel - incorrectSel);
      break;
    }
    case 'grouped_mr': {
      const groups = q.groupedRows || [];
      groups.forEach((g, gIdx) => {
        let gMax = 0;
        let gCorrect = 0;
        let gIncorrect = 0;
        const gAnswers = userAnswers[gIdx] || {};
        const options = g.options || [];
        
        options.forEach((opt, oIdx) => {
          const isSelected = gAnswers[oIdx] === true;
          if (opt.correct) {
            gMax++;
            if (isSelected) gCorrect++;
          } else {
            if (isSelected) gIncorrect++;
          }
        });
        
        maxScore += gMax;
        score += Math.max(0, gCorrect - gIncorrect); // category clamp min 0
      });
      break;
    }
    
    // ================= RATIONALE SCORING (All-or-Nothing) =================
    case 'dyad': {
      maxScore = 1;
      const c = q.cloze || { dropdowns: [] };
      const dropdowns = c.dropdowns || [];
      let dyadCorrect = dropdowns.filter(Boolean).length === 2;
      dropdowns.forEach((dd, idx) => {
        if (dd && dd.options) {
          const correctIdx = dd.options.findIndex(o => o.correct);
          if (parseInt(userAnswers[idx]) !== correctIdx) dyadCorrect = false;
        }
      });
      score = dyadCorrect ? 1 : 0;
      break;
    }
    case 'triad': {
      maxScore = 1;
      const c = q.cloze || { dropdowns: [] };
      const dropdowns = c.dropdowns || [];
      let triadCorrect = dropdowns.filter(Boolean).length === 3;
      dropdowns.forEach((dd, idx) => {
        if (dd && dd.options) {
          const correctIdx = dd.options.findIndex(o => o.correct);
          if (parseInt(userAnswers[idx]) !== correctIdx) triadCorrect = false;
        }
      });
      score = triadCorrect ? 1 : 0;
      break;
    }
  }
  
  playerScores[stepIdx] = { score, max: maxScore };
}

function hasSelectedAnyAnswer(q, stepIdx) {
  if (!q) return false;
  const userAnswers = playerAnswers[stepIdx];

  // 1. Check state object first
  if (userAnswers) {
    switch (q.type) {
      case 'dropdown_cloze':
      case 'cloze':
      case 'drag_drop_cloze':
      case 'dyad':
      case 'triad': {
        const hasVal = Object.values(userAnswers).some(v => v !== undefined && v !== null && v !== '');
        if (hasVal) return true;
        break;
      }
      case 'dropdown_table': {
        const hasVal = Object.values(userAnswers).some(v => v !== undefined && v !== null && v !== '');
        if (hasVal) return true;
        break;
      }
      case 'matrix_mc':
      case 'matrix': {
        const hasVal = Object.values(userAnswers).some(v => v !== undefined && v !== null && v !== '');
        if (hasVal) return true;
        break;
      }
      case 'select_n':
      case 'selectN':
      case 'multiple_choice':
      case 'single':
      case 'select_all':
      case 'sata':
      case 'trend':
      case 'highlight':
      case 'highlight_2': {
        const hasVal = Object.values(userAnswers).some(v => v === true);
        if (hasVal) return true;
        break;
      }
      case 'fill_blank': {
        if (userAnswers.value && userAnswers.value.toString().trim().length > 0) return true;
        break;
      }
      case 'hotspot': {
        if (userAnswers.x !== undefined && userAnswers.y !== undefined) return true;
        break;
      }
      case 'ordered_response': {
        if (Array.isArray(userAnswers.order) && userAnswers.order.length > 0) return true;
        break;
      }
      case 'bowtie': {
        if (userAnswers.action0 || userAnswers.action1 || userAnswers.condition || userAnswers.param0 || userAnswers.param1) return true;
        break;
      }
      case 'matrix_mr': {
        const hasVal = Object.values(userAnswers).some(arr => Array.isArray(arr) && arr.length > 0);
        if (hasVal) return true;
        break;
      }
      case 'grouped_mr': {
        const hasVal = Object.values(userAnswers).some(group => group && Object.values(group).some(v => v === true));
        if (hasVal) return true;
        break;
      }
      default: {
        const hasVal = Object.values(userAnswers).some(v => v !== undefined && v !== null && v !== false && v !== '');
        if (hasVal) return true;
      }
    }
  }


  return false;
}

function showSkipQuestionModal() {
  const modal = document.getElementById('skip-question-modal');
  if (modal) modal.classList.remove('hidden');
}

function closeSkipQuestionModal() {
  const modal = document.getElementById('skip-question-modal');
  if (modal) modal.classList.add('hidden');
}

function confirmSkipQuestion() {
  closeSkipQuestionModal();
  submittedAnswers[playerStepIndex] = true;
  evaluateStepScore(playerStepIndex);
  if (!playerScores[playerStepIndex]) {
    playerScores[playerStepIndex] = { score: 0, max: 1 };
  } else {
    playerScores[playerStepIndex].score = 0; // force zero points
  }

  if (sessionConfig.mode === 'test' && !sessionConfig.isRemediation) {
    if (playerStepIndex < currentCase.screens.length - 1) {
      playerStepIndex++;
      renderPlayerStep(playerStepIndex);
    } else {
      loadResultsView();
    }
  } else {
    renderPlayerStep(playerStepIndex);
    revealPlayerFeedback();
  }
}

function handlePlayerSubmit() {
  const step = currentCase.screens[playerStepIndex];
  if (!step) return;

  const hasAnswer = hasSelectedAnyAnswer(step.question, playerStepIndex);
  if (!hasAnswer) {
    showSkipQuestionModal();
    return;
  }

  submittedAnswers[playerStepIndex] = true;
  evaluateStepScore(playerStepIndex);
  renderPlayerStep(playerStepIndex);
  revealPlayerFeedback();
  // Response submitted toast removed per user request
}

function handlePlayerGiveUp() {
  submittedAnswers[playerStepIndex] = true;
  evaluateStepScore(playerStepIndex);
  playerScores[playerStepIndex].score = 0; // force zero points
  renderPlayerStep(playerStepIndex);
  revealPlayerFeedback();
}

// The feedback card (Correct / Partial Correct / Incorrect, score, rationale) sits
// below the answer options. With long questions on laptop screens it lands below
// the visible part of the question panel, so after submitting, students saw only
// the highlighted answers. Scroll just far enough to show the result and the start
// of the rationale, without pushing the result header above the top of the panel.
function revealPlayerFeedback() {
  const card = document.getElementById('player-feedback-card');
  if (!card || card.classList.contains('hidden')) return;
  const header = card.querySelector('.feedback-header') || card;

  let scroller = card.parentElement;
  while (scroller && scroller !== document.body) {
    const overflowY = getComputedStyle(scroller).overflowY;
    if ((overflowY === 'auto' || overflowY === 'scroll') && scroller.scrollHeight > scroller.clientHeight) break;
    scroller = scroller.parentElement;
  }
  const useWindow = !scroller || scroller === document.body;
  const view = useWindow ? { top: 0, bottom: window.innerHeight } : scroller.getBoundingClientRect();
  const headerRect = header.getBoundingClientRect();

  const WANTED_BELOW_HEADER = 140; // room for the start of the rationale
  const overshoot = headerRect.bottom + WANTED_BELOW_HEADER - view.bottom;
  if (overshoot <= 0) return;
  const delta = Math.min(overshoot, headerRect.top - view.top - 8);
  if (delta <= 0) return;
  (useWindow ? window : scroller).scrollBy({ top: delta, behavior: 'smooth' });
}

function displayPlayerFeedback(stepIdx) {
  const step = currentCase.screens[stepIdx];
  const res = playerScores[stepIdx] || { score: 0, max: 1 };
  
  const badge = document.getElementById('feedback-result-badge');
  const pointsEl = document.getElementById('feedback-score-display');
  const explText = document.getElementById('feedback-explanation-text');
  
  pointsEl.textContent = `Score: ${res.score} / ${res.max} point${res.max !== 1 ? 's' : ''}`;
  explText.innerHTML = step.question.explanation || 'No explanation rationale provided.';
  
  badge.className = 'feedback-badge';
  if (res.score === res.max) {
    badge.classList.add('correct');
    badge.textContent = 'Correct';
  } else if (res.score === 0) {
    badge.classList.add('incorrect');
    badge.textContent = 'Incorrect';
  } else {
    badge.classList.add('partial');
    badge.textContent = 'Partial Correct';
  }
}
