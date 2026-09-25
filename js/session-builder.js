/* Student portal session builder: mode, topic and question-count selection. */

/* ================= NEXTGEN NCLEX SESSION BUILDER ================= */
let sessionBuilderTopics = [];
let sessionBuilderMode = 'review'; // 'review' | 'test'

function initSessionBuilder() {
  // Mode selection cards
  const reviewCard = document.getElementById('mode-card-review');
  const testCard = document.getElementById('mode-card-test');
  const reviewRadio = document.querySelector('input[name="session-mode"][value="review"]');
  const testRadio = document.querySelector('input[name="session-mode"][value="test"]');
  const launchBtnLabel = document.getElementById('launch-btn-label');

  function setSessionMode(mode) {
    sessionBuilderMode = mode;
    if (mode === 'review') {
      if (reviewCard) reviewCard.classList.add('selected');
      if (testCard) testCard.classList.remove('selected');
      if (reviewRadio) reviewRadio.checked = true;
      if (launchBtnLabel) launchBtnLabel.textContent = 'Start Practice Session (Review Mode)';
    } else {
      if (testCard) testCard.classList.add('selected');
      if (reviewCard) reviewCard.classList.remove('selected');
      if (testRadio) testRadio.checked = true;
      if (launchBtnLabel) launchBtnLabel.textContent = 'Start NCLEX Exam Simulation (Test Mode)';
    }
    updateSessionCountsAndBounds();
  }

  if (reviewCard) reviewCard.addEventListener('click', () => setSessionMode('review'));
  if (testCard) testCard.addEventListener('click', () => setSessionMode('test'));
  if (reviewRadio) reviewRadio.addEventListener('change', () => setSessionMode('review'));
  if (testRadio) testRadio.addEventListener('change', () => setSessionMode('test'));

  // Preset buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const cases = parseInt(btn.dataset.cases || '0', 10);
      const standalone = parseInt(btn.dataset.standalone || '0', 10);

      // If no topics are selected currently, auto-select all topics so preset can apply
      if (!sessionBuilderTopics || sessionBuilderTopics.length === 0) {
        document.querySelectorAll('#generator-topics-list .session-topic-checkbox').forEach(cb => {
          cb.checked = true;
          cb.closest('.topic-chip-card')?.classList.add('active');
        });
        const checkboxes = document.querySelectorAll('.session-topic-checkbox:checked');
        sessionBuilderTopics = Array.from(checkboxes).map(cb => cb.value);
      }

      updateSessionCountsAndBounds();

      const casesSlider = document.getElementById('generator-cases-slider');
      const casesInput = document.getElementById('generator-cases-input');
      const stdSlider = document.getElementById('generator-standalone-slider');
      const stdInput = document.getElementById('generator-standalone-input');

      if (casesSlider) casesSlider.value = cases;
      if (casesInput) casesInput.value = cases;
      if (stdSlider) stdSlider.value = standalone;
      if (stdInput) stdInput.value = standalone;

      updateSessionCountsAndBounds();
    });
  });

  // Quantity Sliders & Number inputs sync
  const casesSlider = document.getElementById('generator-cases-slider');
  const casesInput = document.getElementById('generator-cases-input');
  const stdSlider = document.getElementById('generator-standalone-slider');
  const stdInput = document.getElementById('generator-standalone-input');

  if (casesSlider && casesInput) {
    casesSlider.addEventListener('input', () => {
      casesInput.value = casesSlider.value;
      updateSessionCountsAndBounds();
    });
    casesInput.addEventListener('input', () => {
      casesSlider.value = casesInput.value;
      updateSessionCountsAndBounds();
    });
  }

  if (stdSlider && stdInput) {
    stdSlider.addEventListener('input', () => {
      stdInput.value = stdSlider.value;
      updateSessionCountsAndBounds();
    });
    stdInput.addEventListener('input', () => {
      stdSlider.value = stdInput.value;
      updateSessionCountsAndBounds();
    });
  }

  // Launch button
  const launchBtn = document.getElementById('generate-play-btn');
  if (launchBtn) {
    launchBtn.addEventListener('click', generateAndStartSession);
  }

  // Authoring button in student header
  const authBtn = document.getElementById('student-authoring-btn');
  if (authBtn) {
    authBtn.addEventListener('click', () => switchView('dashboard'));
  }

  // Student Course & Unit Filters
  const studentCourseFilterEl = document.getElementById('student-course-filter');
  if (studentCourseFilterEl) {
    studentCourseFilterEl.addEventListener('change', (e) => {
      studentCourseFilter = e.target.value;
      updateStudentUnitFilterOptions();
      filterSessionTopicCards();
    });
  }

  const studentUnitFilterEl = document.getElementById('student-unit-filter');
  if (studentUnitFilterEl) {
    studentUnitFilterEl.addEventListener('change', (e) => {
      studentUnitFilter = e.target.value;
      filterSessionTopicCards();
    });
  }

  // Topic search filter
  const topicSearchInput = document.getElementById('topic-search-input');
  if (topicSearchInput) {
    topicSearchInput.addEventListener('input', () => {
      filterSessionTopicCards();
    });
  }

  // Select All Topics (selects visible topic cards)
  const selectAllTopicsBtn = document.getElementById('topics-select-all-btn');
  if (selectAllTopicsBtn) {
    selectAllTopicsBtn.addEventListener('click', () => {
      document.querySelectorAll('#generator-topics-list .topic-chip-card').forEach(card => {
        if (card.style.display !== 'none') {
          const cb = card.querySelector('.session-topic-checkbox');
          if (cb) {
            cb.checked = true;
            card.classList.add('active');
          }
        }
      });
      updateSessionTopicsFromCheckboxes();
    });
  }

  // Clear All Topics
  const clearAllTopicsBtn = document.getElementById('topics-clear-all-btn');
  if (clearAllTopicsBtn) {
    clearAllTopicsBtn.addEventListener('click', () => {
      document.querySelectorAll('#generator-topics-list .session-topic-checkbox').forEach(cb => {
        cb.checked = false;
        cb.closest('.topic-chip-card')?.classList.remove('active');
      });
      updateSessionTopicsFromCheckboxes();
    });
  }

  updateStudentUnitFilterOptions();
  renderSessionTopicsList();
  renderManualSelectionLists();
}

