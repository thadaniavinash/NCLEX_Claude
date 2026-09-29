/* Editor top bar: breadcrumb (the "Question bank" link goes back), title, chips for course, unit,
   description (edited in a small dialog) and readiness for students, the save status, the ⋯ menu
   (download JSON, copy student link, theme, keyboard shortcuts) and Preview | Save | Launch.
   Ctrl+S saves from anywhere in the editor. */

let editorOpenedAt = null;
let readyChipTimer = null;

function isEditorOpen() {
  const view = document.getElementById('editor-view');
  return !!(view && view.classList.contains('active') && currentCase);
}

/* ---- Save status: quiet when saved, coloured only when something needs attention ---- */
function relativeSaveTime(date) {
  const seconds = (Date.now() - date.getTime()) / 1000;
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)} min ago`;
  const now = new Date();
  if (date.toDateString() === now.toDateString()) return `at ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
  return `on ${date.toLocaleDateString([], { day: 'numeric', month: 'short' })}`;
}

function editorSaveStatus() {
  const base = currentSaveStatus();
  if (base.tone !== 'ok') return base;
  let when = null;
  if (lastSaveOutcome && lastSaveOutcome.ok && editorOpenedAt && lastSaveOutcome.at >= editorOpenedAt) when = lastSaveOutcome.at;
  else if (currentCase && currentCase.updatedAt) when = new Date(currentCase.updatedAt);
  const text = when && !isNaN(when) ? `Saved · ${relativeSaveTime(when)}` : 'Saved';
  return { tone: 'quiet', text };
}

/* ---- Breadcrumb and chips ---- */
function refreshEditorHeader() {
  if (!currentCase) return;
  const kind = document.getElementById('editor-crumb-kind');
  if (kind) {
    const n = currentCase.screens.length;
    kind.textContent = currentCase.isStandalone ? 'Stand-alone question' : `Case study · ${n} screen${n === 1 ? '' : 's'}`;
  }
  refreshMetaChips();
  refreshDescriptionChip();
  refreshReadyChip();
  const themeItem = document.getElementById('editor-theme-toggle-btn');
  if (themeItem) themeItem.textContent = `Switch to ${currentTheme() === 'dark' ? 'light' : 'dark'} theme`;
}

function refreshMetaChips() {
  const course = document.getElementById('case-course-select');
  const unit = document.getElementById('case-unit-select');
  const courseText = document.getElementById('case-course-chip-text');
  const unitText = document.getElementById('case-unit-chip-text');
  if (course && courseText) {
    courseText.textContent = course.value || 'Add course';
    courseText.parentElement.classList.toggle('is-empty', !course.value);
    courseText.parentElement.title = course.value ? `Course: ${course.value}` : 'Choose the course';
  }
  if (unit && unitText) {
    unitText.textContent = unit.value ? unit.value.split(' (')[0] : 'Add unit';
    unitText.parentElement.classList.toggle('is-empty', !unit.value);
    unitText.parentElement.title = unit.value ? `Unit: ${unit.value}` : 'Choose the unit';
  }
}

function refreshDescriptionChip() {
  const btn = document.getElementById('editor-desc-btn');
  const input = document.getElementById('case-desc-input');
  if (!btn || !input) return;
  const filled = input.value.trim().length > 0;
  btn.classList.toggle('is-empty', !filled);
  btn.innerHTML = filled ? '&#9998; Description <span class="chip-ok" aria-hidden="true">&#10003;</span>' : '&#9998; Add description';
  btn.title = filled ? input.value : 'Add a short description (shown in the question bank)';
}

/* ---- Description dialog ---- */
function openDescriptionModal() {
  const modal = document.getElementById('editor-desc-modal');
  const area = document.getElementById('editor-desc-textarea');
  area.value = document.getElementById('case-desc-input').value;
  updateDescriptionCount();
  modal.classList.remove('hidden');
  area.focus();
  area.setSelectionRange(area.value.length, area.value.length);
}

function closeEditorModal(id) {
  document.getElementById(id).classList.add('hidden');
  const opener = id === 'editor-desc-modal' ? 'editor-desc-btn' : 'editor-more-btn';
  const btn = document.getElementById(opener);
  if (btn) btn.focus();
}

