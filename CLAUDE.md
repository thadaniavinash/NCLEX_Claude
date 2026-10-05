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

- `index.html` + `style.css`: single-page app. `#app-shell` (top bar + sidebar, bottom tabs on phones) holds
  the student area (Practise = session builder, My progress, results) and the studio area (Overview,
  Question bank); the exam player and the editor fill the window. Routing: `switchView` / `SHELL_VIEWS`
  in `main.js`.
- `js/` (plain scripts sharing one global scope, loaded in this order; `main.js` last):
  `state.js` (constants, state, IndexedDB), `utils.js` (toast, escapeHTML, nurses' notes formatting,
  shuffleArray), `data.js` (sanitizing, format migrations, load, readiness rule, saving),
  `auth.js` (Supabase Auth admin sign-in), `dashboard.js` (authoring tables, admin login UI),
  `session-builder.js`, `rich-text.js` (text box extras), `table-tools.js` (table toolbar, templates,
  cell hints), `lab-ranges.js` (MCC reference ranges for lab tables), `notes-editor.js`, `cloze-editor.js`, `chart-continuity.js` (chart carry-forward rule),
  `editor-preview.js`, `highlight-editor.js` (highlight passage authoring), `editor-header.js` (editor top bar), `editor.js`, `player.js`, `scoring.js`, `results.js`,
  `progress.js` (My progress, browser-only results), `attempts.js` (unfinished sessions saved in the browser,
  link sessions), `share-link.js` (studio "Share with students" dialog; lazy-loads `js/vendor/qrcode.js`,
  MIT), `overview.js` (studio Overview), `calculator.js`,
  `main.js` (initApp, routing).
- `cases-data.js`: backup of the question bank (`window.NCLEX_CASES`, `window.NCLEX_STANDALONE`), loaded
  when the database can't be reached. Read/write it losslessly with `tools/bank.py` (Python) or
  `tools/supabase.js` (Node). Keep it in sync via the workflow's `download` action.
