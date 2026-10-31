#!/bin/sh
# The supervisor is deliberately dumb: it proves process_gone (a log line and a restart) and nothing
# else. The loop's heartbeat proves loop_stopped; `delivered` with no `answered` proves no_turn.
# A failure that cannot be fixed by restarting (node missing, wrong directory) exits instead of
# looping every 2s: an endless restart keeps the tmux session alive and makes `run.sh status` lie.
set -u
cd /root/.pi/bridge || { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) bridge: cannot enter /root/.pi/bridge - exiting" >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) bridge: node not on PATH ($PATH) - exiting" >&2; exit 1; }
mkdir -p /root/.pi/bridge/state
while :; do
  node bot.js >> /root/.pi/bridge/state/supervisor.log 2>&1
  rc=$?
  printf '%s bridge exited rc=%s; restarting\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$rc" \
    >> /root/.pi/bridge/state/supervisor.log
  [ "$rc" = 2 ] && printf '%s bridge: another loop holds the lock - not restarting\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> /root/.pi/bridge/state/supervisor.log && sleep 30 && continue
  sleep 2
done
