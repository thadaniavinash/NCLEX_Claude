/* Test player: navigation, chart tabs, question navigator and per-question-type renderers. */

/* ================= HIGH FIDELITY NCLEX PLAYER ENGINE ================= */
function initPlayerEvents() {
  document.getElementById('player-quit-btn').addEventListener('click', () => {
    if (confirm("Are you sure you want to quit the quiz? Your current progress will be lost.")) {
      switchView('student');
    }
  });

  // Question Navigator Button (Right-justified) and Drawer Overlay
  const navBtn = document.getElementById('player-nav-btn');
  if (navBtn) navBtn.addEventListener('click', () => toggleQuestionNavigator());

  const closeNavBtn = document.getElementById('close-question-nav-btn');
  if (closeNavBtn) closeNavBtn.addEventListener('click', () => toggleQuestionNavigator(false));

  const navBackdrop = document.getElementById('question-nav-drawer-backdrop');
  if (navBackdrop) navBackdrop.addEventListener('click', () => toggleQuestionNavigator(false));

  // Test Mode Submit Confirmation Modal
  const testModal = document.getElementById('test-submit-modal');
  const testCloseBtn = document.getElementById('test-submit-close-btn');
  const testCancelBtn = document.getElementById('test-submit-cancel-btn');
  const testConfirmBtn = document.getElementById('test-submit-confirm-btn');
  if (testCloseBtn) testCloseBtn.addEventListener('click', closeTestSubmitModal);
  if (testCancelBtn) testCancelBtn.addEventListener('click', closeTestSubmitModal);
  if (testConfirmBtn) testConfirmBtn.addEventListener('click', confirmTestSubmitAndAdvance);
  if (testModal) {
    testModal.addEventListener('click', (e) => {
      if (e.target === testModal) closeTestSubmitModal();
    });
  }

  document.getElementById('player-calc-btn').addEventListener('click', toggleCalculator);
  document.getElementById('close-calc-btn').addEventListener('click', toggleCalculator);

  document.getElementById('player-submit-btn').addEventListener('click', handlePlayerSubmit);
  document.getElementById('player-giveup-btn').addEventListener('click', handlePlayerGiveUp);

  const skipModal = document.getElementById('skip-question-modal');
  const skipNoBtn = document.getElementById('skip-modal-no-btn');
  const skipCloseBtn = document.getElementById('skip-modal-close-btn');
  const skipYesBtn = document.getElementById('skip-modal-yes-btn');

  if (skipNoBtn) skipNoBtn.addEventListener('click', closeSkipQuestionModal);
  if (skipCloseBtn) skipCloseBtn.addEventListener('click', closeSkipQuestionModal);
  if (skipYesBtn) skipYesBtn.addEventListener('click', confirmSkipQuestion);
  if (skipModal) {
    skipModal.addEventListener('click', (e) => {
      if (e.target === skipModal) closeSkipQuestionModal();
    });
  }

  document.getElementById('player-prev-btn').addEventListener('click', () => {
    if (sessionConfig.mode === 'test' && !sessionConfig.isRemediation) {
      return; // No backtracking in Test Mode
    }
    if (playerStepIndex > 0) {
      playerStepIndex--;
      renderPlayerStep(playerStepIndex);
    }
  });

  document.getElementById('player-next-btn').addEventListener('click', () => {
    // 1. In Remediation Mode: free browsing to next question
    if (sessionConfig.isRemediation) {
      if (playerStepIndex < currentCase.screens.length - 1) {
        playerStepIndex++;
        renderPlayerStep(playerStepIndex);
      } else {
        loadResultsView();
      }
      return;
    }

    // 2. In Test Mode: prompt confirmation or skip before advancing (irreversible)
    if (sessionConfig.mode === 'test') {
      const step = currentCase.screens[playerStepIndex];
      const hasAnswer = step ? hasSelectedAnyAnswer(step.question, playerStepIndex) : false;
      if (!hasAnswer) {
        showSkipQuestionModal();
        return;
      }
      showTestSubmitModal();
      return;
    }

    // 3. In Review Mode (Tutor): requires submitting before advancing
    const isSubmitted = submittedAnswers[playerStepIndex];
    if (!isSubmitted) {
      const step = currentCase.screens[playerStepIndex];
      const hasAnswer = step ? hasSelectedAnyAnswer(step.question, playerStepIndex) : false;
      if (!hasAnswer) {
        showSkipQuestionModal();
        return;
      }
      alert("Please submit your response first by clicking the Submit button.");
      return;
    }
    if (playerStepIndex < currentCase.screens.length - 1) {
      playerStepIndex++;
      renderPlayerStep(playerStepIndex);
    } else {
      loadResultsView();
    }
  });
}

function showTestSubmitModal() {
  const modal = document.getElementById('test-submit-modal');
  if (modal) modal.classList.remove('hidden');
}

function closeTestSubmitModal() {
  const modal = document.getElementById('test-submit-modal');
  if (modal) modal.classList.add('hidden');
}

function confirmTestSubmitAndAdvance() {
  closeTestSubmitModal();
  submittedAnswers[playerStepIndex] = true;
  evaluateStepScore(playerStepIndex);
  if (playerStepIndex < currentCase.screens.length - 1) {
    playerStepIndex++;
    renderPlayerStep(playerStepIndex);
  } else {
    loadResultsView();
  }
}

function toggleQuestionNavigator(forceState) {
  const drawer = document.getElementById('question-navigator-drawer');
  const backdrop = document.getElementById('question-nav-drawer-backdrop');
  if (!drawer) return;

  const shouldOpen = typeof forceState === 'boolean' ? forceState : drawer.classList.contains('hidden');
  if (shouldOpen) {
    renderQuestionNavigatorList();
    drawer.classList.remove('hidden');
    if (backdrop) backdrop.classList.remove('hidden');
  } else {
    drawer.classList.add('hidden');
    if (backdrop) backdrop.classList.add('hidden');
  }
}

function startPlayer(caseStudy, config) {
  migrateCaseTypes(caseStudy);
  currentCase = caseStudy;
  playerStepIndex = 0;
  playerActiveTabId = '';
  
  playerAnswers = {};
  submittedAnswers = {};
  playerScores = {};

  if (config) {
    sessionConfig = Object.assign({
      mode: 'review',
      isRemediation: false,
      allowBacktrack: config.mode !== 'test'
    }, config);
  } else {
    sessionConfig = {
      mode: 'review',
      isRemediation: false,
      allowBacktrack: true
    };
  }

  // In remediation review, mark all steps as submitted initially
  if (sessionConfig.isRemediation) {
    currentCase.screens.forEach((s, idx) => {
      submittedAnswers[idx] = true;
      if (!playerScores[idx]) evaluateStepScore(idx);
    });
  }
  
  const calc = document.getElementById('ti108-calculator');
  if (calc) calc.classList.add('hidden');
  closeSkipQuestionModal();
  closeTestSubmitModal();
  toggleQuestionNavigator(false);
  
  switchView('player');
  renderPlayerStep(0);
}

