/* Faculty authoring dashboard (case and stand-alone tables) and admin login. */

/* ================= DASHBOARD ENGINE (FACULTY AUTHORING PORTAL) ================= */
function initDashboardEvents() {
  const authorToStudentBtn = document.getElementById('author-to-student-btn');
  if (authorToStudentBtn) {
    authorToStudentBtn.addEventListener('click', () => switchView('student'));
  }

  const tabCases = document.getElementById('author-tab-cases');
  const tabStandalone = document.getElementById('author-tab-standalone');
  if (tabCases) {
    tabCases.addEventListener('click', () => switchAuthorTab('cases'));
  }
  if (tabStandalone) {
    tabStandalone.addEventListener('click', () => switchAuthorTab('standalone'));
  }

  const createBtn = document.getElementById('create-btn');
  if (createBtn) {
    createBtn.addEventListener('click', () => {
      if (authorCurrentTab === 'cases') {
        createNewCase();
      } else {
        createStandaloneQuestion();
      }
    });
  }

  const courseFilter = document.getElementById('author-course-filter');
  if (courseFilter) {
    courseFilter.addEventListener('change', (e) => {
      authorCourseFilter = e.target.value;
      updateAuthorUnitFilterOptions();
      applyAuthorTableFilters();
    });
  }

  const unitFilter = document.getElementById('author-unit-filter');
  if (unitFilter) {
    unitFilter.addEventListener('change', (e) => {
      authorUnitFilter = e.target.value;
      applyAuthorTableFilters();
    });
  }

  const tableSearch = document.getElementById('author-table-search');
  if (tableSearch) {
    tableSearch.addEventListener('input', (e) => {
      authorSearchQuery = e.target.value.toLowerCase().trim();
      applyAuthorTableFilters();
    });
  }
}

function switchAuthorTab(tab) {
  authorCurrentTab = tab;
  const tabCases = document.getElementById('author-tab-cases');
  const tabStandalone = document.getElementById('author-tab-standalone');
  const casesTableView = document.getElementById('author-cases-table-view');
  const standaloneTableView = document.getElementById('author-standalone-table-view');
  const createLabel = document.getElementById('create-btn-label');

  if (tab === 'cases') {
    if (tabCases) tabCases.classList.add('active');
    if (tabStandalone) tabStandalone.classList.remove('active');
    if (casesTableView) casesTableView.classList.remove('hidden');
    if (standaloneTableView) standaloneTableView.classList.add('hidden');
    if (createLabel) createLabel.textContent = 'Create New Case Study';
  } else {
    if (tabStandalone) tabStandalone.classList.add('active');
    if (tabCases) tabCases.classList.remove('active');
    if (standaloneTableView) standaloneTableView.classList.remove('hidden');
    if (casesTableView) casesTableView.classList.add('hidden');
    if (createLabel) createLabel.textContent = 'Create New Stand-alone Question';
  }

  applyAuthorTableFilters();
}

function updateAuthorUnitFilterOptions() {
  const unitFilter = document.getElementById('author-unit-filter');
  if (!unitFilter) return;

  const currentVal = authorUnitFilter;
  let html = '<option value="ALL">All Units</option>';

  if (authorCourseFilter === 'ALL') {
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
  } else if (authorCourseFilter === 'NURS 1017') {
    html += `
      <optgroup label="NURS 1017 (Pathophysiology 1)">
        ${CURRICULUM_COURSES["NURS 1017"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
    `;
  } else if (authorCourseFilter === 'NURS 1021') {
    html += `
      <optgroup label="NURS 1021 (Pathophysiology 2)">
        ${CURRICULUM_COURSES["NURS 1021"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('')}
      </optgroup>
    `;
  } else if (authorCourseFilter === 'Others') {
    html += '<option value="Others">Others (Unassigned)</option>';
  }

  unitFilter.innerHTML = html;
  const exists = Array.from(unitFilter.options).some(opt => opt.value === currentVal);
  if (exists) {
    unitFilter.value = currentVal;
  } else {
    authorUnitFilter = 'ALL';
    unitFilter.value = 'ALL';
  }
}

