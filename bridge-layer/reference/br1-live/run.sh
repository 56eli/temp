#!/bin/sh
# start|stop|status the debugger bridge v7 (tmux session: bridge) — the replacement for
# /root/.pi/dbg-bot/run.sh. Same interface, same anchoring rule: tmux resolves a target exact first,
# then by prefix, so every session target below is anchored with '='.
#
# The session is NOT the loop. supervise.sh restarts `node bot.js` every 2s, so an unrecoverable
# startup failure (bad token, operator pin mismatch, node missing) leaves the session alive and
# `has-session` permanently true. Liveness is the heartbeat the loop writes, which is the evidence
# CONTRACT.md [supervision] names for loop_stopped.
SESSION=bridge
STATE=/root/.pi/bridge/state
LOG=$STATE/events.jsonl
STALE=90          # 3 x the loop's 30s heartbeat (bot.js)

sess() { tmux has-session -t "=$SESSION" 2>/dev/null; }

hb_epoch() {   # epoch seconds of the last heartbeat, empty when there is none
  ts=$(grep '"event":"heartbeat"' "$LOG" 2>/dev/null | tail -1 | sed -n 's/.*"ts":"\([^"]*\)".*/\1/p')
  [ -n "$ts" ] || return 1
  date -u -d "$ts" +%s 2>/dev/null || return 1
}

loop_age() {   # seconds since the last heartbeat
  then_s=$(hb_epoch) || return 1
  echo $(( $(date -u +%s) - then_s ))
}

loop_state() {
  age=$(loop_age)
  if [ -z "$age" ]; then echo "bridge: loop state UNKNOWN - no heartbeat record in $LOG"; return; fi
  if ! sess; then echo "bridge: loop gone - no session (last heartbeat ${age}s ago)"; return; fi
  if [ "$age" -le "$STALE" ]; then echo "bridge: loop live (last heartbeat ${age}s ago)"
  else echo "bridge: loop STOPPED - session up but last heartbeat ${age}s ago; supervise.sh restarts node every 2s, so read $STATE/supervisor.log"; fi
}

case "$1" in
  start)
    # No token means bot.js throws on start, supervise.sh restarts it every 2 s forever, and the tmux
    # session keeps `sess` true — a start that looks alive and can never work. Refuse before creating it.
    if [ -z "${BRIDGE_BOT_TOKEN:-}" ]; then
      TOKF=$(sed -n 's/.*"token_file"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' /root/.pi/bridge/config.json)
      if [ -z "$TOKF" ] || [ ! -s "$TOKF" ]; then
        echo "bridge: start REFUSED - no token at ${TOKF:-<unset in config.json>} (seat the token first; supervise.sh would loop forever without it)" >&2
        exit 4
      fi
    fi
    if sess; then
      tmux kill-session -t "=$SESSION" 2>/dev/null
      i=0
      while sess && [ "$i" -lt 50 ]; do i=$((i+1)); sleep 0.1; done   # never create before the old session is gone
      if sess; then echo "bridge: start FAILED - session =$SESSION survived kill-session" >&2; exit 1; fi
    fi
    started_at=$(date -u +%s)
    if ! tmux new-session -d -s "$SESSION" 'exec /root/.pi/bridge/supervise.sh'; then
      echo "bridge: start FAILED - tmux new-session refused" >&2; exit 1
    fi
    sleep 1                                  # the session object exists before its child can exit
    if ! sess; then echo "bridge: start FAILED - the session did not survive" >&2; exit 1; fi
    i=0; fresh=""
    while [ "$i" -lt 20 ]; do               # a heartbeat from THIS start, not the previous loop's
      hb=$(hb_epoch)
      if [ -n "$hb" ] && [ "$hb" -ge "$started_at" ]; then fresh=1; break; fi
      i=$((i+1)); sleep 0.5
    done
    if [ -n "$fresh" ]; then echo "bridge: started; loop live (heartbeat after start)"
    else echo "bridge: started, but NO heartbeat since start - check $STATE/supervisor.log" >&2; exit 1; fi ;;
  stop)
    if sess; then tmux kill-session -t "=$SESSION" 2>/dev/null; echo "bridge: stopped"
    else echo "bridge: not running - nothing to stop"; fi ;;
  status)
    if sess; then echo "bridge: session running"; else echo "bridge: session NOT running"; fi
    loop_state
    echo "--- last 3 supervisor lines ---"; tail -3 "$STATE/supervisor.log" 2>/dev/null
    echo "--- last 3 records ---"; tail -3 "$LOG" 2>/dev/null ;;
  probe)
    node /root/.pi/bridge/adapter.js <<'J'
{"op":"codes"}
J
    ;;
  *) echo "usage: run.sh start|stop|status|probe" ;;
esac
