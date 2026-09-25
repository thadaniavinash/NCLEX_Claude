/* Case study editor: screens, chart tabs, rich text, per-question-type configurators and the table cell menu. */

/* ================= TEMPLATE GENERATION TOOL (EDITOR) ================= */
function initEditorEvents() {
  initRichTextEditors();
  
  const themeToggleBtn = document.getElementById('editor-theme-toggle-btn');
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', toggleTheme);
  }

  const courseSelect = document.getElementById('case-course-select');
  if (courseSelect) {
    courseSelect.addEventListener('change', (e) => {
      populateEditorUnitSelect(e.target.value, '');
    });
  }

  document.getElementById('editor-back-btn').addEventListener('click', () => {
    if (!saveCurrentStepData(false, true)) return;
    saveCurrentCaseOrStandalone();
    switchView('dashboard');
  });
  
  document.getElementById('editor-save-btn').addEventListener('click', () => {
    if (!saveCurrentStepData()) return;
    saveCurrentCaseOrStandalone();
    showToast("Progress saved successfully.");
  });

  document.getElementById('editor-export-btn').addEventListener('click', () => {
    if (!saveCurrentStepData()) return;
    saveCurrentCaseOrStandalone();
    exportCaseStudy(currentCase);
  });

  // Question Image Configuration Event Listeners
  const chooseImgBtn = document.getElementById('choose-question-image-btn');
  const imgFileInput = document.getElementById('question-image-file-input');
  const removeImgBtn = document.getElementById('remove-question-image-btn');
  
  if (chooseImgBtn && imgFileInput && removeImgBtn) {
    chooseImgBtn.addEventListener('click', () => imgFileInput.click());
    
    imgFileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
          const base64Str = event.target.result;
          const step = currentCase.screens[currentStepIndex];
          if (step && step.question) {
            step.question.questionImage = base64Str;
            updateImagePreview(base64Str);
          }
        };
        reader.readAsDataURL(file);
      }
    });
    
    removeImgBtn.addEventListener('click', () => {
      const step = currentCase.screens[currentStepIndex];
      if (step && step.question) {
        step.question.questionImage = null;
        imgFileInput.value = '';
        updateImagePreview(null);
      }
    });
  }
  
  document.getElementById('editor-play-btn').addEventListener('click', () => {
    if (!saveCurrentStepData()) return;
    saveCurrentCaseOrStandalone();
    startPlayer(currentCase);
  });

  document.getElementById('add-step-btn').addEventListener('click', addStepToCase);
  document.getElementById('add-tab-btn').addEventListener('click', addTabToStep);
  document.getElementById('delete-active-tab-btn').addEventListener('click', deleteActiveTab);
  
  document.getElementById('tab-title-input').addEventListener('input', (e) => {
    const activeTabItem = document.querySelector(`.tab-editor-item[data-id="${activeTabId}"] span`);
    if (activeTabItem) {
      activeTabItem.textContent = e.target.value;
    }
  });

  document.getElementById('tab-text-input').addEventListener('blur', () => {
    saveActiveTabContent();
  });

  document.getElementById('tab-text-input').addEventListener('focus', (e) => {
    if (!activeTabId) return;
    const step = currentCase.screens[currentStepIndex];
    if (!step) return;
    const tabs = step.leftContent.tabs;
    const tab = tabs.find(t => t.id === activeTabId);
    if (tab && tab.title && /nurse|note|log|progress/i.test(tab.title)) {
      const stripped = stripNursesNotesFormatting(e.target.innerHTML);
      if (e.target.innerHTML !== stripped) {
        e.target.innerHTML = stripped;
      }
    }
  });

  document.getElementById('tab-text-input').addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      document.execCommand('insertHTML', false, '&nbsp;&nbsp;&nbsp;&nbsp;');
    }
  });

  document.getElementById('question-type-select').addEventListener('change', (e) => {
    const prevType = currentCase.screens[currentStepIndex].question.type;
    if (!saveCurrentStepData(true)) {
      e.target.value = prevType;
      return;
    }
    const q = currentCase.screens[currentStepIndex].question;
    q.type = e.target.value;
    
    // Prepopulate defaults based on NGN type
    initializeQuestionTypeDefaults(q);
    
    renderEditorStep(currentStepIndex);
  });
}

