#!/bin/sh
# Saves a secret from the macOS clipboard into .env (gitignored, mode 600). Never prints the secret.
# Usage: copy the secret, then run one of:
#   sh scripts/save-key.sh            Anthropic API key        (sk-ant-…)  -> ANTHROPIC_API_KEY
#   sh scripts/save-key.sh supabase   Supabase access token    (sbp_…)     -> SUPABASE_ACCESS_TOKEN
cd "$(dirname "$0")/.." || exit 1
case "${1:-anthropic}" in
  anthropic) var=ANTHROPIC_API_KEY;    prefix='sk-ant-'; label='an Anthropic key';;
  supabase)  var=SUPABASE_ACCESS_TOKEN; prefix='sbp_';    label='a Supabase access token';;
  *) echo "Unknown kind '$1'. Use: anthropic | supabase"; exit 1;;
esac
k="$(pbpaste | tr -d '[:space:]')"
case "$k" in
  "$prefix"*) ;;
  *) echo "The clipboard doesn't hold $label (it should start with $prefix). Copy it and run this again."; exit 1;;
esac
[ ${#k} -ge 30 ] || { echo "That looks too short. Copy the whole value and run this again."; exit 1; }
umask 077
grep -v "^$var=" .env 2>/dev/null > .env.tmp || true
printf '%s=%s\n' "$var" "$k" >> .env.tmp && mv .env.tmp .env && chmod 600 .env
printf '' | pbcopy
echo "saved $var (starts with ${k%"${k#??????}"}…, ${#k} characters). Clipboard cleared."