- `drafts/`: case studies being written (the DMD case's generator `build_unit3_case4.py` lives here).
- `supabase/setup.sql` (table), `supabase/002_admin_logins.sql` (version column + trigger, `nclex_admins`,
  `is_nclex_admin()`, admin-only update policy).
- `server.js` + `*.bat`: optional local Windows server (`/api/save` writes `cases-data.js`).
- `.github/workflows/supabase.yml`: runs `tools/supabase.js` from GitHub Actions (daily at 06:17 UTC:
  `download`, committing `cases-data.js` and `backup/items/{cases,standalone}/<id>.json` when anything
  changed, which also keeps the free project awake; manual: ping, check, compare-original, download, add,
  patch, upload). Items removed from the database move to `backup/deleted/` (never deleted).
  In the studio: "Download all (JSON)" on the Question bank page and "Download JSON" in each row's ⋯ menu
  save copies on the author's computer (`downloadAllQuestionsJSON` / `downloadItemJSON` in dashboard.js).
  `patch <file>` changes only the listed fields (`[{row, id, path, before, after}]`, e.g.
  `drafts/content_patch.json` from `drafts/build_content_fixes.py`); it refuses the whole patch if any field
  no longer holds its `before` value. Use it (not `upload`) to fix published items from the tools.

## Data format (one item = case study or stand-alone question)

`{ id, title, course, unit, topic, disorder, description, isStandalone?, draft?, updatedAt?, screens: [...] }`.
`updatedAt` (ISO time) is stamped when the editor saves a changed item, and by Duplicate / Hide / Show.
`draft: true` hides a finished item from students (set by the dashboard's Duplicate and "Hide from students").
IDs: `case_<13 digits>` / `standalone_<13 digits>`; NURS 1017 cases use `case_17823<unit>000<n>`
(for example Unit 3 Case 4 = `case_1782370000004`). `topic` and `disorder` currently equal `unit`; units are listed in
`CURRICULUM_COURSES` (`js/state.js`). Case studies have 6 screens following the clinical judgment steps
(recognize cues, analyze cues, prioritize hypotheses, generate solutions, take action, evaluate outcomes).

Each screen: `{ step, leftContent: { intro, tabs: [{ id, title, content(HTML) }] }, question }`.
Nurses' notes rows: `<p class="nurse-note-row"><span class="nurse-note-time">1400:</span><span class="nurse-note-text">...</span></p>`
(labels: `HHMM`, `HHMM (qualifier)`, dates/days such as `09/14 0800`, `Day 3 0800`, `POD 2`; see
`NOTE_LABEL_SOURCE` in `js/utils.js`). Tables use the inline-styled `nclex-editor-table` markup
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
Content conventions: on every case screen after the first whose chart gained a tab or new entries, the
question preamble says so ("The nurse has reviewed the Nurses' Notes from 1130 and the Diagnostic Results.");
the player has no New/Updated markers. Never list correct answers first (shuffle options; if a rationale refers to option
numbers, write "(Option N)" to match); don't number rationale points in a way that looks like option numbers.

## Writing new case studies (draft → review → publish)

New content is developed in its own session, separate from UI/UX work. That session only touches
`drafts/` (and publishes through the workflow); it does not edit `js/`, `style.css` or `index.html`.
Both sessions push to `main`, so pull (rebase) before pushing.

1. **Draft** in `drafts/`: one generator script per case (`build_<unit>_<case>.py`, modelled on
   `drafts/build_unit3_case4.py`) that writes `drafts/<id>_<Title>.json`. Match the structure and style of
   the existing NURS 1017 cases in the same unit (6 screens, tabs that unfold over time, HTML tables,
   `<br>` rationales; option, matrix-row and drop-down labels are shown as plain text, so write “ ” ₂ × ⁹ as
   characters, never HTML tags or entities there). Pick the next free ID in the unit's range (check `cases-data.js` and `drafts/`).
   Base the content on the resources the user provides; don't duplicate topics that already exist.
2. **Review**: render every screen in the real player (load the JSON into the app with Playwright,
   Supabase blocked), confirm each screen scores full marks with its answer key and passes the readiness
   rule (`itemProblems` returns nothing), and give the user a PDF walkthrough (question + answered
   screenshots per screen) and a Markdown answer key with full rationales. Flag anything that needs
   clinician review. Iterate on the draft until the user approves it. **Drafts are not visible to students.**
   University of Maryland faculty case studies (`drafts/build_umd_cs*.py`, "University of Maryland - CSn",
   course/unit Others) are converted from the Word files on the UMSON NextGen NCLEX library page, with the
   acknowledgment in each screen's `question.footnote`; they were added to the database with `draft: true`
   (hidden from students) at the user's request to put them in the app, and the user publishes them with
   "Show to students" after review.
   All 21 medical-surgical files are converted (CS1 Asthma is in NURS 1021 Unit 3; CS2–CS21 are in Others with
   their stand-alone trends/bow-ties, IDs `case_17907768000NN` / `standalone_1790776801NN1`, except CS2
   `case_1790769567553` and CS2 Trend `standalone_1790776800001`). Shared helpers: `drafts/umd_common.py`
   (SI labs with the author's ranges converted, plain-text option labels, correct answer never first).
   Each generator's review notes go to `drafts/umd_review/CS<nn>.json`; `node drafts/build_umd_review_pdf.js`
   writes the user's to-do list with an answer key per item (`drafts/UMD_Case_Studies_Review_Tasks.pdf`).
3. **Publish** only after the user approves: trigger the Supabase workflow with `action: add`,
   `file: drafts/<file>.json` (needs the `SUPABASE_SECRET_KEY` secret once the admin lock-down SQL has run),
   check the job log, then trigger `action: download` so the workflow commits the refreshed
   `cases-data.js` backup; pull it. Never edit `cases-data.js` by hand for new content, and never use
   `upload` to publish (it replaces the whole bank).
4. To change an already-published case, edit it in the authoring studio (signed in as admin), or ask the
   user before replacing it through the tools.

## Saving and sign-in (how it works)

- Load: database (`select=*`) → if unreachable or empty, fall back to `cases-data.js` and set
  `isDatabaseUnavailable` (saving refused). `?cases=`/`?standalone=` links filter the bank and set
  `isBankFiltered` (saving refused). Content is sanitized on load (`sanitizeItemContent`).
- Save (`saveBankToStorage` in `data.js`): needs a signed-in admin (`getAdminAccessToken`). PATCH with
  `version=eq.<loaded version>` and `Prefer: return=representation`; on conflict, fetch latest, merge this
  page's changes (`mergeBankChanges`), retry. Works without the version column too.
- Readiness (`isReadyForStudents`, `itemProblems` in `data.js`): items with missing stems, incomplete
  answer keys or `draft: true` are hidden from the student portal (session builder); the dashboard
  shows them in its Status column with the reasons. **Links still open them** (user decision, October 2026:
  the author shares single items with a class before the bank goes live): `?case=<id>` / `?standalone=<id>`,
  `&mode=test` (or `exam`) for exam conditions, open any item in the bank (`startLinkSession`).
- `canEditBank()` (`data.js`): the dashboard only offers Create/Edit/Duplicate/Delete to a signed-in admin
  (or on localhost) with the full, database-loaded bank; otherwise it shows a read-only notice.
  `renderSaveStatus()` (`dashboard.js`) shows the real save state in the dashboard and editor headers.

## Checks (serve the repo first: `python3 -m http.server 8765`)

- `node tools/check.js`: every question renders, its answer key scores full marks, the editor's
  open-and-save changes nothing, no case screen drops chart content. Expected: 0 failures, 3 known incomplete items. (Since the September
  2026 content sync it also reports 2 stand-alone items whose chart tab the editor changes on save.)
- `node tools/check-saving.js`: sign-in and saving against a simulated Supabase (13 checks).
- Playwright is preinstalled (global npm); Chromium at `/opt/pw-browsers`. Block `*.supabase.co` in
  tests so nothing is written.
- In earlier sessions this container could not reach `*.supabase.co` (proxy) or github.io; reach the
  database through the GitHub Actions workflow (trigger via the GitHub MCP tools, read job logs).

## User decisions so far

- Keep `files/ECG1.jpg`. The incomplete items (two empty "New Case Study", empty "New Stand-alone
  Question", Case Study 1 (cardio), and a third "New Case Study") were deleted from the database between
  02:45 and 16:52 UTC on 29 Sep 2026, presumably by the author in the studio (to be confirmed); their last
  versions are kept in `backup/deleted/`. Bowtie-Stroke without correct parameters is still hidden.
- Select-all options were shuffled and rationales relabeled "(Option N)" at the user's request.
- The DMD case (NURS 1017 Unit 3 Case Study 4) is in the bank; its medical content still merits
  clinician review.
- UI/UX work was deliberately deferred until the code fixes were done; it is the next phase.
- No student logins for now (no permission to store student data). Students get the GitHub Pages link;
  their progress is kept only in their own browser (`localStorage` `nclex_progress_v1`, see `js/progress.js`),
  with export/import to a file. Nothing about students is sent anywhere. Accounts may come later: the stored
  rows are shaped to map onto a results table.
- The authoring studio is for the user only, for the foreseeable future (others may author in a few years).
- The interface is built from scratch on the app's own design system (a purchased admin template, Inspinia,
  was considered and declined).
- Show the user mock-ups and screenshots in light mode only (their preferred theme); dark mode is still
  checked, just not sent.

## Pending setup (user's side; check the README "Administrators" section)

Until these are done, anyone with the public key can still write the database:
1. Create the admin user (Supabase Authentication → Users, auto-confirm).
2. Disable public email sign-ups.
3. Run `supabase/002_admin_logins.sql` with the admin email filled in.
4. Add the `SUPABASE_SECRET_KEY` repository secret (needed by the workflow's add/upload after step 3).
The old hard-coded admin password is still in git history; the user was told to change it if reused.

## Remaining code work (from the latest review)

1. Test Mode says "Timed Exam Conditions" but there is no timer.
2. Student results are kept only in each student's browser (My progress); saving them centrally needs
   student accounts + a results table (not permitted yet).
3. Finish or remove the 5 hidden items (content decisions).
4. Whole bank saved per row (over 1 MB); one row per item would shrink saves and merges.
5. Images are embedded as base64 in the data; move to Supabase Storage.
6. Browser-storage copy (IndexedDB/localStorage) is written on save but not read when the database works.
7. Editor relies on the deprecated `document.execCommand`.
8. `alert()` used for errors in editor/player; replace with in-page messages.
9. Data fields: `disorder` duplicates `unit`; `availability` unused; "Others" items use old naming.
10. CSS: unused classes removed and colours/type moved to tokens (design-system pass); 126 `!important`
    remain, mostly overriding inline styles from content and JS, so they go away only once those inline
    styles become classes. The editor is still written dark-first (see "Design system").
11. Accessibility: almost no ARIA labels; drag-and-drop questions lack keyboard support.
12. Run `check.js`/`check-saving.js` in CI on every push.
13. The workflow's actions run on Node 20, which GitHub is deprecating.

## UI/UX work

Done (quick fixes): real save status; read-only dashboard when signed out/offline; results page light and
score-aware; honest counts (hidden items); session builder start button says what is missing, empty pools
disabled, manual picks (step 4) can start a session; dashboard Status column + filter, sortable columns,
"⋯" menu (copy link, Duplicate as draft, hide/show, delete); editor step list with clinical judgment step,
question type and readiness; matrix editor fields wrap; labels on icon-only buttons.
Done (player): after Submit every answer says "your answer: correct/incorrect" or "correct answer (not
selected)" (options, matrix cells, drop-downs with the right choice, highlight, bowtie and ordered-response
answer keys); the result explains the scoring rule with the +/- arithmetic (`scoringExplanation` in
`scoring.js`); in-page notices replace the player's alerts; phones get a Chart | Question switch (opens on Chart) and
left-aligned notes. **No "New"/"Updated" tab labels or highlighted new entries (user decision: the real
NCLEX has none).** What changed since the previous screen is stated in the question preamble instead,
e.g. "The nurse has reviewed the Nurses' Notes from 1130 and 1200 and the Diagnostic Results from 1215.".
Done (design system): tokens, light/dark theme for everything except the exam player, type scale, 44px
touch targets, focus ring, small-screen headers (see "Design system" below).
Done (authoring): Nurses' Notes tabs are edited as timed entries (`js/notes-editor.js`: label field +
note text; Tab/Enter/Shift+Enter/Alt+↑↓; labels may be times or dates such as "Day 3 0800", "09/14 0800",
"POD 2"; free-text mode still available, where a time followed by Tab becomes an entry); drop-down/dyad/
triad questions are edited as one sentence with drop-down chips, choice cards, paste-many, shuffle and a
live student/answer-key preview (`js/cloze-editor.js`). New blanks have no correct choice preselected and
the editor warns when the correct choice is listed first. Keyboard answering for drag-and-drop questions
was deliberately not added (user decision: the real exam is answered with a mouse).
Done (authoring comfort): text boxes grow, can be resized and expanded (Esc closes); shortcuts Ctrl+B/I/U,
Ctrl+. superscript, Ctrl+, subscript, Ctrl+Shift+7/8 lists; paste keeps bold/italic/underline/sub/sup/
lists/tables and drops fonts, colours, images and Word markup (`js/rich-text.js`, all formatting goes
through `richCommand()` so `execCommand` can be replaced in one place); table size picker; a new case
starts with the six clinical judgment screens (`NEW_CASE_TEMPLATE`); live preview beside the editor in
the real player (iframe `index.html?preview=1`, "With answers" fills the key; checklist of blockers and
conventions; `js/editor-preview.js`); unsaved-changes marker + leave warning; `updatedAt` stamped on save
and shown as a sortable "Edited" column; question-type filter in the studio.
Done (app frame): one frame for everything except player/editor (top bar with status, theme and sign-in;
sidebar with Practise / My progress for students, Overview / Question bank for the studio, and a small
"Student portal" link at the studio sidebar's foot). Students have no link to the studio (user decision):
it opens only with `?author=1` (or `?studio=1`); `Start-NCLEX-Studio.bat` opens `localhost:3000/?author=1`.
My progress: tiles, score by clinical judgment step (case screens) and by unit, "To revisit" (items whose
latest attempt lost points, "Practise again"), recent sessions, export/import/delete. Sessions record once
when results show (`recordSessionProgress`); items launched from the studio or the editor preview carry
`source: 'studio'` and are not recorded, and their exits return to the question bank (`leaveSession`).
Session screens carry `caseId`/`itemScreen` or `itemId` (`startCompiledSession` in `session-builder.js`).
Studio Overview: counts, needs attention, recently edited, coverage by unit (all curriculum units), stand-alone
question types. `?author=1` opens Overview.
Done (tables, `js/table-tools.js`): while the cursor is in a table cell, a "Row: Above / Below / Delete |
Column: Left / Right / Delete | Delete table" bar appears under that text box's formatting toolbar (acts on
the current cell's row/column; hovering outlines the target; Delete table asks for a second click; replaced
the hidden ▼ cell menu). Tab/Shift+Tab move between cells, Tab in the last cell adds a row, Enter is a line
break inside a cell. Cells never show placeholder text (students used to see "Header 1" in empty cells);
template cells carry a `placeholder` hint drawn over the cell only in the editor, only while it is empty
and has the cursor. Ready-made tables (`TABLE_TEMPLATES`: Vital signs = blank | setting/time header, rows
T, P, RR, BP, Pulse Oximetry Reading (SpO2); Laboratory results = "Laboratory Test and Reference Range" |
time, 4 empty rows) are in the Table picker and in the "Add Tab" menu (Blank / Nurses' Notes / Vital Signs /
Laboratory Results).
Done (player): a `highlight` question (not `highlight_2`) shows the question and its passage in the left
panel with the right panel blank, as on the NCLEX (`.highlight-left` on `.player-center-split`); phones show
it in one column. The only question number is in the player header ("Question 8 of 13"; Test Mode shows
"Question 8" with no total, since the NCLEX's length varies); the panel keeps just "Not complete"/"Complete".
"Case Study Screen N of 6" counts within the screen's own case (`caseScreenLabel`), also in mixed sessions.
No "The following 6 questions refer to ..." banner (removed: the real exam has none).
Done (authoring, September 2026):
- **Chart carry-forward is enforced (user rule: tabs and information are never subtracted).**
  `js/chart-continuity.js`: a tab added on a screen is added (same id) to every later screen; saving a tab
  carries new entries, edits and title changes to later screens (block diff of top-level entries, matched
  by text; an edit pairs only with an entry of the same kind/time label); entries inherited from the
  previous screen that the author deletes are put back with a notice; a tab can only be deleted on the
  screen where it first appears (then from all later screens, two-click confirm). Opening and saving
  without edits changes nothing. The 21 older cases that dropped tabs or entries (mostly screens showing
  only new notes) were restored at the user's request with `drafts/build_chart_restore.js` →
  `drafts/chart_restore_patch.json` (workflow `patch`; `restoreChartContinuity` keeps an earlier table
  whose values a later screen no longer shows above the later one). There is no gap warning in the
  editor any more (user decision); `tools/check.js` fails if a case screen drops chart content.
- Highlight questions (`js/highlight-editor.js`): phrases are marked by selecting text (or clicking a
  table cell) and choosing Correct answer / Distractor / Unmark; they show as `mark.hl-mark` and are
  stored as `{phrase|correct}` / `{phrase}` on save (unchanged passages keep their stored HTML). Live
  count and warnings (none correct, all correct, stray braces, limit below correct count; also in the
  preview checklist). `highlight` is edited in the left column; `highlight_2` can copy a chart tab into
  the passage. Nurses' Notes show as timed rows. "Students may select": same as correct (default for new
  questions), no limit, or a number (`maxCorrectSelections`). No alert()/confirm() there.
- "Draft from chart changes" writes the preamble ("The nurse has reviewed the Nurses' Notes from 1130
  and the Vital Signs.") from what the chart gained since the previous screen (`draftPreambleFromChart`).
- Select-all/multiple-choice options: "Shuffle order" (a correct answer is never left first; "(Option
  N)"/"Option N" in the rationale are renumbered) and a warning when option 1 is correct.
- Bowtie option fields grow to show long text.
- Timed entries for every chart tab without a table or list (not only Nurses' Notes): a new blank tab
  opens as time + note entries; each entry can have an optional bold title on its own line above the
  time and note ("T+"), stored as a `<p><b>Title</b></p>` paragraph just before the entry (the form older
  cases already used; `titleParagraphText` in `js/notes-editor.js`; the old `<b>Title</b><br>` inside
  the note is still read; the × at the right of the title box removes the title). In free-text tabs (tables) T+ adds a bold title line above the table or
  paragraph with the cursor (`insertFreeTextTitle`). Deleting a timed entry, a table row or a column
  takes a second click ("Delete?"), like Delete table (user request, 30 Sep 2026: an entry deleted on
  the screen where it first appears is also removed from later screens and cannot be brought back in the
  studio; the 1000 entry of NURS 1021 Unit 3 Case Study 1 was restored from the 29 Sep backup with
  `drafts/build_restore_1021_u3c1_notes.py` → workflow `patch`).
  Tabs with tables/lists stay in free text (19 of 214 distinct text tabs in September 2026). The Table
  button also works in a timed-entries tab (blank table or ready-made Vital signs / Laboratory results):
  the tab switches to free text with every entry kept and the table goes after the entry with the
  cursor (`tableInsertTarget`); new empty tables carry forward like any entry.
- Tab-filling helpers: every formatting toolbar also has Italic, Underline, a clinical symbols menu
  (Ω▾: ° ≤ ≥ ± × ↑ ↓ µ ² % …; the separate °/≥/≤ buttons were removed, October 2026), one Lists menu
  (≡▾: bullet / numbered, `openListMenu`), Clear formatting and Undo/Redo (`enhanceToolbar` in `js/rich-text.js`, added to
  toolbars created later too) and stays in view while scrolling (sticky). Pasting several "0800 text"
  lines into a timed entry makes one entry each (`handleNoteRowsPaste`). An entry whose time is earlier
  than the one above gets a gentle warning (with the "Day 2" hint), and the next time box suggests
  "after 1400" (`updateNoteTimeHints`). The table bar has "+ Reading": a new time column after the last
  reading, before a trailing Reference/Normal range column (`tableAddReading`). In a lab table, typing a
  test name in the first column and leaving the cell fills "<b>Name</b><br>range" from
  `LAB_REFERENCE_RANGES` (`js/lab-ranges.js`: 127 tests from the Medical Council of Canada "Normal lab
  values" page, SI values exactly as MCC prints them, read September 2026 and cross-checked in two
  independent passes; the author's typed name is kept in bold; review table in
  `drafts/lab_reference_ranges.md`; reviewed and approved by the user as final). User decision: SI
  units only (Canada); MCC's few non-SI values (blood gases mm Hg, BNP pg/mL, …) kept as MCC prints them. mcc.ca blocks plain
  downloads from this container (Cloudflare/nginx 403); the WebFetch tool reaches it.
  Vital Signs values (October 2026, user decision): type only the number; leaving the cell (Tab, click, or
  leaving the text box) adds the unit, and a faint unit shows after the text while typing (editor only):
  T "38.2° C" (user's format; Celsius values 25–45 only), P "112 beats/min", RR "24 breaths/min", BP
  "142/88 mm Hg", SpO2 "94%". Recognized by the row label (or column header): T/Temp, P/HR/Pulse, RR/Resp,
  BP, SpO2/Pulse oximetry. Only a cell holding just the number changes; Ctrl+Z undoes it
  (`VITAL_UNITS`, `addVitalUnit`, `showVitalUnitHint` in `js/table-tools.js`; existing tables untouched).
  The whole bank was brought to the same format (1 Oct 2026, `drafts/build_vitals_units.py` →
  `drafts/vitals_units_patch.json`, workflow `patch`): every temperature in any field is written "38.2° C" /
  "101.2° F" (NCLEX style), and vital-sign rows of chart tables carry beats/min, breaths/min, mm Hg and %
  ("bpm" and "mmHg" replaced). The same script also writes units in running text everywhere (notes,
  rationales, stems, options, passages): "mm Hg", "bpm"/"N/min" → beats/min or breaths/min by the label
  before it, and labelled values without a unit get one ("P 92, RR 22, BP 152/86" → "P 92 beats/min,
  RR 22 breaths/min, BP 152/86 mm Hg"; a bare "P" only in a list with RR or BP). Write new content in
  that format.
  In timed entries, Enter in a note starts a new paragraph (a blank line, `<br><br>`), Shift+Enter a new
  line, Ctrl+Enter (or + Add entry) the next entry. Chart tabs can be moved left/right with the ‹ ›
  arrows on the active tab, only on the screen where the tab first appears; later screens take the same
  order for the tabs they share (`moveActiveTab` in editor.js, `applyTabOrderToLaterScreens` in
  chart-continuity.js). The symbols menu offers "° C" / "° F" (and the plain °).
  **No markers for new entries (user decision): on the NCLEX nothing new is highlighted; the nurse reads
  the whole chart.**
- More room for chart text: narrower screen list (152px); a drag handle between the chart and question
  panes (`initEditorPaneDivider`, 30–75%, remembered per browser in `localStorage.nclex_editor_split`,
  double-click resets, arrow keys move it); less nested padding; timed entries are time (as wide as its
  label) | note | ×, with the entry tools in the tab's toolbar ("T+" title, ↑ ↓ move; `noteToolbarAction`,
  acting on the entry with the cursor). A new case's default tabs share their ids across the six screens
  and its Vital Signs tab starts as the ready-made table.
- Vital Signs tables leave the first header cell empty (user decision: the tab name says it). The
  template does; the 142 existing tables with "Parameter" / "Vital Sign" / "Time" / "Parameter /
  Assessment" there were cleared with `drafts/build_vitals_header.py` → `drafts/vitals_header_patch.json`.
Done (editor top bar, `js/editor-header.js`, September 2026): breadcrumb whose "Question bank" link goes
back (saving first; no separate back arrow), borderless title, chips for Course and Unit (the real
`<select>` sits invisibly over each chip), Description (a dialog; `#case-desc-input` is now a hidden
input) and Ready for students (`itemProblems` on `buildPreviewItem()`, so unsaved edits count; its
popover jumps to a screen or clears the draft flag). Right: quiet "Saved · 3 min ago" status (colour
only for unsaved/failed/offline), ⋯ menu (Download this case (JSON), Copy student link, theme,
Keyboard shortcuts), then Preview | Save | Launch as one group. Save is greyed while there is nothing
new (it still works); Ctrl+S saves.
Done (class links, October 2026; user is not going live yet and gives students one case study link at a
time): the studio's **Share** button (Question bank row, ⋯ menu, the ID badge, and the editor's ⋯ menu "Share
with students…") opens a dialog with two links, Practice (default, feedback after each question) and Exam
(`&mode=test`), Copy buttons and a QR code ("Larger for the projector"). Links always use
`STUDENT_SITE_URL` (js/state.js) unless the studio itself runs on github.io, so copying on localhost works.
The dialog says whether the item is hidden from the portal and warns about unfinished items and unsaved
editor changes. Students' sessions are saved in their browser as they answer (`js/attempts.js`,
`localStorage.nclex_attempts_v1`, item ids + answers only, dropped when an item's `updatedAt`/screen count
changes): reopening a link asks "Continue where you left off?" (player-styled `#resume-modal`, separate for
practice and exam), Quit in a link session goes to `#paused-view` (Continue / Start over), results of a
link session have no "Back to Practise" (Try again, My progress, Review). Practise-page sessions show a
"Continue your … session" banner (`#portal-resume`). Quit while reviewing answers returns to the results.
Sessions launched from the studio or the preview are never saved or recorded.
The full student flow (two pathways, plan + mock-up at the student-flow artifact) is deferred until the bank
is larger (user decision).
Suggested next: the guided student flow (C), inside the Practise page of the frame, once the bank is larger; the student view of
highlight questions (clearer marking and feedback; mock-up discussed, deferred by the user).

### Design system (how to style new work)

- Tokens are at the top of `style.css`: surfaces (`--surface-page`, `--surface`, `--surface-muted`,
  `--surface-sunken`, `--surface-strong`, `--surface-selected`), text (`--text`, `--text-secondary`,
  `--text-muted`, `--text-subtle`, `--text-faint`, `--brand-text`), borders (`--border`, `--border-subtle`,
  `--border-strong`), status (`--success|warning|danger` + `-bg`, `-bg-subtle`, `-border`, `-text`), brand
  (`--brand`, `--brand-hover`, `--brand-bar`, `--text-on-brand`), type (`--fs-2xs` 10px … `--fs-5xl` 40px),
  spacing (`--space-1` 4px … `--space-8` 32px), `--focus-ring`, `--touch-target`. Use them instead of hex
  values, including in inline styles written by JS, so dark mode works.
- Theme: `html[data-theme="light"|"dark"]`, set before first paint by the script in `index.html` (stored
  choice `localStorage.nclex_color_theme`, otherwise the device setting) and switched by `toggleTheme()` /
  any `[data-theme-toggle]` button (portal, studio and editor headers).
- **The player has no themes (user decision).** It imitates the Pearson VUE NCLEX screen, which has one
  fixed colour scheme for all candidates (a colour-changing toggle exists only as an approved disability
  accommodation). `#player-view`, `#test-submit-modal` and `#skip-question-modal` carry
  `.theme-locked-light`, which re-declares the light token values, and the player keeps its original
  literal colours and sizes. Never add a theme toggle or dark styles to the player; check that its
  screenshots are identical with the app in light and in dark.
- The editor (and the login modal, "specific items" list) is still dark-first: base rules use the dark
  `--*-dash` palette and `html:not([data-theme="dark"]) #editor-view ...` rules give the light look.
- Question content keeps its inline colours (white cells, slate text); the `DARK THEME: DETAILS TOKENS
  CANNOT REACH` block maps them in dark mode on the results page (the player always shows them as authored).
- Visual checks: screenshot the states in both themes (desktop 1440 and phone 390) and compare with the
  previous version; `pointer: coarse` rules make controls 44px on touch screens.

### Ideas list

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