function initializeQuestionTypeDefaults(q) {
  // 0/1 Scoring
  if (q.type === 'dropdown_cloze' || q.type === 'drag_drop_cloze' || q.type === 'dyad' || q.type === 'triad') {
    if (!q.cloze) {
      q.cloze = { text: '', dropdowns: [] };
    }
    
    const textStr = q.cloze.text || '';
    const isStandardDefault = !textStr || textStr === 'The patient should be ordered [[drop0]] due to [[drop1]].' || textStr === 'The patient should...[[drop0]]...due to...[[drop1]]';
    const isTriadText = textStr.includes('[[drop2]]') || textStr.includes('and [[drop2]]');
    const isDyadText = !isTriadText && textStr.includes('[[drop1]]');

    if (q.type === 'dyad') {
      if (isStandardDefault || isTriadText || !textStr) {
        q.cloze.text = 'The nurse should...[[drop0]]...as most evidenced by...[[drop1]]';
      }
      // Enforce exactly 2 slots for Dyad
      if (q.cloze.dropdowns.length !== 2) {
        q.cloze.dropdowns = [
          q.cloze.dropdowns[0] || { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] },
          q.cloze.dropdowns[1] || { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] }
        ];
      }
    } else if (q.type === 'triad') {
      if (isStandardDefault || isDyadText || !textStr) {
        q.cloze.text = 'The nurse should...[[drop0]]...as most evidenced by...[[drop1]] and [[drop2]]';
      }
      // Enforce exactly 3 slots for Triad
      if (q.cloze.dropdowns.length !== 3) {
        q.cloze.dropdowns = [
          q.cloze.dropdowns[0] || { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] },
          q.cloze.dropdowns[1] || { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] },
          q.cloze.dropdowns[2] || { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] }
        ];
      }
    } else if (q.type === 'dropdown_cloze' || q.type === 'drag_drop_cloze') {
      const cleanStem = (q.stem || '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, '').trim();
      if (!cleanStem) {
        q.stem = 'Complete the following sentence by choosing from the lists of options.';
      }
      if (!textStr) {
        q.cloze.text = 'The patient should...[[drop0]]...due to...[[drop1]]';
        q.cloze.dropdowns = [
          { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] },
          { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] }
        ];
      }
    }
  } else if (q.type === 'dropdown_table') {
    const cleanStem = (q.stem || '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, '').trim();
    if (!cleanStem) {
      q.stem = 'Complete the following table by...';
    }
    q.dropdownTableHeader1 = '';
    q.dropdownTableHeader2 = '';
    if (!q.dropdownTableRows) {
      q.dropdownTableRows = [
        { label: '', placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }] },
        { label: '', placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }] }
      ];
    }
  } else if (q.type === 'matrix_mc') {
    const cleanStem = (q.stem || '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, '').trim();
    if (!cleanStem || cleanStem === 'For each..., click to specify...') {
      q.stem = '';
    }
    if (!q.matrix) {
      q.matrix = {
        firstColumnHeader: '',
        columns: ['Indicated', 'Not Indicated'],
        rows: [
          { text: '', correctIndex: 0, correctIndices: [0] },
          { text: '', correctIndex: 0, correctIndices: [0] }
        ]
      };
    } else {
      if (q.matrix.firstColumnHeader === 'Potential Interventions' || q.matrix.firstColumnHeader === 'Findings') {
        q.matrix.firstColumnHeader = '';
      }
      const genericRows = ['polyuria', 'weight gain', 'New Row 1', 'New Row 2'];
      q.matrix.rows.forEach(r => {
        if (genericRows.includes(r.text)) {
          r.text = '';
        }
      });
      while (q.matrix.columns.length < 2) q.matrix.columns.push('');
      if (q.matrix.columns.length > 2) q.matrix.columns = q.matrix.columns.slice(0, 2);
    }
  } else if (q.type === 'matrix_mr') {
    const cleanStem = (q.stem || '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, '').trim();
    if (!cleanStem) {
      q.stem = 'For each assessment finding below, click to specify if the finding is consistent with the disease process of ... . Each finding may support more than 1 disease process.';
    }
    if (!q.matrix) {
      q.matrix = {
        firstColumnHeader: '',
        columns: ['', '', ''],
        rows: [
          { text: '', correctIndices: [] },
          { text: '', correctIndices: [] }
        ]
      };
    } else {
      const genericRows = ['polyuria', 'weight gain', 'New Row 1', 'New Row 2'];
      q.matrix.rows.forEach(r => {
        if (genericRows.includes(r.text)) {
          r.text = '';
        }
      });
      while (q.matrix.columns.length < 3) q.matrix.columns.push('');
      if (q.matrix.columns.length > 3) q.matrix.columns = q.matrix.columns.slice(0, 3);
    }
  } else if (q.type === 'select_n') {
    if (!q.options) {
      q.options = [
        { text: 'Option 1', correct: true },
        { text: 'Option 2', correct: true },
        { text: 'Option 3', correct: false }
      ];
    }
    q.limit = q.limit || 2;
  } else if (q.type === 'bowtie') {
    if (!q.bowtieActions) {
      q.bowtieActions = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
      q.bowtieConditions = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
      q.bowtieParams = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
    }
  } else if (q.type === 'multiple_choice') {
    if (!q.options || q.options.length !== 4) {
      const currentOpts = q.options || [];
      q.options = [
        currentOpts[0] || { text: '', correct: true },
        currentOpts[1] || { text: '', correct: false },
        currentOpts[2] || { text: '', correct: false },
        currentOpts[3] || { text: '', correct: false }
      ];
      const hasCorrect = q.options.some(o => o.correct);
      if (!hasCorrect) {
        q.options[0].correct = true;
      }
    }
  } else if (q.type === 'fill_blank') {
    const cleanStem = (q.stem || '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, '').trim();
    if (!cleanStem || cleanStem === 'Add question...') {
      q.stem = '';
    }
    if (!q.correctAnswer || q.correctAnswer === '12.5') {
      q.correctAnswer = '';
    }
  } else if (q.type === 'hotspot') {
    if (!q.imageUrl) {
      q.imageUrl = 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600'; // clinic / anatomy fallback
      q.rect = { x1: 30, y1: 30, x2: 70, y2: 70 };
    }
  } else if (q.type === 'ordered_response') {
    if (!q.orderedOptions) {
      q.orderedOptions = ['First action', 'Second action', 'Third action'];
    }
  }
  // +/- Scoring
  else if (q.type === 'select_all' || q.type === 'trend') {
    if (q.type === 'select_all') {
      if (!q.options || q.options.length < 5) {
        q.options = [
          { text: '', correct: false },
          { text: '', correct: false },
          { text: '', correct: false },
          { text: '', correct: false },
          { text: '', correct: false }
        ];
      }
    } else {
      if (!q.options) {
        q.options = [{ text: 'Fever', correct: true }, { text: 'Cough', correct: false }, { text: 'Dyspnea', correct: true }];
      }
    }
  } else if (q.type === 'highlight' || q.type === 'highlight_2') {
    if (!q.highlightTabs) {
      q.highlightTabs = [
        { id: 'ht_' + Date.now(), title: "Nurses' Notes", content: q.highlightText || 'The client reports {pain in left calf|correct}. Respirations are {shallow and labored|correct}. Temperature is {98.6 F}.' }
      ];
    }
  } else if (q.type === 'grouped_mr') {
    if (!q.groupedRows) {
      q.groupedRows = [
        {
          title: 'Non-pharmacological',
          options: [{ text: 'restrict fluids', correct: true }, { text: 'bed rest', correct: false }]
        },
        {
          title: 'Pharmacological',
          options: [{ text: 'furosemide', correct: true }, { text: 'normal saline bolus', correct: false }]
        }
      ];
    }
  }
}

function startEditor(c) {
  migrateCaseTypes(c);
  currentCase = c;
  currentStepIndex = 0;
  
  const courseSelect = document.getElementById('case-course-select');
  const unitSelect = document.getElementById('case-unit-select');
  if (courseSelect) {
    courseSelect.value = c.course || '';
    populateEditorUnitSelect(c.course || '', c.unit || '');
  }

  const select = document.getElementById('case-disorder-select');
  if (select) {
    select.innerHTML = '<option value="">Categorize Case Study</option>' + 
      PATHOPHYSIOLOGY_DISORDERS.map(d => `<option value="${escapeHTML(d)}">${escapeHTML(d)}</option>`).join('');
    select.value = c.disorder || '';
  }
  
  document.getElementById('case-title-input').value = c.title || '';
  document.getElementById('case-desc-input').value = c.description || '';
  
  const stepsSidebar = document.querySelector('.editor-steps-sidebar');
  if (stepsSidebar) {
    if (c.isStandalone) {
      stepsSidebar.classList.add('hidden');
    } else {
      stepsSidebar.classList.remove('hidden');
    }
  }
  
  switchView('editor');
  renderEditorStep(0);
}

function renderEditorStep(stepIdx) {
  currentStepIndex = stepIdx;
  const step = currentCase.screens[stepIdx];
  if (!step) return;

  currentCase.title = document.getElementById('case-title-input').value;
  currentCase.description = document.getElementById('case-desc-input').value;
  
  renderStepsSidebar();
  
  const stdChartEditor = document.getElementById('standard-chart-editor');
  const highlightPlaceholder = document.getElementById('highlight-chart-placeholder');
  const q = step.question;
  
  if (stdChartEditor && highlightPlaceholder) {
    if (q.type === 'highlight') {
      stdChartEditor.classList.add('hidden');
      highlightPlaceholder.classList.remove('hidden');
    } else {
      stdChartEditor.classList.remove('hidden');
      highlightPlaceholder.classList.add('hidden');
    }
  }
  
  document.getElementById('step-intro-input').innerHTML = step.leftContent.intro || '';
  renderEditorTabs(step.leftContent.tabs);
  
  document.getElementById('question-type-select').value = q.type;
  document.getElementById('question-preamble-input').innerHTML = q.preamble || '';
  
  const stemInput = document.getElementById('question-stem-input');
  if (q.type === 'matrix_mc') {
    stemInput.setAttribute('placeholder', 'For each..., click to specify...');
  } else if (q.type === 'dropdown_table') {
    stemInput.setAttribute('placeholder', 'Complete the following table by...');
  } else if (q.type === 'dropdown_cloze' || q.type === 'drag_drop_cloze') {
    stemInput.setAttribute('placeholder', 'Complete the following sentence by choosing from the lists of options.');
  } else if (q.type === 'fill_blank') {
    stemInput.setAttribute('placeholder', 'Add question...');
  } else {
    stemInput.setAttribute('placeholder', 'e.g. Which of the following findings require follow-up? Select all that apply.');
  }
  stemInput.innerHTML = q.stem || '';
  document.getElementById('question-explanation-input').innerHTML = q.explanation || '';
  
  // Update image preview in editor
  updateImagePreview(q.questionImage || null);
  
  renderDynamicQuestionConfigurator(q);
}

function updateImagePreview(base64Str) {
  const container = document.getElementById('question-image-preview-container');
  const img = document.getElementById('question-image-preview');
  const removeBtn = document.getElementById('remove-question-image-btn');
  
  if (container && img && removeBtn) {
    if (base64Str) {
      img.src = base64Str;
      container.classList.remove('hidden');
      removeBtn.classList.remove('hidden');
    } else {
      img.src = '';
      container.classList.add('hidden');
      removeBtn.classList.add('hidden');
    }
  }
}

function renderStepsSidebar() {
  const stepsList = document.getElementById('editor-steps-list');
  stepsList.innerHTML = '';
  
  currentCase.screens.forEach((step, idx) => {
    const item = document.createElement('div');
    item.className = `step-nav-item ${idx === currentStepIndex ? 'active' : ''}`;
    item.innerHTML = `
      <span>Screen ${idx + 1}</span>
      ${currentCase.screens.length > 1 ? `
        <button class="btn-step-delete" title="Delete Screen">
          <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
        </button>
      ` : ''}
    `;
    
    item.addEventListener('click', (e) => {
      if (e.target.closest('.btn-step-delete')) {
        e.stopPropagation();
        deleteStep(idx);
      } else {
        if (!saveCurrentStepData()) return;
        renderEditorStep(idx);
      }
    });
    
    stepsList.appendChild(item);
  });
}

function addStepToCase() {
  if (!saveCurrentStepData()) return;
  const nextNum = currentCase.screens.length + 1;
  
  // Carry over tabs and intro from previous screen if available, otherwise set default Nurses' Notes
  const prevStep = currentCase.screens[currentCase.screens.length - 1];
  let carriedTabs = [];
  let carriedIntro = '';
  if (prevStep && prevStep.leftContent) {
    if (prevStep.leftContent.tabs) {
      carriedTabs = JSON.parse(JSON.stringify(prevStep.leftContent.tabs));
    }
    carriedIntro = prevStep.leftContent.intro || '';
  } else {
    carriedTabs = [
      { id: 'nn_' + Date.now(), title: "Nurses' Notes", content: '' }
    ];
  }
  
  const newStep = {
    step: nextNum,
    leftContent: {
      intro: carriedIntro,
      tabs: carriedTabs
    },
    question: {
      type: 'select_all',
      stem: '',
      options: [
        { text: '', correct: false },
        { text: '', correct: false },
        { text: '', correct: false },
        { text: '', correct: false },
        { text: '', correct: false }
      ],
      explanation: ''
    }
  };
  
  currentCase.screens.push(newStep);
  renderEditorStep(currentCase.screens.length - 1);
  showToast("Added screen " + nextNum);
}

function deleteStep(idx) {
  if (confirm(`Are you sure you want to delete Screen ${idx + 1}?`)) {
    currentCase.screens.splice(idx, 1);
    currentCase.screens.forEach((s, i) => s.step = i + 1);
    
    const newIdx = Math.max(0, currentStepIndex - 1);
    renderEditorStep(newIdx);
    showToast("Screen deleted.");
  }
}

function renderEditorTabs(tabs) {
  const list = document.getElementById('editor-tabs-list');
  list.innerHTML = '';
  
  if (tabs.length === 0) {
    document.getElementById('tab-content-editor').classList.add('hidden');
    activeTabId = '';
    return;
  }
  
  document.getElementById('tab-content-editor').classList.remove('hidden');
  
  if (!activeTabId || !tabs.find(t => t.id === activeTabId)) {
    activeTabId = tabs[0].id;
  }
  
  tabs.forEach((t) => {
    const tabEl = document.createElement('div');
    tabEl.className = `tab-editor-item ${t.id === activeTabId ? 'active' : ''}`;
    tabEl.setAttribute('data-id', t.id);
    tabEl.innerHTML = `<span>${escapeHTML(t.title)}</span>`;
    
    tabEl.addEventListener('click', () => {
      saveActiveTabContent();
      activeTabId = t.id;
      renderEditorTabs(tabs);
    });
    
    list.appendChild(tabEl);
  });
  
  const activeTab = tabs.find(t => t.id === activeTabId);
  document.getElementById('tab-title-input').value = activeTab.title;
  document.getElementById('tab-text-input').innerHTML = activeTab.content || '';
  document.getElementById('active-tab-label').textContent = `Content for "${activeTab.title}"`;
}

function saveActiveTabContent() {
  if (!activeTabId) return;
  const step = currentCase.screens[currentStepIndex];
  if (!step) return;
  const tabs = step.leftContent.tabs;
  const tab = tabs.find(t => t.id === activeTabId);
  if (tab) {
    tab.title = document.getElementById('tab-title-input').value;
    const rawContent = document.getElementById('tab-text-input').innerHTML;
    tab.content = formatNursesNotes(rawContent, tab.title);
    document.getElementById('tab-text-input').innerHTML = tab.content;
  }
}

function addTabToStep() {
  saveActiveTabContent();
  const tabs = currentCase.screens[currentStepIndex].leftContent.tabs;
  const newId = 'tab_' + Date.now();
  const newTab = {
    id: newId,
    title: 'New Tab',
    content: ''
  };
  
  tabs.push(newTab);
  activeTabId = newId;
  renderEditorStep(currentStepIndex);
}

function deleteActiveTab() {
  const tabs = currentCase.screens[currentStepIndex].leftContent.tabs;
  if (tabs.length <= 1) {
    alert("Must keep at least one chart tab.");
    return;
  }
  
  if (confirm("Delete this chart tab?")) {
    const idx = tabs.findIndex(t => t.id === activeTabId);
    tabs.splice(idx, 1);
    activeTabId = tabs[0].id;
    renderEditorStep(currentStepIndex);
  }
}

function saveCurrentStepData(isChangingType = false, isBackingOut = false) {
  if (!currentCase || currentCase.screens.length === 0) return true;
  
  const courseSelect = document.getElementById('case-course-select');
  const unitSelect = document.getElementById('case-unit-select');
  if (courseSelect && unitSelect) {
    currentCase.course = courseSelect.value || '';
    currentCase.unit = unitSelect.value || '';
    currentCase.disorder = currentCase.unit || currentCase.course || 'Others';
    currentCase.topic = currentCase.unit || currentCase.course || 'Others';
  } else {
    const select = document.getElementById('case-disorder-select');
    if (select) {
      currentCase.disorder = select.value;
    }
  }
  
  currentCase.title = document.getElementById('case-title-input').value;
  currentCase.description = document.getElementById('case-desc-input').value;
  
  const step = currentCase.screens[currentStepIndex];
  if (!step) return true;
  
  step.leftContent.intro = document.getElementById('step-intro-input').innerHTML;
  saveActiveTabContent();
  
  const q = step.question;
  
  q.preamble = document.getElementById('question-preamble-input').innerHTML;
  q.stem = document.getElementById('question-stem-input').innerHTML;
  q.explanation = document.getElementById('question-explanation-input').innerHTML;
  
  // Specific complex sync
  if (q.type === 'fill_blank') {
    const el = document.getElementById('fill-blank-correct-input');
    if (el) q.correctAnswer = el.value;
    const unitEl = document.getElementById('fill-blank-unit-input');
    if (unitEl) q.unit = unitEl.value;
  } else if (q.type === 'hotspot') {
    const el = document.getElementById('hotspot-url-input');
    if (el) q.imageUrl = el.value;
  } else if (q.type === 'highlight' || q.type === 'highlight_2') {
    const el = document.getElementById('highlight-tab-text-input');
    if (el && q.highlightTabs) {
      const activeTab = q.highlightTabs.find(t => t.id === highlightActiveTabId);
      if (activeTab) {
        activeTab.content = el.innerHTML;
      }
    }
    const titleEl = document.getElementById('highlight-tab-title-input');
    if (titleEl && q.highlightTabs) {
      const activeTab = q.highlightTabs.find(t => t.id === highlightActiveTabId);
      if (activeTab) {
        activeTab.title = titleEl.value;
      }
    }
    const maxInput = document.getElementById('highlight-max-correct-input');
    if (maxInput) q.maxCorrectSelections = parseInt(maxInput.value) || null;
  }
  
  const cIdx = caseStudies.findIndex(x => x.id === currentCase.id);
  if (cIdx !== -1) {
    caseStudies[cIdx] = currentCase;
  } else {
    // Also save standalone question back to its array
    const qIdx = standaloneQuestions.findIndex(x => x.id === currentCase.id);
    if (qIdx !== -1) {
      standaloneQuestions[qIdx] = currentCase;
    }
  }
  return true;
}

function exportCaseStudy(c) {
  const jsonStr = JSON.stringify(c, null, 2);
  const blob = new Blob([jsonStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `${c.title.replace(/\s+/g, '_')}_NGN_Quiz.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  showToast("Quiz JSON exported successfully.");
}

/* ================= 17 DYNAMIC EDITOR RENDERERS ================= */
function renderDynamicQuestionConfigurator(q) {
  const box = document.getElementById('question-details-editor');
  box.innerHTML = '';

  switch (q.type) {
    case 'dropdown_cloze':
    case 'drag_drop_cloze':
    case 'dyad':
    case 'triad':
      renderClozeConfigurator(q, box);
      break;
    case 'dropdown_table':
      renderDropdownTableConfigurator(q, box);
      break;
    case 'matrix_mc':
      renderMatrixMcConfigurator(q, box);
      break;
    case 'matrix_mr':
      renderMatrixMrConfigurator(q, box);
      break;
    case 'select_n':
      renderSelectNConfigurator(q, box);
      break;
    case 'bowtie':
      renderBowtieConfigurator(q, box);
      break;
    case 'multiple_choice':
      renderMultipleChoiceConfigurator(q, box);
      break;
    case 'fill_blank':
      renderFillBlankConfigurator(q, box);
      break;
    case 'hotspot':
      renderHotspotConfigurator(q, box);
      break;
    case 'ordered_response':
      renderOrderedResponseConfigurator(q, box);
      break;
    case 'select_all':
    case 'trend':
      renderSataConfigurator(q, box);
      break;
    case 'highlight':
    case 'highlight_2':
      renderHighlightConfigurator(q, box);
      break;
    case 'grouped_mr':
      renderGroupedMrConfigurator(q, box);
      break;
  }
}

function getClozeSegments(text, expectedCount) {
  const regex = /\[\[d(?:r)?op(\d+)\]\]/gi;
  let match;
  const matches = [];
  while ((match = regex.exec(text)) !== null) {
    matches.push({
      index: parseInt(match[1]),
      start: match.index,
      end: regex.lastIndex
    });
  }
  
  matches.sort((a, b) => a.index - b.index);
  
  const segments = [];
  let lastIndex = 0;
  for (let i = 0; i < expectedCount; i++) {
    const currentMatch = matches.find(m => m.index === i);
    if (currentMatch) {
      segments.push(text.substring(lastIndex, currentMatch.start));
      lastIndex = currentMatch.end;
    } else {
      segments.push('');
    }
  }
  segments.push(text.substring(lastIndex));
  return segments;
}

// 1. Cloze (Shared for Dropdown Cloze, Drag & Drop, Dyad, Triad)
function renderClozeConfigurator(q, box) {
  const c = q.cloze || { text: '', dropdowns: [] };
  const wrapper = document.createElement('div');
  
  const isDyadOrTriad = (q.type === 'dyad' || q.type === 'triad');
  
  let instructions = 'Sentence contains drop-down options. Set the choices and placeholder for each slot below.';
  if (q.type === 'dyad') instructions = 'Dyad requires exactly 2 slots: [[drop0]] and [[drop1]]. Both must be correct to score 1 point.';
  if (q.type === 'triad') instructions = 'Triad requires exactly 3 slots: [[drop0]], [[drop1]], and [[drop2]]. All must be correct.';
  
  let expectedSlots;
  if (q.type === 'dyad') {
    expectedSlots = 2;
  } else if (q.type === 'triad') {
    expectedSlots = 3;
  } else {
    if (!c.dropdowns || c.dropdowns.length === 0) {
      c.dropdowns = [
        { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] },
        { placeholder: 'Select...', options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }] }
      ];
    }
    expectedSlots = c.dropdowns.length;
  }
  
  const segments = getClozeSegments(c.text || '', expectedSlots);
  let segmentInputsHTML = '';
  
  for (let i = 0; i <= expectedSlots; i++) {
    let placeholder = 'Text...';
    if (q.type === 'dyad') {
      if (i === 0) placeholder = 'The nurse should...';
      else if (i === 1) placeholder = '...as most evidenced by...';
      else if (i === 2) placeholder = 'Suffix text (optional)...';
    } else if (q.type === 'triad') {
      if (i === 0) placeholder = 'The nurse should...';
      else if (i === 1) placeholder = '...as most evidenced by...';
      else if (i === 2) placeholder = '...and...';
      else if (i === 3) placeholder = 'Suffix text (optional)...';
    } else {
      if (i === 0) placeholder = 'The patient should...';
      else if (i === 1) placeholder = '...due to...';
      else placeholder = 'Suffix text (optional)...';
    }
    
    segmentInputsHTML += `<input type="text" class="cloze-segment-input form-control" data-index="${i}" style="flex: 1; min-width: 140px; font-size:12px; padding:6px;" value="${escapeHTML(segments[i] || '')}" placeholder="${placeholder}">`;
    
    if (i < expectedSlots) {
      segmentInputsHTML += `<span class="cloze-slot-badge" style="background:#025287; color:white; padding:4px 8px; border-radius:4px; font-weight:600; font-size:11px; white-space:nowrap; user-select:none;">[Slot ${i + 1}]</span>`;
    }
  }
  
  const actionButtonsHTML = !isDyadOrTriad ? `
    <div style="margin-top: 10px; display: flex; gap: 8px;">
      <button id="add-cloze-slot-btn" class="btn btn-secondary btn-xs">+ Add Dropdown Slot</button>
      ${expectedSlots > 1 ? `<button id="remove-cloze-slot-btn" class="btn btn-danger btn-xs">- Remove Last Slot</button>` : ''}
    </div>
  ` : '';
  
  wrapper.innerHTML = `
    <div class="cloze-warning">${instructions}</div>
    <div class="form-group">
      <label>Question</label>
      <div style="display:flex; flex-direction:column; gap:10px; background:rgba(255,255,255,0.03); padding:12px; border-radius:var(--radius-sm); border:1px solid var(--border-dash);">
        <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
          ${segmentInputsHTML}
        </div>
        ${actionButtonsHTML}
      </div>
    </div>
    <div id="cloze-dropdowns-settings" style="margin-top: 16px;"></div>
  `;
  
  box.appendChild(wrapper);
  
  const settingsBox = document.getElementById('cloze-dropdowns-settings');
  
  const parseCloze = () => {
    const inputs = Array.from(wrapper.querySelectorAll('.cloze-segment-input'));
    inputs.sort((a, b) => parseInt(a.dataset.index) - parseInt(b.dataset.index));
    const segs = inputs.map(inp => inp.value);
    
    let assembledText = '';
    for (let i = 0; i < expectedSlots; i++) {
      assembledText += (segs[i] || '') + `[[drop${i}]]`;
    }
    assembledText += (segs[expectedSlots] || '');
    c.text = assembledText;
    
    settingsBox.innerHTML = '';
    const regex = /\[\[d(?:r)?op(\d+)\]\]/gi;
    let match;
    const foundIndices = [];
    while ((match = regex.exec(c.text)) !== null) {
      foundIndices.push(parseInt(match[1]));
    }
    const unique = [...new Set(foundIndices)].sort((a,b) => a-b);
    
    const temp = [];
    unique.forEach(idx => {
      if (!c.dropdowns[idx]) {
        c.dropdowns[idx] = {
          placeholder: 'Select...',
          options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }]
        };
      }
      const dd = c.dropdowns[idx];
      temp[idx] = dd;
      
      const card = document.createElement('div');
      card.className = 'cloze-dropdown-card';
      card.innerHTML = `
        <h6>Slot [[drop${idx}]]</h6>
        <input type="text" class="cloze-placeholder-input form-control" value="${escapeHTML(dd.placeholder)}" placeholder="Add placeholder...">
        <div class="options-config-title">
          <span>Choices</span>
          <button class="btn btn-text btn-xs add-choice-btn">+ Add Option</button>
        </div>
        <div class="choices-list"></div>
      `;
      
      card.querySelector('.cloze-placeholder-input').addEventListener('input', (e) => {
        dd.placeholder = e.target.value;
      });
      
      const choicesList = card.querySelector('.choices-list');
      const renderChoices = () => {
        choicesList.innerHTML = '';
        dd.options.forEach((opt, oIdx) => {
          const row = document.createElement('div');
          row.className = 'option-config-row';
          const placeholderText = `Choice ${String.fromCharCode(65 + oIdx)}`;
          
          let val = opt.text || '';
          const genericDefaults = [
            'Choice A', 'Choice B', 'Choice C', 'Choice D', 'Choice E',
            'Choice X', 'Choice Y', 'Choice Z',
            'Choice 1', 'Choice 2', 'Choice 3',
            'Correct Option', 'Incorrect Option', 'New Choice'
          ];
          if (genericDefaults.includes(val)) {
            val = '';
            opt.text = '';
          }
          
          row.innerHTML = `
            <input type="radio" name="cloze-correct-${idx}" class="choice-correct-toggle" ${opt.correct ? 'checked' : ''}>
            <input type="text" class="option-text-input form-control" style="font-size:12px; padding:6px;" value="${escapeHTML(val)}" placeholder="${placeholderText}">
            <button class="btn-option-delete">&times;</button>
          `;
          
          row.querySelector('.option-text-input').addEventListener('input', (e) => {
            opt.text = e.target.value;
          });
          row.querySelector('.choice-correct-toggle').addEventListener('change', () => {
            dd.options.forEach((o, oi) => o.correct = oi === oIdx);
          });
          row.querySelector('.btn-option-delete').addEventListener('click', () => {
            dd.options.splice(oIdx, 1);
            renderChoices();
          });
          choicesList.appendChild(row);
        });
      };
      
      card.querySelector('.add-choice-btn').addEventListener('click', () => {
        dd.options.push({ text: '', correct: false });
        renderChoices();
      });
      
      renderChoices();
      settingsBox.appendChild(card);
    });
    c.dropdowns = temp;
  };
  
  wrapper.querySelectorAll('.cloze-segment-input').forEach(inp => {
    inp.addEventListener('input', parseCloze);
  });
  
  if (!isDyadOrTriad) {
    const addBtn = wrapper.querySelector('#add-cloze-slot-btn');
    if (addBtn) {
      addBtn.addEventListener('click', () => {
        const inputs = Array.from(wrapper.querySelectorAll('.cloze-segment-input'));
        inputs.sort((a, b) => parseInt(a.dataset.index) - parseInt(b.dataset.index));
        const segs = inputs.map(inp => inp.value);
        
        let assembledText = '';
        for (let i = 0; i < expectedSlots; i++) {
          assembledText += (segs[i] || '') + `[[drop${i}]]`;
        }
        assembledText += (segs[expectedSlots] || '');
        c.text = assembledText + `[[drop${expectedSlots}]]`;
        
        c.dropdowns.push({
          placeholder: 'Select...',
          options: [{ text: '', correct: true }, { text: '', correct: false }, { text: '', correct: false }]
        });
        
        renderDynamicQuestionConfigurator(q);
      });
    }
    
    const removeBtn = wrapper.querySelector('#remove-cloze-slot-btn');
    if (removeBtn) {
      removeBtn.addEventListener('click', () => {
        if (expectedSlots <= 1) return;
        
        const inputs = Array.from(wrapper.querySelectorAll('.cloze-segment-input'));
        inputs.sort((a, b) => parseInt(a.dataset.index) - parseInt(b.dataset.index));
        const segs = inputs.map(inp => inp.value);
        
        let assembledText = '';
        for (let i = 0; i < expectedSlots - 1; i++) {
          assembledText += (segs[i] || '') + `[[drop${i}]]`;
        }
        assembledText += (segs[expectedSlots - 1] || '') + (segs[expectedSlots] || '');
        c.text = assembledText;
        
        c.dropdowns.pop();
        
        renderDynamicQuestionConfigurator(q);
      });
    }
  }
  
  parseCloze();
}

// 2. Drop-Down Table Configurator
function renderDropdownTableConfigurator(q, box) {
  const rows = q.dropdownTableRows || [];
  
  if (rows.length === 0) {
    rows.push({
      label: '',
      placeholder: 'Select...',
      options: [{ text: '', correct: true }, { text: '', correct: false }]
    });
    rows.push({
      label: '',
      placeholder: 'Select...',
      options: [{ text: '', correct: true }, { text: '', correct: false }]
    });
    q.dropdownTableRows = rows;
  }

  const wrapper = document.createElement('div');
  wrapper.className = 'dropdown-table-editor-wrapper';
  wrapper.style.marginTop = '12px';

  const renderTable = () => {
    wrapper.innerHTML = '';
    
    const tableContainer = document.createElement('div');
    tableContainer.style.overflowX = 'auto';
    
    const table = document.createElement('table');
    table.className = 'matrix-grid-designer-table';
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';
    table.style.marginBottom = '12px';
    
    // THEAD
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    // Headers are reset when the question type changes (initializeQuestionTypeDefaults),
    // not on every render, so headers an author typed are never erased.
    const h1Val = q.dropdownTableHeader1 || '';
    const h2Val = q.dropdownTableHeader2 || '';
    
    // Column 1 Header Input
    const th1 = document.createElement('th');
    th1.style.padding = '8px';
    th1.style.minWidth = '200px';
    th1.innerHTML = `
      <input type="text" class="form-control dropdown-table-header-1-input" style="font-weight:bold; font-size:12px; padding:6px;" value="${escapeHTML(h1Val)}" placeholder="Column 1 Header Text">
    `;
    th1.querySelector('.dropdown-table-header-1-input').addEventListener('input', (e) => {
      q.dropdownTableHeader1 = e.target.value;
    });
    headerRow.appendChild(th1);
    
    // Column 2 Header Input
    const th2 = document.createElement('th');
    th2.style.padding = '8px';
    th2.style.minWidth = '280px';
    th2.innerHTML = `
      <input type="text" class="form-control dropdown-table-header-2-input" style="font-weight:bold; font-size:12px; padding:6px;" value="${escapeHTML(h2Val)}" placeholder="Column 2 Header Text">
    `;
    th2.querySelector('.dropdown-table-header-2-input').addEventListener('input', (e) => {
      q.dropdownTableHeader2 = e.target.value;
    });
    headerRow.appendChild(th2);
    
    // Action column header
    const thAction = document.createElement('th');
    thAction.style.width = '50px';
    thAction.innerHTML = '';
    headerRow.appendChild(thAction);
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // TBODY
    const tbody = document.createElement('tbody');
    rows.forEach((row, rIdx) => {
      const tr = document.createElement('tr');
      
      // Clean generic row label strings to empty for placeholder behavior
      let rLabel = row.label || '';
      const genericRows = ['Sensory Perception', 'Moisture', 'Activity', 'Mobility', 'Nutrition', 'Friction and Shear'];
      if (genericRows.includes(rLabel)) {
        rLabel = '';
        row.label = '';
      }
      
      // Left Cell: Row label input
      const tdLabel = document.createElement('td');
      tdLabel.style.padding = '8px';
      tdLabel.style.verticalAlign = 'top';
      tdLabel.innerHTML = `
        <input type="text" class="form-control row-label-input" style="font-size:12px; padding:6px; font-weight:500;" value="${escapeHTML(rLabel)}" placeholder="Text...">
      `;
      tdLabel.querySelector('.row-label-input').addEventListener('input', (e) => {
        row.label = e.target.value;
      });
      tr.appendChild(tdLabel);
      
      // Right Cell: Placeholder and Dropdown options configurator
      const tdOptions = document.createElement('td');
      tdOptions.style.padding = '8px';
      tdOptions.innerHTML = `
        <div style="display:flex; flex-direction:column; gap:6px;">
          <input type="text" class="form-control row-placeholder-input" style="font-size:11px; padding:4px 8px; font-style:italic;" value="${escapeHTML(row.placeholder || 'Select...')}" placeholder="Placeholder (e.g. Select...)">
          <div class="row-options-container" style="display:flex; flex-direction:column; gap:4px; margin-top:4px;"></div>
          <button class="btn btn-text btn-xs add-row-option-btn" style="align-self:flex-start; font-size:10px; margin-top:2px;">+ Add Option</button>
        </div>
      `;
      
      const placeholderInput = tdOptions.querySelector('.row-placeholder-input');
      placeholderInput.addEventListener('input', (e) => {
        row.placeholder = e.target.value;
      });
      
      const optionsContainer = tdOptions.querySelector('.row-options-container');
      const renderRowOptions = () => {
        optionsContainer.innerHTML = '';
        const opts = row.options || [];
        opts.forEach((opt, oIdx) => {
          const optDiv = document.createElement('div');
          optDiv.style.display = 'flex';
          optDiv.style.alignItems = 'center';
          optDiv.style.gap = '6px';
          
          let val = opt.text || '';
          const genericDefaults = [
            'Choice A', 'Choice B', 'Choice C',
            'Option 1', 'Option 2', 'Option 3',
            '1 - Correct', '2 - Incorrect', 'Correct Answer', 'Incorrect Answer', 'New Option', 'New Choice'
          ];
          if (genericDefaults.includes(val)) {
            val = '';
            opt.text = '';
          }
          const placeholderText = `Option ${oIdx + 1}`;
          
          optDiv.innerHTML = `
            <input type="radio" name="dropdown-table-correct-radio-${rIdx}" class="row-opt-correct-toggle" ${opt.correct ? 'checked' : ''} style="cursor:pointer;">
            <input type="text" class="form-control row-opt-text-input" style="font-size:11px; padding:4px 6px; flex-grow:1;" value="${escapeHTML(val)}" placeholder="${placeholderText}">
            <button class="delete-opt-btn" style="background:transparent; border:none; color:#ef4444; font-size:16px; cursor:pointer; padding:0 4px;">&times;</button>
          `;
          
          optDiv.querySelector('.row-opt-text-input').addEventListener('input', (e) => {
            opt.text = e.target.value;
          });
          optDiv.querySelector('.row-opt-correct-toggle').addEventListener('change', () => {
            opts.forEach((o, oi) => o.correct = oi === oIdx);
          });
          optDiv.querySelector('.delete-opt-btn').addEventListener('click', () => {
            opts.splice(oIdx, 1);
            renderRowOptions();
          });
          
          optionsContainer.appendChild(optDiv);
        });
      };
      
      tdOptions.querySelector('.add-row-option-btn').addEventListener('click', () => {
        if (!row.options) row.options = [];
        row.options.push({ text: '', correct: false });
        renderRowOptions();
      });
      
      renderRowOptions();
      tr.appendChild(tdOptions);
      
      // Delete Row Button Cell
      const tdDel = document.createElement('td');
      tdDel.style.padding = '8px';
      tdDel.style.verticalAlign = 'top';
      tdDel.style.textAlign = 'center';
      tdDel.innerHTML = `
        <button class="delete-row-btn" style="background:transparent; border:none; color:#ef4444; font-size:18px; cursor:pointer; padding:4px 0 0 0;">&times;</button>
      `;
      tdDel.querySelector('.delete-row-btn').addEventListener('click', () => {
        rows.splice(rIdx, 1);
        renderTable();
      });
      tr.appendChild(tdDel);
      
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    tableContainer.appendChild(table);
    wrapper.appendChild(tableContainer);
    
    // Bottom Action Buttons
    const btnContainer = document.createElement('div');
    btnContainer.style.display = 'flex';
    btnContainer.style.marginTop = '10px';
    
    const addRowBtn = document.createElement('button');
    addRowBtn.className = 'btn btn-secondary btn-xs';
    addRowBtn.textContent = '+ Add Row';
    addRowBtn.addEventListener('click', () => {
      rows.push({
        label: '',
        placeholder: 'Select...',
        options: [{ text: '', correct: true }, { text: '', correct: false }]
      });
      renderTable();
    });
    btnContainer.appendChild(addRowBtn);
    wrapper.appendChild(btnContainer);
  };
  
  renderTable();
  box.appendChild(wrapper);
}

// 3. Matrix MC (Single choice per row)
function renderMatrixMcConfigurator(q, box) {
  renderMatrixBaseConfigurator(q, box, false);
}

// 4. Matrix MR (Multiple response/checkboxes per row)
function renderMatrixMrConfigurator(q, box) {
  renderMatrixBaseConfigurator(q, box, true);
}

function renderMatrixBaseConfigurator(q, box, isMultiResponse) {
  if (!q.matrix) {
    q.matrix = {
      firstColumnHeader: '',
      columns: isMultiResponse ? ['', '', ''] : ['Indicated', 'Not Indicated'],
      rows: isMultiResponse ? [
        { text: '', correctIndices: [], correctIndex: 0 },
        { text: '', correctIndices: [], correctIndex: 0 }
      ] : [
        { text: '', correctIndex: 0, correctIndices: [0] },
        { text: '', correctIndex: 0, correctIndices: [0] }
      ]
    };
  }
  const m = q.matrix;
  if (!m.firstColumnHeader && isMultiResponse) {
    m.firstColumnHeader = '';
  }
  if (!m.columns || m.columns.length < 2) {
    m.columns = isMultiResponse ? ['', '', ''] : ['Indicated', 'Not Indicated'];
  }
  if (!m.rows || m.rows.length === 0) {
    m.rows = isMultiResponse ? [
      { text: '', correctIndex: 0, correctIndices: [] },
      { text: '', correctIndex: 0, correctIndices: [] }
    ] : [
      { text: '', correctIndex: 0, correctIndices: [0] },
      { text: '', correctIndex: 0, correctIndices: [0] }
    ];
  }

  const wrapper = document.createElement('div');
  wrapper.className = 'matrix-table-editor-wrapper';
  wrapper.style.marginTop = '12px';

  const renderTable = () => {
    wrapper.innerHTML = '';
    
    const tableContainer = document.createElement('div');
    tableContainer.style.overflowX = 'auto';
    
    const table = document.createElement('table');
    table.className = 'matrix-grid-designer-table';
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';
    table.style.marginBottom = '12px';
    
    // THEAD
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    // Generic default headers are cleared when the question type changes
    // (initializeQuestionTypeDefaults), not here: clearing on every render erased
    // headers such as "Findings" that authors chose on purpose.
    const h1Val = m.firstColumnHeader || '';

    // First column header input
    const thFirst = document.createElement('th');
    thFirst.style.padding = '8px';
    thFirst.style.minWidth = '180px';
    thFirst.innerHTML = `
      <input type="text" class="form-control matrix-first-header-input" style="font-weight:bold; font-size:12px; padding:6px;" value="${escapeHTML(h1Val)}" placeholder="Add text...">
    `;
    thFirst.querySelector('.matrix-first-header-input').addEventListener('input', (e) => {
      m.firstColumnHeader = e.target.value;
    });
    headerRow.appendChild(thFirst);
    
    // Additional column headers inputs
    m.columns.forEach((col, cIdx) => {
      const thCol = document.createElement('th');
      thCol.style.padding = '8px';
      thCol.style.textAlign = 'center';
      thCol.style.position = 'relative';
      thCol.style.minWidth = '120px';
      thCol.innerHTML = `
        <div style="display:flex; align-items:center; gap:4px; justify-content:center;">
          <input type="text" class="form-control matrix-col-header-input" style="font-size:12px; text-align:center; padding:6px;" value="${escapeHTML(col)}" placeholder="Add text...">
          ${m.columns.length > 2 ? `<button class="delete-col-btn" style="background:transparent; border:none; color:#ef4444; font-size:16px; cursor:pointer; padding:0 4px;">&times;</button>` : ''}
        </div>
      `;
      thCol.querySelector('.matrix-col-header-input').addEventListener('input', (e) => {
        m.columns[cIdx] = e.target.value;
      });
      if (m.columns.length > 2) {
        thCol.querySelector('.delete-col-btn').addEventListener('click', () => {
          m.columns.splice(cIdx, 1);
          // Shift correct indexes if needed
          m.rows.forEach(r => {
            if (isMultiResponse) {
              r.correctIndices = (r.correctIndices || []).filter(idx => idx !== cIdx).map(idx => idx > cIdx ? idx - 1 : idx);
            } else {
              if (r.correctIndex === cIdx) r.correctIndex = 0;
              else if (r.correctIndex > cIdx) r.correctIndex--;
            }
          });
          renderTable();
        });
      }
      headerRow.appendChild(thCol);
    });
    
    // Actions column header
    const thActions = document.createElement('th');
    thActions.style.width = '50px';
    thActions.style.padding = '8px';
    thActions.innerHTML = '';
    headerRow.appendChild(thActions);
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // TBODY
    const tbody = document.createElement('tbody');
    m.rows.forEach((r, rIdx) => {
      const tr = document.createElement('tr');
      
      // Clean generic row label strings to empty for placeholder behavior
      let rText = r.text || '';
      const genericRows = ['polyuria', 'weight gain', 'New Row 1', 'New Row 2'];
      if (genericRows.includes(rText)) {
        rText = '';
        r.text = '';
      }
      
      // Row Label Input
      const tdLabel = document.createElement('td');
      tdLabel.style.padding = '8px';
      tdLabel.innerHTML = `
        <input type="text" class="form-control matrix-row-label-input" style="font-size:12px; padding:6px;" value="${escapeHTML(rText)}" placeholder="Text...">
      `;
      tdLabel.querySelector('.matrix-row-label-input').addEventListener('input', (e) => {
        r.text = e.target.value;
      });
      tr.appendChild(tdLabel);
      
      // Correct indicator cells
      m.columns.forEach((col, cIdx) => {
        const tdCheck = document.createElement('td');
        tdCheck.style.padding = '8px';
        tdCheck.style.textAlign = 'center';
        
        const isChecked = isMultiResponse
          ? (r.correctIndices || []).includes(cIdx)
          : r.correctIndex === cIdx;
        
        tdCheck.innerHTML = `
          <input type="${isMultiResponse ? 'checkbox' : 'radio'}" name="matrix-row-radio-${rIdx}" ${isChecked ? 'checked' : ''} style="transform: scale(1.1); cursor:pointer;">
        `;
        tdCheck.querySelector('input').addEventListener('change', (e) => {
          if (isMultiResponse) {
            if (!r.correctIndices) r.correctIndices = [];
            if (e.target.checked) {
              r.correctIndices.push(cIdx);
            } else {
              r.correctIndices = r.correctIndices.filter(v => v !== cIdx);
            }
          } else {
            r.correctIndex = cIdx;
          }
        });
        tr.appendChild(tdCheck);
      });
      
      // Delete Row Button Cell
      const tdDel = document.createElement('td');
      tdDel.style.padding = '8px';
      tdDel.style.textAlign = 'center';
      tdDel.innerHTML = `
        <button class="delete-row-btn" style="background:transparent; border:none; color:#ef4444; font-size:18px; cursor:pointer; padding:0;">&times;</button>
      `;
      tdDel.querySelector('.delete-row-btn').addEventListener('click', () => {
        m.rows.splice(rIdx, 1);
        renderTable();
      });
      tr.appendChild(tdDel);
      
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    tableContainer.appendChild(table);
    wrapper.appendChild(tableContainer);
    
    // Bottom Action Buttons
    const btnContainer = document.createElement('div');
    btnContainer.style.display = 'flex';
    btnContainer.style.gap = '10px';
    btnContainer.style.marginTop = '10px';
    
    const addRowBtn = document.createElement('button');
    addRowBtn.className = 'btn btn-secondary btn-xs';
    addRowBtn.textContent = '+ Add Row';
    addRowBtn.addEventListener('click', () => {
      m.rows.push({ text: '', correctIndex: 0, correctIndices: [0] });
      renderTable();
    });
    btnContainer.appendChild(addRowBtn);
    
    const addColBtn = document.createElement('button');
    addColBtn.className = 'btn btn-secondary btn-xs';
    addColBtn.textContent = '+ Add Column';
    addColBtn.addEventListener('click', () => {
      m.columns.push('');
      renderTable();
    });
    btnContainer.appendChild(addColBtn);
    
    wrapper.appendChild(btnContainer);
  };
  
  renderTable();
  box.appendChild(wrapper);
}

// 5. Select N Configurator
function renderSelectNConfigurator(q, box) {
  renderOptionsBaseConfigurator(q, box, true, true);
}

// 7. Multiple Choice Configurator
function renderMultipleChoiceConfigurator(q, box) {
  renderOptionsBaseConfigurator(q, box, false, false);
}

// 11. Select All Configurator
function renderSataConfigurator(q, box) {
  renderOptionsBaseConfigurator(q, box, true, false);
}

function renderOptionsBaseConfigurator(q, box, isCheckbox, showNLimit) {
  const wrapper = document.createElement('div');
  if (showNLimit) {
    wrapper.innerHTML = `
      <div class="form-group" style="margin-bottom:16px;">
        <label>Select Exactly N Limit</label>
        <input type="number" id="selectN-limit-input" class="form-control" style="width:100px;" value="${q.limit || 3}">
      </div>
    `;
  }
  wrapper.innerHTML += `
    <div class="options-config-title">
      <span>Options List</span>
      <button id="add-option-btn" class="btn btn-text btn-xs">+ Add Option</button>
    </div>
    <div id="options-config-list"></div>
  `;
  box.appendChild(wrapper);
  
  if (showNLimit) {
    document.getElementById('selectN-limit-input').addEventListener('input', (e) => {
      q.limit = parseInt(e.target.value) || 3;
    });
  }
  
  const list = document.getElementById('options-config-list');
  const renderRows = () => {
    list.innerHTML = '';
    if (!q.options) q.options = [];
    
    q.options.forEach((opt, idx) => {
      const div = document.createElement('div');
      div.className = 'option-config-row';
      div.style.display = 'flex';
      div.style.flexDirection = 'column';
      div.style.gap = '8px';
      div.style.border = '1px solid #334155';
      div.style.padding = '8px';
      div.style.borderRadius = 'var(--radius-sm)';
      div.style.marginBottom = '8px';
      div.style.background = '#1e293b';
      
      const placeholderText = `Option ${String.fromCharCode(65 + idx)}`;
      
      let val = opt.text || '';
      const genericDefaults = [
        'Option A', 'Option B', 'Option C', 'Option D', 'Option E', 'Option F',
        'Option 1', 'Option 2', 'Option 3', 'Option 4'
      ];
      if (genericDefaults.includes(val)) {
        val = '';
        opt.text = '';
      }
      
      div.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px; width:100%;">
          <input type="${isCheckbox ? 'checkbox' : 'radio'}" name="correct-option-group" class="option-correct-toggle" ${opt.correct ? 'checked' : ''}>
          <input type="text" class="option-text-input form-control" style="flex-grow:1;" value="${escapeHTML(val)}" placeholder="${placeholderText}">
          <button class="btn-option-delete">&times;</button>
        </div>
        <div style="display:flex; align-items:center; gap:8px; width:100%;">
          <span style="font-size:11px; color:#94a3b8; flex-shrink:0;">Image URL:</span>
          <input type="text" class="option-image-input form-control" style="font-size:11px; padding:4px 8px; flex-grow:1; height:24px;" value="${escapeHTML(opt.imageUrl || '')}" placeholder="Option image URL or Base64 data...">
          <button class="btn btn-secondary btn-xs select-image-file-btn" style="font-size:10px; height:24px; padding:0 8px; flex-shrink:0;">Choose File</button>
          <input type="file" class="option-image-file-input" accept="image/*" style="display:none;">
        </div>
      `;
      
      div.querySelector('.option-text-input').addEventListener('input', (e) => {
        opt.text = e.target.value;
      });
      div.querySelector('.option-image-input').addEventListener('input', (e) => {
        opt.imageUrl = e.target.value;
      });
      
      const fileInput = div.querySelector('.option-image-file-input');
      const selectBtn = div.querySelector('.select-image-file-btn');
      const imgInput = div.querySelector('.option-image-input');
      
      selectBtn.addEventListener('click', () => {
        fileInput.click();
      });
      fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (evt) => {
          opt.imageUrl = evt.target.result;
          imgInput.value = evt.target.result;
          showToast("Image loaded from local computer.");
        };
        reader.readAsDataURL(file);
      });

      div.querySelector('.option-correct-toggle').addEventListener('change', (e) => {
        if (isCheckbox) {
          opt.correct = e.target.checked;
        } else {
          q.options.forEach((o, oi) => o.correct = oi === idx);
        }
      });
      div.querySelector('.btn-option-delete').addEventListener('click', () => {
        q.options.splice(idx, 1);
        renderRows();
      });
      
      list.appendChild(div);
    });
  };
  
  renderRows();
  
  document.getElementById('add-option-btn').addEventListener('click', () => {
    if (!q.options) q.options = [];
    q.options.push({ text: 'New Option', correct: false });
    renderRows();
  });
}