function renderDashboard() {
  // 1. Calculate KPI Summary Metrics
  const totalCases = caseStudies.length;
  const totalScreens = caseStudies.reduce((sum, c) => sum + (c.screens ? c.screens.length : 0), 0);
  const totalStandalone = standaloneQuestions.length;

  const count1017 = caseStudies.filter(c => c.course === 'NURS 1017').length +
                    standaloneQuestions.filter(q => q.course === 'NURS 1017').length;

  const count1021 = caseStudies.filter(c => c.course === 'NURS 1021').length +
                    standaloneQuestions.filter(q => q.course === 'NURS 1021').length;

  // 2. Update KPI Elements in DOM
  const kpiCasesCount = document.getElementById('author-kpi-cases-count');
  const kpiCasesScreens = document.getElementById('author-kpi-cases-screens');
  const kpiStandaloneCount = document.getElementById('author-kpi-standalone-count');
  const kpi1017Count = document.getElementById('author-kpi-1017-count');
  const kpi1021Count = document.getElementById('author-kpi-1021-count');

  if (kpiCasesCount) kpiCasesCount.textContent = `${totalCases} Cases`;
  if (kpiCasesScreens) kpiCasesScreens.textContent = `${totalScreens} Unfolding Clinical Screens`;
  if (kpiStandaloneCount) kpiStandaloneCount.textContent = `${totalStandalone} Questions`;
  if (kpi1017Count) kpi1017Count.textContent = `${count1017} Items`;
  if (kpi1021Count) kpi1021Count.textContent = `${count1021} Items`;

  // 3. Update Tab Badges
  const tabCasesBadge = document.getElementById('author-tab-cases-badge');
  const tabStandaloneBadge = document.getElementById('author-tab-standalone-badge');
  if (tabCasesBadge) tabCasesBadge.textContent = totalCases;
  if (tabStandaloneBadge) tabStandaloneBadge.textContent = totalStandalone;

  // 4. Render Tables
  renderAuthorCasesTable();
  renderAuthorStandaloneTable();
  applyAuthorTableFilters();
}

function renderAuthorCasesTable() {
  const tbody = document.getElementById('author-cases-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (caseStudies.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:32px; color:#64748b; font-style:italic;">No case studies available. Click "Create New Case Study" to begin.</td></tr>`;
    return;
  }

  caseStudies.forEach(c => {
    const tr = document.createElement('tr');
    tr.className = 'author-case-row';
    tr.dataset.course = c.course || 'Others';
    tr.dataset.unit = c.unit || c.topic || 'Others';
    tr.dataset.id = c.id;
    tr.dataset.title = (c.title || '').toLowerCase();
    tr.dataset.desc = (c.description || '').toLowerCase();

    const courseBadge = c.course === 'NURS 1017'
      ? `<span class="badge-course-1017">NURS 1017</span>`
      : c.course === 'NURS 1021'
        ? `<span class="badge-course-1021">NURS 1021</span>`
        : `<span class="badge-course-other">Unassigned</span>`;

    const unitBadge = `<span class="badge-unit">${escapeHTML(c.unit || c.topic || 'Others')}</span>`;
    const screensCount = c.screens ? c.screens.length : 0;
    const screensBadge = `<span class="badge-screens">${screensCount} Screens</span>`;

    tr.innerHTML = `
      <td>
        <div class="author-scenario-title">${escapeHTML(c.title || 'Untitled Case')}</div>
        <div class="author-scenario-desc">${escapeHTML(c.description || 'No description.')}</div>
        <span class="author-scenario-id card-id-badge" data-id="${c.id}" title="Click to copy direct LMS link for students"><svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-1px; margin-right:3px;"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>ID: ${escapeHTML(c.id)}</span>
      </td>
      <td>${courseBadge}</td>
      <td>${unitBadge}</td>
      <td>${screensBadge}</td>
      <td class="author-actions-cell">
        <div class="author-actions-wrapper">
          <button class="btn-author-edit edit-case-btn" data-id="${c.id}">Edit</button>
          <button class="btn-author-launch play-case-btn" data-id="${c.id}">Launch</button>
          <button class="btn-author-delete delete-case-btn" data-id="${c.id}">Delete</button>
        </div>
      </td>
    `;

    tr.querySelector('.edit-case-btn').addEventListener('click', () => startEditor(c));
    tr.querySelector('.play-case-btn').addEventListener('click', () => startPlayer(c));
    tr.querySelector('.delete-case-btn').addEventListener('click', () => {
      const caseTitle = c.title || 'Untitled Case';
      if (confirm(`Are you sure you want to delete case study "${caseTitle}"? This action cannot be undone.`)) {
        caseStudies = caseStudies.filter(x => x.id !== c.id);
        saveCasesToStorage();
        if (db) deleteFromStore('case_studies', c.id);
        showToast(`Case study "${caseTitle}" deleted.`);
        renderDashboard();
      }
    });

    tr.querySelector('.card-id-badge').addEventListener('click', (e) => {
      e.stopPropagation();
      const baseUrl = window.location.protocol.startsWith('http')
        ? (window.location.origin + window.location.pathname)
        : 'https://thadaniavinash.github.io/NCLEX/';
      const directUrl = `${baseUrl}?case=${encodeURIComponent(c.id)}`;
      navigator.clipboard.writeText(directUrl);
      showToast(`Copied LMS link for "${c.title}"!`);
    });

    tbody.appendChild(tr);
  });
}

