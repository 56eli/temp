# 12 — Measurements, 2026-10-31

*[agent: 2026-10-31 — sb3. Vantage: container `61981c58c9e7`, uid 0, cwd `/workspace`, bridge at
`/root/.pi/bridge`; no Docker socket, so only this cage's bridge was reachable. Times UTC.]*

Everything below was measured today unless it says otherwise. Commands are given so a reader can
repeat them; where a command writes, it wrote only under `/tmp`.

## 1. What is deployed

```
$ sha256sum /root/.pi/bridge/contract/CONTRACT.md
c26551c23282496ae4f70f750d3f77e566d006cc9dc10bbdf6f52ec3c178849b
$ git -C /home/ubuntu/botrunner show 09859c1:services/bridge-contract/CONTRACT.md | sha256sum
c26551c23282496ae4f70f750d3f77e566d006cc9dc10bbdf6f52ec3c178849b
$ git show 06a8f26:services/bridge-contract/CONTRACT.md | sha256sum     # contract branch head
c26551c23282496ae4f70f750d3f77e566d006cc9dc10bbdf6f52ec3c178849b
```

The deployed contract is byte-identical to the contract branch head (`06a8f26`) and to the devcage
commit `09859c1` it was installed from. `bridge.js`, `state.js` and `adapter.js` are byte-identical to
`09859c1`; `bot.js`, `reply.js` and `supervise.sh` carry the local deltas listed in
`reference/br1-live/PROVENANCE` (writer lock, trailing `--force`, heartbeat check in `reply.js`,
supervisor guards).

**Divergence found today:** the *devcage* branch head `16e4acd` adds **C33 attachments** to its own
copy of the contract (625 lines, 39 arms, 33 rules). The *contract* branch `06a8f26` does not contain
that commit (`git merge-base --is-ancestor 16e4acd origin/agent/bridge-contract-v7-2026-10-25` →
false). So "v7" currently names two texts; the deployed boxes run the one without C33.

## 2. The checker on the contract package

Extracted the branch to `/tmp/bsc` (`git archive origin/agent/bridge-contract-v7-2026-10-25`), then:

```
$ cd /tmp/bsc/bridge-contract && python3 tools/check.py
CHECK PASSED: 38 arms, 32 rules, 9 codes, one file            rc=0
```

Caveat, disclosed: the C1 check runs `git log` for `CONTRACT.md`, so the extracted copy failed C1
until I ran `git init` + one commit **in `/tmp`**. That is a property of the copy, not of the package.

```
$ python3 tools/check.py --adapters
adapters: 4 x 9 ops, 18 unreachable
  SKIP bugger.py … / debugger.py …   (their bridge.py is not mounted on this host)
CHECK FAILED: sb2.py 9 ops — no module /root/.pi/dbg-bot2 (this is not sb2's cage)
```

The sb2 failures are correct: that adapter imports sb2's own module, and this seat is not sb2. From
here, "the sb2 box passes" is a repository claim, not my measurement.

## 3. Conformance against the live sb3 box

Adapter: a nine-line `/tmp` wrapper that pipes each request to `node /root/.pi/bridge/adapter.js`
(read-only; it calls the box's own functions).

```
$ python3 conformance/run.py --box sb3br1 --allow-skips C14,C15,C16,C17,C18,C20,C30
…
PASS  gate_operator_accepted … PASS  codes_are_distinct
PASS  line_grammar_round_trip / line_flattens_multiline / line_is_one_line / directive_carries_message_id
PASS  notice_shape_declared          shape ok, sig=none
SKIP  notice_signature_verifies      no key on this box
SKIP  notice_truncated_signature_refused / notice_cross_class_refused
PASS  no_key_means_labelled_unsigned delivered and labelled sig=none
PASS  log_reminder_after_answer_refused   checked 20555 records since start
FAIL  log_transitions_legal          transitions outside the table:
      injected->reminder_unsigned, reminder_unsigned->delivered (2 requests)
PASS  notice_cadence_matches_box / log_no_abolished_reminder / log_words_declared
PASS  manifest_covers_every_arm / codes_are_declared / unaddressed_is_silence
PASS  ack_once_before_answer  52 acks / 51 answers, one each and in order
PASS  reminder_is_not_an_answer / no_orphan_holds / one_message_one_request / terminal_is_final
PASS  identity_reported  code_identity 8bc1b4517fa72e83 on the last start record
PASS  supervision_axes   ['loop_stopped','no_turn','process_gone']

box=sb3br1  34 passed, 1 failed, 3 skipped  (contract v7)      rc=1
```

Without `--allow-skips` the same three arms skip and the command adds an `UNMEASURED` line; the
exit code stays 1 because a failure outranks a skip. (Exit 2 is the code reserved for "skips you did
not name" when nothing failed.)

Also note the allowance had to name C14–C18 and C30 **even though those arms pass on this box** —
that is the contract branch's record of an older sb2 box, not this box's state. Run it without the
allowance on a modern Node box and read the skips you actually get (here: only the three C20 arms).

### The finding, precisely

```
$ python3 conformance/run.py --log /root/.pi/bridge/state/events.jsonl
replayed 20556 records
     2  illegal transition injected -> reminder_unsigned for <id>
     2  illegal transition reminder_unsigned -> delivered for <id>
4 violations in 2 classes
```

Both are real, live requests:

```
2026-10-28T10:39:55Z accepted   1564951845758046249
2026-10-28T10:39:55Z injected   1564951845758046249
2026-10-28T10:59:58Z reminder_unsigned  minutes=20
2026-10-28T11:00:08Z delivered  1564951845758046249
```

**Diagnosis: this is a contract defect, not a box bug.** `[states].ladder` includes `reminder` and
`reminder_unsigned`, but `[states].transitions` has no edge into or out of them, and the prose above
the block says notices are "excluded rather than legalised". Any box that fires a live reminder and
then delivers will trip this arm. Fix by either removing the two words from `ladder` (matching the
prose) or adding `[injected, reminder_unsigned]` and `[reminder_unsigned, delivered]` (matching
practice) — then re-run the replay.

## 4. Can-fail

```
$ python3 conformance/run.py --box sb3br1 --selftest
== baseline: sb3br1        34 passed, 1 failed, 3 skipped
== mutant: accept_all      23 passed, 12 failed, 3 skipped
   caught by 11 arms: codes_are_distinct, gate_bot_author_refused, gate_dm_stranger_refused,
   gate_empty_refused, gate_no_mention_refused, gate_other_author_refused, gate_role_only_refused,
   gate_stranger_only_refused, gate_wrong_channel_refused, gate_wrong_guild_refused,
   unaddressed_is_silence
== mutant: bad_sig         32 passed, 3 failed, 3 skipped
   caught by 2 arms: no_key_means_labelled_unsigned, notice_shape_declared
== mutant: bad_log         clean 0 violations; doctored 2 violations
SELFTEST PASSED: every mutation was caught
```

The already-red arm (`log_transitions_legal`) was excluded from the catch count, as the suite
requires: a mutation must turn a **green** arm red.

## 5. Live behaviour

```
$ sh /root/.pi/bridge/run.sh status
bridge: session running
bridge: loop live (last heartbeat 20s ago)
--- last 3 supervisor lines ---
2026-10-28T10:48:05.001Z another loop holds /root/.pi/bridge/state/loop.lock (pid 322); exiting
2026-10-28T10:48:05Z bridge exited rc=2; restarting
2026-10-28T10:48:05Z bridge: another loop holds the lock - not restarting
```

* Loop `pid 322`, started `2026-10-28T10:39:49Z`, uptime 275,524 s at 15:11Z; heartbeat every 30 s.
* The last three lines are a **second loop being refused** and the supervisor backing off — the
  writer-lock path working, live.
* This very instruction was relayed while the measurement ran:
  `15:09:24 accepted id=1566106827123466301 chars=432`, `15:09:25 injected`.
* Gate refusals over the whole log (20,556 records, 11,068 `refused`):
  `bot_author 9903, other_author 468, wrong_channel 450, pinged_other_user 231, pinged_nobody 15,
  empty 1`. The bot_author mass is bot DMs and other agents' traffic in the channel — normal, not a fault.

Adapter probes (all read-only):

```
config   → {"operator_id":"847445853584883712","bot_id":"1564946284094292069",
            "role_ids":["1564948507779923980"],"guild_id":"1489236876736069662",
            "channel_id":"1561512381480181860","reminder_every_s":1200,"pane":"=spac3:0.0"}
codes    → 8 codes (all declared; thread_not_in_scope is the declared optional gap)
vocab    → 32 words, all declared
line     → "[discord:addressed 2026-10-31T15:10:00Z msg=999] one two\n"
sign     → "BRIDGE REMINDER: … (request 999, 20 minutes). … [kind=notice ts=1792710000 sig=none]"
classify → accept / "status";  refuse / pinged_nobody;  etc.
```

## 6. Negative space — what was **not** verified

* **The other three bridges** (`pi-br1`, `sb2`, `devcage`) were not reachable from this seat: no
  Docker socket, and they are sibling containers. Their rows in `README.md` and `reference/BOXES.md`
  are the repository's own record, not my measurement.
* **A signed reminder on a live box.** No key exists here (`/etc/spacebridge/` absent), so the signed
  half of C20 is SKIP. The verifier is exercised by the sb2 box's own tests with a test key; I did
  not run that suite.
* **Attachments / C33.** Not deployed, so not exercisable. The branch code was read, not run.
* **A live DM lane.** The `dm_stranger` refusal is measured through the adapter; an actual DM
  round-trip was not performed (it needs the operator's account).
* **Thread behaviour.** The box has no thread policy; a thread under the channel would be
  `wrong_channel`. Not exercised against a real thread.
* **Post-failure behaviour.** The reference logs a failed answer post and leaves the request open;
  I did not induce a Discord failure to watch it.
* **Recovery from a real crash.** The restart window was read in the code and observed in records
  from 2026-10-28; I did not restart the live loop to reproduce it (that would be a state change).

## 7. Where the artifacts in this pack came from

| path | source |
|---|---|
| `reference/contract-v7/*` | `git archive origin/agent/bridge-contract-v7-2026-10-25` (head `06a8f26`), unmodified |
| `reference/br1-live/*` | the running files at `/root/.pi/bridge` (copied read-only, no secret present) |
| `reference/br1-live/config.example.json` | `09859c1:services/bridge-devcage/config.example.json` |
| the live config itself | **not copied**; it is 0600 and names paths only, but a config is deployment, not standard |
| token / notice key | **never read**; only their configured paths are named |

The only files written during this task were under `/tmp` (extraction, the throwaway git repo, the
adapter shim, this pack), `/root/.pi/handoff/ugger-2026-10-31/` (a copy of this pack), and the
publish to `56eli/placeholder` (2026-10-31T15:2xZ). The original target `56eli/temp` refused both
tokens with `403 ... denied to 56eli`; the owner then said "please push to placeholder instead".
