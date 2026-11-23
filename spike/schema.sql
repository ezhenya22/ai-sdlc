-- ADR-000 risk spike: one table, guest sign-in, realtime. Throwaway: dropped when Stage 5 builds the real schema.
create table if not exists public.spike_pings (
  id          uuid primary key default gen_random_uuid(),
  room        text not null check (room ~ '^[a-z0-9-]{3,32}$'),
  author      uuid not null default auth.uid(),
  body        text not null check (char_length(body) between 1 and 140),
  sent_at     timestamptz not null,
  created_at  timestamptz not null default now()
);

alter table public.spike_pings enable row level security;

-- Auto-grant is off for this project, so access is granted explicitly, to signed-in users only (guests included).
revoke all on public.spike_pings from anon, authenticated;
grant select, insert on public.spike_pings to authenticated;

drop policy if exists spike_read_recent on public.spike_pings;
create policy spike_read_recent on public.spike_pings
  for select to authenticated
  using (created_at > now() - interval '1 day');

drop policy if exists spike_insert_own on public.spike_pings;
create policy spike_insert_own on public.spike_pings
  for insert to authenticated
  with check (author = auth.uid());

do $$ begin
  alter publication supabase_realtime add table public.spike_pings;
exception when duplicate_object then null; end $$;
