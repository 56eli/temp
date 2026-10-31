# Boxes — the deployment sheet

**This file is allowed to differ.** Everything here is a fact about one machine, not a rule: two boxes may
disagree here and both be conformant. A row that was measured says when and how; a row that was not is
marked *reported* and is that box's own testimony, not an observation from this repository.

| row | `sb2` (this container, bot `rebugger`) | `debugger` (container `pi-br1`) | `bugger` (host `pidev`/E11) |
|---|---|---|---|
| supervisor | tmux-hosted loop, `supervise.sh`, session `spac2-bridge` — **measured**: `kill -TERM` at 19:56:29Z, `start` record 10 s later, no human act | systemd unit, `Type=simple` | systemd user unit + separate doctor unit/timer |
| survives a logout | unverified — PID 1 is `sleep infinity`; nothing starts the loop after a container recreate | `Linger=yes` | `Linger=yes` (was `no` for a day while the unit read `enabled`) |
| loop-stopped detection | `watchdog()` exits when no tick for 60 s — cannot tell slow from hung | not armed | `doctor.py`, staleness alone, `wchan`/`stat` before any kill |
| restart window (C24/R8) | **measured 2026-10-25 21:03:50Z**, pid 170889: after the restart the only records are `start`, `restart-window` (`cleared_channels=2, dropped_held=0`), `binding` and two `baseline` — nothing older relayed, no burst. Before R8 the same action re-read answers from offset 0 (343 `unattributed` in one burst) and could poll for messages sent while the process was down | adapter present, not deployed — no run | adapter present, not deployed — no run |
| notice signing key | **absent**: `/etc/spacebridge/notice.key` does not exist. Since R6 (20:03Z) the pane reminder is delivered anyway, labelled `sig=none`, and recorded as `reminder_unsigned` | absent | present, derived from the bot token; two schemes, one key |
| notice line shape | **measured 2026-10-25 22:06Z**: the operator's own sentence with `[kind=notice ts=… sig=…]`, `notice_shape_declared` PASS (`shape ok, sig=none`) | same family as v6, unmeasured here | one `kind=` field missing; instruction signatures 16 hex — reported |
| code identity | `code_identity` in every `start` record; **`76c0560e2592ee51`** on the start at 21:03:50Z | the loop | loop + `reply.py` + `verify.py` + `doctor.py` — reported |
| idle window / poll | `interval_for()`: poll ≤ 30 s, pane read 5 s, inject timeout 10 s | not stated | beat 60 s, doctor timer 60 s, stale 180 s (coupled) |
| conformance run | **29 passed, 0 failed, 9 skipped** — exit 0 at 22:06Z with `--allow-skips C14,C15,C16,C17,C18,C20,C30` and `code_identity 76c0560e2592ee51`; exit 2 without the allowance | not run — adapter present, not deployed | not run — adapter present, not deployed |
| the nine skips (7 rule ids) | C14/C15/C16/C17 no renderer seam · C18 no word-set seam · C20 ×3 need a signing key · C30 supervision lives in the runner. Nine arms, seven ids, which is why the allowance names ids | — | — |
| own test suite | `selftest.py`: **64 arms, 0 failed** (measured 21:02Z) | 23 arms — reported | 34 arms — reported |
| log | `/root/.pi/dbg-bot2/dbg-bot.log` (2,429,781 B, mtime 22:06Z): **127 records since the 21:03:50Z start, 0 violations, 12 words all declared**. The whole file at 22:09Z replays 19,554 records and 230 violations in 15 classes — a count of that moment, since the file grows while the box runs — and every violation was written by code this sheet has since replaced — the `--log` mode reads the whole file on purpose and the box arms read only the running process | `dbg-bot.log`, no rotation | append-only JSONL, no rotation |

## sb2 — what changed on 2026-10-25, and the proof for each

Two restarts (19:51:20Z and 19:56:29Z), no other container touched. Both are recorded as `start` records
with a `code_identity`, so a claim about "the running code" can be checked against them.

