-- NCLEX_Claude: one-time setup for the NEW Supabase project.
-- Run this in the new project's dashboard: SQL Editor -> New query -> paste -> Run.
-- It mirrors the original app's layout: one table with a 'cases' row and a
-- 'standalone' row, each holding the full JSON array.

create table if not exists public.nclex_data (
  key  text primary key,
  data jsonb not null default '[]'::jsonb
);

alter table public.nclex_data enable row level security;

-- The app reads and saves with the project's publishable key, so that key
-- needs read and update access. It cannot create or delete rows.
drop policy if exists "nclex_data read"   on public.nclex_data;
drop policy if exists "nclex_data update" on public.nclex_data;
create policy "nclex_data read"   on public.nclex_data for select to anon, authenticated using (true);
create policy "nclex_data update" on public.nclex_data for update to anon, authenticated using (true) with check (true);

insert into public.nclex_data (key, data) values
  ('cases', '[]'::jsonb),
  ('standalone', '[]'::jsonb)
on conflict (key) do nothing;
