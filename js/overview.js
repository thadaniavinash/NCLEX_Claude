/* Authoring studio: Overview page (the state of the question bank). Everything here is worked out from
   the bank itself; student results never leave students' browsers, so there are no class reports. */

function renderOverview() {
  const box = document.getElementById('overview-content');
  if (!box) return;
  const all = caseStudies.concat(standaloneQuestions);
  const visibleCases = studentCaseStudies();
  const visibleSingles = studentStandaloneQuestions();
  const needsWork = all.filter(i => !isReadyForStudents(i));
  const monthAgo = Date.now() - 30 * 24 * 3600 * 1000;
  const recentlyEdited = all.filter(i => i.updatedAt && Date.parse(i.updatedAt) >= monthAgo)
    .sort((a, b) => String(b.updatedAt).localeCompare(String(a.updatedAt)));

  const tiles = [
    { label: 'Case studies', value: caseStudies.length, sub: `${visibleCases.length} visible to students` },
    { label: 'Stand-alone questions', value: standaloneQuestions.length, sub: `${visibleSingles.length} visible to students` },
    { label: 'Hidden from students', value: needsWork.length, sub: needsWork.length ? 'unfinished or drafts' : 'everything is published', tone: needsWork.length ? 'warn' : '' },
    { label: 'Edited in the last 30 days', value: recentlyEdited.length, sub: recentlyEdited.length ? `latest ${relativeTime(recentlyEdited[0].updatedAt)}` : 'no recent edits' }
  ];

  const kindTag = item => `<span class="kind-tag${item.isStandalone ? '' : ' case'}">${item.isStandalone ? 'Stand-alone' : 'Case study'}</span>`;
  const openLabel = canEditBank() ? 'Edit' : 'Preview';
  const itemRow = (item, detail) => `
      <li class="app-list-row">
        <span class="app-list-main"><strong>${escapeHTML(item.title || 'Untitled')}</strong>
          <span class="muted">${kindTag(item)} ${detail}</span></span>
        <button type="button" class="app-btn small" data-open-item="${escapeHTML(item.id)}">${openLabel}</button>
      </li>`;

  const attention = needsWork.map(i => itemRow(i, escapeHTML(itemProblems(i).join('; ')))).join('');
  const edited = recentlyEdited.slice(0, 6).map(i => itemRow(i, `${escapeHTML(unitParts(i.unit || i.topic).num)} · edited ${escapeHTML(relativeTime(i.updatedAt))}`)).join('');

  // Coverage: every curriculum unit, including the ones with nothing yet (counts are items students can see).
  const countIn = (list, course, unit) => list.filter(i => (i.course || 'Others') === course && (i.unit || i.topic || 'Others') === unit).length;
  const coverageRows = Object.entries(CURRICULUM_COURSES).flatMap(([course, units]) => units.map(unit => ({ course, unit })))
    .concat([{ course: 'Others', unit: 'Others' }])
    .map(({ course, unit }) => {
      const c = countIn(visibleCases, course, unit);
      const s = countIn(visibleSingles, course, unit);
      const hidden = countIn(needsWork, course, unit);
      const cell = n => n ? n : '<span class="muted" aria-label="none">–</span>';
      return `<tr class="${c + s === 0 ? 'is-gap' : ''}"><th scope="row">${unitLabelHTML(course, unit)}</th>
        <td class="num">${cell(c)}</td><td class="num">${cell(s)}</td><td class="num muted">${hidden || ''}</td></tr>`;
    }).join('');

  const typeCounts = {};
  visibleSingles.forEach(q => {
    const t = (q.screens && q.screens[0] && q.screens[0].question && q.screens[0].question.type) || 'unknown';
    typeCounts[t] = (typeCounts[t] || 0) + 1;
  });
  const typeMax = Math.max(1, ...Object.values(typeCounts));
  const typeRows = Object.entries(typeCounts).sort((a, b) => b[1] - a[1]).map(([t, n]) => `
      <tr><th scope="row">${escapeHTML(getQuestionTypeLabel(t) || t)}</th>
        <td class="bar"><span class="meter" role="img" aria-label="${n} questions"><span class="meter-fill" style="width:${Math.round(n / typeMax * 100)}%"></span></span></td>
        <td class="num">${n}</td></tr>`).join('');

  box.innerHTML = `
    <div class="stat-grid">${tiles.map(t => `
      <div class="stat-tile${t.tone ? ' tone-' + t.tone : ''}"><span class="stat-label">${t.label}</span><span class="stat-value">${t.value}</span><span class="stat-sub">${t.sub}</span></div>`).join('')}
    </div>

    <div class="app-grid-2">
      <section class="app-card" aria-labelledby="overview-attention-title">
        <div class="app-card-head">
          <div><h2 id="overview-attention-title" class="app-card-title">Needs attention</h2>
          <p class="app-card-sub">Hidden from students until these are fixed.</p></div>
          <button type="button" class="app-btn small" data-goto-bank="hidden">Show in question bank</button>
        </div>
        ${attention ? `<ul class="app-list">${attention}</ul>` : '<p class="app-card-sub">Every item is ready for students.</p>'}
      </section>

      <section class="app-card" aria-labelledby="overview-edited-title">
        <h2 id="overview-edited-title" class="app-card-title">Recently edited</h2>
        ${edited ? `<ul class="app-list">${edited}</ul>` : '<p class="app-card-sub">Nothing edited in the last 30 days.</p>'}
      </section>
    </div>

    <div class="app-grid-2 wide-left">
      <section class="app-card" aria-labelledby="overview-coverage-title">
        <h2 id="overview-coverage-title" class="app-card-title">Coverage by unit</h2>
        <p class="app-card-sub">Items students can see in each unit. Shaded rows have nothing yet.</p>
        <table class="meter-table coverage-table">
          <thead><tr><th scope="col">Unit</th><th scope="col" class="num">Case studies</th><th scope="col" class="num">Stand-alone</th><th scope="col" class="num">Hidden</th></tr></thead>
          <tbody>${coverageRows}</tbody>
        </table>
      </section>

      <section class="app-card" aria-labelledby="overview-types-title">
        <h2 id="overview-types-title" class="app-card-title">Stand-alone question types</h2>
        <p class="app-card-sub">Visible stand-alone questions by type.</p>
        <table class="meter-table">
          <thead><tr><th scope="col">Type</th><th scope="col"><span class="visually-hidden">Bar</span></th><th scope="col" class="num">Count</th></tr></thead>
          <tbody>${typeRows}</tbody>
        </table>
      </section>
    </div>`;
}

function initOverviewEvents() {
  const view = document.getElementById('overview-view');
  if (!view) return;
  view.addEventListener('click', e => {
    const open = e.target.closest('[data-open-item]');
    if (open) {
      const item = findBankItem(open.dataset.openItem);
      if (!item) return;
      if (canEditBank()) startEditor(item);
      else startPlayer(item, { source: 'studio' });
      return;
    }
    const bank = e.target.closest('[data-goto-bank]');
    if (bank) {
      const status = document.getElementById('author-status-filter');
      if (status) status.value = bank.dataset.gotoBank;
      authorStatusFilter = bank.dataset.gotoBank;
      switchView('dashboard');
    }
  });
}
