/* Sentence editor for drop-down cloze, drag-and-drop cloze, dyad and triad questions.

   The author writes the whole sentence in one box and inserts drop-downs where the blanks go. Each
   blank is a chip in the text; its choices are edited in the card below the sentence, and a preview
   shows the sentence as students see it and as it reads with the correct answers. The data stays in
   the existing shape: cloze.text with [[dropN]] markers (numbered in sentence order) and
   cloze.dropdowns[N] = { placeholder, options: [{ text, correct }] }. */

const CLOZE_REQUIRED_BLANKS = { dyad: 2, triad: 3 };
const CLOZE_DEFAULT_TEXT = {
  dyad: 'The client is most likely experiencing [[drop0]] as evidenced by [[drop1]].',
  triad: 'The client is at highest risk for [[drop0]] as evidenced by [[drop1]] and [[drop2]].',
  dropdown_cloze: 'The nurse should first [[drop0]] because the client [[drop1]].',
  drag_drop_cloze: 'The nurse should first [[drop0]] because the client [[drop1]].'
};

// A new blank has three empty choices and no correct one yet, so the author picks it on purpose
// (and the readiness check keeps the question from students until they do).
function newClozeBlank() {
  return { placeholder: 'Select...', options: [{ text: '', correct: false }, { text: '', correct: false }, { text: '', correct: false }] };
}

