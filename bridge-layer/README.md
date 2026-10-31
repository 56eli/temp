# The pi bridge layer on br1 — a standard, an implementation, and a guide to copying it

**What this pack is.** Everything a third party needs to understand, run, and adapt the Discord
bridge layer that the pi agent cages on br1 use: the normative contract, the running code, the
conformance suite, the operational runbook, the measured state of the box on 2026-10-31, and a menu
of features you can take or leave.

**What this pack is not.** It is not a second authority. The authoritative artefacts are the files in
`reference/` — `CONTRACT.md` (the rules) and `RULINGS.md` (the only thing that can override them).
Where this pack's prose and those files disagree, those files win. My readings are tagged
`[agent: 2026-10-31 — sb3]`; measurements carry the UTC time they were taken.

---

## The layer in one page

A "bridge" is a small long-lived process, one per agent, that is the only channel between a human on
Discord and an agent sitting in a terminal pane:

```
Discord ──gateway──▶ gate ──▶ record ──▶ pane line ──▶ tmux pane ──▶ agent
                        │                                              │
                        └──── ack, reminders ◀── channel ◀── post ◀── reply tool ◀── agent writes
```

* **Inbound.** The loop receives a Discord message event, decides whether it is an *instruction*
  (the "gate"), writes an `accepted` record, posts an acknowledgement, renders exactly one line and
  types it into the agent's pane.
* **Outbound.** The agent answers by running a tool with the request id: `reply.js <message-id>
  "<text>"`. The tool validates the id and appends to a queue file; the loop tails that file, posts
  the answer to Discord and closes the request.
* **Memory.** Two append-only JSONL files: the event log (written by the loop) and the answer queue
  (written by the reply tool). There is no database, no daemon, no IPC, and no shared state between
  bridges. A restart deliberately forgets in-flight work.
* **Proof.** The rules live in one file that also carries a machine-readable block; the same file
  drives the code and a black-box conformance suite that can measure any box through a 9-operation
  JSON adapter. "A gate that cannot fail is not a gate" is enforced mechanically (`--selftest`).

The standard is `CONTRACT.md` v7: 32 rules (C1–C32) in the deployed copy, 38 conformance arms,
8 refusal codes. A newer branch commit adds C33 (attachments) for 33 rules / 39 arms — see
§"Two versions" below.

---

## Read this pack in this order

| # | file | what it settles |
|---|---|---|
| 1 | `01-architecture.md` | the components, the data flow, the topology, and why it is shaped this way |
| 2 | `02-the-contract.md` | what the contract is, how its machine block works, the rule inventory |
| 3 | `03-the-gate.md` | every test a message must pass, every refusal code, worked examples |
| 4 | `04-the-line-and-the-pane.md` | the exact bytes typed into a pane, and how injection is done safely |
| 5 | `05-records-states-and-restart.md` | the event vocabulary, the state ladder, restart semantics, the answer path |
| 6 | `06-reminders-and-the-notice.md` | cadence, the notice line's shape, HMAC signing and unsigned mode |
| 7 | `07-supervision-and-operations.md` | the three failure axes, the supervisor, the lock, the silent-bridge runbook |
| 8 | `08-conformance.md` | how to measure a box, the adapter protocol, exit codes, can-fail |
| 9 | `09-integration-guide.md` | step-by-step build: Discord app → install → seat a token → verify |
| 10 | `10-feature-menu.md` | **what you need and what you can skip**, with the cost of skipping |
| 11 | `11-porting-notes.md` | what is essential vs incidental (Discord, Node, tmux), and the pitfalls |
| 12 | `12-measurements-2026-10-31.md` | what I measured on br1, with commands, output and UTC |
| — | `reference/` | verbatim contract package, the running code, config example |

If you read only two files, read `10-feature-menu.md` and `reference/contract-v7/CONTRACT.md`.

---

## Two versions, and what br1 actually runs

