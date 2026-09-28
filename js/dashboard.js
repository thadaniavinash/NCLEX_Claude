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

  const statusFilter = document.getElementById('author-status-filter');
  if (statusFilter) {
    statusFilter.addEventListener('change', (e) => {
      authorStatusFilter = e.target.value;
      applyAuthorTableFilters();
    });
  }

  const readOnlySignInBtn = document.getElementById('author-readonly-signin-btn');
  if (readOnlySignInBtn) {
    readOnlySignInBtn.addEventListener('click', () => {
      const loginBtn = document.getElementById('admin-login-btn');
      if (loginBtn) loginBtn.click();
    });
  }

  initAuthorTableSorting();

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
  // 1. Summary counts (hidden = not shown to students yet; see itemProblems in data.js)
  const totalCases = caseStudies.length;
  const totalScreens = caseStudies.reduce((sum, c) => sum + (c.screens ? c.screens.length : 0), 0);
  const totalStandalone = standaloneQuestions.length;
  const hiddenCases = totalCases - studentCaseStudies().length;
  const hiddenStandalone = totalStandalone - studentStandaloneQuestions().length;

  const count1017 = caseStudies.filter(c => c.course === 'NURS 1017').length +
                    standaloneQuestions.filter(q => q.course === 'NURS 1017').length;

  const count1021 = caseStudies.filter(c => c.course === 'NURS 1021').length +
                    standaloneQuestions.filter(q => q.course === 'NURS 1021').length;

  const setText = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
  const hiddenNote = n => n ? ` • ${n} hidden from students` : '';
  setText('author-kpi-cases-count', `${totalCases} Cases`);
  setText('author-kpi-cases-screens', `${totalScreens} screens${hiddenNote(hiddenCases)}`);
  setText('author-kpi-standalone-count', `${totalStandalone} Questions`);
  setText('author-kpi-standalone-sub', hiddenStandalone ? `${hiddenStandalone} hidden from students` : 'All visible to students');
  setText('author-kpi-1017-count', `${count1017} Items`);
  setText('author-kpi-1021-count', `${count1021} Items`);
  setText('author-tab-cases-badge', totalCases);
  setText('author-tab-standalone-badge', totalStandalone);

  renderSaveStatus();
  renderAuthorReadOnlyNotice();
  renderAuthorTable('cases');
  renderAuthorTable('standalone');
  applyAuthorTableFilters();
}

/* ---- Save status (dashboard sub-bar and editor header) ---- */
function currentSaveStatus() {
  if (isBankFiltered) return { tone: 'muted', text: 'Read-only: this link opened part of the bank' };
  if (isDatabaseUnavailable) return { tone: 'warn', text: 'Offline: showing the backup copy, saving is off' };
  if (lastSaveOutcome && !lastSaveOutcome.ok) return { tone: 'error', text: 'Last save failed, see the message and try again' };
  if (!canEditBank()) return { tone: 'muted', text: 'Signed out: sign in to make changes' };
  if (lastSaveOutcome) {
    const time = lastSaveOutcome.at.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return { tone: 'ok', text: `Saved at ${time}` };
  }
  return { tone: 'ok', text: isAdminLoggedIn ? 'Connected: signed in as administrator' : 'Connected' };
}

function renderSaveStatus() {
  const status = currentSaveStatus();
  document.querySelectorAll('.save-status-indicator').forEach(el => {
    el.dataset.tone = status.tone;
    const text = el.querySelector('.save-status-text');
    if (text) text.textContent = status.text;
  });
}

function renderAuthorReadOnlyNotice() {
  const notice = document.getElementById('author-readonly-notice');
  const text = document.getElementById('author-readonly-notice-text');
  const signInBtn = document.getElementById('author-readonly-signin-btn');
  if (!notice || !text) return;
  let message = '';
  if (isBankFiltered) {
    message = 'This page was opened with a link to part of the bank, so editing is turned off. Open the app without ?cases= or ?standalone= to edit.';
  } else if (isDatabaseUnavailable) {
    message = 'The database could not be reached, so this is the backup copy and editing is turned off. Reload the page to try again.';
  } else if (!canEditBank()) {
    message = 'You are signed out. Sign in as an administrator to create, edit or delete items. You can still launch any item to preview it.';
  }
  notice.classList.toggle('hidden', !message);
  const createBtn = document.getElementById('create-btn');
  if (createBtn) createBtn.classList.toggle('hidden', !canEditBank());
  text.textContent = message;
  if (signInBtn) signInBtn.classList.toggle('hidden', !(message && !isBankFiltered && !isDatabaseUnavailable));
}

