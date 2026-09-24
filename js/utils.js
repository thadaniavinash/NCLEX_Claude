/* Small shared helpers: toast messages, HTML escaping and nurses' notes formatting. */

/* ================= TOAST NOTIFICATION UTILITY ================= */
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) reverse forwards';
    toast.addEventListener('animationend', () => toast.remove());
  }, 3000);
}

/* ================= ESCAPING UTILITIES ================= */
function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, 
    tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag)
  );
}

function stripNursesNotesFormatting(html) {
  if (!html) return '';
  const temp = document.createElement('div');
  temp.innerHTML = html;
  
  temp.querySelectorAll('.nurse-note-row').forEach(row => {
    row.classList.remove('nurse-note-row');
    row.style.paddingLeft = '';
    row.style.textIndent = '';
  });
  
  temp.querySelectorAll('.nurse-note-time, .nurse-note-text').forEach(span => {
    const parent = span.parentNode;
    if (parent) {
      while (span.firstChild) {
        parent.insertBefore(span.firstChild, span);
      }
      parent.removeChild(span);
    }
  });
  
  return temp.innerHTML;
}

function formatNursesNotes(html, tabTitle) {
  if (!tabTitle || !/nurse|note|log|progress/i.test(tabTitle)) {
    return html;
  }
  if (!html) return '';

  const temp = document.createElement('div');
  temp.innerHTML = html;

  Array.from(temp.childNodes).forEach(child => {
    // Keep rows that already carry an authored time label such as "0800 (DOL 2)"
    // or "Postoperative Day 4"; re-detecting them would only recognize plain times.
    if (isAuthoredNoteRow(child)) return;

    let nodes = [child];
    if (child.nodeType === Node.ELEMENT_NODE) {
      const holder = document.createElement('div');
      holder.innerHTML = stripNursesNotesFormatting(child.outerHTML);
      nodes = Array.from(holder.childNodes);
      nodes.forEach(n => temp.insertBefore(n, child));
      temp.removeChild(child);
    }
    nodes.forEach(node => formatNoteNode(node, temp));
  });

  return temp.innerHTML;
}

// A note's time label: "0800", "08:00", or a time with a short qualifier such as "0800 (DOL 2)".
const NOTE_TIME_REGEX = /^\s*(\b\d{2}:?\d{2}\b(?:\s*\([^()<>]{1,60}\))?)\s*:\s*(.*)/is;

function isAuthoredNoteRow(node) {
  if (node.nodeType !== Node.ELEMENT_NODE || !node.classList.contains('nurse-note-row') || node.children.length !== 2) return false;
  const [time, text] = node.children;
  const label = time.textContent.replace(/ /g, ' ').trim();
  return time.classList.contains('nurse-note-time') && text.classList.contains('nurse-note-text') &&
    time.children.length === 0 && label.length > 0 && label.length <= 60;
}

function formatNoteNode(child, parent) {
  if (child.nodeType === Node.ELEMENT_NODE) {
    const tagName = child.tagName.toLowerCase();
    if (['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(tagName)) {
      // Strip any existing <b>/<strong> tags around time digits to clean up
      let innerHTML = child.innerHTML.replace(/<\/?(?:strong|b)>/g, '').trim();
      const match = innerHTML.match(NOTE_TIME_REGEX);

      if (match) {
        const rawTime = match[1];
        const restHtml = match[2].trim();
        child.className = 'nurse-note-row';
        child.innerHTML = `<span class="nurse-note-time">${rawTime}:</span><span class="nurse-note-text">${restHtml}</span>`;
      } else {
        child.classList.remove('nurse-note-row');
      }
    }
  } else if (child.nodeType === Node.TEXT_NODE && child.textContent.trim()) {
    const text = child.textContent.trim();
    const match = text.match(NOTE_TIME_REGEX);
    const newP = document.createElement('p');
    if (match) {
      const rawTime = match[1];
      const restText = match[2].trim();
      newP.className = 'nurse-note-row';
      newP.innerHTML = `<span class="nurse-note-time">${escapeHTML(rawTime)}:</span><span class="nurse-note-text">${escapeHTML(restText)}</span>`;
    } else {
      newP.textContent = text;
    }
    parent.replaceChild(newP, child);
  }
}