// 6. Bowtie Configurator
function renderBowtieConfigurator(q, box) {
  if (!q.bowtieActions) q.bowtieActions = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
  if (!q.bowtieConditions) q.bowtieConditions = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
  if (!q.bowtieParams) q.bowtieParams = [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }];
  
  if (!q.bowtieLeftPlaceholder) q.bowtieLeftPlaceholder = '';
  if (!q.bowtieCenterPlaceholder) q.bowtieCenterPlaceholder = '';
  if (!q.bowtieRightPlaceholder) q.bowtieRightPlaceholder = '';
  
  if (!q.bowtieCol1Header) q.bowtieCol1Header = '';
  if (!q.bowtieCol2Header) q.bowtieCol2Header = '';
  if (!q.bowtieCol3Header) q.bowtieCol3Header = '';

  const wrapper = document.createElement('div');
  wrapper.style.display = 'flex';
  wrapper.style.flexDirection = 'column';
  wrapper.style.gap = '20px';

  wrapper.innerHTML = `
    <div style="background:#1e293b; padding:12px; border-radius:var(--radius-sm); border:1px solid #334155;">
      <h5 style="margin-top:0; margin-bottom:12px; color:white; font-size:13px; font-weight:600;">Bowtie Diagram Targets Placeholders</h5>
      <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px;">
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:10px; color:#94a3b8; margin-bottom:4px;">Left Targets (Actions)</label>
          <input type="text" id="bowtie-left-holder" class="form-control" style="font-size:11px; padding:4px;" value="${escapeHTML(q.bowtieLeftPlaceholder)}" placeholder="Action to Take">
        </div>
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:10px; color:#94a3b8; margin-bottom:4px;">Center Target (Condition)</label>
          <input type="text" id="bowtie-center-holder" class="form-control" style="font-size:11px; padding:4px;" value="${escapeHTML(q.bowtieCenterPlaceholder)}" placeholder="Condition Most Likely Experiencing">
        </div>
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:10px; color:#94a3b8; margin-bottom:4px;">Right Targets (Parameters)</label>
          <input type="text" id="bowtie-right-holder" class="form-control" style="font-size:11px; padding:4px;" value="${escapeHTML(q.bowtieRightPlaceholder)}" placeholder="Parameter to Monitor">
        </div>
      </div>
    </div>

    <div style="background:#1e293b; padding:12px; border-radius:var(--radius-sm); border:1px solid #334155;">
      <h5 style="margin-top:0; margin-bottom:12px; color:white; font-size:13px; font-weight:600;">Bowtie Table Configuration</h5>
      <p style="font-size:11px; color:#94a3b8; margin-top:-6px; margin-bottom:12px;">Mark the correct choices that should be dragged into the targets (exactly 2 in Col 1, 1 in Col 2, and 2 in Col 3).</p>
      
      <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:16px;">
        <!-- Column 1 -->
        <div style="display:flex; flex-direction:column; gap:8px;">
          <input type="text" id="bowtie-col1-header" class="form-control" style="font-weight:bold; text-align:center; font-size:12px;" value="${escapeHTML(q.bowtieCol1Header)}" placeholder="Actions to Take">
          <div id="bowtie-col1-list" style="display:flex; flex-direction:column; gap:6px;"></div>
          <button id="add-bowtie-col1-btn" class="btn btn-secondary btn-xs" style="margin-top:4px;">+ Add Choice</button>
        </div>
        
        <!-- Column 2 -->
        <div style="display:flex; flex-direction:column; gap:8px;">
          <input type="text" id="bowtie-col2-header" class="form-control" style="font-weight:bold; text-align:center; font-size:12px;" value="${escapeHTML(q.bowtieCol2Header)}" placeholder="Potential Conditions">
          <div id="bowtie-col2-list" style="display:flex; flex-direction:column; gap:6px;"></div>
          <button id="add-bowtie-col2-btn" class="btn btn-secondary btn-xs" style="margin-top:4px;">+ Add Choice</button>
        </div>
        
        <!-- Column 3 -->
        <div style="display:flex; flex-direction:column; gap:8px;">
          <input type="text" id="bowtie-col3-header" class="form-control" style="font-weight:bold; text-align:center; font-size:12px;" value="${escapeHTML(q.bowtieCol3Header)}" placeholder="Parameters to Monitor">
          <div id="bowtie-col3-list" style="display:flex; flex-direction:column; gap:6px;"></div>
          <button id="add-bowtie-col3-btn" class="btn btn-secondary btn-xs" style="margin-top:4px;">+ Add Choice</button>
        </div>
      </div>
    </div>
  `;
  
  box.appendChild(wrapper);

  // Bind placeholder inputs
  document.getElementById('bowtie-left-holder').addEventListener('input', (e) => q.bowtieLeftPlaceholder = e.target.value);
  document.getElementById('bowtie-center-holder').addEventListener('input', (e) => q.bowtieCenterPlaceholder = e.target.value);
  document.getElementById('bowtie-right-holder').addEventListener('input', (e) => q.bowtieRightPlaceholder = e.target.value);
  
  document.getElementById('bowtie-col1-header').addEventListener('input', (e) => q.bowtieCol1Header = e.target.value);
  document.getElementById('bowtie-col2-header').addEventListener('input', (e) => q.bowtieCol2Header = e.target.value);
  document.getElementById('bowtie-col3-header').addEventListener('input', (e) => q.bowtieCol3Header = e.target.value);

  // Helper to render rows inside each list
  const renderColList = (listId, array) => {
    const listEl = document.getElementById(listId);
    listEl.innerHTML = '';
    array.forEach((opt, idx) => {
      const row = document.createElement('div');
      row.className = 'option-config-row';
      row.style.gap = '4px';
      row.style.marginBottom = '2px';
      row.innerHTML = `
        <input type="checkbox" class="bowtie-correct-toggle" ${opt.correct ? 'checked' : ''} style="margin-right:2px;">
        <input type="text" class="form-control bowtie-input" style="font-size:11px; padding:2px 4px; height:24px;" value="${escapeHTML(opt.text)}" placeholder="Option ${idx + 1}">
        <button class="btn-option-delete" style="font-size:14px; padding:0 4px;">&times;</button>
      `;
      
      row.querySelector('.bowtie-input').addEventListener('input', (e) => {
        opt.text = e.target.value;
      });
      row.querySelector('.bowtie-correct-toggle').addEventListener('change', (e) => {
        opt.correct = e.target.checked;
      });
      row.querySelector('.btn-option-delete').addEventListener('click', () => {
        array.splice(idx, 1);
        renderColList(listId, array);
      });
      listEl.appendChild(row);
    });
  };

  const renderAll = () => {
    renderColList('bowtie-col1-list', q.bowtieActions);
    renderColList('bowtie-col2-list', q.bowtieConditions);
    renderColList('bowtie-col3-list', q.bowtieParams);
  };

  renderAll();

  document.getElementById('add-bowtie-col1-btn').addEventListener('click', () => {
    q.bowtieActions.push({ text: 'New Choice', correct: false });
    renderColList('bowtie-col1-list', q.bowtieActions);
  });
  document.getElementById('add-bowtie-col2-btn').addEventListener('click', () => {
    q.bowtieConditions.push({ text: 'New Choice', correct: false });
    renderColList('bowtie-col2-list', q.bowtieConditions);
  });
  document.getElementById('add-bowtie-col3-btn').addEventListener('click', () => {
    q.bowtieParams.push({ text: 'New Choice', correct: false });
    renderColList('bowtie-col3-list', q.bowtieParams);
  });
}