// Marks items students cannot see yet, with the reasons.
function readinessBadge(item) {
  const problems = itemProblems(item);
  if (!problems.length) return '<span class="status-pill ready">Visible</span>';
  const first = problems[0] === 'marked as draft' ? 'Draft' : 'Hidden';
  return `<span class="status-pill hidden-item" title="${escapeHTML('Hidden from students: ' + problems.join('; '))}">${first}</span>`;
}

function readinessReasons(item) {
  const problems = itemProblems(item);
  if (!problems.length) return '';
  const shown = problems.slice(0, 2).join('; ') + (problems.length > 2 ? ` (+${problems.length - 2} more)` : '');
  return `<div class="author-readiness-reasons">Hidden from students: ${escapeHTML(shown)}</div>`;
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

const AUTHOR_TABLES = {
  cases: { tbody: 'author-cases-tbody', rowClass: 'author-case-row', noun: 'case study', untitled: 'Untitled Case', linkParam: 'case',
           empty: 'No case studies available. Click "Create New Case Study" to begin.' },
  standalone: { tbody: 'author-standalone-tbody', rowClass: 'author-standalone-row', noun: 'stand-alone question', untitled: 'Untitled Question', linkParam: 'standalone',
                empty: 'No stand-alone questions available. Click "Create New Stand-alone Question" to begin.' }
};

function authorBank(kind) {
  return kind === 'cases' ? caseStudies : standaloneQuestions;
}

function saveAuthorBank(kind) {
  return kind === 'cases' ? saveCasesToStorage() : saveStandaloneToStorage();
}

function renderAuthorTable(kind) {
  const cfg = AUTHOR_TABLES[kind];
  const tbody = document.getElementById(cfg.tbody);
  if (!tbody) return;
  tbody.innerHTML = '';
  const items = authorBank(kind);

  if (items.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:32px; color:#64748b; font-style:italic;">${cfg.empty}</td></tr>`;
    return;
  }

  const editable = canEditBank();
  items.forEach((item, bankIndex) => {
    const tr = document.createElement('tr');
    tr.className = cfg.rowClass;
    tr.dataset.course = item.course || 'Others';
    tr.dataset.unit = item.unit || item.topic || 'Others';
    tr.dataset.id = item.id;
    tr.dataset.title = (item.title || '').toLowerCase();
    tr.dataset.desc = (item.description || '').toLowerCase();
    tr.dataset.ready = isReadyForStudents(item) ? 'ready' : 'hidden';
    tr.dataset.order = bankIndex;

    const courseBadge = item.course === 'NURS 1017'
      ? `<span class="badge-course-1017">NURS 1017</span>`
      : item.course === 'NURS 1021'
        ? `<span class="badge-course-1021">NURS 1021</span>`
        : `<span class="badge-course-other">Unassigned</span>`;
    const unitBadge = `<span class="badge-unit">${escapeHTML(item.unit || item.topic || 'Others')}</span>`;
    let thirdColumn;
    if (kind === 'cases') {
      const screensCount = item.screens ? item.screens.length : 0;
      thirdColumn = `<span class="badge-screens">${screensCount} Screens</span>`;
    } else {
      const qType = item.screens && item.screens[0] && item.screens[0].question ? item.screens[0].question.type : '';
      thirdColumn = `<span class="badge-screens" style="background:#f1f5f9; color:#334155; border-color:#cbd5e1;">${escapeHTML(getQuestionTypeLabel(qType))}</span>`;
    }
    const title = item.title || cfg.untitled;

    tr.innerHTML = `
      <td>
        <div class="author-scenario-title">${escapeHTML(title)}</div>
        <div class="author-scenario-desc">${escapeHTML(item.description || 'No description.')}</div>
        ${readinessReasons(item)}
        <span class="author-scenario-id card-id-badge" data-id="${escapeHTML(item.id)}" title="Click to copy direct LMS link for students"><svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-1px; margin-right:3px;"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>ID: ${escapeHTML(item.id)}</span>
      </td>
      <td>${courseBadge}</td>
      <td>${unitBadge}</td>
      <td>${thirdColumn}</td>
      <td>${readinessBadge(item)}</td>
      <td class="author-actions-cell">
        <div class="author-actions-wrapper">
          ${editable ? `<button class="btn-author-edit" type="button">Edit</button>` : ''}
          <button class="btn-author-launch" type="button">${editable ? 'Launch' : 'Preview'}</button>
          <button class="btn-author-more" type="button" aria-haspopup="menu" aria-expanded="false" aria-label="More actions for ${escapeHTML(title)}" title="More actions">&#8943;</button>
        </div>
      </td>
    `;

    const editBtn = tr.querySelector('.btn-author-edit');
    if (editBtn) editBtn.addEventListener('click', () => startEditor(item));
    tr.querySelector('.btn-author-launch').addEventListener('click', () => startPlayer(item));
    tr.querySelector('.btn-author-more').addEventListener('click', (e) => {
      e.stopPropagation();
      openAuthorRowMenu(e.currentTarget, kind, item);
    });
    tr.querySelector('.card-id-badge').addEventListener('click', (e) => {
      e.stopPropagation();
      copyStudentLink(kind, item);
    });

    tbody.appendChild(tr);
  });
}

function copyStudentLink(kind, item) {
  const baseUrl = window.location.protocol.startsWith('http')
    ? (window.location.origin + window.location.pathname)
    : 'https://thadaniavinash.github.io/NCLEX/';
  const directUrl = `${baseUrl}?${AUTHOR_TABLES[kind].linkParam}=${encodeURIComponent(item.id)}`;
  navigator.clipboard.writeText(directUrl);
  showToast(`Copied student link for "${escapeHTML(item.title || item.id)}".`);
}

/* ---- Row "more actions" menu (one shared popup, placed next to the clicked button) ---- */
function closeAuthorRowMenu() {
  const menu = document.getElementById('author-row-menu');
  if (menu) menu.remove();
  document.querySelectorAll('.btn-author-more[aria-expanded="true"]').forEach(b => b.setAttribute('aria-expanded', 'false'));
}

function openAuthorRowMenu(button, kind, item) {
  const wasOpenHere = button.getAttribute('aria-expanded') === 'true';
  closeAuthorRowMenu();
  if (wasOpenHere) return;

  const editable = canEditBank();
  const actions = [{ label: 'Copy student link', run: () => copyStudentLink(kind, item) }];
  if (editable) {
    actions.push({ label: 'Duplicate', run: () => duplicateAuthorItem(kind, item) });
    actions.push(item.draft === true
      ? { label: 'Show to students', run: () => setAuthorItemDraft(kind, item, false) }
      : { label: 'Hide from students (draft)', run: () => setAuthorItemDraft(kind, item, true) });
    actions.push({ label: 'Delete…', danger: true, run: () => deleteAuthorItem(kind, item) });
  }

  const menu = document.createElement('div');
  menu.id = 'author-row-menu';
  menu.className = 'author-row-menu';
  menu.setAttribute('role', 'menu');
  actions.forEach(action => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.setAttribute('role', 'menuitem');
    btn.className = action.danger ? 'danger' : '';
    btn.textContent = action.label;
    btn.addEventListener('click', () => { closeAuthorRowMenu(); action.run(); });
    menu.appendChild(btn);
  });
  document.body.appendChild(menu);

  const rect = button.getBoundingClientRect();
  const menuHeight = menu.offsetHeight;
  const top = rect.bottom + 4 + menuHeight > window.innerHeight ? rect.top - 4 - menuHeight : rect.bottom + 4;
  menu.style.top = `${Math.max(8, top)}px`;
  menu.style.left = `${Math.max(8, rect.right - menu.offsetWidth)}px`;
  button.setAttribute('aria-expanded', 'true');
  menu.querySelector('button').focus();
}