function renderPlayerStep(stepIdx) {
  playerStepIndex = stepIdx;
  const step = currentCase.screens[stepIdx];
  if (!step) return;
  
  document.getElementById('player-progress-text').textContent = `${stepIdx + 1} of ${currentCase.screens.length}`;
  document.getElementById('player-question-number-title').textContent = `Question ${stepIdx + 1}`;
  
  const isSubmitted = submittedAnswers[stepIdx] || sessionConfig.isRemediation;
  
  const statusEl = document.getElementById('player-question-status-text');
  statusEl.textContent = isSubmitted ? 'Complete' : 'Not complete';
  
  const isStepStandalone = currentCase.isStandalone || step.isStandalone;
  const screenLabel = document.getElementById('player-screen-label');
  if (isStepStandalone) {
    screenLabel.style.display = 'none';
  } else {
    screenLabel.style.display = 'block';
    screenLabel.textContent = `Case Study Screen ${stepIdx + 1} of ${currentCase.screens.length}`;
  }
  document.getElementById('player-intro-text').innerHTML = step.leftContent.intro || '';
  
  // Full-width adaptive layout for questions with no tabs
  const splitContainer = document.querySelector('.player-center-split');
  if (splitContainer) {
    const hasLeftContent = step.leftContent && step.leftContent.tabs && step.leftContent.tabs.length > 0 && step.question.type !== 'highlight';
    if (!hasLeftContent) {
      splitContainer.classList.add('full-width');
    } else {
      splitContainer.classList.remove('full-width');
    }
  }

  // Question Navigator button visibility: Hidden in active Test Mode, Visible in Review Mode & Remediation Review
  const navBtn = document.getElementById('player-nav-btn');
  if (navBtn) {
    if (sessionConfig.mode === 'test' && !sessionConfig.isRemediation) {
      navBtn.style.display = 'none';
    } else {
      navBtn.style.display = 'inline-flex';
    }
  }

  // Case Transition Banner (Shown when a case study begins)
  const caseBanner = document.getElementById('player-case-banner');
  const bannerText = document.getElementById('player-case-banner-text');
  if (caseBanner && bannerText) {
    const isNewCaseStart = !isStepStandalone && (stepIdx === 0 || currentCase.screens[stepIdx - 1]?.isStandalone || (currentCase.screens[stepIdx - 1]?.caseId && currentCase.screens[stepIdx - 1]?.caseId !== step.caseId));
    if (isNewCaseStart) {
      const caseName = step.caseTitle || currentCase.title || 'Unfolding Clinical Case';
      bannerText.innerHTML = `The following 6 questions refer to this clinical scenario: <strong>${caseName}</strong>.`;
      caseBanner.classList.remove('hidden');
    } else {
      caseBanner.classList.add('hidden');
    }
  }

  // Populate and show full-width meta header if in highlight question type
  const fullwidthHeader = document.getElementById('player-fullwidth-meta-header');
  if (fullwidthHeader) {
    if (step.question.type === 'highlight') {
      fullwidthHeader.classList.remove('hidden');
      document.getElementById('player-fullwidth-question-number-title').textContent = `Question ${stepIdx + 1}`;
      document.getElementById('player-fullwidth-question-status-text').textContent = isSubmitted ? 'Complete' : 'Not complete';
      
      const fwScreenLabel = document.getElementById('player-fullwidth-screen-label');
      if (fwScreenLabel) {
        if (isStepStandalone) {
          fwScreenLabel.style.display = 'none';
        } else {
          fwScreenLabel.style.display = 'block';
          fwScreenLabel.textContent = `Case Study Screen ${stepIdx + 1} of ${currentCase.screens.length}`;
        }
      }
    } else {
      fullwidthHeader.classList.add('hidden');
    }
  }

  renderPlayerTabs(step.leftContent.tabs);
  renderQuestionNavigatorList();
  
  const preambleEl = document.getElementById('player-question-preamble');
  if (preambleEl) {
    if (step.question.preamble && step.question.preamble.trim() && step.question.preamble.trim() !== '<br>') {
      preambleEl.innerHTML = step.question.preamble;
      preambleEl.classList.remove('hidden');
    } else {
      preambleEl.innerHTML = '';
      preambleEl.classList.add('hidden');
    }
  }

  // Source footnote (e.g. copyright attribution), shown below the submit button
  const footnoteEl = document.getElementById('player-question-footnote');
  if (footnoteEl) {
    if (step.question.footnote && step.question.footnote.trim()) {
      footnoteEl.innerHTML = step.question.footnote;
      footnoteEl.style.cssText = 'margin-top:14px;padding-top:10px;border-top:1px solid #ccc;font-size:0.78em;color:#888;font-style:italic;';
    } else {
      footnoteEl.innerHTML = '';
      footnoteEl.style.cssText = '';
    }
  }

  // Render question image in player if present
  const imgContainer = document.getElementById('player-question-image-container');
  const playerImg = document.getElementById('player-question-image');
  if (imgContainer && playerImg) {
    if (step.question.questionImage) {
      playerImg.src = step.question.questionImage;
      imgContainer.classList.remove('hidden');
    } else {
      playerImg.src = '';
      imgContainer.classList.add('hidden');
    }
  }
  
  document.getElementById('player-question-stem').innerHTML = step.question.stem || '';
  
  renderPlayerAnswersBox(step.question, stepIdx);
  
  // Footer navigation buttons
  const prevBtn = document.getElementById('player-prev-btn');
  const nextBtn = document.getElementById('player-next-btn');

  // Previous button: strictly hidden in active Test Mode
  if (sessionConfig.mode === 'test' && !sessionConfig.isRemediation) {
    prevBtn.style.display = 'none';
  } else {
    prevBtn.style.display = 'inline-flex';
    prevBtn.disabled = stepIdx === 0;
  }

  // Next button label
  const isLast = (stepIdx === currentCase.screens.length - 1);
  if (sessionConfig.mode === 'test' && !sessionConfig.isRemediation) {
    nextBtn.innerHTML = isLast
      ? 'Finish Exam & Submit <svg viewBox="0 0 24 24" width="16" height="16" style="vertical-align: middle; fill: currentColor; margin-left: 6.5px; transform: rotate(180deg);"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>'
      : 'Submit & Next <svg viewBox="0 0 24 24" width="16" height="16" style="vertical-align: middle; fill: currentColor; margin-left: 6.5px; transform: rotate(180deg);"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>';
  } else {
    nextBtn.innerHTML = isLast
      ? 'Finish attempt <svg viewBox="0 0 24 24" width="16" height="16" style="vertical-align: middle; fill: currentColor; margin-left: 6.5px; transform: rotate(180deg);"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>'
      : 'Next <svg viewBox="0 0 24 24" width="16" height="16" style="vertical-align: middle; fill: currentColor; margin-left: 6.5px; transform: rotate(180deg);"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>';
  }
  
  const submitBtn = document.getElementById('player-submit-btn');
  const giveupBtn = document.getElementById('player-giveup-btn');
  
  if (sessionConfig.isRemediation) {
    // In remediation review, hide submit actions
    if (submitBtn) submitBtn.style.display = 'none';
    if (giveupBtn) giveupBtn.style.display = 'none';
  } else if (sessionConfig.mode === 'test') {
    // In test mode, submission happens on "Submit & Next" button
    if (submitBtn) submitBtn.style.display = 'none';
    if (giveupBtn) giveupBtn.style.display = 'none';
  } else {
    if (submitBtn) {
      submitBtn.style.display = '';
      submitBtn.disabled = isSubmitted;
    }
    if (giveupBtn) {
      giveupBtn.style.display = 'none';
      giveupBtn.disabled = isSubmitted;
    }
  }
  
  // Feedback card: only shown in Review Mode (after submit) or in Remediation Review
  const feedbackCard = document.getElementById('player-feedback-card');
  if (sessionConfig.isRemediation || (sessionConfig.mode === 'review' && isSubmitted)) {
    feedbackCard.classList.remove('hidden');
    displayPlayerFeedback(stepIdx);
  } else {
    feedbackCard.classList.add('hidden');
  }
}

function renderPlayerTabs(tabs) {
  const tabsBar = document.getElementById('player-chart-tabs');
  const contentBox = document.getElementById('player-chart-content');
  tabsBar.innerHTML = '';
  contentBox.innerHTML = '';
  
  if (!tabs || tabs.length === 0) {
    contentBox.innerHTML = '<p style="color:#9ca3af; font-style:italic;">No chart entries.</p>';
    return;
  }
  
  if (!playerActiveTabId || !tabs.find(t => t.id === playerActiveTabId)) {
    playerActiveTabId = tabs[0].id;
  }
  
  tabs.forEach(t => {
    const tabBtn = document.createElement('button');
    tabBtn.className = `patient-chart-tab ${t.id === playerActiveTabId ? 'active' : ''}`;
    tabBtn.textContent = t.title;
    tabBtn.addEventListener('click', () => {
      playerActiveTabId = t.id;
      renderPlayerTabs(tabs);
    });
    tabsBar.appendChild(tabBtn);
  });
  
  const activeTab = tabs.find(t => t.id === playerActiveTabId);
  contentBox.innerHTML = activeTab ? formatNursesNotes(activeTab.content, activeTab.title) : '';
}