// 8. Fill-in-blank calculation Configurator
function renderFillBlankConfigurator(q, box) {
  const wrapper = document.createElement('div');
  wrapper.className = 'form-group';
  wrapper.innerHTML = `
    <div style="display: flex; gap: 12px; align-items: flex-end;">
      <div style="flex: 1;">
        <label for="fill-blank-correct-input">Correct Answer (Numeric value or word)</label>
        <input type="text" id="fill-blank-correct-input" class="form-control" value="${escapeHTML(q.correctAnswer || '')}" placeholder="Type answer...">
      </div>
      <div style="flex: 1;">
        <label for="fill-blank-unit-input">Unit</label>
        <input type="text" id="fill-blank-unit-input" class="form-control" value="${escapeHTML(q.unit || '')}" placeholder="Type Unit">
      </div>
    </div>
  `;
  box.appendChild(wrapper);
}

// 9. Hotspot Configurator
function renderHotspotConfigurator(q, box) {
  const wrapper = document.createElement('div');
  wrapper.innerHTML = `
    <div class="form-group" style="margin-bottom:12px;">
      <label for="hotspot-url-input">Hotspot Image URL</label>
      <input type="text" id="hotspot-url-input" class="form-control" value="${escapeHTML(q.imageUrl || '')}">
    </div>
    <div class="cloze-warning">Draw a box on the image below to set the correct coordinates.</div>
    <div style="text-align:center;">
      <div id="hotspot-editor-img-container" class="hotspot-image-container">
        <img id="hotspot-editor-img" class="hotspot-image" src="${escapeHTML(q.imageUrl || '')}" alt="Hotspot Image">
        <div id="hotspot-editor-box" class="hotspot-target-region" style="display:none;"></div>
      </div>
    </div>
  `;
  box.appendChild(wrapper);
  
  const imgInput = document.getElementById('hotspot-url-input');
  const imgEl = document.getElementById('hotspot-editor-img');
  const targetBox = document.getElementById('hotspot-editor-box');
  const imgContainer = document.getElementById('hotspot-editor-img-container');
  
  imgInput.addEventListener('change', (e) => {
    imgEl.src = e.target.value;
    q.imageUrl = e.target.value;
  });
  
  // Set current visual box
  const showSavedBox = () => {
    const r = q.rect;
    if (r) {
      targetBox.style.display = 'block';
      targetBox.style.left = Math.min(r.x1, r.x2) + '%';
      targetBox.style.top = Math.min(r.y1, r.y2) + '%';
      targetBox.style.width = Math.abs(r.x2 - r.x1) + '%';
      targetBox.style.height = Math.abs(r.y2 - r.y1) + '%';
    }
  };
  
  imgEl.onload = showSavedBox;
  showSavedBox();
  
  // Drawing logic
  let startX = 0, startY = 0, drawing = false;
  
  imgContainer.addEventListener('mousedown', (e) => {
    if (e.target !== imgEl && e.target !== targetBox) return;
    drawing = true;
    const rect = imgContainer.getBoundingClientRect();
    startX = ((e.clientX - rect.left) / rect.width) * 100;
    startY = ((e.clientY - rect.top) / rect.height) * 100;
    q.rect = { x1: startX, y1: startY, x2: startX, y2: startY };
    showSavedBox();
  });
  
  imgContainer.addEventListener('mousemove', (e) => {
    if (!drawing) return;
    const rect = imgContainer.getBoundingClientRect();
    const currentX = ((e.clientX - rect.left) / rect.width) * 100;
    const currentY = ((e.clientY - rect.top) / rect.height) * 100;
    
    q.rect.x2 = Math.min(100, Math.max(0, currentX));
    q.rect.y2 = Math.min(100, Math.max(0, currentY));
    showSavedBox();
  });
  
  window.addEventListener('mouseup', () => {
    drawing = false;
  });
}