function updateDescriptionCount() {
  const n = document.getElementById('editor-desc-textarea').value.length;
  document.getElementById('editor-desc-count').textContent = `${n} character${n === 1 ? '' : 's'}`;
}

function applyDescription() {
  const input = document.getElementById('case-desc-input');
  const value = document.getElementById('editor-desc-textarea').value.replace(/\s*\n\s*/g, ' ').trim();
  if (value !== input.value) {
    input.value = value;
    currentCase.description = value;
    setEditorDirty(true);
  }
  refreshDescriptionChip();
  closeEditorModal('editor-desc-modal');
}

/* ---- Ready for students (the same rule as the question bank's Status column) ---- */
function currentEditorProblems() {
  if (!currentCase) return [];
  return itemProblems(typeof buildPreviewItem === 'function' ? buildPreviewItem() : currentCase);
}

function refreshReadyChip() {
  const btn = document.getElementById('editor-ready-btn');
  if (!btn || !currentCase) return;
  const problems = currentEditorProblems();
  const others = problems.filter(p => p !== 'marked as draft');
  btn.classList.remove('is-ready', 'is-hidden');
  if (!problems.length) {
    btn.classList.add('is-ready');
    btn.innerHTML = '&#10003; Ready for students';
  } else {
    btn.classList.add('is-hidden');
    btn.innerHTML = others.length
      ? `&#9888; ${others.length} problem${others.length === 1 ? '' : 's'}`
      : '&#9888; Draft: hidden';
  }
  btn.title = problems.length ? `Hidden from students: ${problems.join('; ')}` : 'Students can see this item';
  const pop = document.getElementById('editor-ready-pop');
  if (pop && !pop.classList.contains('hidden')) renderReadyPopover();
}

function scheduleReadyChip() {
  clearTimeout(readyChipTimer);
  readyChipTimer = setTimeout(refreshReadyChip, 400);
}

function renderReadyPopover() {
  const pop = document.getElementById('editor-ready-pop');
  const problems = currentEditorProblems();
  const noun = currentCase.isStandalone ? 'question' : 'case';
  if (!problems.length) {
    pop.innerHTML = `<p class="ready-pop-head ok">&#10003; Ready for students</p>
      <p class="ready-pop-note">Every screen has a question and a complete answer key, so students can see this ${noun} once it is saved.</p>`;
    return;
  }
  const items = problems.map(p => {
    if (p === 'marked as draft') {
      return `<li><span>Marked as a draft</span><button type="button" class="ready-pop-action" data-ready-action="undraft">Show to students</button></li>`;
    }
    const m = /^screen (\d+): (.*)$/.exec(p);
    if (m && !currentCase.isStandalone) {
      return `<li><button type="button" class="ready-pop-screen" data-ready-screen="${Number(m[1]) - 1}">Screen ${m[1]}</button><span>${escapeHTML(m[2])}</span></li>`;
    }
    return `<li><span>${escapeHTML(m ? m[2] : p)}</span></li>`;
  }).join('');
  pop.innerHTML = `<p class="ready-pop-head">Hidden from students</p>
    <ul class="ready-pop-list">${items}</ul>
    <p class="ready-pop-note">Checked against your edits on this page. Fix these, save, and students will see this ${noun}.</p>`;
}

function setReadyPopover(open) {
  const pop = document.getElementById('editor-ready-pop');
  const btn = document.getElementById('editor-ready-btn');
  if (!pop || !btn) return;
  if (open) renderReadyPopover();
  pop.classList.toggle('hidden', !open);
  btn.setAttribute('aria-expanded', open ? 'true' : 'false');
}

function setEditorMoreMenu(open) {
  const menu = document.getElementById('editor-more-menu');
  const btn = document.getElementById('editor-more-btn');
  if (!menu || !btn) return;
  menu.classList.toggle('hidden', !open);
  btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  if (open) menu.querySelector('button').focus();
}