| fix | cause it removed | proof |
|---|---|---|
| retention (C32) | `accepted` and `answered` were two 200-entry rings evicting independently, so an answered request looked open and its reminder fired — 19:32:49Z and 19:42:23Z, for requests answered 2026-10-22/23 | `log_reminder_after_answer_refused` PASS on the running process; the replay of the whole log names the 6 historical ones it would have caught |
| truncation (C12, withdrawn by R7 20:41Z — historical) | `sanitize()` sliced at 1,800 characters, so a long order was delivered cut short with no record | the truncation was removed and a 1,801-character instruction is now delivered whole (`t_long_instruction_is_delivered_whole`, box suite); the length *rule* C12 was withdrawn and its code abolished, so no arm asserts a refusal |
| addressing (C5, reversed by R7 20:41Z) | `addressing()` returned on the first positive test, so the mention set decided the answer | **R7 makes a bot ping sufficient and the other mentions content**, so the refusal was withdrawn: `gate_bot_ping_with_others_accepted` PASS (the stranger's `<@id>` survives in the instruction), plus `gate_stranger_only_refused` and `gate_role_only_refused` for messages that never pinged the bot |
| codes (C5) | `dm_channel_undefined`, `empty_instruction` predated the contract | renamed to `dm_stranger`, `empty`; `codes_are_distinct` PASS |
| unattributed answers (C18) | `reply.py` posted an answer with an id no instruction held, leaving the request open | unknown id now exits 4 and posts nothing; `--force` posts and records the force |
| notice shape measured, not skipped (C19) | the rule about the notice's look was folded together with the signature, so it SKIPped for want of a key while this sheet admitted the box broke it | split into shape (C19) and signature (C20). 22:06Z: `notice_shape_declared` **PASS** on sb2 (`shape ok, sig=none`); it went red first, which is how the missing `kind=`/`ts=` fields were found and fixed |
| pane reminder with no key (C20/R6) | the box withheld a reminder the agent needed, to protect a signature nobody was reading | `no_key_means_labelled_unsigned` PASS: the box's own line builder returns `[BRIDGE msg=… sig=none] …`; the box's own suite arm asserts delivery *and* the marker |
| reminder cadence (C22/R2) | the box ran the 10- and 60-minute notices that R2 abolished | `REMINDER_EVERY_S = 1200`; `log_no_abolished_reminder` PASS since start **and**, since the independent review, `notice_cadence_matches_box` PASS — the abolished-word arm alone never measured the cadence |

**Not changed, and why:** the notice's *signature* (C20). No key exists on this box, so a signed line cannot be
built and three arms are SKIP. Creating `/etc/spacebridge/notice.key` is the operator's act; it was blocked once
by a safety rule and was not worked around. R6 makes that missing key a degraded mode rather than a silence.

## What the review changed here

An agent on another host read the package and filed seven findings; the repairs are the table above plus the arms
added for nine rules that had none. The one thing it changed *in this sheet* is the row that used to say the notice
line "lacks C19's `kind=notice` and `ts=` fields" while calling the box conformant: the sheet can no longer claim
that, because an arm now measures it.

**A defect the replay found, and what it cost (2026-10-25 20:51Z).** Restarting the bridge produced 343 `unattributed`
records in one burst. Cause: `apply_answers()` reads `answers.jsonl` from `state['answers_offset']`, and startup began
at offset 0, so every historical answer was re-read — and because R3 closes the backlog at startup, almost every one
then matched "no accepted instruction with that id", which was false when it was answered. 336 answer records exist;
343 records were written. Fixed by starting the offset at the current end of the file, and pinned with the arm
`t_restart_does_not_replay_answer_history` in the box's own suite: history is not news. This one was found by the
log replay and by nothing else, which is the argument for having it.

## sb2 — the whole log replayed (18,697 records)

`run.py --log` reports **71 violations in 15 classes**, every one of them written by code that no longer
runs:

```
  24  illegal transition answered-with-receipt -> delivered
  14  illegal transition held -> delivered
   7  illegal transition expired -> delivered
   3  reminder after answer: notice_unsigned_not_injected
   3  reminder after answer: ticker-injected
```

The three `reminder after answer` pairs are tonight's six stale reminders. They are the reason C32 exists,
and the reason the arm now measures the running process rather than a fixed 24-hour window: a box that has
just been fixed must not be judged on records its previous code wrote.

## `debugger` and `bugger` — adapters, not deployments

`conformance/adapters/_peer.py` drives either box's own `bridge.py` unmodified. Point `PI_PEER_HOME` at a
directory holding that file (a mount, or a copy taken over ssh) and the suite measures that box:

```sh
PI_PEER_HOME=/mnt/debugger-bridge python3 conformance/run.py --box debugger
PI_PEER_HOME=/mnt/bugger-bridge   python3 conformance/run.py --box bugger
```

Neither has been run from here: no mount of either bridge exists on this host, and putting a file on those
machines is the operator's call. Until then their rows above are their own record, which is how three boxes
drifted in the first place.