// 10. Ordered Response Configurator
function renderOrderedResponseConfigurator(q, box) {
  const steps = q.orderedOptions || [];
  const wrapper = document.createElement('div');
  wrapper.innerHTML = `
    <div class="options-config-title">
      <span>Steps in CORRECT Order</span>
      <button id="add-order-opt-btn" class="btn btn-text btn-xs">+ Add Step</button>
    </div>
    <div id="ordered-items-config-list"></div>
  `;
  box.appendChild(wrapper);
  
  const list = document.getElementById('ordered-items-config-list');
  const renderSteps = () => {
    list.innerHTML = '';
    steps.forEach((step, idx) => {
      const div = document.createElement('div');
      div.className = 'option-config-row';
      div.innerHTML = `
        <span style="font-weight:bold; color:var(--nclex-sky); width:20px;">${idx + 1}.</span>
        <input type="text" class="form-control step-input-field" value="${escapeHTML(step)}">
        <button class="btn-option-delete">&times;</button>
      `;
      div.querySelector('.step-input-field').addEventListener('input', (e) => {
        steps[idx] = e.target.value;
      });
      div.querySelector('.btn-option-delete').addEventListener('click', () => {
        steps.splice(idx, 1);
        renderSteps();
      });
      list.appendChild(div);
    });
  };
  
  renderSteps();
  
  document.getElementById('add-order-opt-btn').addEventListener('click', () => {
    steps.push('Next instruction step');
    q.orderedOptions = steps;
    renderSteps();
  });
}

