# NCLEX_Claude

Experimental copy of the NCLEX NGN Case Study Studio. Changes here do not affect
the original `NCLEX` app or its database.

## Layout

| Path | What it is |
|---|---|
| `index.html`, `style.css` | The single-page app (student portal, test player, authoring studio) |
| `cases-data.js` | **The question bank**: every case study and stand-alone question. The only data file the app loads |
| `js/` | App code, one file per feature, loaded in order by `index.html` (`main.js` last) |
| `tools/` | Maintenance scripts (below) |
| `drafts/` | Case studies being written, not yet in the bank |
| `supabase/setup.sql` | One-time setup for this copy's own Supabase project |
| `server.js`, `*.bat` | Optional local server for Windows: saves from the editor go straight to `cases-data.js` |

This copy is not connected to a database yet (`USE_SUPABASE = false` in `js/data.js`), so
it loads `cases-data.js`, and edits made in the authoring studio are lost on reload.
Content changes are made in `cases-data.js` and committed.

## Tools

- `python3 tools/bump_version.py` - after changing any `.js` or `.css` file (or
  `cases-data.js`), stamps a new `?v=` on them in `index.html` so browsers fetch the new version.
- `node tools/check.js [base-url]` - with the repo served locally
  (`python3 -m http.server 8765`), loads the real app in headless Chromium and, for every
  question, checks it renders, that its answer key scores full marks, and that opening and
  saving it in the editor changes nothing. Supabase and `/api/save` are blocked while it runs.
- `tools/bank.py` - Python helpers to read and write `cases-data.js` without changing its format.
