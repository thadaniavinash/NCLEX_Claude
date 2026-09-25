# NCLEX_Claude

Experimental copy of the NCLEX NGN Case Study Studio. Changes here do not affect
the original `NCLEX` app or its database.

## Layout

| Path | What it is |
|---|---|
| `index.html`, `style.css` | The single-page app (student portal, test player, authoring studio) |
| `cases-data.js` | Backup copy of the question bank (every case study and stand-alone question), used when the database cannot be reached |
| `js/` | App code, one file per feature, loaded in order by `index.html` (`main.js` last) |
| `tools/` | Maintenance scripts (below) |
| `drafts/` | Case studies being written, not yet in the bank |
| `supabase/setup.sql` | One-time setup for this copy's own Supabase project |
| `server.js`, `*.bat` | Optional local server for Windows: saves from the editor go straight to `cases-data.js` |

The app loads and saves the question bank in this copy's own Supabase project
(`wgnrcopjkylviiyllsgz`, configured in `js/data.js`); the original app's database is never
written. If the database cannot be reached, or returns an empty bank, the app falls back to
`cases-data.js` and refuses to save, so an older copy can never overwrite newer questions.
`cases-data.js` is the backup: `node tools/supabase.js download` refreshes it from the
database, and `upload` loads it into the database.

## Administrators

Saving is protected by Supabase Auth (see `js/auth.js`): editors sign in with an email and
password, and the database only accepts saves from accounts listed in `nclex_admins`.
One-time setup (Supabase dashboard of this project):

1. **Authentication -> Users -> Add user -> Create new user**: your email and a strong password,
   with *Auto Confirm User* ticked.
2. **Authentication -> Sign In / Providers -> Email**: turn off *Allow new users to sign up*
   (only accounts you create can then exist).
3. **SQL Editor**: run `supabase/002_admin_logins.sql` after replacing `YOUR-EMAIL@example.com`
   with that email. Add more admins later with
   `insert into public.nclex_admins (email) values ('someone@example.com');`
4. **GitHub -> Settings -> Secrets and variables -> Actions -> New repository secret**:
   `SUPABASE_SECRET_KEY` = the project's secret key (Supabase -> Project Settings -> API Keys).
   The workflow's `add` and `upload` actions need it once saving is restricted to admins.

Unfinished items (a screen with no question text, or an answer key that cannot score full
marks) are kept out of student sessions and marked *Hidden from students* in the studio.

## Tools

- `python3 tools/bump_version.py` - after changing any `.js` or `.css` file (or
  `cases-data.js`), stamps a new `?v=` on them in `index.html` so browsers fetch the new version.
- `node tools/check.js [base-url]` - with the repo served locally
  (`python3 -m http.server 8765`), loads the real app in headless Chromium and, for every
  question, checks it renders, that its answer key scores full marks, and that opening and
  saving it in the editor changes nothing. Supabase and `/api/save` are blocked while it runs.
- `node tools/check-saving.js` - checks admin sign-in and saving (including two editors saving
  at once) against a simulated Supabase.
- `node tools/supabase.js <ping|check|compare-original|download|add|upload>` - manage the
  database (see the comment at the top of the file). The **Supabase** GitHub Actions workflow
  runs the same commands from the Actions tab, and pings the project daily so the free tier is
  not paused.
- `tools/bank.py` - Python helpers to read and write `cases-data.js` without changing its format.