function getQuestionTypeLabel(type) {
  const mapping = {
    'dropdown_cloze': 'Drop-Down Cloze',
    'drag_drop_cloze': 'Drag-and-Drop Cloze',
    'dropdown_table': 'Drop-Down Table',
    'matrix_mc': 'Matrix Multiple Choice',
    'select_n': 'Select N Multiple Response',
    'bowtie': 'Bowtie',
    'multiple_choice': 'Multiple Choice',
    'fill_blank': 'Fill-in-the-Blank',
    'hotspot': 'Hotspot',
    'ordered_response': 'Ordered Response',
    'select_all': 'Select All (SATA)',
    'highlight': 'Highlight Text/Table',
    'highlight_2': 'Highlight Text/Table-2',
    'matrix_mr': 'Matrix Multiple Response',
    'grouped_mr': 'Grouped Multiple Response',
    'trend': 'Trend',
    'dyad': 'Dyad Rationale',
    'triad': 'Triad Rationale'
  };
  return mapping[type] || type;
}

function renderAuthorStandaloneTable() {
  const tbody = document.getElementById('author-standalone-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (standaloneQuestions.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:32px; color:#64748b; font-style:italic;">No stand-alone questions available. Click "Create New Stand-alone Question" to begin.</td></tr>`;
    return;
  }

  standaloneQuestions.forEach(q => {
    const tr = document.createElement('tr');
    tr.className = 'author-standalone-row';
    tr.dataset.course = q.course || 'Others';
    tr.dataset.unit = q.unit || q.topic || 'Others';
    tr.dataset.id = q.id;
    tr.dataset.title = (q.title || '').toLowerCase();
    tr.dataset.desc = (q.description || '').toLowerCase();

    const courseBadge = q.course === 'NURS 1017'
      ? `<span class="badge-course-1017">NURS 1017</span>`
      : q.course === 'NURS 1021'
        ? `<span class="badge-course-1021">NURS 1021</span>`
        : `<span class="badge-course-other">Unassigned</span>`;

    const unitBadge = `<span class="badge-unit">${escapeHTML(q.unit || q.topic || 'Others')}</span>`;
    const qType = q.screens && q.screens[0] && q.screens[0].question ? q.screens[0].question.type : '';
    const formatBadge = `<span class="badge-screens" style="background:#f1f5f9; color:#334155; border-color:#cbd5e1;">${escapeHTML(getQuestionTypeLabel(qType))}</span>`;

    tr.innerHTML = `
      <td>
        <div class="author-scenario-title">${escapeHTML(q.title || 'Untitled Question')}</div>
        <div class="author-scenario-desc">${escapeHTML(q.description || 'No description.')}</div>
        <span class="author-scenario-id card-id-badge" data-id="${q.id}" title="Click to copy direct LMS link for students"><svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-1px; margin-right:3px;"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>ID: ${escapeHTML(q.id)}</span>
      </td>
      <td>${courseBadge}</td>
      <td>${unitBadge}</td>
      <td>${formatBadge}</td>
      <td class="author-actions-cell">
        <div class="author-actions-wrapper">
          <button class="btn-author-edit edit-q-btn" data-id="${q.id}">Edit</button>
          <button class="btn-author-launch play-q-btn" data-id="${q.id}">Launch</button>
          <button class="btn-author-delete delete-q-btn" data-id="${q.id}">Delete</button>
        </div>
      </td>
    `;

    tr.querySelector('.edit-q-btn').addEventListener('click', () => startEditor(q));
    tr.querySelector('.play-q-btn').addEventListener('click', () => startPlayer(q));
    tr.querySelector('.delete-q-btn').addEventListener('click', () => {
      const qTitle = q.title || 'Untitled Question';
      if (confirm(`Are you sure you want to delete stand-alone question "${qTitle}"? This action cannot be undone.`)) {
        standaloneQuestions = standaloneQuestions.filter(x => x.id !== q.id);
        saveStandaloneToStorage();
        if (db) deleteFromStore('standalone_questions', q.id);
        showToast(`Stand-alone question "${qTitle}" deleted.`);
        renderDashboard();
      }
    });

    tr.querySelector('.card-id-badge').addEventListener('click', (e) => {
      e.stopPropagation();
      const baseUrl = window.location.protocol.startsWith('http')
        ? (window.location.origin + window.location.pathname)
        : 'https://thadaniavinash.github.io/NCLEX/';
      const directUrl = `${baseUrl}?standalone=${encodeURIComponent(q.id)}`;
      navigator.clipboard.writeText(directUrl);
      showToast(`Copied LMS link for "${q.title}"!`);
    });

    tbody.appendChild(tr);
  });
}