function renderHighlightConfigurator(q, box) {
  if (!q.highlightTabs) {
    q.highlightTabs = [
      { id: 'ht_' + Date.now(), title: "Nurses' Notes", content: q.highlightText || '' }
    ];
  }
  
  if (!highlightActiveTabId || !q.highlightTabs.find(t => t.id === highlightActiveTabId)) {
    highlightActiveTabId = q.highlightTabs[0].id;
  }
  
  const activeTab = q.highlightTabs.find(t => t.id === highlightActiveTabId);
  
  const wrapper = document.createElement('div');
  wrapper.className = 'highlight-tabs-editor-container';
  wrapper.innerHTML = `
    <div class="cloze-warning" style="margin-bottom: 12px;">
      Wrap phrases in curly braces like: <strong>{unstable vitals|correct}</strong> for correct findings, or <strong>{temperature of 98.6 F}</strong> for incorrect findings that are click-selectable.
    </div>
    
    <div class="tabs-editor-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
      <h5 style="margin:0;">Highlight Chart Tabs</h5>
      <button id="add-highlight-tab-btn" class="btn btn-text btn-xs">+ Add Tab</button>
    </div>
    
    <div id="highlight-editor-tabs-list" class="tabs-list-horizontal" style="display:flex; gap:4px; margin-bottom:8px; border-bottom:1px solid var(--border-color); padding-bottom:4px; overflow-x:auto;">
      ${q.highlightTabs.map(t => `
        <div class="tab-editor-item ${t.id === highlightActiveTabId ? 'active' : ''}" data-id="${t.id}" style="padding: 6px 12px; border: 1px solid var(--border-color); border-bottom: none; border-radius: 4px 4px 0 0; cursor: pointer; font-size:13px; font-weight:500;">
          <span>${escapeHTML(t.title)}</span>
        </div>
      `).join('')}
    </div>
    
    <div id="highlight-tab-content-editor" class="tab-content-editor-box" style="border: 1px solid var(--border-color); padding: 12px; border-radius: 4px; background: var(--background-secondary);">
      <div class="form-group no-margin">
        <label style="display:block; margin-bottom: 6px; font-weight: 500; font-size:13px;">Content for "${escapeHTML(activeTab.title)}"</label>
        <input type="text" id="highlight-tab-title-input" class="tab-title-rename" placeholder="Tab Title" value="${escapeHTML(activeTab.title)}" style="width:100%; padding:6px; border:1px solid var(--border-color); border-radius:4px; margin-bottom:10px; font-size:13px;">
        
        <div class="rich-editor-container" style="border:1px solid var(--border-color); border-radius:4px; overflow:hidden; background:#ffffff; margin-bottom:10px;">
          <div class="rich-editor-toolbar" style="display:flex; flex-wrap:wrap; gap:4px; padding:6px; border-bottom:1px solid var(--border-color); background:var(--background-primary);">
            <button type="button" class="toolbar-btn" data-cmd="bold" title="Bold"><b>B</b></button>
            <button type="button" class="toolbar-btn" data-cmd="superscript" title="Superscript">x<sup>2</sup></button>
            <button type="button" class="toolbar-btn" data-cmd="subscript" title="Subscript">x<sub>2</sub></button>
            <button type="button" class="toolbar-btn btn-symbol" data-symbol="&deg;" title="Degree Symbol">&deg;</button>
            <button type="button" class="toolbar-btn btn-symbol" data-symbol="&ge;" title="Greater Than or Equal to">&ge;</button>
            <button type="button" class="toolbar-btn btn-symbol" data-symbol="&le;" title="Less Than or Equal to">&le;</button>
            <button type="button" class="toolbar-btn" data-cmd="insertUnorderedList" title="Bullet List">• List</button>
            <button type="button" class="toolbar-btn" data-cmd="insertOrderedList" title="Numbered List">1. List</button>
            <button type="button" class="toolbar-btn table-insert-btn" title="Insert Table">
              <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" style="vertical-align: middle;"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>
              Table
            </button>
          </div>
          <div contenteditable="true" class="rich-text-editor" id="highlight-tab-text-input" placeholder="Enter chart text or tables here..." style="min-height: 150px; padding: 12px; outline: none; font-size:14px; line-height:1.5;">${activeTab.content || ''}</div>
        </div>
        
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <button id="delete-highlight-tab-btn" class="btn btn-danger btn-xs">Delete This Tab</button>
          <div>
            <label for="highlight-max-correct-input" style="font-size:12px; margin-right: 6px;">Max Correct (optional):</label>
            <input type="number" id="highlight-max-correct-input" class="form-control" style="width: 70px; display:inline-block; padding:4px;" min="1" value="${q.maxCorrectSelections || ''}">
          </div>
        </div>
      </div>
    </div>
  `;
  box.appendChild(wrapper);
  
  // Attach event listeners for highlight tabs editor
  const titleInput = document.getElementById('highlight-tab-title-input');
  titleInput.addEventListener('input', (e) => {
    activeTab.title = e.target.value;
    const tabHeader = document.querySelector(`#highlight-editor-tabs-list .tab-editor-item[data-id="${highlightActiveTabId}"] span`);
    if (tabHeader) tabHeader.textContent = e.target.value;
  });
  
  // Tab switching
  const tabItems = wrapper.querySelectorAll('#highlight-editor-tabs-list .tab-editor-item');
  tabItems.forEach(item => {
    item.addEventListener('click', () => {
      activeTab.content = document.getElementById('highlight-tab-text-input').innerHTML;
      highlightActiveTabId = item.getAttribute('data-id');
      renderDynamicQuestionConfigurator(q);
    });
  });
  
  // Add tab
  document.getElementById('add-highlight-tab-btn').addEventListener('click', () => {
    activeTab.content = document.getElementById('highlight-tab-text-input').innerHTML;
    const newId = 'ht_' + Date.now();
    q.highlightTabs.push({
      id: newId,
      title: 'New Tab',
      content: ''
    });
    highlightActiveTabId = newId;
    renderDynamicQuestionConfigurator(q);
  });
  
  // Delete tab
  document.getElementById('delete-highlight-tab-btn').addEventListener('click', () => {
    if (q.highlightTabs.length <= 1) {
      alert("Must keep at least one tab.");
      return;
    }
    if (confirm("Delete this tab?")) {
      const idx = q.highlightTabs.findIndex(t => t.id === highlightActiveTabId);
      q.highlightTabs.splice(idx, 1);
      highlightActiveTabId = q.highlightTabs[0].id;
      renderDynamicQuestionConfigurator(q);
    }
  });
}