function renderClozeSentenceEditor(q, box) {
  if (!q.cloze) q.cloze = { text: '', dropdowns: [] };
  const c = q.cloze;
  if (!Array.isArray(c.dropdowns)) c.dropdowns = [];
  const required = CLOZE_REQUIRED_BLANKS[q.type] || 0;
  const blankByKey = new Map(); // chip key -> dropdown object
  let nextKey = 0;

  const wrapper = document.createElement('div');
  wrapper.className = 'cloze-editor';
  wrapper.innerHTML = `
    <div class="cloze-warning">${required
      ? `A ${q.type} has exactly ${required} drop-downs, and students earn the point only when all ${required} are correct.`
      : 'Write the sentence, then put the cursor where a blank goes and click Insert drop-down.'}</div>
    <div class="form-group">
      <label>Sentence</label>
      <div class="cloze-sentence-toolbar">
        <button type="button" class="btn btn-secondary btn-xs cloze-insert-btn">+ Insert drop-down at cursor</button>
        <span class="cloze-blank-count"></span>
      </div>
      <div class="cloze-sentence-editor" contenteditable="true" role="textbox" aria-multiline="true" aria-label="Sentence with drop-downs"></div>
      <p class="cloze-sentence-help">Click a drop-down in the sentence to edit its choices. Delete it like a word with Backspace.</p>
    </div>
    <div class="cloze-blank-cards"></div>
    <div class="cloze-preview">
      <div class="cloze-preview-title">Student view</div>
      <div class="cloze-preview-student"></div>
      <div class="cloze-preview-title">Reads with the correct answers</div>
      <div class="cloze-preview-key"></div>
    </div>`;
  box.appendChild(wrapper);

  const sentence = wrapper.querySelector('.cloze-sentence-editor');
  const cards = wrapper.querySelector('.cloze-blank-cards');
  const insertBtn = wrapper.querySelector('.cloze-insert-btn');
  const countEl = wrapper.querySelector('.cloze-blank-count');

  const chipHtml = (dd) => {
    const key = `b${nextKey++}`;
    blankByKey.set(key, dd);
    return `<span class="cloze-chip" contenteditable="false" data-key="${key}" tabindex="0" role="button"></span>`;
  };

  // Sentence text -> editor HTML with chips.
  sentence.innerHTML = (c.text || '').replace(/\[\[d(?:r)?op(\d+)\]\]/gi, (m, n) => {
    const idx = parseInt(n, 10);
    if (!c.dropdowns[idx]) c.dropdowns[idx] = newClozeBlank();
    return chipHtml(c.dropdowns[idx]);
  });

  const chips = () => Array.from(sentence.querySelectorAll('.cloze-chip'));
  const correctText = dd => { const o = (dd.options || []).find(x => x.correct); return o ? o.text : ''; };

  // Editor -> cloze.text and cloze.dropdowns, numbered in sentence order.
  const sync = () => {
    const list = chips();
    const oldIndex = new Map(c.dropdowns.map((dd, i) => [dd, i]));
    const ordered = list.map(chip => blankByKey.get(chip.dataset.key));
    const clone = sentence.cloneNode(true);
    Array.from(clone.querySelectorAll('.cloze-chip')).forEach((chip, i) => chip.replaceWith(document.createTextNode(`[[drop${i}]]`)));
    c.text = clone.innerHTML.replace(/(<br\s*\/?>\s*)+$/i, '').replace(/^(\s|&nbsp;)+|(\s|&nbsp;)+$/g, '');
    if (Array.isArray(c.scoreGroups)) {
      const newIndex = new Map(ordered.map((dd, i) => [oldIndex.get(dd), i]));
      c.scoreGroups = c.scoreGroups.map(g => g.map(i => newIndex.get(i)).filter(i => i !== undefined)).filter(g => g.length > 1);
    }
    c.dropdowns = ordered;
    refresh();
  };

  const refresh = () => {
    const list = chips();
    list.forEach((chip, i) => {
      const dd = blankByKey.get(chip.dataset.key);
      const answer = correctText(dd);
      chip.innerHTML = `<span class="cloze-chip-num">${i + 1}</span>${answer ? escapeHTML(answer) : '<em>choose answer</em>'}`;
      chip.setAttribute('aria-label', `Drop-down ${i + 1}${answer ? ': ' + answer : ', no correct answer yet'}. Press Enter to edit its choices.`);
    });
    countEl.textContent = required
      ? `${list.length} of ${required} drop-downs${list.length !== required ? ` (needs exactly ${required})` : ''}`
      : `${list.length} drop-down${list.length === 1 ? '' : 's'}`;
    countEl.classList.toggle('is-wrong', required ? list.length !== required : list.length === 0);
    insertBtn.disabled = !!required && list.length >= required;
    renderPreview();
  };

  const renderPreview = () => {
    let i = 0;
    const student = (c.text || '').replace(/\[\[d(?:r)?op\d+\]\]/gi, () => {
      const dd = c.dropdowns[i++] || {};
      return `<select disabled class="cloze-preview-select"><option>${escapeHTML(dd.placeholder || 'Select...')}</option></select>`;
    });
    i = 0;
    const key = (c.text || '').replace(/\[\[d(?:r)?op\d+\]\]/gi, () => {
      const answer = correctText(c.dropdowns[i++] || {});
      return answer ? `<strong class="cloze-preview-answer">${escapeHTML(answer)}</strong>` : '<strong class="cloze-preview-missing">[no correct answer]</strong>';
    });
    wrapper.querySelector('.cloze-preview-student').innerHTML = student || '<em>Empty sentence</em>';
    wrapper.querySelector('.cloze-preview-key').innerHTML = key || '<em>Empty sentence</em>';
  };

  const renderCards = (focusIndex) => {
    cards.innerHTML = '';
    c.dropdowns.forEach((dd, idx) => {
      if (!Array.isArray(dd.options)) dd.options = [];
      const card = document.createElement('div');
      card.className = 'cloze-dropdown-card';
      card.dataset.index = idx;
      card.innerHTML = `
        <div class="cloze-card-head">
          <span class="cloze-chip-num">${idx + 1}</span>
          <strong>Drop-down ${idx + 1}</strong>
          <label class="cloze-placeholder-label">Placeholder
            <input type="text" class="form-control cloze-placeholder-input" value="${escapeHTML(dd.placeholder || 'Select...')}">
          </label>
        </div>
        <div class="cloze-choices"></div>
        <div class="cloze-card-warning" role="status"></div>
        <div class="cloze-card-actions">
          <button type="button" class="btn btn-text btn-xs cloze-add-choice">+ Add choice</button>
          <button type="button" class="btn btn-text btn-xs cloze-paste-toggle">Paste several choices</button>
          <button type="button" class="btn btn-text btn-xs cloze-shuffle" title="Mix the order so the correct answer is not first">Shuffle order</button>
        </div>
        <div class="cloze-paste hidden">
          <textarea class="form-control cloze-paste-input" rows="4" placeholder="One choice per line"></textarea>
          <button type="button" class="btn btn-secondary btn-xs cloze-paste-apply">Add these choices</button>
        </div>`;
      const choices = card.querySelector('.cloze-choices');
      const warn = card.querySelector('.cloze-card-warning');

      const updateWarning = () => {
        const opts = dd.options;
        const nCorrect = opts.filter(o => o.correct).length;
        let msg = '';
        if (nCorrect !== 1) msg = 'Mark exactly one correct choice.';
        else if (opts.some(o => !hasText(o.text))) msg = 'Fill in or delete the empty choices.';
        else if (opts.length > 1 && opts[0].correct) msg = 'The correct choice is listed first, where students may spot it. Use Shuffle order.';
        warn.textContent = msg;
        warn.classList.toggle('hidden', !msg);
      };

      const renderChoices = (focusChoice) => {
        choices.innerHTML = '';
        dd.options.forEach((opt, oIdx) => {
          const row = document.createElement('div');
          row.className = 'option-config-row cloze-choice-row';
          row.innerHTML = `
            <input type="radio" name="cloze-correct-${idx}" class="choice-correct-toggle" ${opt.correct ? 'checked' : ''} aria-label="Choice ${oIdx + 1} is correct" title="Correct answer">
            <input type="text" class="option-text-input form-control" value="${escapeHTML(opt.text || '')}" placeholder="Choice ${oIdx + 1}" aria-label="Drop-down ${idx + 1}, choice ${oIdx + 1}">
            <button type="button" class="btn-option-delete" aria-label="Delete choice ${oIdx + 1}" title="Delete choice">&times;</button>`;
          const text = row.querySelector('.option-text-input');
          text.addEventListener('input', () => { opt.text = text.value; updateWarning(); refresh(); });
          text.addEventListener('keydown', e => {
            if (e.key !== 'Enter') return;
            e.preventDefault();
            if (oIdx === dd.options.length - 1) { dd.options.push({ text: '', correct: false }); renderChoices(oIdx + 1); }
            else choices.querySelectorAll('.option-text-input')[oIdx + 1].focus();
          });
          row.querySelector('.choice-correct-toggle').addEventListener('change', () => {
            dd.options.forEach((o, oi) => { o.correct = oi === oIdx; });
            updateWarning(); refresh();
          });
          row.querySelector('.btn-option-delete').addEventListener('click', () => {
            dd.options.splice(oIdx, 1);
            renderChoices(); refresh();
          });
          choices.appendChild(row);
        });
        updateWarning();
        if (typeof focusChoice === 'number') {
          const input = choices.querySelectorAll('.option-text-input')[focusChoice];
          if (input) input.focus();
        }
      };

      card.querySelector('.cloze-placeholder-input').addEventListener('input', e => { dd.placeholder = e.target.value; renderPreview(); });
      card.querySelector('.cloze-add-choice').addEventListener('click', () => { dd.options.push({ text: '', correct: false }); renderChoices(dd.options.length - 1); });
      card.querySelector('.cloze-paste-toggle').addEventListener('click', () => {
        const paste = card.querySelector('.cloze-paste');
        paste.classList.toggle('hidden');
        if (!paste.classList.contains('hidden')) paste.querySelector('textarea').focus();
      });
      card.querySelector('.cloze-paste-apply').addEventListener('click', () => {
        const lines = card.querySelector('.cloze-paste-input').value.split(/\r?\n/).map(l => l.replace(/^\s*(?:[-•*]|\d+[.)])\s*/, '').trim()).filter(Boolean);
        if (!lines.length) return;
        dd.options = dd.options.filter(o => hasText(o.text)).concat(lines.map(text => ({ text, correct: false })));
        card.querySelector('.cloze-paste-input').value = '';
        card.querySelector('.cloze-paste').classList.add('hidden');
        renderChoices(); refresh();
      });
      card.querySelector('.cloze-shuffle').addEventListener('click', () => {
        if (dd.options.length < 2) return;
        let shuffled;
        do { shuffled = shuffleArray(dd.options); } while (shuffled[0].correct && shuffled.some(o => !o.correct));
        dd.options = shuffled;
        renderChoices(); refresh();
      });

      renderChoices();
      cards.appendChild(card);
    });
    if (typeof focusIndex === 'number') focusCard(focusIndex);
  };

  const focusCard = (idx) => {
    const card = cards.querySelector(`.cloze-dropdown-card[data-index="${idx}"]`);
    if (!card) return;
    card.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    card.classList.add('is-focused');
    setTimeout(() => card.classList.remove('is-focused'), 1200);
    const firstEmpty = Array.from(card.querySelectorAll('.option-text-input')).find(i => !i.value) || card.querySelector('.option-text-input');
    if (firstEmpty) firstEmpty.focus();
  };

  // Typing in the sentence (including deleting a chip) renumbers the blanks.
  sentence.addEventListener('input', () => {
    const before = c.dropdowns.length;
    sync();
    if (c.dropdowns.length !== before) renderCards();
  });
  sentence.addEventListener('paste', e => {
    e.preventDefault();
    document.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain'));
  });
  sentence.addEventListener('click', e => {
    const chip = e.target.closest('.cloze-chip');
    if (chip) focusCard(chips().indexOf(chip));
  });
  sentence.addEventListener('keydown', e => {
    const chip = e.target.closest && e.target.closest('.cloze-chip');
    if (chip && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); focusCard(chips().indexOf(chip)); }
    if (e.key === 'Enter' && !chip) e.preventDefault(); // one sentence, no line breaks
  });

  insertBtn.addEventListener('mousedown', e => e.preventDefault()); // keep the cursor in the sentence
  insertBtn.addEventListener('click', () => {
    const dd = newClozeBlank();
    const holder = document.createElement('span');
    holder.innerHTML = chipHtml(dd);
    const chip = holder.firstChild;
    const sel = window.getSelection();
    if (sel.rangeCount && sentence.contains(sel.getRangeAt(0).commonAncestorContainer)) {
      const range = sel.getRangeAt(0);
      range.deleteContents();
      range.insertNode(document.createTextNode(' '));
      range.insertNode(chip);
      range.insertNode(document.createTextNode(' '));
    } else {
      sentence.appendChild(document.createTextNode(' '));
      sentence.appendChild(chip);
    }
    sync();
    renderCards(chips().indexOf(chip));
  });

  refresh();
  renderCards();
}
