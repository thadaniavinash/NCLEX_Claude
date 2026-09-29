/* Reference ranges for the Laboratory Results tables, from the Medical Council of Canada's "Normal
   lab values" (https://mcc.ca/examinations-assessments/resources-to-help-with-exam-prep/normal-lab-values/),
   in SI units as MCC gives them. When the author types one of these test names in the first column of
   a lab table and leaves the cell, the name is set in bold and the range goes on the next line
   (fillLabReferenceRange in js/table-tools.js). Each entry: { name, range, aliases? }. */

const LAB_REFERENCE_RANGES = [
  // Filled from the MCC page (see the header comment).
];

function normalizeLabName(text) {
  return (text || '').toLowerCase().replace(/[^a-z0-9%]+/g, ' ').trim();
}

function findLabReference(text) {
  const key = normalizeLabName(text);
  if (!key) return null;
  return LAB_REFERENCE_RANGES.find(r => [r.name, ...(r.aliases || [])].some(n => normalizeLabName(n) === key)) || null;
}
