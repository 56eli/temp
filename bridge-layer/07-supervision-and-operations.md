# 07 — Supervision and operations

*[agent: 2026-10-31 — sb3. Rule C30/C31; supervisor evidence is from the live sb3 `supervisor.log`.]*

## Three failure axes, three pieces of evidence

C30's point is that "the bridge is down" is three different failures, and one signal cannot detect
all three:

| axis | what it looks like | its evidence | what it is **not** |
|---|---|---|---|
| **process gone** | the loop exited / was killed / the container restarted | a supervisor log line with an exit code, or `NRestarts`; a fresh `start` record | a live tmux session — the session outlives `node` |
| **loop stopped** | the process exists but the event loop is blocked (the historic `send-keys` that sat in state `S` for 55.6 minutes) | **heartbeat age** against a threshold the loop cannot reach honestly (`30 s` beat, `90 s` stale) | a heartbeat that a timer writes from a different process |
| **no turn** | the line reached the pane, the model never answered | `injected`/`delivered` with no `answered` inside the reminder window | `injected` — that is transport evidence only |

The reference writes the heartbeat **inside the loop** (`setInterval(..., 30000)`), carrying `pid`,
`uptime_s` and `loop: true`. That is what makes it evidence for axis 2 rather than decoration.

## The supervisor

`supervise.sh` is deliberately dumb: it runs `node bot.js`, appends stderr to `supervisor.log`, and on
exit writes one line with the code and restarts after 2 s. It proves *process gone* and nothing else.

Three hardening details in the shipped version, each earned:

```sh
cd /root/.pi/bridge || { log "cannot enter ... - exiting"; exit 1; }   # not a restart loop
command -v node >/dev/null 2>&1 || { log "node not on PATH ($PATH) - exiting"; exit 1; }
[ "$rc" = 2 ] && log "another loop holds the lock - not restarting" && sleep 30 && continue
```

Without the first two, a bad token or a missing `node` produces a restart every 2 s forever: the
tmux session stays alive, `has-session` stays true, and every status command lies. Without the third,
the writer-lock refusal (exit 2) becomes a 2-second hot loop.

Live evidence from sb3, 2026-10-28T10:48:05Z:

```
2026-10-28T10:48:05.001Z another loop holds /root/.pi/bridge/state/loop.lock (pid 322); exiting
2026-10-28T10:48:05Z bridge exited rc=2; restarting
2026-10-28T10:48:05Z bridge: another loop holds the lock - not restarting
```

That is a second loop being refused, the supervisor backing off, and the live loop (pid 322) surviving.

## The writer lock

One loop per token. A second `bot.js` on the same token would ack, inject and post twice, and
`reply.js` would look correct from both. The reference takes `<state_dir>/loop.lock`:

* read the pid; if it is **not** a live process whose `/proc/<pid>/cmdline` contains `bot.js`, the
  lock is stale (crash, container restart) and is taken over — a reboot never needs a human on a
  lock file;
* otherwise write `writer-lock-refused` to the log and exit **2**;
* remove the lock on exit only if it still names this pid.

Pid reuse is why the `cmdline` check exists: a bare pid can belong to a stranger.

## The control script (`run.sh`)

```
run.sh start | stop | status | probe
```

`start` is where the design shows:

1. refuse **before creating the session** if neither `BRIDGE_BOT_TOKEN` nor the configured token file
   is readable — otherwise the supervisor loops forever and the session looks alive;
2. kill an existing session and **wait for it to be gone** (never create before the old session is
   gone);
3. create the session running `supervise.sh`; confirm the session survived;
4. wait up to 10 s for a **heartbeat from this start** (timestamp ≥ start instant), not the previous
   loop's heartbeat. If none arrives, exit 1 and say to read `supervisor.log`.

`status` prints two independent facts — session running? loop live? — because they disagree exactly
when it matters. `probe` runs the adapter's `codes` op.

## The silent-bridge runbook

Every step is read-only until step 5.

1. **Is the loop alive?** Look at the last heartbeat.
   ```sh
   tail -1 /root/.pi/bridge/state/events.jsonl
   # {"ts":"...","event":"heartbeat","pid":322,"uptime_s":275524,"loop":true}
   ```
   Older than ~60–90 s ⇒ a frozen loop (axis 2).
2. **Did the supervisor restart it, and why?**
   ```sh
   tail -3 /root/.pi/bridge/state/supervisor.log
   # 2026-10-28T10:48:05Z bridge exited rc=2; restarting
   ```
3. **Did the message reach the loop at all?**
   ```sh
   grep <request-id> /root/.pi/bridge/state/events.jsonl
   ```
   * nothing ⇒ the gate never accepted it: wrong channel/guild, bot author, another user's mention, or
     the message was sent with mentions suppressed.
   * `accepted` then nothing ⇒ it never reached the pane (axis 3, injection).
   * `injected` then nothing ⇒ it is in the pane and the agent has not answered. **Not a bridge fault.**
   * `delivered` with no `answered` ⇒ look for `abandoned_restart` on the same id: the bridge
     restarted while the request was open, so the answer was never sent.
4. **Did an answer exist but never leave?**
   ```sh
   grep -c '"reply_to":"<request-id>"' /root/.pi/bridge/state/answers.jsonl
   ```
5. **Answer by hand** (a write, so it is the last step): `node reply.js <id> "<text>"`. If it exits 4,
   the request is closed — check `answers.jsonl` before re-sending, and use `--force` only when you
   mean to record a second answer.

## Code identity (C31)

Every `start` record carries `code_identity`: the first 16 hex of SHA-256 over `bridge.js`, `bot.js`,
`reply.js`, `state.js` in that order, concatenated. It covers the loop, the reply tool and the notice
verifier — the three things that must agree about the contract — and nothing else. What it buys:

* a fix and a restart look identical from outside; the hash tells them apart;
* "the running code" is a checkable claim: a conformance run can quote the identity it measured;
* a rolled-back file shows up as an identity change on the next start.

It is **not** a security control: anyone who can write the files can also write the hash.

Live: `code_identity 8bc1b4517fa72e83` on the start at 2026-10-28T10:39:49Z (pid 322), unchanged at
2026-10-31T15:11Z.

## Deployment facts that surprise people

* **The container filesystem is not durable; the mounted home is.** On sb2 the bridge lives at
  `/root/.pi/bridge243` because `/root/.pi` is the mounted home and the install script hardcodes
  `/home/dev/bridge` for devcage. Name your directory after what survives a recreate.
* **A tmux session is not a process.** `has-session` true + heartbeat stale = the failure the
  control script exists to name.
* **The operator's DM channel is created lazily.** Fetching it at `ready` is how the first DM works;
  a bot that has never been DMed may have no channel cached until the event arrives.
* **Never put a token on a command line.** `reply.js` does not need one; the loop reads the token file
  the config names, or `BRIDGE_BOT_TOKEN` from its own environment.