function applyAuthorTableFilters() {
  const currentTabIsCases = (authorCurrentTab === 'cases');
  const rows = currentTabIsCases
    ? document.querySelectorAll('#author-cases-tbody .author-case-row')
    : document.querySelectorAll('#author-standalone-tbody .author-standalone-row');

  let visibleCount = 0;
  const totalCount = rows.length;

  rows.forEach(tr => {
    const rowCourse = tr.dataset.course;
    const rowUnit = tr.dataset.unit;
    const rowId = (tr.dataset.id || '').toLowerCase();
    const rowTitle = tr.dataset.title || '';
    const rowDesc = tr.dataset.desc || '';

    let matchesCourse = (authorCourseFilter === 'ALL' || rowCourse === authorCourseFilter);
    let matchesUnit = (authorUnitFilter === 'ALL' || rowUnit === authorUnitFilter);
    let matchesSearch = (!authorSearchQuery || rowTitle.includes(authorSearchQuery) || rowDesc.includes(authorSearchQuery) || rowId.includes(authorSearchQuery));

    if (matchesCourse && matchesUnit && matchesSearch) {
      tr.style.display = '';
      visibleCount++;
    } else {
      tr.style.display = 'none';
    }
  });

  const countText = document.getElementById('author-filtered-count-text');
  if (countText) {
    const itemType = currentTabIsCases ? 'Case Studies' : 'Stand-alone Questions';
    countText.textContent = `Showing ${visibleCount} of ${totalCount} ${itemType}`;
  }
}

