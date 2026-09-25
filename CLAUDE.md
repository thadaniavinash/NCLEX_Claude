# CLAUDE.md

Context for working on **NCLEX_Claude**: an experimental copy of the NCLEX NGN Case Study Studio
(nursing exam practice: unfolding case studies and stand-alone questions for NURS 1017 / NURS 1021).
The original app lives in `thadaniavinash/NCLEX` with its own Supabase database. **Never modify the
original repo or write to its database.** This repo was copied from the original at commit `a922452`.
Work is committed and pushed directly to `main` here; GitHub Pages serves `main`.

## Hard rules

- **Original database is read-only.** `https://taprukpiubqsckahocaz.supabase.co` may only be read
  (`tools/supabase.js compare-original`). This copy's database is `https://wgnrcopjkylviiyllsgz.supabase.co`.
- **Never lose question data.** Before overwriting the database, run `compare-original`/`download` to see
  what changed. Use `add` for new items, not `upload`. Don't reintroduce anything that can save a partial
  or fallback bank (see the save safeguards below).
- **Medical content must be accurate** and nursing-focused (NCSBN clinical judgment model). Flag anything
  that needs clinician review.
- **Don't put secrets or the user's email in the repo** (public repo). The Supabase publishable keys in the
  code are meant to be public; the secret key lives only in the GitHub secret `SUPABASE_SECRET_KEY`.
- Before each push: run the checks below, and stamp versions with `python3 tools/bump_version.py` after
  changing any `.js`, `.css` or `cases-data.js`.

## Layout

- `index.html` + `style.css`: single-page app with views: student portal (session builder), player,
  results, authoring dashboard + editor.
- `js/` (plain scripts sharing one global scope, loaded in this order; `main.js` last):
  `state.js` (constants, state, IndexedDB), `utils.js` (toast, escapeHTML, nurses' notes formatting,
  shuffleArray), `data.js` (sanitizing, format migrations, load, readiness rule, saving),
  `auth.js` (Supabase Auth admin sign-in), `dashboard.js` (authoring tables, admin login UI),
  `session-builder.js`, `editor.js` (+ table cell menu), `player.js`, `scoring.js`, `results.js`,
  `calculator.js`, `main.js` (initApp, routing).
- `cases-data.js`: backup of the question bank (`window.NCLEX_CASES`, `window.NCLEX_STANDALONE`), loaded
  when the database can't be reached. Read/write it losslessly with `tools/bank.py` (Python) or
  `tools/supabase.js` (Node). Keep it in sync via the workflow's `download` action.
