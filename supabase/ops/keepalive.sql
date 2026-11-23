-- Keep-alive for the Free plan: Supabase pauses Free projects after about a week of low database activity
-- (https://supabase.com/docs/guides/platform/free-project-pausing). A daily GitHub Action calls keepalive(),
-- which writes one row, so there is real database activity every day. Nothing else is exposed: the table is
-- unreadable to clients and the function only bumps a timestamp and a counter.
create table if not exists public.ops_heartbeat (
  id        int primary key check (id = 1),
  last_ping timestamptz not null default now(),
  pings     bigint not null default 0
);
alter table public.ops_heartbeat enable row level security;
revoke all on public.ops_heartbeat from anon, authenticated;
insert into public.ops_heartbeat (id) values (1) on conflict (id) do nothing;

create or replace function public.keepalive() returns timestamptz
language sql security definer set search_path = public as $$
  update public.ops_heartbeat set last_ping = now(), pings = pings + 1 where id = 1 returning last_ping;
$$;
revoke all on function public.keepalive() from public, anon, authenticated;
grant execute on function public.keepalive() to anon;