/* ================= ADMIN MANAGEMENT SYSTEM ================= */
function initAdminEvents() {
  const adminLoginBtn = document.getElementById('admin-login-btn');
  const adminLogoutBtn = document.getElementById('admin-logout-btn');
  const loginModal = document.getElementById('login-modal');
  const loginCancelBtn = document.getElementById('login-cancel-btn');
  const adminLoginForm = document.getElementById('admin-login-form');
  const loginUsernameInput = document.getElementById('login-username');
  const loginPasswordInput = document.getElementById('login-password');
  const loginErrorMsg = document.getElementById('login-error-msg');

  if (adminLoginBtn) {
    adminLoginBtn.addEventListener('click', () => {
      if (loginUsernameInput) loginUsernameInput.value = '';
      if (loginPasswordInput) loginPasswordInput.value = '';
      if (loginErrorMsg) loginErrorMsg.classList.add('hidden');
      if (loginModal) {
        loginModal.classList.remove('hidden');
        if (loginUsernameInput) loginUsernameInput.focus();
      }
    });
  }

  if (loginCancelBtn && loginModal) {
    loginCancelBtn.addEventListener('click', () => {
      loginModal.classList.add('hidden');
    });
  }

  if (loginModal) {
    loginModal.addEventListener('click', (e) => {
      if (e.target === loginModal) {
        loginModal.classList.add('hidden');
      }
    });
  }

  if (adminLoginForm) {
    adminLoginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = loginUsernameInput.value.trim();
      const password = loginPasswordInput.value;
      const submitBtn = adminLoginForm.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
      if (loginErrorMsg) loginErrorMsg.classList.add('hidden');

      const result = await signInAdmin(email, password);
      if (submitBtn) submitBtn.disabled = false;
      if (result.ok) {
        loginPasswordInput.value = '';
        if (loginModal) loginModal.classList.add('hidden');
        showToast("Logged in as Administrator", "success");
        applyAdminState();
      } else if (loginErrorMsg) {
        loginErrorMsg.textContent = result.message;
        loginErrorMsg.classList.remove('hidden');
      }
    });
  }

  if (adminLogoutBtn) {
    adminLogoutBtn.addEventListener('click', () => {
      if (confirm("Are you sure you want to log out of admin mode?")) {
        signOutAdmin();
        showToast("Logged out of Admin Mode", "success");
        applyAdminState();
      }
    });
  }
}

function applyAdminState() {
  const loggedOutEl = document.getElementById('admin-status-logged-out');
  const loggedInEl = document.getElementById('admin-status-logged-in');
  if (isAdminLoggedIn) {
    if (loggedOutEl) loggedOutEl.classList.add('hidden');
    if (loggedInEl) loggedInEl.classList.remove('hidden');
  } else {
    if (loggedOutEl) loggedOutEl.classList.remove('hidden');
    if (loggedInEl) loggedInEl.classList.add('hidden');
  }

  renderDashboard();
}

function populateEditorUnitSelect(selectedCourse, selectedUnit) {
  const unitSelect = document.getElementById('case-unit-select');
  if (!unitSelect) return;

  let html = '<option value="">Unit: Select Unit</option>';
  if (selectedCourse === 'NURS 1017' && CURRICULUM_COURSES["NURS 1017"]) {
    html += CURRICULUM_COURSES["NURS 1017"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('');
  } else if (selectedCourse === 'NURS 1021' && CURRICULUM_COURSES["NURS 1021"]) {
    html += CURRICULUM_COURSES["NURS 1021"].map(u => `<option value="${escapeHTML(u)}">${escapeHTML(u)}</option>`).join('');
  } else {
    html += '<option value="Others">Others</option>';
  }
  unitSelect.innerHTML = html;
  if (selectedUnit) {
    unitSelect.value = selectedUnit;
  }
}

function createStandaloneQuestion() {
  const newId = 'standalone_' + Date.now();
  const newQ = {
    id: newId,
    title: 'New Stand-alone Question',
    description: '',
    isStandalone: true,
    screens: [
      {
        step: 1,
        leftContent: {
          intro: '',
          tabs: []
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
  
  standaloneQuestions.push(newQ);
  saveStandaloneToStorage();
  startEditor(newQ);
  showToast("New standalone question initialized.");
}