function updateStudentUnitFilterOptions() {
  const unitFilter = document.getElementById('student-unit-filter');
  if (!unitFilter) return;

  const currentVal = studentUnitFilter;
  let html = '<option value="ALL">All Units</option>';

  if (studentCourseFilter === 'ALL') {
    html += `
      <optgroup label="NURS 1017 (Pathophysiology 1)">
        ${CURRICULUM_COURSES["NURS 1017"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
      <optgroup label="NURS 1021 (Pathophysiology 2)">
        ${CURRICULUM_COURSES["NURS 1021"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
      <optgroup label="Other Topics">
        <option value="Others">Others (Unassigned)</option>
      </optgroup>
    `;
  } else if (studentCourseFilter === 'NURS 1017') {
    html += `
      <optgroup label="NURS 1017 (Pathophysiology 1)">
        ${CURRICULUM_COURSES["NURS 1017"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
    `;
  } else if (studentCourseFilter === 'NURS 1021') {
    html += `
      <optgroup label="NURS 1021 (Pathophysiology 2)">
        ${CURRICULUM_COURSES["NURS 1021"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
    `;
  } else if (studentCourseFilter === 'Others') {
    html += '<option value="Others">Others (Unassigned)</option>';
  }

  unitFilter.innerHTML = html;
  const exists = Array.from(unitFilter.options).some(opt => opt.value === currentVal);
  if (exists) {
    unitFilter.value = currentVal;
  } else {
    studentUnitFilter = 'ALL';
    unitFilter.value = 'ALL';
  }
}