// 14. Grouped Multiple Response Configurator
function renderGroupedMrConfigurator(q, box) {
  const groups = q.groupedRows || [];
  const wrapper = document.createElement('div');
  wrapper.innerHTML = `
    <div class="options-config-title">
      <span>Checkbox Groups</span>
      <button id="add-grouped-category-btn" class="btn btn-text btn-xs">+ Add Group</button>
    </div>
    <div id="grouped-categories-editor-container"></div>
  `;
  box.appendChild(wrapper);
  
  const container = document.getElementById('grouped-categories-editor-container');
  const renderGroups = () => {
    container.innerHTML = '';
    groups.forEach((g, gIdx) => {
      const card = document.createElement('div');
      card.className = 'cloze-dropdown-card';
      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
          <input type="text" class="form-control group-title-input" style="font-weight:bold; width:80%;" value="${escapeHTML(g.title)}" placeholder="Group Name (e.g. Pharmacological)">
          <button class="btn btn-danger btn-xs delete-group-btn">Delete Group</button>
        </div>
        <div class="options-config-title">
          <span>Options</span>
          <button class="btn btn-text btn-xs add-group-opt-btn">+ Add Option</button>
        </div>
        <div class="group-opts-list"></div>
      `;
      
      card.querySelector('.group-title-input').addEventListener('input', (e) => {
        g.title = e.target.value;
      });
      card.querySelector('.delete-group-btn').addEventListener('click', () => {
        groups.splice(gIdx, 1);
        renderGroups();
      });
      
      const optsList = card.querySelector('.group-opts-list');
      const renderGroupOptions = () => {
        optsList.innerHTML = '';
        g.options.forEach((opt, oIdx) => {
          const div = document.createElement('div');
          div.className = 'option-config-row';
          div.innerHTML = `
            <input type="checkbox" class="opt-correct-toggle" ${opt.correct ? 'checked' : ''}>
            <input type="text" class="form-control opt-text-input" style="font-size:12px; padding:6px;" value="${escapeHTML(opt.text)}">
            <button class="btn-option-delete">&times;</button>
          `;
          
          div.querySelector('.opt-text-input').addEventListener('input', (e) => {
            opt.text = e.target.value;
          });
          div.querySelector('.opt-correct-toggle').addEventListener('change', (e) => {
            opt.correct = e.target.checked;
          });
          div.querySelector('.btn-option-delete').addEventListener('click', () => {
            g.options.splice(oIdx, 1);
            renderGroupOptions();
          });
          optsList.appendChild(div);
        });
      };
      
      card.querySelector('.add-group-opt-btn').addEventListener('click', () => {
        g.options.push({ text: 'New Option', correct: false });
        renderGroupOptions();
      });
      
      renderGroupOptions();
      container.appendChild(card);
    });
  };
  
  renderGroups();
  
  document.getElementById('add-grouped-category-btn').addEventListener('click', () => {
    groups.push({
      title: 'New Group',
      options: [{ text: 'Correct action', correct: true }, { text: 'Incorrect action', correct: false }]
    });
    q.groupedRows = groups;
    renderGroups();
  });
}

let selectedTableCellElement = null;

function setupTableInteractionMenu() {
  let menu = document.getElementById('table-interaction-menu');
  if (!menu) {
    menu = document.createElement('div');
    menu.id = 'table-interaction-menu';
    menu.style.position = 'absolute';
    menu.style.display = 'none';
    menu.style.zIndex = '10000';
    menu.style.background = '#1e293b';
    menu.style.border = '1px solid #475569';
    menu.style.borderRadius = 'var(--radius-md)';
    menu.style.padding = '6px';
    menu.style.boxShadow = 'var(--shadow-lg)';
    menu.style.gap = '4px';
    menu.style.flexDirection = 'column';
    menu.style.maxHeight = '180px';
    menu.style.overflowY = 'auto';
    menu.style.width = '160px';
    menu.innerHTML = `
      <button id="tbl-menu-add-row-below" class="btn btn-secondary btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">+ Add Row Below</button>
      <button id="tbl-menu-add-row-above" class="btn btn-secondary btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">+ Add Row Above</button>
      <button id="tbl-menu-delete-row" class="btn btn-danger btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">- Delete Row</button>
      <div style="border-top:1px solid #334155; margin:4px 0;"></div>
      <button id="tbl-menu-add-col-right" class="btn btn-secondary btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">+ Add Column Right</button>
      <button id="tbl-menu-add-col-left" class="btn btn-secondary btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">+ Add Column Left</button>
      <button id="tbl-menu-delete-col" class="btn btn-danger btn-xs" style="text-align:left; justify-content:flex-start; width:100%;">- Delete Column</button>
    `;
    document.body.appendChild(menu);

    // Context Actions implementation
    menu.querySelector('#tbl-menu-add-row-below').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const row = selectedTableCellElement.closest('tr');
      const parent = row.parentNode;
      const colsCount = row.cells.length;
      
      const newRow = document.createElement('tr');
      for (let j = 0; j < colsCount; j++) {
        const newCell = document.createElement('td');
        newCell.setAttribute('placeholder', 'Cell');
        newCell.style.border = '1px solid #ccd8e0';
        newCell.style.padding = '8px';
        newCell.style.minWidth = '80px';
        newCell.style.background = 'white';
        newCell.style.color = '#1e293b';
        newRow.appendChild(newCell);
      }
      if (row.nextSibling) {
        parent.insertBefore(newRow, row.nextSibling);
      } else {
        parent.appendChild(newRow);
      }
      menu.style.display = 'none';
    });

    menu.querySelector('#tbl-menu-add-row-above').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const row = selectedTableCellElement.closest('tr');
      const parent = row.parentNode;
      const colsCount = row.cells.length;
      
      const newRow = document.createElement('tr');
      const isHeader = parent.tagName.toLowerCase() === 'thead';
      for (let j = 0; j < colsCount; j++) {
        const newCell = document.createElement(isHeader ? 'th' : 'td');
        if (isHeader) {
          newCell.setAttribute('placeholder', `Header ${j+1}`);
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.background = '#025287';
          newCell.style.color = 'white';
          newCell.style.fontWeight = '600';
          newCell.style.textAlign = 'left';
        } else {
          newCell.setAttribute('placeholder', 'Cell');
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.minWidth = '80px';
          newCell.style.background = 'white';
          newCell.style.color = '#1e293b';
        }
        newRow.appendChild(newCell);
      }
      parent.insertBefore(newRow, row);
      menu.style.display = 'none';
    });

    menu.querySelector('#tbl-menu-delete-row').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const row = selectedTableCellElement.closest('tr');
      const table = selectedTableCellElement.closest('table');
      if (table.querySelectorAll('tr').length > 1) {
        row.remove();
      }
      menu.style.display = 'none';
    });

    menu.querySelector('#tbl-menu-add-col-right').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const cellIndex = selectedTableCellElement.cellIndex;
      const table = selectedTableCellElement.closest('table');
      const rows = table.querySelectorAll('tr');
      
      rows.forEach(r => {
        const isHeader = r.closest('thead') !== null;
        const targetCell = r.cells[cellIndex];
        const newCell = document.createElement(isHeader ? 'th' : 'td');
        
        if (isHeader) {
          newCell.setAttribute('placeholder', 'Header');
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.background = '#025287';
          newCell.style.color = 'white';
          newCell.style.fontWeight = '600';
          newCell.style.textAlign = 'left';
        } else {
          newCell.setAttribute('placeholder', 'Cell');
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.minWidth = '80px';
          newCell.style.background = 'white';
          newCell.style.color = '#1e293b';
        }
        if (targetCell && targetCell.nextSibling) {
          r.insertBefore(newCell, targetCell.nextSibling);
        } else {
          r.appendChild(newCell);
        }
      });
      menu.style.display = 'none';
    });

    menu.querySelector('#tbl-menu-add-col-left').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const cellIndex = selectedTableCellElement.cellIndex;
      const table = selectedTableCellElement.closest('table');
      const rows = table.querySelectorAll('tr');
      
      rows.forEach(r => {
        const isHeader = r.closest('thead') !== null;
        const targetCell = r.cells[cellIndex];
        const newCell = document.createElement(isHeader ? 'th' : 'td');
        
        if (isHeader) {
          newCell.setAttribute('placeholder', 'Header');
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.background = '#025287';
          newCell.style.color = 'white';
          newCell.style.fontWeight = '600';
          newCell.style.textAlign = 'left';
        } else {
          newCell.setAttribute('placeholder', 'Cell');
          newCell.style.border = '1px solid #ccd8e0';
          newCell.style.padding = '8px';
          newCell.style.minWidth = '80px';
          newCell.style.background = 'white';
          newCell.style.color = '#1e293b';
        }
        r.insertBefore(newCell, targetCell);
      });
      menu.style.display = 'none';
    });

    menu.querySelector('#tbl-menu-delete-col').addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!selectedTableCellElement) return;
      const cellIndex = selectedTableCellElement.cellIndex;
      const table = selectedTableCellElement.closest('table');
      const rows = table.querySelectorAll('tr');
      
      if (selectedTableCellElement.closest('tr').cells.length > 1) {
        rows.forEach(r => {
          if (r.cells[cellIndex]) {
            r.cells[cellIndex].remove();
          }
        });
      }
      menu.style.display = 'none';
    });
  }

  // Bind mousedown listener to table elements inside editor to position the menu
  document.addEventListener('mousedown', (e) => {
    // If click/mousedown is inside the menu itself, do nothing
    if (e.target.closest('#table-interaction-menu')) {
      return;
    }
    
    // Check if mousedown was inside a contenteditable rich-text cell
    const cell = e.target.closest('[contenteditable="true"] td, [contenteditable="true"] th');
    if (cell) {
      const rect = cell.getBoundingClientRect();
      const clickedX = e.clientX;
      const clickedY = e.clientY;
      const insideChevronX = (clickedX >= rect.right - 24 && clickedX <= rect.right);
      const insideChevronY = (clickedY >= rect.top && clickedY <= rect.top + 24);
      
      if (insideChevronX && insideChevronY) {
        if (menu.style.display === 'flex' && selectedTableCellElement === cell) {
          menu.style.display = 'none';
          selectedTableCellElement = null;
        } else {
          selectedTableCellElement = cell;
          menu.style.display = 'flex';
          
          const menuHeight = 180;
          const screenHeight = window.innerHeight;
          const offsetBelow = rect.bottom + menuHeight;
          
          if (offsetBelow > screenHeight && rect.top > menuHeight) {
            menu.style.top = `${rect.top + window.scrollY - menuHeight}px`;
          } else {
            menu.style.top = `${rect.bottom + window.scrollY}px`;
          }
          menu.style.left = `${rect.left + window.scrollX}px`;
        }
      } else {
        menu.style.display = 'none';
      }
    } else {
      menu.style.display = 'none';
    }
  });
}
