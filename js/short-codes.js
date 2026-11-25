/* Short codes: a case study or stand-alone question can be opened by typing a code such as "C-7KD4M"
   on the Home page, as well as by its link (links keep working as the backup).

   A code is "C" (case study) or "Q" (stand-alone question), a hyphen, and five characters worked out
   from the item's id, so it never changes when the item is renamed, edited or moved to another unit, and
   nothing is stored in the database. The characters leave out 0, 1, I, L and O, which are easy to
   misread on a slide. Typing is forgiving: any case, with or without the hyphen or the letter.
   Several codes typed together (separated by spaces or commas) open as one session, which is how a set
   of stand-alone questions is shared. tools/check.js fails if two items ever share a code. */

const SHORT_CODE_ALPHABET = '23456789ABCDEFGHJKMNPQRSTUVWXYZ'; // 31 characters
const SHORT_CODE_LENGTH = 5;

function shortCodeBody(id) {
  // FNV-1a, 32 bits
  let h = 0x811c9dc5;
  const s = String(id);
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  const base = SHORT_CODE_ALPHABET.length;
  let n = h % Math.pow(base, SHORT_CODE_LENGTH);
  let out = '';
  for (let i = 0; i < SHORT_CODE_LENGTH; i++) {
    out = SHORT_CODE_ALPHABET[n % base] + out;
    n = Math.floor(n / base);
  }
  return out;
}

function isStandaloneItem(item) {
  return !!(item && (item.isStandalone || String(item.id).startsWith('standalone_')));
}

function itemShortCode(item) {
  return `${isStandaloneItem(item) ? 'Q' : 'C'}-${shortCodeBody(item.id)}`;
}

// code body -> item, over every item (hidden ones too: like links, codes open anything the author shares).
// A body shared by two items maps to null, so neither opens by code (their links still work).
function shortCodeIndex() {
  const index = new Map();
  caseStudies.concat(standaloneQuestions).forEach(item => {
    const body = shortCodeBody(item.id);
    index.set(body, index.has(body) ? null : item);
  });
  return index;
}

// "c-7kd4m", "C7KD4M", "7kd4m" -> the item, or null.
function findItemByShortCode(text) {
  let s = String(text || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
  if (s.length === SHORT_CODE_LENGTH + 1 && (s[0] === 'C' || s[0] === 'Q')) s = s.slice(1);
  if (s.length !== SHORT_CODE_LENGTH) return null;
  return shortCodeIndex().get(s) || null;
}

const LINK_ID_PARAMS = ['case', 'caseId', 'cases', 'id', 'standalone', 'question', 'q'];

// What a student typed or pasted into the Home page's "Open" box: one or more codes, or a link.
// Returns { items, mode (from a link's &mode=test, otherwise null), unknown: [what matched nothing] }.
function parseOpenRequest(text) {
  const items = [];
  const unknown = [];
  let mode = null;
  const add = item => { if (item && !items.includes(item)) items.push(item); };
  const byId = id => findBankItem(id) || caseStudies.concat(standaloneQuestions).find(i => i.id.toLowerCase() === String(id).toLowerCase());

  // "C 7KD4M" and "C - 7KD4M" are one code, not two words.
  const joined = String(text || '').replace(/(^|[\s,;])([CQ])\s*[-–]?\s+([A-Z0-9]{5})(?=$|[\s,;])/gi, '$1$2$3');
  joined.split(/[\s,;]+/).filter(Boolean).forEach(token => {
    if (/[?=/]/.test(token) || /^https?:/i.test(token)) {
      let url = null;
      try { url = new URL(token, window.location.href); } catch (e) { url = null; }
      const ids = url ? LINK_ID_PARAMS.flatMap(p => url.searchParams.getAll(p)).flatMap(v => v.split(',')).filter(Boolean) : [];
      if (url && /^(test|exam)$/i.test(url.searchParams.get('mode') || '')) mode = 'test';
      const found = ids.map(byId).filter(Boolean);
      if (found.length) found.forEach(add); else unknown.push(token);
      return;
    }
    const item = findItemByShortCode(token) || (/^(case|standalone)_\d+$/i.test(token) ? byId(token) : null);
    if (item) add(item); else unknown.push(token);
  });
  return { items, mode, unknown };
}