document.addEventListener('click', (e) => {
  if (!e.target.closest('#author-row-menu')) closeAuthorRowMenu();
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && document.getElementById('author-row-menu')) closeAuthorRowMenu();
});
window.addEventListener('resize', closeAuthorRowMenu);
document.addEventListener('scroll', closeAuthorRowMenu, true);

// A copy starts as a draft, so students never see two identical items.
function duplicateAuthorItem(kind, item) {
  const list = authorBank(kind);
  const copy = JSON.parse(JSON.stringify(item));
  copy.id = (kind === 'cases' ? 'case_' : 'standalone_') + Date.now();
  copy.title = `${item.title || AUTHOR_TABLES[kind].untitled} (copy)`;
  copy.draft = true;
  list.splice(list.indexOf(item) + 1, 0, copy);
  saveAuthorBank(kind);
  renderDashboard();
  showToast(`Duplicated as "${escapeHTML(copy.title)}". It stays hidden from students until you choose Show to students.`);
}

function setAuthorItemDraft(kind, item, isDraft) {
  if (isDraft) item.draft = true;
  else delete item.draft;
  saveAuthorBank(kind);
  renderDashboard();
  if (!isDraft && !isReadyForStudents(item)) {
    showToast(`"${escapeHTML(item.title || item.id)}" is no longer a draft, but stays hidden until: ${escapeHTML(itemProblems(item).join('; '))}.`, 'warning');
  }
}