function renderQuestionNavigatorList() {
  const drawerList = document.getElementById('question-nav-drawer-list');
  if (!drawerList || !currentCase || !currentCase.screens) return;
  drawerList.innerHTML = '';

  currentCase.screens.forEach((step, idx) => {
    const item = document.createElement('div');
    item.className = 'nav-drawer-item';
    if (idx === playerStepIndex) item.classList.add('active');

    const isSub = submittedAnswers[idx];
    if (isSub) item.classList.add('complete');

    // Title / Context label
    const typeLabel = (step.question.type || 'Question').toUpperCase().replace(/_/g, ' ');
    const isStepStandalone = currentCase.isStandalone || step.isStandalone;
    const contextLabel = isStepStandalone ? 'Stand-alone Question' : (step.caseTitle || currentCase.title || `Case Study Screen ${step.step || (idx + 1)}`);

    let badgeClass = 'badge-incomplete';
    let badgeText = 'Incomplete';

    if (sessionConfig.isRemediation) {
      const sc = playerScores[idx] || { score: 0, max: 1 };
      if (sc.score === sc.max) {
        badgeClass = 'badge-correct';
        badgeText = `✓ Correct (${sc.score}/${sc.max})`;
      } else if (sc.score > 0) {
        badgeClass = 'badge-partial';
        badgeText = `Partial (${sc.score}/${sc.max})`;
      } else {
        badgeClass = 'badge-incorrect';
        badgeText = `✗ Incorrect (0/${sc.max})`;
      }
    } else if (idx === playerStepIndex) {
      badgeClass = 'badge-current';
      badgeText = 'Current';
    } else if (isSub) {
      badgeClass = 'badge-complete';
      badgeText = 'Complete';
    }

    item.innerHTML = `
      <div class="nav-drawer-item-left">
        <div class="nav-drawer-item-num">${idx + 1}</div>
        <div class="nav-drawer-item-info">
          <span class="nav-drawer-item-title">${contextLabel}</span>
          <span class="nav-drawer-item-sub">Question ${idx + 1} &bull; ${typeLabel}</span>
        </div>
      </div>
      <span class="nav-drawer-item-badge ${badgeClass}">${badgeText}</span>
    `;

    item.addEventListener('click', () => {
      // In Review Mode or Remediation review, student can jump freely
      if (sessionConfig.mode === 'review' || sessionConfig.isRemediation) {
        renderPlayerStep(idx);
        toggleQuestionNavigator(false);
      } else {
        showToast("Backtracking is not permitted during Test Mode.", "info");
      }
    });

    drawerList.appendChild(item);
  });
}