function filterSessionTopicCards() {
  const q = (document.getElementById('topic-search-input')?.value || '').toLowerCase().trim();
  const cards = document.querySelectorAll('#generator-topics-list .topic-chip-card');
  let visibleCount = 0;

  cards.forEach(card => {
    const cardCourse = card.dataset.course || '';
    const cardUnit = card.dataset.unit || '';
    const cardText = card.textContent.toLowerCase();

    const matchesCourse = (studentCourseFilter === 'ALL' || cardCourse === studentCourseFilter);
    const matchesUnit = (studentUnitFilter === 'ALL' || cardUnit === studentUnitFilter);
    const matchesSearch = (!q || cardText.includes(q));

    if (matchesCourse && matchesUnit && matchesSearch) {
      card.style.display = 'flex';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });

  // If a specific unit was selected in dropdown (not 'ALL'), auto-select its checkbox if none is selected
  if (studentUnitFilter !== 'ALL') {
    cards.forEach(card => {
      if (card.dataset.unit === studentUnitFilter) {
        const cb = card.querySelector('.session-topic-checkbox');
        if (cb && !cb.checked) {
          cb.checked = true;
          card.classList.add('active');
          updateSessionTopicsFromCheckboxes();
        }
      }
    });
  }

  let emptyMsg = document.getElementById('generator-topics-empty-msg');
  if (visibleCount === 0) {
    if (!emptyMsg) {
      emptyMsg = document.createElement('div');
      emptyMsg.id = 'generator-topics-empty-msg';
      emptyMsg.style.cssText = 'color:#64748b; font-style:italic; padding: 16px; text-align: center;';
      emptyMsg.textContent = 'No matching units or topics found for the selected course and unit.';
      document.getElementById('generator-topics-list')?.appendChild(emptyMsg);
    } else {
      emptyMsg.style.display = 'block';
    }
  } else if (emptyMsg) {
    emptyMsg.style.display = 'none';
  }
}

function renderSessionTopicsList() {
  const container = document.getElementById('generator-topics-list');
  if (!container) return;

  const topicDescriptions = {
    'Unit 1 (Introduction to Pathophysiology)': 'Cell injury, adaptation, homeostasis, disease etiology',
    'Unit 2 (Cellular Basis of Disease)': 'Hypertrophy, hyperplasia, metaplasia, dysplasia, necrosis',
    'Unit 3 (Genetic and Developmental Disorders)': 'Chromosomal, Mendelian, Down, Turner, Klinefelter syndromes',
    'Unit 4 (Neoplasia)': 'Carcinogenesis, oncogenes, tumor suppressors, benign vs malignant',
    'Unit 5 (Integumentary Disorders and Burns)': 'Skin lesions, infections, burns (Rule of 9s, Parkland, depths)',
    'Unit 6 (Musculoskeletal Disorders)': 'Fractures, osteoporosis, arthritis, compartment syndrome',
    'Unit 7 (Neurological Disorders)': 'Stroke, intracranial pressure, seizures, neurological deficit',
    'Unit 8 (Pain)': 'Nociceptive, neuropathic, pain management, assessment',
    'Unit 9 (Disorders of the Eyes and Ears)': 'Glaucoma, cataracts, macular degeneration, hearing loss',
    'Unit 10 (Stress and Disease)': 'GAS, cortisol, neuroendocrine response, stress adaptation',
    'Unit 11 (Endocrine Disorders)': 'DKA, HHS, thyroid storm, adrenal disorders, diabetes care',
    'Unit 1 (Blood Disorders)': 'Anemias, coagulopathies, sickle cell disease, transfusions',
    'Unit 2 (Cardiovascular Disorders)': 'Heart failure, MI, dysrhythmias, hypertension, shock',
    'Unit 3 (Respiratory Disorders)': 'COPD, asthma, pulmonary embolism, ARDS, pneumonia',
    'Unit 4 (Inflammation and Immune Disorders)': 'Sepsis, autoimmune, anaphylaxis, hypersensitivity',
    'Unit 5 (Leukemias and Lymphomas)': 'Acute/chronic leukemia, Hodgkin/non-Hodgkin lymphoma',
    'Unit 6 (Gastrointestinal Disorders)': 'Pancreatitis, cirrhosis, bowel obstruction, GI bleed, IBD',
    'Unit 7 (Urinary Disorders)': 'AKI, CKD, nephrotic syndrome, glomerulonephritis',
    'Unit 8 (Fluid, Electrolytes, and Acid-Base Imbalances)': 'Hyponatremia, hyperkalemia, acidosis, alkalosis',
    'Unit 9 (Reproductive Disorders)': 'Reproductive tract pathology, hormonal imbalances',
    'Cardiovascular Disorders': 'Heart failure, MI, dysrhythmias, hypertension',
    'Endocrine Disorders': 'DKA, HHS, thyroid storm, diabetes care',
    'Respiratory Disorders': 'COPD, asthma, pulmonary embolism, ARDS',
    'GI Disorders': 'Pancreatitis, cirrhosis, bowel obstruction, GI bleed',
    'Neurological Disorders': 'Stroke, increased ICP, seizures, neuro checks',
    'Immune disorders': 'Sepsis, anaphylaxis, infection control, immunity',
    'Others': 'General pathophysiology, fundamentals, multisystem'
  };

  const topicsMap = {};

  // 1. Pre-populate ALL curriculum units in strict course order so units with 0 cases (e.g. Unit 1 Blood Disorders) are visible
  CURRICULUM_COURSES["NURS 1017"].forEach(u => {
    topicsMap[u] = { cases: 0, standalone: 0, course: "NURS 1017" };
  });
  CURRICULUM_COURSES["NURS 1021"].forEach(u => {
    topicsMap[u] = { cases: 0, standalone: 0, course: "NURS 1021" };
  });
  topicsMap["Others"] = { cases: 0, standalone: 0, course: "Others" };
  
  // 2. Collect topics from cases
  studentCaseStudies().forEach(c => {
    const t = (c.unit || c.topic || c.disorder || 'Others').trim();
    if (!topicsMap[t]) {
      topicsMap[t] = { cases: 0, standalone: 0, course: c.course || 'Others' };
    }
    topicsMap[t].cases++;
    if (c.course && !topicsMap[t].course) topicsMap[t].course = c.course;
  });

  // 3. Collect topics from standalone
  studentStandaloneQuestions().forEach(s => {
    const t = (s.unit || s.topic || s.disorder || 'Others').trim();
    if (!topicsMap[t]) {
      topicsMap[t] = { cases: 0, standalone: 0, course: s.course || 'Others' };
    }
    topicsMap[t].standalone++;
    if (s.course && !topicsMap[t].course) topicsMap[t].course = s.course;
  });

  // 4. Sort topics: All NURS 1017 units first, followed by NURS 1021, followed by Others
  const sortedTopics = Object.keys(topicsMap).sort((a, b) => {
    const isAOther = (a.toLowerCase() === 'others' || a.toLowerCase().startsWith('other'));
    const isBOther = (b.toLowerCase() === 'others' || b.toLowerCase().startsWith('other'));
    if (isAOther && !isBOther) return 1;
    if (!isAOther && isBOther) return -1;

    const idxA1017 = CURRICULUM_COURSES["NURS 1017"].indexOf(a);
    const idxB1017 = CURRICULUM_COURSES["NURS 1017"].indexOf(b);
    const idxA1021 = CURRICULUM_COURSES["NURS 1021"].indexOf(a);
    const idxB1021 = CURRICULUM_COURSES["NURS 1021"].indexOf(b);

    // If both are NURS 1017, order by curriculum sequence (Unit 1 to 11)
    if (idxA1017 !== -1 && idxB1017 !== -1) return idxA1017 - idxB1017;
    // NURS 1017 always comes before NURS 1021 and Others
    if (idxA1017 !== -1) return -1;
    if (idxB1017 !== -1) return 1;

    // If both are NURS 1021, order by curriculum sequence (Unit 1 to 9)
    if (idxA1021 !== -1 && idxB1021 !== -1) return idxA1021 - idxB1021;
    // NURS 1021 always comes before Others
    if (idxA1021 !== -1) return -1;
    if (idxB1021 !== -1) return 1;

    return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
  });
  container.innerHTML = '';

  if (sortedTopics.length === 0) {
    container.innerHTML = '<div style="color:#64748b; font-style:italic; padding: 8px;">No topics found in library.</div>';
    return;
  }

  sortedTopics.forEach(topic => {
    const counts = topicsMap[topic];
    const desc = topicDescriptions[topic] || 'Clinical scenario practice';

    // Determine course
    let course = counts.course || '';
    if (!course) {
      if (CURRICULUM_COURSES["NURS 1017"].includes(topic)) {
        course = "NURS 1017";
      } else if (CURRICULUM_COURSES["NURS 1021"].includes(topic)) {
        course = "NURS 1021";
      } else {
        course = "Others";
      }
    }

    const card = document.createElement('label');
    card.className = 'topic-chip-card';
    card.dataset.course = course;
    card.dataset.unit = topic;
    card.innerHTML = `
      <div class="topic-chip-left">
        <input type="checkbox" class="session-topic-checkbox" value="${escapeHTML(topic)}" style="accent-color: #025287; cursor: pointer; width: 16px; height: 16px;">
        <div>
          <div class="topic-chip-name">
            ${escapeHTML(topic)}
            ${course && course !== 'Others' ? `<span class="topic-course-tag ${course === 'NURS 1021' ? 'course-1021' : 'course-1017'}">${escapeHTML(course)}</span>` : ''}
          </div>
          <div style="font-size: 11px; color: #64748b; font-weight: normal; margin-top: 1px;">${escapeHTML(desc)}</div>
        </div>
      </div>
      <span class="topic-chip-counts">${counts.cases} Cases &bull; ${counts.standalone} Qs</span>
    `;

    const cb = card.querySelector('.session-topic-checkbox');
    cb.addEventListener('change', () => {
      if (cb.checked) card.classList.add('active');
      else card.classList.remove('active');
      updateSessionTopicsFromCheckboxes();
    });

    container.appendChild(card);
  });

  filterSessionTopicCards();
  updateSessionTopicsFromCheckboxes();
}

function updateSessionTopicsFromCheckboxes() {
  const checkboxes = document.querySelectorAll('.session-topic-checkbox:checked');
  sessionBuilderTopics = Array.from(checkboxes).map(cb => cb.value);
  updateSessionCountsAndBounds();
}

function updateSessionCountsAndBounds() {
  // Available pool from selected topics
  const availableCases = studentCaseStudies().filter(c => sessionBuilderTopics.includes((c.topic || c.disorder || 'General').trim()));
  const availableStandalone = studentStandaloneQuestions().filter(s => sessionBuilderTopics.includes((s.topic || s.disorder || 'General').trim()));

  const maxCases = Math.min(3, availableCases.length);
  const maxStandalone = Math.min(67, availableStandalone.length);

  const casesAvailEl = document.getElementById('cases-avail-text');
  const stdAvailEl = document.getElementById('standalone-avail-text');
  if (casesAvailEl) casesAvailEl.textContent = `Avail: ${availableCases.length} (Max 3)`;
  if (stdAvailEl) stdAvailEl.textContent = `Avail: ${availableStandalone.length} (Max 67)`;

  const casesSlider = document.getElementById('generator-cases-slider');
  const casesInput = document.getElementById('generator-cases-input');
  const stdSlider = document.getElementById('generator-standalone-slider');
  const stdInput = document.getElementById('generator-standalone-input');

  if (casesSlider && casesInput) {
    casesSlider.max = maxCases;
    casesInput.max = maxCases;
    if (parseInt(casesInput.value || '0', 10) > maxCases) {
      casesInput.value = maxCases;
      casesSlider.value = maxCases;
    }
  }

  if (stdSlider && stdInput) {
    stdSlider.max = maxStandalone;
    stdInput.max = maxStandalone;
    if (parseInt(stdInput.value || '0', 10) > maxStandalone) {
      stdInput.value = maxStandalone;
      stdSlider.value = maxStandalone;
    }
  }

  let casesVal = parseInt(casesInput ? casesInput.value : '0', 10) || 0;
  let stdVal = parseInt(stdInput ? stdInput.value : '0', 10) || 0;

  // Enforce 85 questions cap: (cases * 6) + standalone <= 85
  const maxQuestionsCap = 85;
  const casesQuestions = casesVal * 6;
  if (casesQuestions + stdVal > maxQuestionsCap) {
    stdVal = maxQuestionsCap - casesQuestions;
    if (stdVal < 0) stdVal = 0;
    if (stdInput) stdInput.value = stdVal;
    if (stdSlider) stdSlider.value = stdVal;
  }

  const totalQuestions = casesQuestions + stdVal;

  const casesNote = document.getElementById('cases-questions-note');
  const stdNote = document.getElementById('standalone-questions-note');
  if (casesNote) casesNote.textContent = `${casesVal} Case Stud${casesVal === 1 ? 'y' : 'ies'} = ${casesQuestions} Questions`;
  if (stdNote) stdNote.textContent = `${stdVal} Stand-alone Question${stdVal === 1 ? '' : 's'}`;

  const totalValEl = document.getElementById('session-total-questions-val');
  const statusBadge = document.getElementById('session-total-status-badge');
  const launchBtn = document.getElementById('generate-play-btn');

  if (totalValEl) totalValEl.textContent = totalQuestions;

  const estMins = Math.round(totalQuestions * 1.3);
  const estTimeEl = document.getElementById('session-est-time-val');
  if (estTimeEl) estTimeEl.textContent = estMins;

  const pillTotalEl = document.getElementById('pill-total-text');
  if (pillTotalEl) pillTotalEl.textContent = `${totalQuestions} Questions`;

  const pillTimeEl = document.getElementById('pill-time-text');
  if (pillTimeEl) pillTimeEl.textContent = `(Est. ${estMins} Mins)`;

  const pillModeEl = document.getElementById('pill-mode-text');
  if (pillModeEl) pillModeEl.textContent = (sessionBuilderMode === 'review' ? 'Review Mode' : 'Test Mode');

  const topicsBadge = document.getElementById('topics-selected-count-badge');
  const allTopicCards = document.querySelectorAll('#generator-topics-list .topic-chip-card');
  const activeTopicCards = document.querySelectorAll('#generator-topics-list .topic-chip-card.active');
  if (topicsBadge) {
    topicsBadge.textContent = `${activeTopicCards.length} of ${allTopicCards.length} Selected`;
  }

  const poolCountsText = document.getElementById('topic-pool-counts-text');
  if (poolCountsText) {
    const poolCaseQuestions = availableCases.length * 6;
    poolCountsText.textContent = `${availableCases.length} Cases (${poolCaseQuestions} Qs) + ${availableStandalone.length} Standalone`;
  }

  if (statusBadge) {
    if (totalQuestions === 0) {
      statusBadge.textContent = 'Select at least 1 Question';
      statusBadge.className = 'total-status error';
      if (launchBtn) launchBtn.disabled = true;
    } else {
      statusBadge.textContent = `Ready (${sessionBuilderMode === 'review' ? 'Practice' : 'Exam'})`;
      statusBadge.className = 'total-status';
      if (launchBtn) launchBtn.disabled = false;
    }
  }
}

function renderManualSelectionLists() {
  const casesList = document.getElementById('generator-cases-list');
  const standaloneList = document.getElementById('generator-standalone-list');
  if (!casesList || !standaloneList) return;

  casesList.innerHTML = '';
  standaloneList.innerHTML = '';

  if (studentCaseStudies().length === 0) {
    casesList.innerHTML = '<p style="color:var(--text-dash-secondary); font-style:italic; padding:8px;">No case studies available.</p>';
  } else {
    studentCaseStudies().forEach(c => {
      const item = document.createElement('label');
      item.className = 'generator-item-label';
      item.innerHTML = `
        <input type="checkbox" class="generator-case-checkbox" data-id="${c.id}">
        <span class="item-name">${escapeHTML(c.title)}</span>
        <span class="item-meta">(${c.screens ? c.screens.length : 0} screens &bull; ${escapeHTML(c.topic || c.disorder || '')})</span>
      `;
      casesList.appendChild(item);
    });
  }

  if (studentStandaloneQuestions().length === 0) {
    standaloneList.innerHTML = '<p style="color:var(--text-dash-secondary); font-style:italic; padding:8px;">No stand-alone questions available.</p>';
  } else {
    studentStandaloneQuestions().forEach(q => {
      const item = document.createElement('label');
      item.className = 'generator-item-label';
      item.innerHTML = `
        <input type="checkbox" class="generator-standalone-checkbox" data-id="${q.id}">
        <span class="item-name">${escapeHTML(q.title)}</span>
        <span class="item-meta">(1 screen &bull; ${escapeHTML(q.topic || q.disorder || '')})</span>
      `;
      standaloneList.appendChild(item);
    });
  }
}

function generateAndStartSession() {
  // Check if manual selection was explicitly made in the advanced accordion
  const manualCaseCbs = Array.from(document.querySelectorAll('.generator-case-checkbox:checked'));
  const manualStdCbs = Array.from(document.querySelectorAll('.generator-standalone-checkbox:checked'));

  let selectedCaseStudies = [];
  let selectedStandalone = [];

  if (manualCaseCbs.length > 0 || manualStdCbs.length > 0) {
    // Use manual selection
    selectedCaseStudies = manualCaseCbs.map(cb => caseStudies.find(x => x.id === cb.dataset.id)).filter(Boolean);
    selectedStandalone = manualStdCbs.map(cb => standaloneQuestions.find(x => x.id === cb.dataset.id)).filter(Boolean);
  } else {
    // Use Topic & Quantity configuration
    const availableCases = studentCaseStudies().filter(c => sessionBuilderTopics.includes((c.topic || c.disorder || 'General').trim()));
    const availableStandalone = studentStandaloneQuestions().filter(s => sessionBuilderTopics.includes((s.topic || s.disorder || 'General').trim()));

    const casesInput = document.getElementById('generator-cases-input');
    const stdInput = document.getElementById('generator-standalone-input');
    const casesQty = Math.min(3, parseInt(casesInput ? casesInput.value : '0', 10) || 0);
    const stdQty = Math.min(67, parseInt(stdInput ? stdInput.value : '0', 10) || 0);

    // Shuffle and slice requested count
    const shuffledCases = [...availableCases].sort(() => 0.5 - Math.random());
    const shuffledStd = [...availableStandalone].sort(() => 0.5 - Math.random());

    selectedCaseStudies = shuffledCases.slice(0, casesQty);
    selectedStandalone = shuffledStd.slice(0, stdQty);
  }

  if (selectedCaseStudies.length === 0 && selectedStandalone.length === 0) {
    showToast("Please select topics and questions to generate your session.", "error");
    return;
  }

  const compiledCase = {
    id: 'compiled_session_' + Date.now(),
    title: sessionBuilderMode === 'review' ? 'NCLEX Practice Session' : 'NextGen NCLEX Exam Simulation',
    description: `A custom ${sessionBuilderMode} testing session containing ${selectedCaseStudies.length} case studies and ${selectedStandalone.length} stand-alone questions.`,
    screens: []
  };

  let currentStepNum = 1;

  // 1. Add Case Studies (each with full 6 chronological unfolding screens)
  selectedCaseStudies.forEach(c => {
    if (c && c.screens) {
      c.screens.forEach((screen, screenIdx) => {
        const screenCopy = JSON.parse(JSON.stringify(screen));
        screenCopy.step = currentStepNum++;
        screenCopy.caseId = c.id;
        screenCopy.caseTitle = c.title;
        screenCopy.isCaseStart = (screenIdx === 0);
        screenCopy.isStandalone = false;
        compiledCase.screens.push(screenCopy);
      });
    }
  });

  // 2. Add Stand-alone Questions
  selectedStandalone.forEach(q => {
    if (q && q.screens) {
      q.screens.forEach(screen => {
        const screenCopy = JSON.parse(JSON.stringify(screen));
        screenCopy.step = currentStepNum++;
        screenCopy.isStandalone = true;
        screenCopy.caseTitle = q.title || 'Stand-alone Question';
        compiledCase.screens.push(screenCopy);
      });
    }
  });

  startPlayer(compiledCase, {
    mode: sessionBuilderMode,
    isRemediation: false,
    allowBacktrack: (sessionBuilderMode === 'review')
  });
}

function createNewCase() {
  const newId = 'case_' + Date.now();
  const newCase = {
    id: newId,
    title: 'New Case Study',
    description: '',
    screens: [
      {
        step: 1,
        leftContent: {
          intro: '',
          tabs: [
            { id: 'nn_' + Date.now(), title: "Nurses' Notes", content: '' }
          ]
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
      }
    ]
  };
  
  caseStudies.push(newCase);
  saveCasesToStorage();
  startEditor(newCase);
  showToast("New case study initialized.");
}

function updateToolbarStates(editor) {
  const container = editor.closest('.rich-editor-container');
  if (!container) return;
  const toolbar = container.querySelector('.rich-editor-toolbar');
  if (!toolbar) return;

  toolbar.querySelectorAll('.toolbar-btn[data-cmd]').forEach(btn => {
    const cmd = btn.dataset.cmd;
    try {
      if (document.queryCommandState(cmd)) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    } catch (e) {
      // queryCommandState might fail for some commands
    }
  });
}

function initRichTextEditors() {
  // Prevent focus loss from contenteditable on mousedown
  document.body.addEventListener('mousedown', (e) => {
    const btn = e.target.closest('.rich-editor-toolbar .toolbar-btn');
    if (btn) {
      e.preventDefault();
    }
  });

  document.body.addEventListener('click', (e) => {
    const btn = e.target.closest('.rich-editor-toolbar .toolbar-btn');
    if (!btn) return;
    
    e.preventDefault();
    
    const container = btn.closest('.rich-editor-container');
    if (!container) return;
    
    const editor = container.querySelector('.rich-text-editor');
    if (!editor) return;
    
    const isAlreadyFocused = (document.activeElement === editor || editor.contains(document.activeElement));
    
    // Save current selection range before applying command
    const selection = window.getSelection();
    let savedRange = null;
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      if (editor.contains(range.commonAncestorContainer)) {
        savedRange = range.cloneRange();
      }
    }
    
    const cmd = btn.dataset.cmd;
    const symbol = btn.dataset.symbol;
    
    if (cmd) {
      document.execCommand(cmd, false, null);
    } else if (symbol) {
      document.execCommand('insertText', false, symbol);
    } else if (btn.classList.contains('table-insert-btn')) {
      insertTableAtCursor(editor, 3, 2);
    }
    
    // Restore focus and selection range (only if not already focused, or if text was selected)
    if (!isAlreadyFocused) {
      editor.focus();
    }
    if (savedRange && !savedRange.collapsed) {
      selection.removeAllRanges();
      selection.addRange(savedRange);
    }
    
    // Immediately update toolbar active states
    updateToolbarStates(editor);
  });

  // Keep toolbar states synced on cursor movement / selection change
  document.body.addEventListener('keyup', (e) => {
    const editor = e.target.closest('.rich-text-editor');
    if (editor) updateToolbarStates(editor);
  });
  document.body.addEventListener('mouseup', (e) => {
    const editor = e.target.closest('.rich-text-editor');
    if (editor) updateToolbarStates(editor);
  });
  document.body.addEventListener('click', (e) => {
    const editor = e.target.closest('.rich-text-editor');
    if (editor) updateToolbarStates(editor);
  });
  document.body.addEventListener('focusin', (e) => {
    const editor = e.target.closest('.rich-text-editor');
    if (editor) updateToolbarStates(editor);
  });

  // Force plain text paste in contenteditable editors to prevent font modifications
  document.addEventListener('paste', (e) => {
    const editor = e.target.closest('.rich-text-editor');
    if (!editor) return;

    e.preventDefault();
    const text = (e.originalEvent || e).clipboardData.getData('text/plain');
    document.execCommand('insertText', false, text);
  });
}



function insertTableAtCursor(editorDiv, rows, cols) {
  let tableHTML = '<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">';
  // Header Row
  tableHTML += '<thead><tr>';
  for (let j = 0; j < cols; j++) {
    tableHTML += `<th placeholder="Header ${j+1}" style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;"></th>`;
  }
  tableHTML += '</tr></thead><tbody>';
  // Data Rows
  for (let i = 0; i < rows; i++) {
    tableHTML += '<tr>';
    for (let j = 0; j < cols; j++) {
      tableHTML += '<td placeholder="Cell" style="border:1px solid #ccd8e0; padding:8px; min-width:80px; background:white; color:#1e293b;"></td>';
    }
    tableHTML += '</tr>';
  }
  tableHTML += '</tbody></table><p><br></p>';
  
  editorDiv.focus();
  const selection = window.getSelection();
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    // Ensure selection is inside the editor
    if (editorDiv.contains(range.commonAncestorContainer)) {
      range.deleteContents();
      const el = document.createElement('div');
      el.innerHTML = tableHTML;
      const frag = document.createDocumentFragment();
      let node, lastNode;
      while ((node = el.firstChild)) {
        lastNode = frag.appendChild(node);
      }
      range.insertNode(frag);
      if (lastNode) {
        range.setStartAfter(lastNode);
        range.collapse(true);
        selection.removeAllRanges();
        selection.addRange(range);
      }
      return;
    }
  }
  // Fallback if not focused/inside editor
  editorDiv.innerHTML += tableHTML;
}