- `drafts/`: case studies being written (the DMD case's generator `build_unit3_case4.py` lives here).
- `supabase/setup.sql` (table), `supabase/002_admin_logins.sql` (version column + trigger, `nclex_admins`,
  `is_nclex_admin()`, admin-only update policy).
- `server.js` + `*.bat`: optional local Windows server (`/api/save` writes `cases-data.js`).
- `.github/workflows/supabase.yml`: runs `tools/supabase.js` from GitHub Actions (ping daily; manual:
  check, compare-original, download (commits the backup), add, upload).

## Data format (one item = case study or stand-alone question)

`{ id, title, course, unit, topic, disorder, description, isStandalone?, screens: [...] }`.
IDs: `case_<13 digits>` / `standalone_<13 digits>`; NURS 1017 cases use `case_17823<unit>000<n>`
(for example Unit 3 Case 4 = `case_1782370000004`). `topic` and `disorder` currently equal `unit`; units are listed in
`CURRICULUM_COURSES` (`js/state.js`). Case studies have 6 screens following the clinical judgment steps
(recognize cues, analyze cues, prioritize hypotheses, generate solutions, take action, evaluate outcomes).

Each screen: `{ step, leftContent: { intro, tabs: [{ id, title, content(HTML) }] }, question }`.
Nurses' notes rows: `<p class="nurse-note-row"><span class="nurse-note-time">1400:</span><span class="nurse-note-text">...</span></p>`
(time labels may be `HHMM` or `HHMM (qualifier)`). Tables use the inline-styled `nclex-editor-table` markup
seen in existing cases. Rationale (`explanation`) is HTML; use `<br>`, not `\n`.

Question types (`question.type`) and their answer keys:
- `select_all`, `trend`, `multiple_choice`, `select_n` (`limit`): `options: [{ text, correct }]`
- `matrix_mc` (`matrix.rows[].correctIndex`), `matrix_mr` (`rows[].correctIndices`); `matrix.columns`,
  `matrix.firstColumnHeader`
- `dropdown_cloze`, `dyad`, `triad`: `cloze: { text: "... [[drop0]] ...", dropdowns: [{ placeholder, options: [{ text, correct }] }] }`
  (the legacy `dropdown_cloze: {sentences, dropdowns}` shape is converted on load; don't author it)
- `highlight`, `highlight_2`: `highlightTabs: [{ id, title, content }]` with `{phrase|correct}` / `{phrase}` markup
- `bowtie`: `bowtieActions` (2 correct), `bowtieConditions` (1), `bowtieParams` (2)
- `ordered_response`: `orderedOptions` in the correct order (the player shuffles)
Content conventions: never list correct answers first (shuffle options; if a rationale refers to option
numbers, write "(Option N)" to match); don't number rationale points in a way that looks like option numbers.

## Saving and sign-in (how it works)

- Load: database (`select=*`) → if unreachable or empty, fall back to `cases-data.js` and set
  `isDatabaseUnavailable` (saving refused). `?cases=`/`?standalone=` links filter the bank and set
  `isBankFiltered` (saving refused). Content is sanitized on load (`sanitizeItemContent`).
- Save (`saveBankToStorage` in `data.js`): needs a signed-in admin (`getAdminAccessToken`). PATCH with
  `version=eq.<loaded version>` and `Prefer: return=representation`; on conflict, fetch latest, merge this
  page's changes (`mergeBankChanges`), retry. Works without the version column too.
- Readiness (`isReadyForStudents`, `itemProblems` in `data.js`): items with missing stems or incomplete
  answer keys are hidden from students (session builder, direct links) and badged in the dashboard.

## Checks (serve the repo first: `python3 -m http.server 8765`)

- `node tools/check.js`: every question renders, its answer key scores full marks, the editor's
  open-and-save changes nothing. Expected: 0 failures, 4 known incomplete items.
- `node tools/check-saving.js`: sign-in and saving against a simulated Supabase (13 checks).
- Playwright is preinstalled (global npm); Chromium at `/opt/pw-browsers`. Block `*.supabase.co` in
  tests so nothing is written.
- In earlier sessions this container could not reach `*.supabase.co` (proxy) or github.io; reach the
  database through the GitHub Actions workflow (trigger via the GitHub MCP tools, read job logs).

## User decisions so far

- Keep `files/ECG1.jpg`. Keep the incomplete items (two empty "New Case Study", empty "New Stand-alone
  Question", Bowtie-Stroke without correct parameters, Case Study 1 (cardio) with a blank correct
  drop-down option); they are hidden from students until the author finishes them.
- Select-all options were shuffled and rationales relabeled "(Option N)" at the user's request.
- The DMD case (NURS 1017 Unit 3 Case Study 4) is in the bank; its medical content still merits
  clinician review.
- UI/UX work was deliberately deferred until the code fixes were done; it is the next phase.

## Pending setup (user's side; check the README "Administrators" section)

Until these are done, anyone with the public key can still write the database:
1. Create the admin user (Supabase Authentication → Users, auto-confirm).
2. Disable public email sign-ups.
3. Run `supabase/002_admin_logins.sql` with the admin email filled in.
4. Add the `SUPABASE_SECRET_KEY` repository secret (needed by the workflow's add/upload after step 3).
The old hard-coded admin password is still in git history; the user was told to change it if reused.

## Remaining code work (from the latest review)

1. Test Mode says "Timed Exam Conditions" but there is no timer.
2. Student results/progress are never saved (would need student accounts + a results table).
3. Finish or remove the 5 hidden items (content decisions).
4. Whole bank saved per row (over 1 MB); one row per item would shrink saves and merges.
5. Images are embedded as base64 in the data; move to Supabase Storage.
6. Browser-storage copy (IndexedDB/localStorage) is written on save but not read when the database works.
7. Editor relies on the deprecated `document.execCommand`.
8. `alert()` used for errors in editor/player; replace with in-page messages.
9. Data fields: `disorder` duplicates `unit`; `availability` unused; "Others" items use old naming.
10. CSS: 79 unused classes, 22 duplicated rule blocks, 113 `!important` (do during the redesign).
11. Accessibility: almost no ARIA labels; drag-and-drop questions lack keyboard support.
12. Run `check.js`/`check-saving.js` in CI on every push.
13. The workflow's actions run on Node 20, which GitHub is deprecating.

## UI/UX ideas (next phase; user to pick where to start, 1-3 suggested first)

1. Simplify the Session Builder into a guided flow (mode, topics, count, start) with quick-start and resume.
2. Mobile-friendly player: chart and question as tabs/drawer instead of stacked.
3. Clearer feedback: per-option ✓/✗ against the student's choice.
4. Structured rationales ("why correct/incorrect" per option, collapsible).
5. A real Test Mode timer with warnings and per-question timing.
6. Student progress dashboard (by unit and clinical judgment step, retry missed questions).
7. Results page broken down by clinical judgment step, with review of wrong answers.
8. Better chart readability (timestamped notes, trend highlighting, new-tab markers as the case unfolds).
9. Calculator and navigator as docked panels with keyboard shortcuts.
10. Authoring preview side by side with live validation.
11. Authoring templates and "duplicate case".
12. Consistent design system (tokens, spacing, type, dark mode, touch targets).
13. Accessibility (keyboard, screen readers, focus, colour-blind-safe states, text resize).
14. Inline messages instead of alerts/toasts for important information.
15. Instructor tools (assign sets, share links, class results).
16. Studio search/filter by topic, type, status, last edited; bulk actions.
17. Faster loading (skeletons, lazy images, offline/backup banner).