/* ================= 17 PLAYER OPTIONS RENDERERS ================= */
function renderPlayerAnswersBox(q, stepIdx) {
  const box = document.getElementById('player-answer-box');
  if (!box) return;
  box.innerHTML = '';
  const isSubmitted = submittedAnswers[stepIdx];
  const userAnswers = playerAnswers[stepIdx];

  try {
    switch (q.type) {
      case 'dropdown_cloze':
      case 'cloze':
      case 'dyad':
      case 'triad':
        renderPlayerDropdownCloze(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'drag_drop_cloze':
        renderPlayerDragDropCloze(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'dropdown_table':
        renderPlayerDropdownTable(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'matrix_mc':
      case 'matrix':
        renderPlayerMatrixMc(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'matrix_mr':
        renderPlayerMatrixMr(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'select_n':
      case 'selectN':
        renderPlayerSelectN(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'bowtie':
        renderPlayerBowtie(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'multiple_choice':
      case 'single':
        renderPlayerMultipleChoice(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'fill_blank':
        renderPlayerFillBlank(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'hotspot':
        renderPlayerHotspot(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'ordered_response':
        renderPlayerOrderedResponse(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'select_all':
      case 'sata':
      case 'trend':
        renderPlayerSata(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'highlight':
      case 'highlight_2':
        renderPlayerHighlight(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      case 'grouped_mr':
        renderPlayerGroupedMr(q, stepIdx, box, isSubmitted, userAnswers);
        break;
      default:
        console.warn("Unknown question type:", q.type);
        box.innerHTML = `<div style="color:var(--accent-red); padding:16px; border:1px solid var(--accent-red); background-color:rgba(239, 68, 68, 0.05); border-radius:4px; font-size:13px;">
          <strong>Error:</strong> Unknown question type "${escapeHTML(q.type)}".
        </div>`;
    }
  } catch (err) {
    console.error("Error rendering player answers box:", err);
    box.innerHTML = `<div style="color:var(--accent-red); padding:16px; border:1px solid var(--accent-red); background-color:rgba(239, 68, 68, 0.05); border-radius:4px; font-size:13px;">
      <strong>Error rendering answer options:</strong> ${escapeHTML(err.message)}<br>
      <small style="display:block; margin-top:8px; opacity:0.8;">This could be due to legacy or corrupted case study data. Try recreating or editing the case study.</small>
    </div>`;
  }
}

// 1. Dropdown Cloze & Rationales (Dyad / Triad)
function renderPlayerDropdownCloze(q, stepIdx, box, isSubmitted, userAnswers) {
  const c = q.cloze || { text: '', dropdowns: [] };
  const container = document.createElement('div');
  container.className = 'cloze-sentence';
  
  let baseText = c.text || '';
  const regex = /\[\[d(?:r)?op(\d+)\]\]/gi;
  let lastIndex = 0;
  let match;
  
  const stateAnswers = userAnswers || {};
  const dropdowns = c.dropdowns || [];
  
  while ((match = regex.exec(baseText)) !== null) {
    const textSpan = document.createElement('span');
    textSpan.innerHTML = baseText.substring(lastIndex, match.index);
    container.appendChild(textSpan);
    const idx = parseInt(match[1]);
    const dd = dropdowns[idx];
    
    if (dd && dd.options) {
      const select = document.createElement('select');
      select.className = 'cloze-select';
      if (isSubmitted) select.disabled = true;
      
      const defOpt = document.createElement('option');
      defOpt.textContent = dd.placeholder || 'Select...';
      defOpt.value = '';
      select.appendChild(defOpt);
      
      const savedVal = stateAnswers[idx];
      dd.options.forEach((opt, oIdx) => {
        const oEl = document.createElement('option');
        oEl.textContent = opt.text || '';
        oEl.value = oIdx;
        if (savedVal !== undefined && parseInt(savedVal) === oIdx) {
          oEl.selected = true;
        }
        select.appendChild(oEl);
      });
      
      if (isSubmitted) {
        const correctIdx = dd.options.findIndex(o => o.correct);
        if (parseInt(savedVal) === correctIdx) {
          select.classList.add('show-correct');
        } else {
          select.classList.add('show-incorrect');
        }
      } else {
        select.addEventListener('change', (e) => {
          if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
          playerAnswers[stepIdx][idx] = e.target.value !== '' ? parseInt(e.target.value) : undefined;
        });
      }
      container.appendChild(select);
    } else {
      const fallback = document.createElement('span');
      fallback.textContent = `[drop${idx}]`;
      container.appendChild(fallback);
    }
    lastIndex = regex.lastIndex;
  }
  const endSpan = document.createElement('span');
  endSpan.innerHTML = baseText.substring(lastIndex);
  container.appendChild(endSpan);
  box.appendChild(container);
}

// 2. Drag and Drop Cloze
function renderPlayerDragDropCloze(q, stepIdx, box, isSubmitted, userAnswers) {
  const c = q.cloze || { text: '', dropdowns: [] };
  const container = document.createElement('div');
  container.className = 'cloze-sentence';
  
  const stateAnswers = userAnswers || {}; // { dropIdx: optionText }
  const dropdowns = c.dropdowns || [];
  
  let baseText = c.text || '';
  const regex = /\[\[d(?:r)?op(\d+)\]\]/gi;
  let lastIndex = 0;
  let match;
  
  while ((match = regex.exec(baseText)) !== null) {
    const textSpan = document.createElement('span');
    textSpan.innerHTML = baseText.substring(lastIndex, match.index);
    container.appendChild(textSpan);
    const idx = parseInt(match[1]);
    const dd = dropdowns[idx];
    
    if (dd) {
      const slot = document.createElement('div');
      slot.className = 'drag-blank-slot';
      
      const placedVal = stateAnswers[idx];
      if (placedVal) {
        slot.classList.add('occupied');
        slot.textContent = placedVal;
      } else {
        slot.textContent = `[Slot ${idx + 1}]`;
      }
      
      if (isSubmitted) {
        const correctText = dd.options ? (dd.options.find(o => o.correct)?.text || '') : '';
        if (placedVal === correctText) {
          slot.classList.add('show-correct');
        } else {
          slot.classList.add('show-incorrect');
        }
      } else {
        // Click blank to clear
        slot.addEventListener('click', () => {
          if (stateAnswers[idx]) {
            delete stateAnswers[idx];
            playerAnswers[stepIdx] = stateAnswers;
            renderPlayerStep(stepIdx);
          }
        });
      }
      container.appendChild(slot);
    }
    lastIndex = regex.lastIndex;
  }
  const endSpan = document.createElement('span');
  endSpan.innerHTML = baseText.substring(lastIndex);
  container.appendChild(endSpan);
  box.appendChild(container);
  
  // Options pool
  if (!isSubmitted) {
    const pool = document.createElement('div');
    pool.className = 'drag-options-pool';
    pool.innerHTML = '<span style="font-size:11px; width:100%; font-weight:700; color:#64748b; margin-bottom:4px;">Drag / Click a term to place in blank slots:</span>';
    
    // Aggregate options
    const allOptions = [];
    dropdowns.forEach(dd => {
      if (dd && dd.options) dd.options.forEach(o => allOptions.push(o.text));
    });
    const uniqueOptions = [...new Set(allOptions)];
    
    uniqueOptions.forEach(optText => {
      const isAlreadyPlaced = Object.values(stateAnswers).includes(optText);
      const token = document.createElement('div');
      token.className = `drag-option-token ${isAlreadyPlaced ? 'placed' : ''}`;
      token.textContent = optText;
      
      if (!isAlreadyPlaced) {
        token.addEventListener('click', () => {
          // Find first empty slot
          const targetIndex = dropdowns.findIndex((dd, i) => dd && !stateAnswers[i]);
          if (targetIndex !== -1) {
            if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
            playerAnswers[stepIdx][targetIndex] = optText;
            renderPlayerStep(stepIdx);
          }
        });
      }
      pool.appendChild(token);
    });
    box.appendChild(pool);
  }
}

// 3. Drop-Down Table
function renderPlayerDropdownTable(q, stepIdx, box, isSubmitted, userAnswers) {
  const rows = q.dropdownTableRows || [];
  const stateAnswers = userAnswers || {};
  const tbl = document.createElement('table');
  tbl.className = 'exam-matrix-table';
  
  const header1 = q.dropdownTableHeader1 || 'Category Findings';
  const header2 = q.dropdownTableHeader2 || 'Clinical Assessment Score / Selection';
  
  tbl.innerHTML = `
    <thead>
      <tr>
        <th>${escapeHTML(header1)}</th>
        <th>${escapeHTML(header2)}</th>
      </tr>
    </thead>
    <tbody></tbody>
  `;
  const tbody = tbl.querySelector('tbody');
  
  rows.forEach((row, rIdx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${escapeHTML(row.label)}</td>
      <td>
        <select class="cloze-select row-select-box" style="width:100%; max-width:260px;" ${isSubmitted ? 'disabled' : ''}>
          <option value="">${escapeHTML(row.placeholder || 'Select...')}</option>
        </select>
      </td>
    `;
    
    const select = tr.querySelector('.row-select-box');
    const savedVal = stateAnswers[rIdx];
    
    const rowOptions = row.options || [];
    rowOptions.forEach((opt, oIdx) => {
      const oEl = document.createElement('option');
      oEl.textContent = opt.text || '';
      oEl.value = oIdx;
      if (savedVal !== undefined && parseInt(savedVal) === oIdx) oEl.selected = true;
      select.appendChild(oEl);
    });
    
    if (isSubmitted) {
      const correctIdx = rowOptions.findIndex(o => o.correct);
      if (parseInt(savedVal) === correctIdx) {
        select.classList.add('show-correct');
      } else {
        select.classList.add('show-incorrect');
      }
    } else {
      select.addEventListener('change', (e) => {
        if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
        playerAnswers[stepIdx][rIdx] = e.target.value !== '' ? parseInt(e.target.value) : undefined;
      });
    }
    
    tbody.appendChild(tr);
  });
  box.appendChild(tbl);
}

// 4. Matrix MC (Single choice per row)
function renderPlayerMatrixMc(q, stepIdx, box, isSubmitted, userAnswers) {
  renderPlayerMatrixBase(q, stepIdx, box, isSubmitted, userAnswers, false);
}

// 13. Matrix MR (Multiple response checkboxes per row)
function renderPlayerMatrixMr(q, stepIdx, box, isSubmitted, userAnswers) {
  renderPlayerMatrixBase(q, stepIdx, box, isSubmitted, userAnswers, true);
}

function renderPlayerMatrixBase(q, stepIdx, box, isSubmitted, userAnswers, isMultiResponse) {
  const m = q.matrix || { columns: [], rows: [] };
  const columns = m.columns || [];
  const rows = m.rows || [];
  const tbl = document.createElement('table');
  tbl.className = isMultiResponse ? 'exam-matrix-table matrix-mr-table' : 'exam-matrix-table';
  
  let html = `<thead><tr><th>${escapeHTML(m.firstColumnHeader || (isMultiResponse ? 'Findings' : 'Column 1'))}</th>`;
  columns.forEach(col => { html += `<th>${escapeHTML(col)}</th>`; });
  html += `</tr></thead><tbody>`;
  
  const savedAnswers = userAnswers || {};
  
  rows.forEach((r, rIdx) => {
    html += `<tr><td>${escapeHTML(r.text)}</td>`;
    columns.forEach((col, cIdx) => {
      let isChecked = false;
      if (isMultiResponse) {
        isChecked = (savedAnswers[rIdx] || []).includes(cIdx);
      } else {
        isChecked = savedAnswers[rIdx] === cIdx;
      }
      
      let cellClass = '';
      if (isSubmitted) {
        const isCorrect = isMultiResponse
          ? (r.correctIndices || []).includes(cIdx)
          : r.correctIndex === cIdx;
        
        if (isCorrect) {
          cellClass = 'matrix-cell-correct';
        } else if (isChecked && !isCorrect) {
          cellClass = 'matrix-cell-incorrect';
        }
      }
      
      html += `<td class="${cellClass}">
        <input type="${isMultiResponse ? 'checkbox' : 'radio'}" name="player-matrix-row-${rIdx}" ${isChecked ? 'checked' : ''} ${isSubmitted ? 'disabled' : ''} data-row="${rIdx}" data-col="${cIdx}">
      </td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody>`;
  tbl.innerHTML = html;
  
  if (!isSubmitted) {
    tbl.querySelectorAll('input').forEach(input => {
      input.addEventListener('change', (e) => {
        const row = parseInt(e.target.dataset.row);
        const col = parseInt(e.target.dataset.col);
        if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
        
        if (isMultiResponse) {
          if (!playerAnswers[stepIdx][row]) playerAnswers[stepIdx][row] = [];
          if (e.target.checked) {
            playerAnswers[stepIdx][row].push(col);
          } else {
            playerAnswers[stepIdx][row] = playerAnswers[stepIdx][row].filter(v => v !== col);
          }
        } else {
          playerAnswers[stepIdx][row] = col;
        }
      });
    });
  }
  
  box.appendChild(tbl);
  
  const note = document.createElement('div');
  note.className = 'matrix-note';
  note.textContent = isMultiResponse 
    ? 'Note: Each column must have at least 1 response option selected.' 
    : 'Note: Each row must have only 1 response option selected.';
  box.appendChild(note);
}

// 5. Select N Response
function renderPlayerSelectN(q, stepIdx, box, isSubmitted, userAnswers) {
  const wrapper = document.createElement('div');
  const limit = q.limit || 3;
  wrapper.innerHTML = '';
  
  const savedVal = userAnswers || {};
  const options = q.options || [];
  
  options.forEach((opt, oIdx) => {
    const row = document.createElement('label');
    row.className = 'exam-option-row';
    const isChecked = savedVal[oIdx] === true;
    if (isChecked) row.classList.add('checked');
    
    if (isSubmitted) {
      if (opt.correct) row.classList.add('show-correct');
      else if (isChecked && !opt.correct) row.classList.add('show-incorrect');
    }
    
    row.innerHTML = `
      <input type="checkbox" name="selectN-group" ${isChecked ? 'checked' : ''} ${isSubmitted ? 'disabled' : ''}>
      <div style="display:flex; flex-direction:column; gap:6px; width:100%;">
        <span class="option-text-label">${oIdx + 1}. ${escapeHTML(opt.text)}</span>
        ${opt.imageUrl ? `<img src="${escapeHTML(opt.imageUrl)}" class="option-image" style="max-width:300px; max-height:200px; border-radius:4px; border:1px solid #e5e7eb; margin-top:4px;">` : ''}
      </div>
    `;
    
    if (!isSubmitted) {
      const input = row.querySelector('input');
      input.addEventListener('change', () => {
        const currentCount = Object.values(playerAnswers[stepIdx] || {}).filter(Boolean).length;
        if (input.checked && currentCount >= limit) {
          input.checked = false;
          alert(`You can only select up to ${limit} choices.`);
          return;
        }
        if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
        playerAnswers[stepIdx][oIdx] = input.checked;
        
        if (input.checked) row.classList.add('checked');
        else row.classList.remove('checked');
      });
    }
    wrapper.appendChild(row);
  });
  box.appendChild(wrapper);
}

// 6. Bowtie Player
function renderPlayerBowtie(q, stepIdx, box, isSubmitted, userAnswers) {
  const leftPH = q.bowtieLeftPlaceholder || 'Action to Take';
  const centerPH = q.bowtieCenterPlaceholder || 'Condition Most Likely Experiencing';
  const rightPH = q.bowtieRightPlaceholder || 'Parameter to Monitor';
  
  const col1Header = q.bowtieCol1Header || 'Actions to Take';
  const col2Header = q.bowtieCol2Header || 'Potential Conditions';
  const col3Header = q.bowtieCol3Header || 'Parameters to Monitor';

  const container = document.createElement('div');
  container.className = 'bowtie-container';
  container.style.display = 'flex';
  container.style.flexDirection = 'column';
  container.style.gap = '20px';
  container.style.width = '100%';

  const uA = userAnswers || {};
  const actions = q.bowtieActions || [];
  const conditions = q.bowtieConditions || [];
  const params = q.bowtieParams || [];

  let html = `
    <div class="bowtie-diagram-wrapper" style="display:flex; justify-content:space-between; align-items:center; position:relative; min-height:220px; padding:20px; background:#ffffff; border:0px; border-radius:var(--radius-md); box-shadow:none; user-select:none;">
      
      <svg style="position:absolute; top:20px; left:20px; width:calc(100% - 40px); height:calc(100% - 40px); pointer-events:none; stroke:#cbd5e1; stroke-width:0.5;" viewBox="0 0 100 100" preserveAspectRatio="none">
        <line x1="30" y1="22.2" x2="35" y2="50" />
        <line x1="30" y1="77.8" x2="35" y2="50" />
        <line x1="70" y1="22.2" x2="65" y2="50" />
        <line x1="70" y1="77.8" x2="65" y2="50" />
      </svg>

      <!-- Left Targets Column -->
      <div style="display:flex; flex-direction:column; justify-content:space-between; height:180px; width:30%; z-index:1;">
        <div id="bowtie-target-left1" class="bowtie-target-zone" data-col="1" style="background:#ecf5f4; border:1.5px solid #025287; border-radius:4px; height:80px; display:flex; align-items:center; justify-content:center; padding:8px; text-align:center; position:relative; transition:all 0.2s;">
          <span class="placeholder-text" style="color:#025287; font-size:13px; font-weight:500; opacity:0.6;">${escapeHTML(leftPH)}</span>
        </div>
        <div id="bowtie-target-left2" class="bowtie-target-zone" data-col="1" style="background:#ecf5f4; border:1.5px solid #025287; border-radius:4px; height:80px; display:flex; align-items:center; justify-content:center; padding:8px; text-align:center; position:relative; transition:all 0.2s;">
          <span class="placeholder-text" style="color:#025287; font-size:13px; font-weight:500; opacity:0.6;">${escapeHTML(leftPH)}</span>
        </div>
      </div>

      <!-- Center Target Column -->
      <div style="display:flex; flex-direction:column; justify-content:center; height:180px; width:30%; z-index:1;">
        <div id="bowtie-target-center" class="bowtie-target-zone" data-col="2" style="background:#bae6f2; border:1.5px solid #0891b2; border-radius:4px; height:80px; display:flex; align-items:center; justify-content:center; padding:8px; text-align:center; position:relative; transition:all 0.2s;">
          <span class="placeholder-text" style="color:#0891b2; font-size:13px; font-weight:500; opacity:0.6;">${escapeHTML(centerPH)}</span>
        </div>
      </div>

      <!-- Right Targets Column -->
      <div style="display:flex; flex-direction:column; justify-content:space-between; height:180px; width:30%; z-index:1;">
        <div id="bowtie-target-right1" class="bowtie-target-zone" data-col="3" style="background:#ecf0f5; border:1.5px solid #475569; border-radius:4px; height:80px; display:flex; align-items:center; justify-content:center; padding:8px; text-align:center; position:relative; transition:all 0.2s;">
          <span class="placeholder-text" style="color:#475569; font-size:13px; font-weight:500; opacity:0.6;">${escapeHTML(rightPH)}</span>
        </div>
        <div id="bowtie-target-right2" class="bowtie-target-zone" data-col="3" style="background:#ecf0f5; border:1.5px solid #475569; border-radius:4px; height:80px; display:flex; align-items:center; justify-content:center; padding:8px; text-align:center; position:relative; transition:all 0.2s;">
          <span class="placeholder-text" style="color:#475569; font-size:13px; font-weight:500; opacity:0.6;">${escapeHTML(rightPH)}</span>
        </div>
      </div>

    </div>
  `;

  html += `
    <div class="bowtie-table-wrapper" style="display:flex; gap:16px; width:100%; user-select:none;">
      
      <!-- Column 1 (Ingredients) -->
      <div style="flex:1; border:1.5px solid #000000; border-radius:4px; background:#ffffff; overflow:hidden; align-self: flex-start;">
        <div style="background:#e9f1f7; border-bottom:1.5px solid #000000; padding:10px; font-weight:bold; font-size:13px; text-align:center; color:#1e293b;">
          ${escapeHTML(col1Header)}
        </div>
        <div id="bowtie-table-col1" style="padding:8px; display:flex; flex-direction:column; gap:8px;"></div>
      </div>

      <!-- Column 2 (Orders) -->
      <div style="flex:1; border:1.5px solid #000000; border-radius:4px; background:#ffffff; overflow:hidden; align-self: flex-start;">
        <div style="background:#e9f1f7; border-bottom:1.5px solid #000000; padding:10px; font-weight:bold; font-size:13px; text-align:center; color:#1e293b;">
          ${escapeHTML(col2Header)}
        </div>
        <div id="bowtie-table-col2" style="padding:8px; display:flex; flex-direction:column; gap:8px;"></div>
      </div>

      <!-- Column 3 (Materials) -->
      <div style="flex:1; border:1.5px solid #000000; border-radius:4px; background:#ffffff; overflow:hidden; align-self: flex-start;">
        <div style="background:#e9f1f7; border-bottom:1.5px solid #000000; padding:10px; font-weight:bold; font-size:13px; text-align:center; color:#1e293b;">
          ${escapeHTML(col3Header)}
        </div>
        <div id="bowtie-table-col3" style="padding:8px; display:flex; flex-direction:column; gap:8px;"></div>
      </div>

    </div>
  `;

  container.innerHTML = html;
  box.appendChild(container);

  const placeItemInTarget = (col, idx, targetZone) => {
    const existingItem = targetZone.querySelector('.bowtie-drag-item');
    if (existingItem) {
      const origCol = parseInt(existingItem.dataset.col);
      const origIdx = parseInt(existingItem.dataset.idx);
      const homeSlot = container.querySelector(`.bowtie-home-slot[data-col="${origCol}"][data-idx="${origIdx}"]`);
      if (homeSlot) {
        homeSlot.appendChild(existingItem);
      }
    }
    
    const item = container.querySelector(`.bowtie-drag-item[data-col="${col}"][data-idx="${idx}"]`);
    if (item) {
      targetZone.appendChild(item);
      checkPlaceholderVisibility();
      saveState();
    }
  };

  const checkPlaceholderVisibility = () => {
    container.querySelectorAll('.bowtie-target-zone').forEach(zone => {
      const item = zone.querySelector('.bowtie-drag-item');
      const placeholder = zone.querySelector('.placeholder-text');
      if (placeholder) {
        placeholder.style.display = item ? 'none' : 'block';
      }
    });
  };

  const saveState = () => {
    if (isSubmitted) return;
    const a0Item = container.querySelector('#bowtie-target-left1 .bowtie-drag-item');
    const a1Item = container.querySelector('#bowtie-target-left2 .bowtie-drag-item');
    const condItem = container.querySelector('#bowtie-target-center .bowtie-drag-item');
    const p0Item = container.querySelector('#bowtie-target-right1 .bowtie-drag-item');
    const p1Item = container.querySelector('#bowtie-target-right2 .bowtie-drag-item');
    
    playerAnswers[stepIdx] = {
      action0: a0Item ? a0Item.textContent.trim() : '',
      action1: a1Item ? a1Item.textContent.trim() : '',
      condition: condItem ? condItem.textContent.trim() : '',
      param0: p0Item ? p0Item.textContent.trim() : '',
      param1: p1Item ? p1Item.textContent.trim() : ''
    };
  };

  const populateColumn = (colId, list, colNum, itemColor) => {
    const colList = container.querySelector(`#${colId}`);
    colList.innerHTML = '';
    list.forEach((opt, idx) => {
      const slot = document.createElement('div');
      slot.className = 'bowtie-home-slot';
      slot.dataset.col = colNum;
      slot.dataset.idx = idx;
      slot.style.height = '48px';
      slot.style.background = itemColor;
      slot.style.border = '1px solid #cbd5e1';
      slot.style.borderRadius = '4px';
      slot.style.display = 'flex';
      slot.style.alignItems = 'center';
      slot.style.justifyContent = 'center';
      slot.style.overflow = 'hidden';
      
      const item = document.createElement('div');
      item.className = 'bowtie-drag-item';
      item.draggable = !isSubmitted;
      item.dataset.col = colNum;
      item.dataset.idx = idx;
      item.textContent = opt.text;
      item.style.width = '100%';
      item.style.height = '100%';
      item.style.display = 'flex';
      item.style.alignItems = 'center';
      item.style.justifyContent = 'center';
      item.style.padding = '8px 12px';
      item.style.background = itemColor;
      item.style.color = '#0f172a';
      item.style.fontWeight = '500';
      item.style.fontSize = '12px';
      item.style.textAlign = 'center';
      item.style.cursor = isSubmitted ? 'default' : 'grab';
      item.style.transition = 'opacity 0.2s';

      if (!isSubmitted) {
        item.addEventListener('dragstart', (e) => {
          e.dataTransfer.setData('text/plain', JSON.stringify({ col: colNum, idx: idx }));
          item.style.opacity = '0.5';
        });
        item.addEventListener('dragend', () => {
          item.style.opacity = '1';
        });
        
        slot.addEventListener('dragover', (e) => {
          e.preventDefault();
        });
        slot.addEventListener('drop', (e) => {
          e.preventDefault();
          const data = JSON.parse(e.dataTransfer.getData('text/plain'));
          if (data.col === colNum && data.idx === idx) {
            const dragEl = container.querySelector(`.bowtie-drag-item[data-col="${data.col}"][data-idx="${data.idx}"]`);
            if (dragEl) {
              slot.appendChild(dragEl);
              checkPlaceholderVisibility();
              saveState();
            }
          }
        });
      }

      slot.appendChild(item);
      colList.appendChild(slot);
    });
  };

  populateColumn('bowtie-table-col1', actions, 1, '#ecf5f4');
  populateColumn('bowtie-table-col2', conditions, 2, '#bae6f2');
  populateColumn('bowtie-table-col3', params, 3, '#ecf0f5');

  if (!isSubmitted) {
    container.querySelectorAll('.bowtie-target-zone').forEach(zone => {
      zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.style.transform = 'scale(1.02)';
      });
      zone.addEventListener('dragleave', () => {
        zone.style.transform = 'none';
      });
      zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.style.transform = 'none';
        try {
          const data = JSON.parse(e.dataTransfer.getData('text/plain'));
          const targetCol = parseInt(zone.dataset.col);
          if (data.col !== targetCol) {
            showToast("Invalid placement! Option doesn't match this target type.", "error");
            return;
          }
          placeItemInTarget(data.col, data.idx, zone);
        } catch (err) {
          console.error(err);
        }
      });
    });
  }

  if (uA.action0) {
    const el = Array.from(container.querySelectorAll('.bowtie-drag-item[data-col="1"]')).find(item => item.textContent.trim() === uA.action0);
    if (el) placeItemInTarget(1, parseInt(el.dataset.idx), container.querySelector('#bowtie-target-left1'));
  }
  if (uA.action1) {
    const el = Array.from(container.querySelectorAll('.bowtie-drag-item[data-col="1"]')).find(item => item.textContent.trim() === uA.action1);
    if (el) placeItemInTarget(1, parseInt(el.dataset.idx), container.querySelector('#bowtie-target-left2'));
  }
  if (uA.condition) {
    const el = Array.from(container.querySelectorAll('.bowtie-drag-item[data-col="2"]')).find(item => item.textContent.trim() === uA.condition);
    if (el) placeItemInTarget(2, parseInt(el.dataset.idx), container.querySelector('#bowtie-target-center'));
  }
  if (uA.param0) {
    const el = Array.from(container.querySelectorAll('.bowtie-drag-item[data-col="3"]')).find(item => item.textContent.trim() === uA.param0);
    if (el) placeItemInTarget(3, parseInt(el.dataset.idx), container.querySelector('#bowtie-target-right1'));
  }
  if (uA.param1) {
    const el = Array.from(container.querySelectorAll('.bowtie-drag-item[data-col="3"]')).find(item => item.textContent.trim() === uA.param1);
    if (el) placeItemInTarget(3, parseInt(el.dataset.idx), container.querySelector('#bowtie-target-right2'));
  }

  if (isSubmitted) {
    const checkTarget = (targetEl, correctList) => {
      const item = targetEl.querySelector('.bowtie-drag-item');
      const val = item ? item.textContent.trim() : '';
      const correctTexts = correctList.filter(x => x.correct).map(x => x.text);
      if (val && correctTexts.includes(val)) {
        targetEl.style.border = '2px solid #22c55e';
        targetEl.style.boxShadow = '0 0 8px rgba(34, 197, 94, 0.4)';
      } else {
        targetEl.style.border = '2px solid #ef4444';
        targetEl.style.boxShadow = '0 0 8px rgba(239, 68, 68, 0.4)';
      }
    };
    checkTarget(container.querySelector('#bowtie-target-left1'), actions);
    checkTarget(container.querySelector('#bowtie-target-left2'), actions);
    checkTarget(container.querySelector('#bowtie-target-center'), conditions);
    checkTarget(container.querySelector('#bowtie-target-right1'), params);
    checkTarget(container.querySelector('#bowtie-target-right2'), params);
  }
}

// 7. Multiple Choice (Radio list)
function renderPlayerMultipleChoice(q, stepIdx, box, isSubmitted, userAnswers) {
  const wrapper = document.createElement('div');
  const savedVal = userAnswers || {};
  const options = q.options || [];
  
  options.forEach((opt, oIdx) => {
    const row = document.createElement('label');
    row.className = 'exam-option-row';
    const isChecked = savedVal[oIdx] === true;
    if (isChecked) row.classList.add('checked');
    
    if (isSubmitted) {
      if (opt.correct) row.classList.add('show-correct');
      else if (isChecked && !opt.correct) row.classList.add('show-incorrect');
    }
    
    row.innerHTML = `
      <input type="radio" name="single-mc" ${isChecked ? 'checked' : ''} ${isSubmitted ? 'disabled' : ''}>
      <div style="display:flex; flex-direction:column; gap:6px; width:100%;">
        <span class="option-text-label">${oIdx + 1}. ${escapeHTML(opt.text)}</span>
        ${opt.imageUrl ? `<img src="${escapeHTML(opt.imageUrl)}" class="option-image" style="max-width:300px; max-height:200px; border-radius:4px; border:1px solid #e5e7eb; margin-top:4px;">` : ''}
      </div>
    `;
    
    if (!isSubmitted) {
      row.querySelector('input').addEventListener('change', () => {
        playerAnswers[stepIdx] = { [oIdx]: true };
        wrapper.querySelectorAll('.exam-option-row').forEach(el => el.classList.remove('checked'));
        row.classList.add('checked');
      });
    }
    wrapper.appendChild(row);
  });
  box.appendChild(wrapper);
}

function renderPlayerFillBlank(q, stepIdx, box, isSubmitted, userAnswers) {
  const wrapper = document.createElement('div');
  wrapper.className = 'form-group';
  
  const val = userAnswers ? userAnswers.value : '';
  const unitText = q.unit ? ' ' + q.unit : '';
  
  wrapper.innerHTML = `
    <div style="display: inline-flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 500; margin: 16px 0; flex-wrap: nowrap;">
      <span style="white-space: nowrap;">Answer: </span>
      <input type="text" id="player-blank-input" class="form-control" 
        style="max-width:300px; width:220px; background-color:#f8fafc; border:1.5px solid #000000; color:#000000; display: inline-block; margin: 0; vertical-align: middle; border-radius: 0;" 
        value="${escapeHTML(val)}" ${isSubmitted ? 'disabled' : ''}>
      <span style="white-space: nowrap;">${escapeHTML(unitText)}</span>
    </div>
  `;
  
  if (isSubmitted) {
    const input = wrapper.querySelector('input');
    const correctVal = (q.correctAnswer || '').toString().trim().toLowerCase();
    const userVal = (val || '').toString().trim().toLowerCase();
    if (correctVal === userVal || parseFloat(correctVal) === parseFloat(userVal)) {
      input.style.borderColor = 'var(--accent-green)';
      input.style.backgroundColor = 'rgba(16, 185, 129, 0.08)';
    } else {
      input.style.borderColor = 'var(--accent-red)';
      input.style.backgroundColor = 'rgba(239, 68, 68, 0.08)';
    }
  } else {
    wrapper.querySelector('input').addEventListener('input', (e) => {
      playerAnswers[stepIdx] = { value: e.target.value };
    });
  }
  box.appendChild(wrapper);
}

// 9. Hotspot Player
function renderPlayerHotspot(q, stepIdx, box, isSubmitted, userAnswers) {
  const wrapper = document.createElement('div');
  wrapper.style.textAlign = 'center';
  
  const click = userAnswers || {}; // { x: val, y: val }
  
  wrapper.innerHTML = `
    <div id="hotspot-play-container" class="hotspot-image-container">
      <img id="hotspot-play-img" class="hotspot-image" src="${escapeHTML(q.imageUrl)}" alt="Hotspot Graphic">
      ${click.x !== undefined ? `<div class="hotspot-click-marker" style="left:${click.x}%; top:${click.y}%;"></div>` : ''}
      ${isSubmitted ? `<div class="hotspot-target-region" style="left:${Math.min(q.rect.x1, q.rect.x2)}%; top:${Math.min(q.rect.y1, q.rect.y2)}%; width:${Math.abs(q.rect.x2 - q.rect.x1)}%; height:${Math.abs(q.rect.y2 - q.rect.y1)}%;"></div>` : ''}
    </div>
  `;
  
  const container = wrapper.querySelector('#hotspot-play-container');
  if (!isSubmitted) {
    container.addEventListener('click', (e) => {
      const bounds = container.getBoundingClientRect();
      const clickX = ((e.clientX - bounds.left) / bounds.width) * 100;
      const clickY = ((e.clientY - bounds.top) / bounds.height) * 100;
      
      playerAnswers[stepIdx] = { x: clickX, y: clickY };
      
      // Place marker in DOM
      let marker = container.querySelector('.hotspot-click-marker');
      if (!marker) {
        marker = document.createElement('div');
        marker.className = 'hotspot-click-marker';
        container.appendChild(marker);
      }
      marker.style.left = clickX + '%';
      marker.style.top = clickY + '%';
    });
  }
  
  box.appendChild(wrapper);
}

// 10. Ordered Response Player
function renderPlayerOrderedResponse(q, stepIdx, box, isSubmitted, userAnswers) {
  const correctSequence = q.orderedOptions || [];
  const stateAnswers = userAnswers || { order: [] }; // { order: [items] }
  
  // Shuffled options list (only generated once or stored)
  if (!stateAnswers.shuffled) {
    // Never start an ordering question already in the correct order.
    const distinctItems = new Set(correctSequence).size > 1;
    do {
      stateAnswers.shuffled = shuffleArray(correctSequence);
    } while (distinctItems && stateAnswers.shuffled.every((item, i) => item === correctSequence[i]));
    // Remove items already placed in ordered box
    stateAnswers.shuffled = stateAnswers.shuffled.filter(item => !stateAnswers.order.includes(item));
  }
  
  const container = document.createElement('div');
  container.className = 'ordered-response-container';
  
  container.innerHTML = `
    <div>
      <div class="order-box-title">Unordered Options</div>
      <div id="order-left-box" class="order-box"></div>
    </div>
    <div class="order-actions-col">
      <button id="move-right-btn" class="btn-order-action" ${isSubmitted ? 'disabled' : ''}>&rarr;</button>
      <button id="move-left-btn" class="btn-order-action" ${isSubmitted ? 'disabled' : ''}>&larr;</button>
    </div>
    <div>
      <div class="order-box-title">Your Ordered Steps</div>
      <div id="order-right-box" class="order-box"></div>
    </div>
    <div class="order-actions-col" style="padding-left: 6px;">
      <button id="move-up-btn" class="btn-order-action" ${isSubmitted ? 'disabled' : ''}>&uarr;</button>
      <button id="move-down-btn" class="btn-order-action" ${isSubmitted ? 'disabled' : ''}>&darr;</button>
    </div>
  `;
  
  const leftBox = container.querySelector('#order-left-box');
  const rightBox = container.querySelector('#order-right-box');
  
  let selectedLeftItem = null;
  let selectedRightItem = null;
  
  const renderItemLists = () => {
    leftBox.innerHTML = '';
    rightBox.innerHTML = '';
    
    // Left Box Unordered
    stateAnswers.shuffled.forEach(item => {
      const el = document.createElement('div');
      el.className = `order-item ${selectedLeftItem === item ? 'selected' : ''}`;
      el.textContent = item;
      if (!isSubmitted) {
        el.addEventListener('click', () => {
          selectedLeftItem = item;
          selectedRightItem = null;
          renderItemLists();
        });
      }
      leftBox.appendChild(el);
    });
    
    // Right Box Ordered
    stateAnswers.order.forEach((item, idx) => {
      const el = document.createElement('div');
      el.className = `order-item ${selectedRightItem === item ? 'selected' : ''}`;
      el.innerHTML = `
        <span>${idx + 1}. ${escapeHTML(item)}</span>
      `;
      if (isSubmitted) {
        if (correctSequence[idx] === item) {
          el.style.borderColor = 'var(--accent-green)';
          el.style.backgroundColor = 'rgba(16, 185, 129, 0.05)';
        } else {
          el.style.borderColor = 'var(--accent-red)';
          el.style.backgroundColor = 'rgba(239, 68, 68, 0.05)';
        }
      } else {
        el.addEventListener('click', () => {
          selectedRightItem = item;
          selectedLeftItem = null;
          renderItemLists();
        });
      }
      rightBox.appendChild(el);
    });
  };
  
  renderItemLists();
  
  // Wire Action buttons
  if (!isSubmitted) {
    container.querySelector('#move-right-btn').addEventListener('click', () => {
      if (selectedLeftItem) {
        stateAnswers.order.push(selectedLeftItem);
        stateAnswers.shuffled = stateAnswers.shuffled.filter(x => x !== selectedLeftItem);
        selectedLeftItem = null;
        playerAnswers[stepIdx] = stateAnswers;
        renderItemLists();
      }
    });
    
    container.querySelector('#move-left-btn').addEventListener('click', () => {
      if (selectedRightItem) {
        stateAnswers.shuffled.push(selectedRightItem);
        stateAnswers.order = stateAnswers.order.filter(x => x !== selectedRightItem);
        selectedRightItem = null;
        playerAnswers[stepIdx] = stateAnswers;
        renderItemLists();
      }
    });
    
    container.querySelector('#move-up-btn').addEventListener('click', () => {
      if (selectedRightItem) {
        const idx = stateAnswers.order.indexOf(selectedRightItem);
        if (idx > 0) {
          // Swap up
          stateAnswers.order[idx] = stateAnswers.order[idx - 1];
          stateAnswers.order[idx - 1] = selectedRightItem;
          playerAnswers[stepIdx] = stateAnswers;
          renderItemLists();
        }
      }
    });
    
    container.querySelector('#move-down-btn').addEventListener('click', () => {
      if (selectedRightItem) {
        const idx = stateAnswers.order.indexOf(selectedRightItem);
        if (idx !== -1 && idx < stateAnswers.order.length - 1) {
          // Swap down
          stateAnswers.order[idx] = stateAnswers.order[idx + 1];
          stateAnswers.order[idx + 1] = selectedRightItem;
          playerAnswers[stepIdx] = stateAnswers;
          renderItemLists();
        }
      }
    });
  }
  
  box.appendChild(container);
}

// 11. Select All (SATA / Trend)
function renderPlayerSata(q, stepIdx, box, isSubmitted, userAnswers) {
  const wrapper = document.createElement('div');
  const savedVal = userAnswers || {};
  const options = q.options || [];
  
  options.forEach((opt, oIdx) => {
    const row = document.createElement('label');
    row.className = 'exam-option-row';
    const isChecked = savedVal[oIdx] === true;
    if (isChecked) row.classList.add('checked');
    
    if (isSubmitted) {
      if (opt.correct) row.classList.add('show-correct');
      else if (isChecked && !opt.correct) row.classList.add('show-incorrect');
    }
    
    row.innerHTML = `
      <input type="checkbox" ${isChecked ? 'checked' : ''} ${isSubmitted ? 'disabled' : ''}>
      <div style="display:flex; flex-direction:column; gap:6px; width:100%;">
        <span class="option-text-label">${oIdx + 1}. ${escapeHTML(opt.text)}</span>
        ${opt.imageUrl ? `<img src="${escapeHTML(opt.imageUrl)}" class="option-image" style="max-width:300px; max-height:200px; border-radius:4px; border:1px solid #e5e7eb; margin-top:4px;">` : ''}
      </div>
    `;
    
    if (!isSubmitted) {
      row.querySelector('input').addEventListener('change', (e) => {
        if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
        playerAnswers[stepIdx][oIdx] = e.target.checked;
        if (e.target.checked) row.classList.add('checked');
        else row.classList.remove('checked');
      });
    }
    wrapper.appendChild(row);
  });
  box.appendChild(wrapper);
}

// 12. Highlight Text/Table Player
function renderPlayerHighlight(q, stepIdx, box, isSubmitted, userAnswers) {
  const container = document.createElement('div');
  container.className = 'player-highlight-tabs-container';
  
  if (!q.highlightTabs) {
    q.highlightTabs = [
      { id: 'ht_' + Date.now(), title: "Nurses' Notes", content: q.highlightText || '' }
    ];
  }
  
  if (!playerHighlightActiveTabId || !q.highlightTabs.find(t => t.id === playerHighlightActiveTabId)) {
    playerHighlightActiveTabId = q.highlightTabs[0].id;
  }
  
  const activeTab = q.highlightTabs.find(t => t.id === playerHighlightActiveTabId);
  
  if (q.maxCorrectSelections) {
    const limitInfo = document.createElement('div');
    limitInfo.className = 'highlight-limit-info';
    limitInfo.style.marginBottom = '12px';
    limitInfo.style.fontSize = '13px';
    limitInfo.style.fontWeight = '700';
    limitInfo.style.color = '#025287';
    limitInfo.textContent = `Select ${q.maxCorrectSelections} correct findings.`;
    container.appendChild(limitInfo);
  }
  
  // Render tabs bar (always show, even if there's only 1 tab)
  const tabsBar = document.createElement('div');
  tabsBar.className = 'patient-chart-tabs-bar';
  q.highlightTabs.forEach(t => {
    const tabBtn = document.createElement('button');
    tabBtn.className = `patient-chart-tab ${t.id === playerHighlightActiveTabId ? 'active' : ''}`;
    tabBtn.textContent = t.title;
    tabBtn.addEventListener('click', () => {
      playerHighlightActiveTabId = t.id;
      box.innerHTML = '';
      renderPlayerHighlight(q, stepIdx, box, isSubmitted, userAnswers);
    });
    tabsBar.appendChild(tabBtn);
  });
  container.appendChild(tabsBar);
  
  // Calculate global index offset for the active tab's highlight items
  let globalHighlightIdx = 0;
  for (let i = 0; i < q.highlightTabs.indexOf(activeTab); i++) {
    const text = q.highlightTabs[i].content || '';
    const matches = text.match(/\{([^{|]+)(?:\|([^{}]+))?\}/g) || [];
    globalHighlightIdx += matches.length;
  }
  
  // Content container with border (uses patient-chart-content styling)
  const contentBox = document.createElement('div');
  contentBox.className = 'patient-chart-content';
  
  const passage = document.createElement('div');
  passage.className = 'highlight-passage';
  
  const rawText = activeTab.content || '';
  // Format nurses notes styling
  const formattedHtml = formatNursesNotes(rawText, activeTab.title);
  passage.innerHTML = formattedHtml;
  
  let currentLocalHIdx = 0;
  const savedAnswers = userAnswers || {};
  
  function processNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent;
      if (!text.includes('{')) return;
      
      const regex = /\{([^{|]+)(?:\|([^{}]+))?\}/g;
      const fragment = document.createDocumentFragment();
      let match;
      let lastIndex = 0;
      let hasMatch = false;
      
      while ((match = regex.exec(text)) !== null) {
        hasMatch = true;
        if (match.index > lastIndex) {
          fragment.appendChild(document.createTextNode(text.substring(lastIndex, match.index)));
        }
        
        const phrase = match[1];
        const isCorrect = match[2] === 'correct';
        const currentHIdx = globalHighlightIdx + (currentLocalHIdx++);
        
        const span = document.createElement('span');
        span.className = 'highlight-span';
        span.textContent = phrase;
        
        const isSelected = savedAnswers[currentHIdx] === true;
        if (isSelected) span.classList.add('selected');
        
        if (isSubmitted) {
          if (isCorrect) {
            span.classList.add('show-correct');
          } else if (isSelected) {
            span.classList.add('show-incorrect');
          }
        } else {
          span.addEventListener('click', () => {
            if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
            
            const state = !playerAnswers[stepIdx][currentHIdx];
            if (state && q.maxCorrectSelections) {
              const selectedCount = Object.values(playerAnswers[stepIdx]).filter(v => v === true).length;
              if (selectedCount >= q.maxCorrectSelections) {
                showToast(`You can only select up to ${q.maxCorrectSelections} findings.`, "error");
                return;
              }
            }
            
            playerAnswers[stepIdx][currentHIdx] = state;
            if (state) {
              span.classList.add('selected');
            } else {
              span.classList.remove('selected');
            }
          });
        }
        
        fragment.appendChild(span);
        lastIndex = regex.lastIndex;
      }
      
      if (hasMatch) {
        if (lastIndex < text.length) {
          fragment.appendChild(document.createTextNode(text.substring(lastIndex)));
        }
        node.parentNode.replaceChild(fragment, node);
      }
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      // Process children
      const children = Array.from(node.childNodes);
      children.forEach(child => processNode(child));
    }
  }
  
  processNode(passage);
  
  contentBox.appendChild(passage);
  container.appendChild(contentBox);
  box.appendChild(container);
}

// 14. Grouped Multiple Response Player
function renderPlayerGroupedMr(q, stepIdx, box, isSubmitted, userAnswers) {
  const groups = q.groupedRows || [];
  const container = document.createElement('div');
  
  const savedAnswers = userAnswers || {}; // { groupIdx: { oIdx: boolean } }
  
  groups.forEach((g, gIdx) => {
    const card = document.createElement('div');
    card.className = 'grouped-mr-category';
    
    card.innerHTML = `
      <div class="grouped-mr-category-title">${escapeHTML(g.title)}</div>
      <div class="grouped-mr-category-body"></div>
    `;
    const body = card.querySelector('.grouped-mr-category-body');
    const groupSavedVal = savedAnswers[gIdx] || {};
    const options = g.options || [];
    
    options.forEach((opt, oIdx) => {
      const row = document.createElement('label');
      row.className = 'exam-option-row';
      const isChecked = groupSavedVal[oIdx] === true;
      if (isChecked) row.classList.add('checked');
      
      if (isSubmitted) {
        if (opt.correct) row.classList.add('show-correct');
        else if (isChecked && !opt.correct) row.classList.add('show-incorrect');
      }
      
      row.innerHTML = `
        <input type="checkbox" ${isChecked ? 'checked' : ''} ${isSubmitted ? 'disabled' : ''}>
        <span class="option-text-label">${escapeHTML(opt.text)}</span>
      `;
      
      if (!isSubmitted) {
        row.querySelector('input').addEventListener('change', (e) => {
          if (!playerAnswers[stepIdx]) playerAnswers[stepIdx] = {};
          if (!playerAnswers[stepIdx][gIdx]) playerAnswers[stepIdx][gIdx] = {};
          
          playerAnswers[stepIdx][gIdx][oIdx] = e.target.checked;
          if (e.target.checked) row.classList.add('checked');
          else row.classList.remove('checked');
        });
      }
      
      body.appendChild(row);
    });
    container.appendChild(card);
  });
  box.appendChild(container);
}