function initEditorHeader() {
  const view = document.getElementById('editor-view');
  ['case-course-select', 'case-unit-select'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', () => setTimeout(refreshMetaChips));
  });

  // Description dialog
  document.getElementById('editor-desc-btn').addEventListener('click', openDescriptionModal);
  document.getElementById('editor-desc-textarea').addEventListener('input', updateDescriptionCount);
  document.getElementById('editor-desc-textarea').addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); applyDescription(); }
  });
  document.getElementById('editor-desc-done').addEventListener('click', applyDescription);
  document.getElementById('editor-desc-cancel').addEventListener('click', () => closeEditorModal('editor-desc-modal'));

  // Keyboard shortcuts dialog
  document.getElementById('editor-shortcuts-btn').addEventListener('click', () => {
    setEditorMoreMenu(false);
    document.getElementById('editor-shortcuts-modal').classList.remove('hidden');
    document.getElementById('editor-shortcuts-close').focus();
  });
  document.getElementById('editor-shortcuts-close').addEventListener('click', () => closeEditorModal('editor-shortcuts-modal'));

  // A click on the dimmed background closes either dialog (the description is not changed).
  document.querySelectorAll('.editor-modal-overlay').forEach(overlay => {
    overlay.addEventListener('mousedown', e => { if (e.target === overlay) closeEditorModal(overlay.id); });
  });

  // ⋯ menu
  const moreBtn = document.getElementById('editor-more-btn');
  const moreMenu = document.getElementById('editor-more-menu');
  moreBtn.addEventListener('click', () => setEditorMoreMenu(moreMenu.classList.contains('hidden')));
  moreMenu.addEventListener('click', e => {
    if (!e.target.closest('button')) return;
    setEditorMoreMenu(false);
    if (e.target.closest('[data-theme-toggle]')) setTimeout(refreshEditorHeader);
  });
  moreMenu.addEventListener('keydown', e => {
    const items = Array.from(moreMenu.querySelectorAll('button'));
    const i = items.indexOf(document.activeElement);
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      items[(i + (e.key === 'ArrowDown' ? 1 : items.length - 1)) % items.length].focus();
    }
  });
  document.getElementById('editor-copy-link-btn').addEventListener('click', () => {
    if (!currentCase) return;
    copyStudentLink(currentCase.isStandalone ? 'standalone' : 'cases', currentCase);
    if (!isReadyForStudents(currentCase)) showToast('Students can open the link once this item is ready for students and saved.', 'warning');
  });

  // Ready for students
  const readyBtn = document.getElementById('editor-ready-btn');
  const readyPop = document.getElementById('editor-ready-pop');
  readyBtn.addEventListener('click', () => setReadyPopover(readyPop.classList.contains('hidden')));
  readyPop.addEventListener('click', e => {
    const screen = e.target.closest('[data-ready-screen]');
    if (screen) {
      setReadyPopover(false);
      if (!saveCurrentStepData()) return;
      renderEditorStep(Number(screen.dataset.readyScreen));
      return;
    }
    if (e.target.closest('[data-ready-action="undraft"]')) {
      delete currentCase.draft;
      setEditorDirty(true);
      refreshReadyChip();
      renderReadyPopover();
    }
  });

  document.addEventListener('mousedown', e => {
    if (!e.target.closest('.editor-more-wrap')) setEditorMoreMenu(false);
    if (!e.target.closest('.editor-ready-wrap')) setReadyPopover(false);
  });

  // Edits anywhere may change readiness.
  ['input', 'change', 'click'].forEach(type => view.addEventListener(type, scheduleReadyChip));

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      const open = document.querySelector('.editor-modal-overlay:not(.hidden)');
      if (open) { e.preventDefault(); closeEditorModal(open.id); return; }
      if (!moreMenu.classList.contains('hidden')) { setEditorMoreMenu(false); moreBtn.focus(); }
      if (!readyPop.classList.contains('hidden')) { setReadyPopover(false); readyBtn.focus(); }
    }
    if ((e.ctrlKey || e.metaKey) && !e.altKey && !e.shiftKey && (e.key === 's' || e.key === 'S') && isEditorOpen()) {
      e.preventDefault();
      document.getElementById('editor-save-btn').click();
    }
  });

  // Keeps "Saved · 3 min ago" current.
  setInterval(() => { if (isEditorOpen()) renderSaveStatus(); }, 30000);
}