function deleteAuthorItem(kind, item) {
  const cfg = AUTHOR_TABLES[kind];
  const title = item.title || cfg.untitled;
  if (!confirm(`Delete ${cfg.noun} "${title}"? This cannot be undone.`)) return;
  if (kind === 'cases') caseStudies = caseStudies.filter(x => x.id !== item.id);
  else standaloneQuestions = standaloneQuestions.filter(x => x.id !== item.id);
  saveAuthorBank(kind);
  if (db) deleteFromStore(kind === 'cases' ? 'case_studies' : 'standalone_questions', item.id);
  showToast(`Deleted "${escapeHTML(title)}".`);
  renderDashboard();
}

/* ---- Filtering and sorting ---- */
let authorStatusFilter = 'ALL';
let authorSort = { key: '', dir: 1 };

function applyAuthorTableFilters() {
  const currentTabIsCases = (authorCurrentTab === 'cases');
  const tbody = document.getElementById(currentTabIsCases ? 'author-cases-tbody' : 'author-standalone-tbody');
  const rows = tbody ? Array.from(tbody.querySelectorAll('tr[data-id]')) : [];

  let visibleCount = 0;
  const totalCount = rows.length;

  rows.forEach(tr => {
    const rowId = (tr.dataset.id || '').toLowerCase();
    const matchesCourse = (authorCourseFilter === 'ALL' || tr.dataset.course === authorCourseFilter);
    const matchesUnit = (authorUnitFilter === 'ALL' || tr.dataset.unit === authorUnitFilter);
    const matchesStatus = (authorStatusFilter === 'ALL' || tr.dataset.ready === authorStatusFilter);
    const matchesSearch = (!authorSearchQuery || tr.dataset.title.includes(authorSearchQuery) || tr.dataset.desc.includes(authorSearchQuery) || rowId.includes(authorSearchQuery));

    if (matchesCourse && matchesUnit && matchesStatus && matchesSearch) {
      tr.style.display = '';
      visibleCount++;
    } else {
      tr.style.display = 'none';
    }
  });

  // Sort (bank order when no column is chosen)
  if (tbody) {
    const key = authorSort.key;
    const value = tr => key === 'title' ? tr.dataset.title
      : key === 'course' ? tr.dataset.course
      : key === 'unit' ? tr.dataset.unit
      : key === 'status' ? tr.dataset.ready : '';
    rows.sort((a, b) => {
      const cmp = key ? value(a).localeCompare(value(b), undefined, { numeric: true, sensitivity: 'base' }) * authorSort.dir : 0;
      return cmp || (a.dataset.order - b.dataset.order);
    }).forEach(tr => tbody.appendChild(tr));
  }
  document.querySelectorAll('.pv-table th[data-sort]').forEach(th => {
    th.setAttribute('aria-sort', th.dataset.sort === authorSort.key ? (authorSort.dir === 1 ? 'ascending' : 'descending') : 'none');
  });

  const countText = document.getElementById('author-filtered-count-text');
  if (countText) {
    const itemType = currentTabIsCases ? 'Case Studies' : 'Stand-alone Questions';
    countText.textContent = `Showing ${visibleCount} of ${totalCount} ${itemType}`;
  }
}

function initAuthorTableSorting() {
  document.querySelectorAll('.pv-table th[data-sort]').forEach(th => {
    const label = th.textContent.trim();
    th.innerHTML = `<button type="button" class="th-sort-btn">${escapeHTML(label)}<span class="th-sort-arrow" aria-hidden="true"></span></button>`;
    th.querySelector('button').addEventListener('click', () => {
      const key = th.dataset.sort;
      if (authorSort.key !== key) authorSort = { key, dir: 1 };
      else if (authorSort.dir === 1) authorSort = { key, dir: -1 };
      else authorSort = { key: '', dir: 1 };
      applyAuthorTableFilters();
    });
  });
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
