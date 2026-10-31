# 06 — Reminders and the notice

*[agent: 2026-10-31 — sb3. Rules C19, C20, C22; the live notice below was produced by the running box.]*

## Why a reminder exists

The operator (R2): remind every twenty minutes from prompt **entry** for an answer on Discord, and
stop when an outcome exists. R7 added the pane half: *"reminders to the agent are a good thing
because sometimes agents forget to answer."*

So a reminder has two audiences and two sinks:

| audience | sink | content |
|---|---|---|
| the human | the eligible channel | the notice sentence |
| the agent | the pane, as a typed line | the same notice sentence |

It is **not** an answer, it never occupies the answer slot (C23), and it is **not** a new instruction
— it carries no directive, so a well-written agent sees it as a cue, not a task.

## Cadence

```
every_s   = 1200
step      = n * every_s from entry, n = 1, 2, 3, ... with no upper bound
examples  = [20, 40, 60, 80, 100] minutes
```

The reference implementation computes `due = floor((now - entryAt) / 1200)` and fires when
`due > req.reminders`, which makes the n-th reminder due at `n * 1200 s` **from entry**, not from
delivery and not from the previous reminder. A prompt that never reached a turn still reminds.

The cadence is a **formula, not a list**, on purpose: an earlier version declared `minutes = [20,
40, 60]`, which would have made a conformant box that reminded at 80 minutes non-conformant for want
of a declared value. The contract now ships the formula and calls the list `examples`.

`notice_cadence_matches_box` measures it in two directions: the box's own `reminder_every_s` must
equal `[notice].every_s`, and the formula must reproduce the examples.

Measured on sb3, a real reminder (not a fixture):

```
entry  2026-10-28T10:39:55Z  accepted 1564951845758046249
fire   2026-10-28T10:59:58Z  reminder_unsigned  minutes=20
reply  2026-10-28T11:00:08Z  delivered / answered
```

## The notice line

The shape is the operator's own neutral sentence (2026-10-25 20:41Z), with the request id and the
minutes in the sentence and three machine fields in a trailing bracket:

```
BRIDGE REMINDER: A discord message hasn't been answered by you yet (request <id>, <minutes> minutes). The owner is still waiting for an answer on discord. If you are still working on the task you can finish it first, otherwise report back on discord. [kind=notice ts=<unix> sig=<64 hex|none>]
```

Normative grammar (`[notice].shape_grammar`, Python named groups; JS spells them `(?<name>`):

```regex
^BRIDGE REMINDER: A discord message hasn't been answered by you yet \(request (?P<msg>[0-9]+), (?P<minutes>[0-9]+) minutes\)\. The owner is still waiting for an answer on discord\. If you are still working on the task you can finish it first, otherwise report back on discord\. \[kind=notice ts=(?P<ts>[0-9]+) sig=(?P<sig>[0-9a-f]{64}|none)\]$
```

Why the shape is split from the signature (C19 vs C20): they used to be one rule that needed a key,
so on a box with no key the rule was unmeasurable — and the one box the deployment sheet measured
was violating it while no arm could go red. **Shape is a parser's job and is measurable always;
signature is a key's job.** That split is the single most useful lesson in the package.

## Signing

```
algorithm  = hmac-sha256
canonical  = kind=notice;msg={msg};minutes={minutes};ts={unix}
encoding   = lowercase hex, 64 chars
compare    = constant time, whole string
```

* The key is read from a file at call time (`cfg.notice_key`, default
  `/etc/spacebridge/notice.key`), trimmed; empty or absent ⇒ no key.
* A signed line proves the bridge wrote it. An unsigned one proves nothing — so the line says which
  it is (`sig=none`), and the record word says which it is (`reminder` vs `reminder_unsigned`).
* Verification refuses: a line that does not match the shape (`status: shape`), the literal `none`
  (`unsigned`), a missing key (`no-key`), and any mismatch — truncated, invented, or a valid
  signature for a *different* class of line (`signature`). Truncation is compared as a whole string,
  so a 63-character prefix cannot pass.
* The `ts` in the canonical form is the Unix second, and the verifier receives `ts` — a signature
  over a different timestamp fails, which is what makes replay detectable.

## Unsigned mode (R6)

*"just allow the pane reminder, it's internal communication"*

With no key provisioned:

* the pane reminder **is delivered**, labelled `sig=none`;
* the channel reminder is unchanged;
* the record is `reminder_unsigned`;
* nothing is withheld and nothing is invented.

What you must **not** do: emit a signature-shaped digest without a key. `no_key_means_labelled_unsigned`
fails a box that does (`sig=[0-9a-f]{64}` on an unsigned line), because that is a line claiming a
proof it cannot have.

Measured: `/etc/spacebridge/` does not exist on br1, so all four bridges that were checked run
unsigned; the three C20 signature arms are SKIP and must be named with `--allow-skips C20`. A signed
path was measured on the sb2 box's own tests with a test key; a **live signed** reminder has not been
observed on br1.

## Provisioning a key (if you want the signed path)

The operator's act, not the agent's — it was blocked once by a safety rule on br1 and not worked
around. Once a key exists, the three C20 arms stop skipping:

```sh
install -d -m 700 /etc/spacebridge
umask 077
# generate 32 random bytes, hex, without echoing them into a shell history:
head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n' > /etc/spacebridge/notice.key
chmod 600 /etc/spacebridge/notice.key
```

Both ends must use the same key bytes: the canonical string is hashed as UTF-8 text (the trimmed file
contents), not as decoded hex, unless your implementation injects a hex key explicitly (`sign`/`verify`
ops accept `key_hex`, which the suite uses for tests).

## Do you need reminders at all?

Yes, if a human is waiting. The failure mode without them is exactly the one the operator described:
an instruction was acknowledged and never became an answer, and nothing said so. If you run without
reminders, you lose the only signal that distinguishes "agent is thinking" from "agent never saw it"
— the `delivered`-with-no-`answered` axis in §07 depends on them.