| | deployed on the four br1 bridges | devcage branch head |
|---|---|---|
| contract | v7, commit `09859c1` (2026-10-26T00:11Z) | v7 + C33 attachments, commit `16e4acd` |
| rules / arms / codes | 32 / 38 / 9 | 33 / 39 / 9 |
| attachments | not supported: an addressed message with only a file is refused `empty` | accepted, file stored under the state dir, path appended to the pane line |

Measured 2026-10-31: the deployed `contract/CONTRACT.md` in this cage is **byte-identical** to
`origin/agent/bridge-contract-v7-2026-10-25` at `09859c1`, and also to that branch's head `06a8f26`
(sha256 `c26551c2…`). C33 does **not** exist on the contract branch. It was added on the *devcage*
branch at `16e4acd` ("owner model + C33 attachment rule; verified 36/0/3"), which carries its own
copy of the package — the two branches have diverged, and neither contains the other's head. C33 is
real code there and **not running here**. If you want attachments, take `16e4acd`'s package, not the
deployed copy — and say which branch you took, or the next reader will think "v7" means one thing.

---

## The four boxes on br1 (repository record, not re-measured here)

| bridge | cage | bridge dir | pane | notes |
|---|---|---|---|---|
| `debugger#8647` (SPACEBRAIN) | `pi-br1` | `/root/.pi/bridge` | `=spac:0.0` | |
| `rebugger#1482` | `sb2` | `/root/.pi/bridge243` | `spac2:0.0` | dir is `bridge243`, not `bridge` |
| `ugger#1344` | `sb3` | `/root/.pi/bridge` | `=spac3:0.0` | **the box measured in this pack** |
| `dev#2156` | `devcage` | `/home/dev/bridge` | `seat` | the reference Node implementation |

All four answer in guild `1489236876736069662`, channel `1561512381480181860`, from operator
`847445853584883712`. Each holds its **own copy** of `CONTRACT.md`; "four copies, one version" is the
thing to re-check when one bridge starts behaving differently from its neighbours.

Only `sb3` was reachable from this seat (no Docker socket; the other cages are sibling containers).
The other three rows are the repository's own record (`docs/BRIDGES.md`, measured 2026-10-29T15:2xZ).

---

## Status: measured 2026-10-31

* Contract copy identical to upstream `09859c1`; `tools/check.py` PASSES on an extracted copy
  (38 arms, 32 rules, 9 codes).
* Conformance against the live sb3 box: **34 passed, 1 failed, 3 skipped**; `--selftest` passes
  (every mutation caught). The one failure is a **ladder gap in the contract itself**, not a box
  bug: the box writes `reminder_unsigned` between `injected` and `delivered`, and the transition
  table has no edges for reminder words although the ladder list contains them. Reproduced twice in
  the live log (4 violations). See `12-measurements-2026-10-31.md`.
* 3 skips are the signed-notice arms: there is **no notice key** on this box
  (`/etc/spacebridge/` does not exist), so reminders are delivered labelled `sig=none` (R6).
* Loop uptime 275,524 s at 15:11Z (started 2026-10-28T10:39:49Z, pid 322), heartbeat every 30 s.

---

## Where this pack is published

`56eli/placeholder`, directory `bridge-layer/` — 2026-10-31, on the owner's instruction ("please push
to placeholder instead"). The original target `56eli/temp` was refused with `403 Permission to
56eli/temp.git denied to 56eli` for both tokens available on the box; the write token pushes to
`temp`'s siblings including `placeholder`, so the scope was the repository, not the credential.

## Licence, provenance, and how to correct this pack

The contract package and the code are the br1 estate's own work, published here for integration.
Provenance of every quote and measurement is inline. The operator's words are quoted verbatim in
`reference/contract-v7/RULINGS.md` and are the only override for any rule; nothing in this pack
raises a proposal to a rule.

Corrections: change `reference/CONTRACT.md`'s source first, then this prose — never the other way
round, or the two will disagree and you will believe the wrong one.
