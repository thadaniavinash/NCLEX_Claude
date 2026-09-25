-- NCLEX_Claude: restrict saving to administrators, and make simultaneous saves safe.
-- Run once in the project's dashboard: SQL Editor -> New query -> paste -> Run.
-- Before running, replace YOUR-EMAIL@example.com (at the bottom) with the email of the admin
-- account you created under Authentication -> Users.

-- 1. A version number on each row. Every save bumps it, and the app only saves if the row
--    is still at the version it loaded, so two editors can no longer silently overwrite
--    each other's work (the app merges their changes instead).
alter table public.nclex_data add column if not exists version integer not null default 0;

create or replace function public.nclex_data_bump_version() returns trigger
language plpgsql as $$
begin
  new.version := old.version + 1;
  return new;
end;
$$;

drop trigger if exists nclex_data_bump_version on public.nclex_data;
create trigger nclex_data_bump_version before update on public.nclex_data
  for each row execute function public.nclex_data_bump_version();

-- 2. Who may save: accounts whose email is listed here. The table has row level security
--    and no policies, so it cannot be read or changed through the public API.
create table if not exists public.nclex_admins (email text primary key);
alter table public.nclex_admins enable row level security;

create or replace function public.is_nclex_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.nclex_admins
    where lower(email) = lower(coalesce(auth.jwt() ->> 'email', ''))
  );
$$;
revoke all on function public.is_nclex_admin() from public;
grant execute on function public.is_nclex_admin() to anon, authenticated;

-- 3. Everyone can still read the question bank; only signed-in admins can save it.
--    (The secret key used by the GitHub Actions workflow bypasses these rules.)
drop policy if exists "nclex_data update" on public.nclex_data;
create policy "nclex_data update" on public.nclex_data
  for update to authenticated
  using (public.is_nclex_admin())
  with check (public.is_nclex_admin());

-- 4. Your admin account. Add a line per extra admin.
insert into public.nclex_admins (email) values ('YOUR-EMAIL@example.com') on conflict do nothing;