function toggleTheme(forceLight) {
  let targetLight;
  if (typeof forceLight === 'boolean') {
    targetLight = forceLight;
  } else {
    const isCurrentlyLight = document.body.classList.contains('light-mode');
    targetLight = !isCurrentlyLight;
  }
  
  if (targetLight) {
    document.body.classList.add('light-mode');
    try {
      localStorage.setItem('nclex_theme', 'light');
    } catch (e) {
      console.warn("localStorage is blocked:", e);
    }
  } else {
    document.body.classList.remove('light-mode');
    try {
      localStorage.setItem('nclex_theme', 'dark');
    } catch (e) {
      console.warn("localStorage is blocked:", e);
    }
  }

  // Sync both buttons
  ['editor-theme-toggle-btn', 'dashboard-theme-toggle-btn'].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) {
      const sunIcon = btn.querySelector('.sun-icon');
      const moonIcon = btn.querySelector('.moon-icon');
      if (targetLight) {
        if (sunIcon) sunIcon.style.display = 'none';
        if (moonIcon) {
          moonIcon.style.display = 'block';
          moonIcon.classList.remove('hidden');
        }
      } else {
        if (sunIcon) sunIcon.style.display = 'block';
        if (moonIcon) {
          moonIcon.style.display = 'none';
          moonIcon.classList.add('hidden');
        }
      }
    }
  });
}
