#!/usr/bin/env python3
"""Conformance suite — black-box arms against any box, over its own adapter.

    python3 run.py --list                  # the arms, the rule each enforces, what it must catch
    python3 run.py --box sb2               # every arm; a box that cannot answer an arm is SKIP
    python3 run.py --log <path> [--since]  # replay a box's own records
    python3 run.py --selftest --box sb2    # can-fail: three mutations, the suite must go red
    python3 run.py --box sb2 --allow-skips C19,C20   # the documented no-key case, named in the command

Exit codes, because a machine reads only this one:
    0  every declared arm ran and passed (skips only where the command names the rule it allows)
    1  at least one arm failed
    2  an arm was skipped that the command did not allow — an unmeasured rule is not a satisfied one

A box is a command that speaks JSON on stdin and stdout (`adapters/`, `ADAPTER` section below); no
daemon, no shared state, no import of a box's internals. That is why the same suite measures a bridge
in another container or on another host.

An arm returns True (pass), False (fail) or None (SKIP). **SKIP is never a pass**: an unmeasured rule
is not a satisfied one. The contract's block in `../CONTRACT.md` declares every arm; `tools/check.py`
fails when a declared arm has no implementation or an implementation is undeclared (C28).

## ADAPTER — the protocol

`config` → `{operator_id, bot_id, role_ids[], guild_id, channel_id}` · `classify {msg,cfg}` →
`{action, code, instruction}` · `sign {msg_id,minutes,ts,key_hex}` → `{line}` · `verify {line,key_hex,ts}`
→ `{rc,status}` · `line {msg_id,text,ts}` → `{line}` · `vocabulary` → `{words}` · `log` → `{path}` ·
`codes` → `{codes}` (the refusal codes the box can emit, as data). A field a box cannot answer is `null`,
and the arm it feeds is SKIP — which the exit code treats as unmet unless the command allows it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTRACT = tomllib.loads(
    re.search(r"```toml\n(.*?)\n```", (ROOT / "CONTRACT.md").read_text(encoding="utf-8"), re.S).group(1)
)
ARMS = CONTRACT["arm"]
CODES = {k for k, v in CONTRACT["codes"].items() if isinstance(v, str) and k != "rule"}
WORDS = set(CONTRACT["receipts"]["event"]) | set(CONTRACT["receipts"]["operational"]) | set(
    CONTRACT["receipts"]["forward"]
)
ABOLISHED = set(CONTRACT["receipts"]["abolished"])
TRANSITIONS = {tuple(t) for t in CONTRACT["states"]["transitions"]}
LADDER = set(CONTRACT["states"]["ladder"])
REMINDER_WORDS = {"ticker-injected", "reminder", "notice10", "notice60", "notice_unsigned_not_injected"}
ANSWER_WORDS = {"answered-with-receipt", "answered-without-receipt", "delivered"}

STRANGER = "361033318273384449"
FOREIGN_ROLE = "999999999999999999"
LIMIT = int(CONTRACT["instruction"]["max_instruction_chars"])


# ------------------------------------------------------------------ a box, as a command

class Box:
    def __init__(self, name: str, mutant: str | None = None):
        script = HERE / "adapters" / f"{name}.py"
        if not script.exists():
            raise SystemExit(f"no adapter for box {name!r}: expected {script}")
        self.name = name
        self.mutant = mutant
        self._config: dict | None = None
        self.env = dict(os.environ)
        if mutant:
            self.env["PI_TARGET"] = str(script)
            self.env["PI_MUTANT"] = mutant
            self.command = [sys.executable, str(HERE / "adapters" / "_proxy.py")]
        else:
            self.command = [sys.executable, str(script)]

    def call(self, op: str, **req) -> dict:
        payload = json.dumps({"op": op, **req})
        proc = subprocess.run(self.command, input=payload, capture_output=True, text=True, env=self.env, timeout=120)
        if proc.returncode != 0:
            return {"error": f"adapter rc={proc.returncode}: {proc.stderr.strip()[:300]}"}
        try:
            return json.loads(proc.stdout or "{}")
        except json.JSONDecodeError:
            return {"error": f"adapter printed non-JSON: {proc.stdout[:200]}"}

    def config(self) -> dict:
        if self._config is None:
            self._config = self.call("config")
            if "error" in self._config:
                raise SystemExit(f"box {self.name}: {self._config['error']}")
        return self._config


def ids(box: Box) -> dict:
    cfg = box.config()
    roles = [str(r) for r in (cfg.get("role_ids") or [])]
    return {
        "bot": str(cfg["bot_id"]),
        "operator": str(cfg["operator_id"]),
        "role": roles[0] if roles else "0",
        "channel": str(cfg["channel_id"]),
        "guild": str(cfg["guild_id"]),
    }


def message_for(box: Box, **over) -> dict:
    """A message Discord could deliver: `content` follows `mentions`, as it does upstream.

    A fixture whose text disagrees with its mention array is impossible in life, and a gate that refuses
    it is not more correct — it is measuring the fixture.
    """
    known = ids(box)
    base = {
        "id": "1563900000000000001",
        "channel_id": known["channel"],
        "guild_id": known["guild"],
        "author": {"id": known["operator"], "bot": False},
        "mentions": [{"id": known["bot"], "bot": True}],
        "mention_roles": [],
        "dm": False,
        "thread_parent_id": None,
        "text": "status",
    }
    base.update(over)
    if "content" not in over:
        parts = [f"<@{m['id']}>" for m in base["mentions"]] + [f"<@&{r}>" for r in base["mention_roles"]]
        text = base.pop("text", "")
        base["content"] = " ".join(parts + ([text] if text else []))
    return base


def verdict(box: Box, msg: dict) -> dict:
    return box.call("classify", msg=msg, cfg=box.config())


def expect_accept(box: Box, msg: dict):
    got = verdict(box, msg)
    if "error" in got:
        return None, got["error"]
    ok = got.get("action") == "accept"
    return ok, f"expected accept, got {got.get('action')}/{got.get('code')}"


def expect_refusal(box: Box, msg: dict, code: str):
    got = verdict(box, msg)
    if "error" in got:
        return None, got["error"]
    ok = got.get("action") == "refuse" and got.get("code") == code
    return ok, f"expected refuse/{code}, got {got.get('action')}/{got.get('code')}"


# ------------------------------------------------------------------ arms: the gate (C3–C13)

def arm_gate_operator_accepted(box):
    return expect_accept(box, message_for(box))


def arm_gate_role_mention_accepted(box):
    return expect_accept(box, message_for(box, mentions=[], mention_roles=[ids(box)["role"]]))


def arm_gate_bot_ping_with_others_accepted(box):
    """C5, R7: a ping to the bot is a sufficient address, whatever else the message mentions.

    Operator, 2026-10-25 20:41Z, verbatim: "Any ping to bot is a valid request further specific with message
    contents addressing individual parties for custom requests." This arm replaces two refusals that were the
    opposite rule: a bot ping plus a stranger, and a bot ping plus a foreign role, both of which used to be refused.
    """
    known = ids(box)
    msg = message_for(box, mentions=[{"id": known["bot"]}, {"id": STRANGER}], mention_roles=[FOREIGN_ROLE])
    out = box.call("classify", msg=msg, cfg=box.config())
    action = out.get("action")
    if action is None:
        return None, "box exposes no gate"
    if action != "accept":
        return False, f"a ping to the bot with other mentions was {action!r} ({out.get('code')!r})"
    instruction = str(out.get("instruction") or "")
    # The bot's own ping is the addressing prefix and is stripped on purpose; the *other* party is content and must
    # survive, because that is the whole point of a request that names who each part is for.
    if STRANGER not in instruction:
        return False, f"the instruction dropped the other party it should have carried: {instruction[:90]!r}"
    return True, "accepted, and the other party is preserved as content"


def arm_gate_no_mention_refused(box):
    return expect_refusal(box, message_for(box, mentions=[], mention_roles=[]), "pinged_nobody")


def arm_gate_stranger_only_refused(box):
    return expect_refusal(box, message_for(box, mentions=[{"id": STRANGER}], mention_roles=[]), "pinged_other_user")


def arm_gate_role_only_refused(box):
    """R7: an unheld role is not an address to the bot, and `foreign_role` is abolished. The diagnosis is the same
    one an unmentioned message gets — this bot was not addressed."""
    return expect_refusal(box, message_for(box, mentions=[], mention_roles=[FOREIGN_ROLE]), "pinged_nobody")


def arm_gate_other_author_refused(box):
    return expect_refusal(box, message_for(box, author={"id": STRANGER, "bot": False}), "other_author")


def arm_gate_bot_author_refused(box):
    return expect_refusal(box, message_for(box, author={"id": "1561535600186753135", "bot": True}), "bot_author")


def arm_gate_wrong_channel_refused(box):
    return expect_refusal(box, message_for(box, channel_id="1561512381480181861"), "wrong_channel")


def arm_gate_wrong_guild_refused(box):
    return expect_refusal(box, message_for(box, guild_id="1194598173742731284"), "wrong_guild")


def arm_gate_dm_stranger_refused(box):
    return expect_refusal(
        box, message_for(box, dm=True, channel_id="9", guild_id=None, author={"id": STRANGER, "bot": False}), "dm_stranger"
    )


def arm_gate_empty_refused(box):
    return expect_refusal(box, message_for(box, text=""), "empty")


def arm_codes_are_distinct(box):
    known = ids(box)
    cases = {
        "pinged_nobody": message_for(box, mentions=[], mention_roles=[]),
        # R7: a bot ping plus a stranger is accepted, so the case that reaches this code is a message aimed at
        # somebody else and not at this bot at all.
        "pinged_other_user": message_for(box, mentions=[{"id": STRANGER}], mention_roles=[]),
        "other_author": message_for(box, author={"id": STRANGER, "bot": False}),
        "bot_author": message_for(box, author={"id": "1561535600186753135", "bot": True}),
        "wrong_channel": message_for(box, channel_id="1561512381480181861"),
        "wrong_guild": message_for(box, guild_id="1194598173742731284"),
        "dm_stranger": message_for(box, dm=True, channel_id="9", guild_id=None, author={"id": STRANGER, "bot": False}),
        "empty": message_for(box, text=""),
    }
    seen: dict[str, str] = {}
    for want, msg in cases.items():
        got = verdict(box, msg).get("code")
        if got in seen:
            return False, f"{want} and {seen[got]} both reported {got}"
        seen[got] = want
    wrong = [f"{want}->{got}" for want, got in seen.items() if got != want]
    return (not wrong), "distinct" if not wrong else "; ".join(wrong)


# ------------------------------------------------------------------ arms: the line (C14–C17)

def arm_line_grammar_round_trip(box):
    out = box.call("line", msg_id="1563900000000000002", text="status", ts="2026-10-25T12:00:00Z")
    line = out.get("line")
    if line is None:
        return None, "box does not expose its renderer"
    pattern = re.compile(CONTRACT["line"]["directive_grammar"])
    m = pattern.match(line)
    if not m:
        return False, f"line does not match the grammar: {line!r}"
    return m.group("msg") == "1563900000000000002", f"id in the line is {m.group('msg')}"


def arm_line_flattens_multiline(box):
    out = box.call("line", msg_id="1563900000000000003", text="one\ntwo\rthree", ts="2026-10-25T12:00:00Z")
    line = out.get("line")
    if line is None:
        return None, "box does not expose its renderer"
    if line.count("\n") != 1 or not line.endswith("\n"):
        return False, f"line is not one line with one newline: {line!r}"
    return "one two three" in line, f"text was not flattened: {line!r}"


def arm_vocabulary_is_closed(box):
    listed = box.call("vocabulary").get("words")
    if listed is None:
        return None, "box exposes no vocabulary op, so its words cannot be judged from outside"
    extra = sorted(set(listed) - WORDS)
    return (not extra), f"undeclared words: {extra}" if extra else "all words declared"


# ------------------------------------------------------------------ arms: the notice (C19–C20)

def _notice_key() -> bytes | None:
    path = CONTRACT["notice"].get("test_key_path", "/etc/spacebridge/notice.key")
    try:
        return Path(path).read_bytes().strip() or None
    except OSError:
        return None


def arm_notice_shape_declared(box):
    """C19: the notice's *shape*, measurable with no key at all.

    Splitting shape from signature is the fix for the defect that made C19 unmeasurable: the one rule about what a
    notice looks like was admitted to be violated by the one box the deployment sheet measured, and no arm could go
    red about it. Shape is a parser's job; the signature is C20's.
    """
    out = box.call("sign", msg_id="1563900000000000008", minutes=20, ts=1792710000, key_hex=None)
    line = out.get("line")
    if not line:
        return None, "box exposes no notice-line builder"
    pattern = re.compile(CONTRACT["notice"]["shape_grammar"])
    m = pattern.match(line)
    if not m:
        fields = CONTRACT["notice"]["shape_fields"]
        present = [f for f in fields if f + "=" in line]
        return False, f"line lacks {sorted(set(fields) - set(present))}: {line.strip()[:110]!r}"
    return True, f"shape ok, sig={'none' if m.group('sig') == 'none' else '64 hex'}"


def arm_notice_cadence_matches_box(box):
    """C22: the cadence is a formula, and this arm asks the box what its own constant says.

    The defect this closes (independent review, 2026-10-25): C22 was "armed" only by
    `log_no_abolished_reminder`, which measures the two abolished *words* and says nothing about 1200 s. An arm that
    asserts a proxy makes a rule look measured when it is not — so the cadence gets an arm of its own, and the proxy
    keeps its own name and its own meaning.

    Measurable in two directions: the box's constant must equal `[notice].every_s`, and the declared `step` formula must
    reproduce the declared `examples`. A box whose cadence is 600 s goes red naming both numbers.
    """
    notice = CONTRACT["notice"]
    every = int(notice.get("every_s", 0))
    if every <= 0:
        return False, "no [notice].every_s to check"
    examples = [int(x) for x in notice.get("examples", [])]
    formula = [every * n // 60 for n in range(1, len(examples) + 1)]
    if formula != examples:
        return False, f"step formula gives {formula} minutes, contract says {examples}"
    got = box.call("config")
    if not isinstance(got, dict) or got.get("reminder_every_s") is None:
        return None, "box exposes no reminder-cadence seam (config op returns no reminder_every_s)"
    theirs = int(got["reminder_every_s"])
    return theirs == every, f"box reminds every {theirs} s, contract says {every} s"


def arm_notice_signature_verifies(box):
    key = _notice_key()
    if not key:
        # No key on this host means no signed line can be built, so nothing here can be measured. R6 makes the
        # *unsigned* delivery measurable instead, and `no_key_means_labelled_unsigned` measures it.
        return None, "no key on this box: a signed line cannot be built, so it cannot be verified"
    out = box.call("sign", msg_id="1563900000000000004", minutes=20, ts=1792710000, key_hex=key.hex())
    line = out.get("line")
    if not line:
        return None, "box produced no line (no key provisioned on this box)"
    got = box.call("verify", line=line, key_hex=key.hex(), ts=1792710000)
    return got.get("rc") == 0, f"verify answered rc={got.get('rc')} {got.get('status')}"


def arm_notice_truncated_signature_refused(box):
    key = _notice_key()
    if not key:
        return None, "no key on this box, so a signature cannot be built to truncate"
    out = box.call("sign", msg_id="1563900000000000005", minutes=20, ts=1792710000, key_hex=key.hex())
    line = (out.get("line") or "").rstrip("\n")
    if not line:
        return None, "box produced no line"
    short = re.sub(r"sig=[0-9a-f]{64}", "sig=" + "0" * 63, line) + "\n"
    tail = re.sub(r"sig=([0-9a-f]{63})([0-9a-f])", lambda m: "sig=" + m.group(1) + ("0" if m.group(2) != "0" else "1"), line) + "\n"
    a = box.call("verify", line=short, key_hex=key.hex(), ts=1792710000)
    b = box.call("verify", line=tail, key_hex=key.hex(), ts=1792710000)
    ok = a.get("rc") != 0 and b.get("rc") != 0
    return ok, f"truncated rc={a.get('rc')}, flipped-tail rc={b.get('rc')}"


def arm_notice_cross_class_refused(box):
    key = _notice_key()
    if not key:
        return None, "no key on this box"
    line = "[BRIDGE kind=instruction msg=1563900000000000006 minutes=20 ts=1792710000 sig=" + "0" * 64 + "]\n"
    got = box.call("verify", line=line, key_hex=key.hex(), ts=1792710000)
    return got.get("rc") != 0, f"cross-class line answered rc={got.get('rc')}"


def arm_no_key_means_labelled_unsigned(box):
    """C20 + R6: with no key the pane reminder is delivered, and it says `sig=none`. A line that carries a
    signature-shaped hex without a key would be worse than either — it would claim a proof it cannot have."""
    out = box.call("sign", msg_id="1563900000000000007", minutes=20, ts=1792710000, key_hex=None)
    line = out.get("line")
    if line is None:
        return None, "box exposes no signing seam"
    if line == "":
        return False, "box withheld the reminder; R6 requires it delivered and labelled"
    marker = CONTRACT["notice"].get("unsigned_marker", "sig=none")
    if marker not in line:
        return False, f"unsigned reminder is not labelled: {line!r}"
    if re.search(r"sig=[0-9a-f]{64}", line):
        return False, "unsigned reminder carries a signature-shaped digest"
    return True, f"delivered and labelled {marker}"


# ------------------------------------------------------------------ arms: records (C18, C24, C32)

def _records(box, since=None) -> list[dict] | dict:
    """The box's own records, from the start of the running process unless `since` says otherwise.

    A window is not a detail: before 2026-10-25 these arms read a fixed 24 hours, so a box that had just been
    fixed still failed on records its previous code wrote. The running code is what a conformance run is about,
    so the window opens at the last `start` record — and a box that writes no `start` has no window and SKIPs.
    """
    out = box.call("log")
    path = out.get("path")
    if not path:
        return {"error": "box does not expose its log path"}
    rows = []
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        rows.append(rec)
    if since:
        return [r for r in rows if str(r.get("ts", "")) >= since]
    starts = [i for i, r in enumerate(rows) if str(r.get("event")) == "start"]
    if not starts:
        return {"error": "no `start` record, so the running code's window cannot be found"}
    return rows[starts[-1]:]


def _window() -> str:
    return (dt.datetime.utcnow() - dt.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")


def arm_log_reminder_after_answer_refused(box):
    rows = _records(box)
    if isinstance(rows, dict):
        return None, rows["error"]
    answered, bad = set(), []
    for rec in rows:
        mid = str(rec.get("id") or "")
        event = str(rec.get("event") or "")
        if event in ANSWER_WORDS:
            answered.add(mid)
        elif event in REMINDER_WORDS and mid and mid in answered:
            bad.append(f"{event} at {mid}")
    return (not bad), f"reminder after an answer: {bad[:5]}" if bad else f"checked {len(rows)} records since start"


def arm_log_transitions_legal(box):
    rows = _records(box)
    if isinstance(rows, dict):
        return None, rows["error"]
    state, bad = {}, []
    for rec in rows:
        mid, event = str(rec.get("id") or ""), str(rec.get("event") or "")
        if not mid or event not in LADDER:
            continue
        prev = state.get(mid)
        if prev is None:
            state[mid] = event
            continue
        if (prev, event) not in TRANSITIONS and prev != event:
            bad.append(f"{prev}->{event} at {mid}")
        state[mid] = event
    return (not bad), f"transitions outside the table: {bad[:5]}" if bad else f"checked {len(rows)} records since start"


def arm_log_words_declared(box):
    rows = _records(box)
    if isinstance(rows, dict):
        return None, rows["error"]
    seen = {str(r.get("event")) for r in rows if r.get("event")}
    extra = sorted(seen - WORDS)
    return (not extra), f"undeclared words since start: {extra}" if extra else f"{len(seen)} words since start, all declared"


def arm_log_no_abolished_reminder(box):
    rows = _records(box)
    if isinstance(rows, dict):
        return None, rows["error"]
    bad = [str(r.get("event")) for r in rows if str(r.get("event")) in ABOLISHED]
    return (not bad), f"abolished reminder words still written: {len(bad)}" if bad else "no abolished reminder since start"


# ------------------------------------------------------------------ arms: derived (C28–C29)


def arm_unaddressed_is_silence(box):
    """C2: an unaddressed message is silence — refused once, named, and nothing left to type into the pane."""
    out = box.call("classify", msg=message_for(box, mentions=[], mention_roles=[]), cfg=box.config())
    action = out.get("action")
    if action is None:
        return None, "box exposes no gate"
    if action != "refuse":
        return False, f"an unaddressed message was {action!r}"
    if out.get("code") != "pinged_nobody":
        return False, f"refused as {out.get('code')!r}, so the diagnosis was lost"
    if out.get("instruction"):
        return False, f"a refusal carried an instruction: {str(out['instruction'])[:60]!r}"
    return True, "silent, one refusal, nothing to type"


def arm_line_is_one_line(box):
    """C14: the pane line is the directive, then the text, then exactly one newline."""
    out = box.call("line", msg_id="1563900000000000012", text="first\nsecond", ts=1792710000)
    line = out.get("line")
    if line is None:
        return None, "box does not expose its renderer"
    if not line.endswith("\n"):
        return False, f"no terminating newline: {line!r}"
    if line.count("\n") != 1:
        return False, f"{line.count(chr(10))} newlines: the pane would see {line.count(chr(10)) + 1} lines"
    if "first" not in line or "second" not in line:
        return False, "the text did not survive rendering"
    return True, "directive, text, one newline"


def arm_directive_carries_message_id(box):
    """C16: the id in the directive is the instruction's own message id, so a reply can name the request."""
    mid = "1563900000000000013"
    out = box.call("line", msg_id=mid, text="x", ts=1792710000)
    line = out.get("line")
    if line is None:
        return None, "box does not expose its renderer"
    if mid not in line:
        return False, f"the directive does not carry {mid}: {line.strip()[:100]!r}"
    return True, "message id present in the directive"


def arm_ack_once_before_answer(box):
    """C21: one acknowledgement per request, keyed by message id, and it precedes the answer.

    Measured from the records the box writes: `accepted` is written when the ack is posted, so a second
    `accepted` for one id is a second ack, and an answer that precedes its `accepted` record means the answer
    went out first.
    """
    rows = _records(box)
    if isinstance(rows, dict):
        return None, rows["error"]
    seen, first_accept, answers = {}, {}, {}
    for rec in rows:
        ev, mid = str(rec.get("event")), str(rec.get("id") or "")
        if ev == "accepted" and mid:
            seen[mid] = seen.get(mid, 0) + 1
            first_accept.setdefault(mid, str(rec.get("ts")))
        if ev == "reply" and rec.get("reply_to"):
            answers.setdefault(str(rec["reply_to"]), str(rec.get("ts")))
    doubled = sorted(i for i, n in seen.items() if n > 1)
    if doubled:
        return False, f"{len(doubled)} request(s) acknowledged more than once: {doubled[:3]}"
    early = [i for i, ts in answers.items() if i in first_accept and first_accept[i] > ts]
    if early:
        return False, f"answered before acknowledged: {early[:3]}"
    return True, f"checked {len(seen)} ack(s) and {len(answers)} answer(s), one each and in order"


def arm_reminder_is_not_an_answer(box):
    """C23: a reminder never occupies the answer slot — it carries no answer fields at all."""
    rows = _records(box)
    if isinstance(rows, dict):
        return None, rows["error"]
    seen, bad = 0, []
    for rec in rows:
        if str(rec.get("event")) != "reminder":
            continue
        seen += 1
        answer_fields = [f for f in ("reply_to", "chars", "parts") if f in rec]
        if answer_fields:
            bad.append(f"{rec.get('id')} carries {answer_fields}")
        if not rec.get("id") or "minutes" not in rec:
            bad.append(f"{rec.get('id')} does not name its request and its minutes")
    if bad:
        return False, f"{len(bad)} reminder(s) shaped like answers: {bad[:2]}"
    return True, f"checked {seen} reminder record(s), none in the answer slot"


def arm_no_orphan_holds(box):
    """C25: a held instruction is drained later, or the process that held it ended. No third case."""
    rows = _records(box)
    if isinstance(rows, dict):
        return None, rows["error"]
    later: dict[str, int] = {}
    held: list[tuple[int, str]] = []
    for i, rec in enumerate(rows):
        ev, mid = str(rec.get("event")), str(rec.get("id") or "")
        if ev == "start":
            later = {}  # R3: a restart closes everything non-terminal, silently and finally
        if ev == "held" and mid:
            held.append((i, mid))
        for word in ("injected", "injected-queued", "delivered", "ticker-held", "queued"):
            if ev == word and mid:
                later[mid] = i
        if ev.startswith("answered") and mid:
            later[mid] = i
    orphan = [(i, mid) for i, mid in held if later.get(mid, -1) < i]
    if orphan:
        return False, f"{len(orphan)} held instruction(s) never drained: {[m for _, m in orphan[:3]]}"
    return True, f"checked {len(held)} hold(s), every one drained or closed by a restart"


def arm_one_message_one_request(box):
    """C26: one Discord message id is one request, however many times the poller sees it."""
    rows = _records(box)
    if isinstance(rows, dict):
        return None, rows["error"]
    counts: dict[str, int] = {}
    for rec in rows:
        if str(rec.get("event")) == "accepted" and rec.get("id"):
            counts[str(rec["id"])] = counts.get(str(rec["id"]), 0) + 1
    doubled = sorted(i for i, n in counts.items() if n > 1)
    if doubled:
        return False, f"{len(doubled)} message id(s) accepted twice: {doubled[:3]}"
    return True, f"checked {len(counts)} accepted record(s), one per message id"


def arm_terminal_is_final(box):
    """C27: a terminal state is final — no request carries two of them."""
    rows = _records(box)
    if isinstance(rows, dict):
        return None, rows["error"]
    terminal = set(CONTRACT["states"]["terminal"])
    counts: dict[str, list[str]] = {}
    for rec in rows:
        ev, mid = str(rec.get("event")), str(rec.get("id") or "")
        if ev in terminal and mid:
            counts.setdefault(mid, []).append(ev)
    twice = {i: v for i, v in counts.items() if len(v) > 1}
    if twice:
        head = list(twice.items())[:2]
        return False, f"{len(twice)} request(s) reached a terminal state twice: {head}"
    return True, f"checked {len(counts)} terminal record(s), one per request"


def arm_identity_reported(box):
    """C31: the running code says what it is, on the record, at start — loop, reply tool and verifier together."""
    rows = _records(box)
    if isinstance(rows, dict):
        return None, rows["error"]
    starts = [r for r in rows if str(r.get("event")) == "start"]
    if not starts:
        return None, "box writes no start record, so its identity cannot be read"
    ident = str(starts[-1].get("code_identity") or "")
    if not ident:
        return False, "the start record carries no code_identity"
    if not re.fullmatch(r"[0-9a-f]{16}", ident):
        return False, f"code_identity is not sixteen hex characters: {ident!r}"
    return True, f"code_identity {ident} on the last start record"


def arm_supervision_axes(box):
    """C30: three axes, each with its own evidence. A heartbeat proves the loop and never the process."""
    out = box.call("supervision")
    axes = out.get("axes")
    if axes is None:
        return None, "box exposes no supervision seam: process, loop and idle are watched elsewhere"
    required = set(CONTRACT["supervision"]["axes"])
    missing = sorted(required - set(axes))
    if missing:
        return False, f"no evidence for {missing}"
    return True, f"three axes present: {sorted(required)}"


def arm_manifest_covers_every_arm(box):
    declared = {a["name"] for a in ARMS}
    implemented = {n[len("arm_"):] for n in globals() if n.startswith("arm_")}
    missing = sorted(declared - implemented)
    extra = sorted(implemented - declared)
    for arm in ARMS:
        if arm["rule"] not in CONTRACT["rules"]:
            return False, f"{arm['name']} cites {arm['rule']}, which the registry does not define"
    return (not missing and not extra), f"missing={missing} extra={extra}"


def arm_codes_are_declared(box):
    """C29, measured from outside instead of guessed from source text.

    The earlier body scanned the adapter's own file for a fixed token list, so a box that worded its refusals in
    prose passed without being measured at all — and it was never actually replaced, which the suite caught only
    when a code was abolished and the arm stayed green. The box now says which codes it can emit and the comparison
    runs both ways.
    """
    listed = box.call("codes").get("codes")
    if listed is None:
        return None, "box cannot enumerate its refusal codes"
    emitted = {str(c) for c in listed}
    extra = sorted(emitted - CODES)
    optional = set(CONTRACT["codes"].get("optional") or [])
    missing = sorted(CODES - emitted - optional)
    if extra:
        abolished = [c for c in extra if c in (CONTRACT["codes"].get("abolished") or {})]
        why = f" (abolished by ruling: {abolished})" if abolished else ""
        return False, f"codes the box emits but the contract does not declare: {extra}{why}"
    if missing:
        return False, f"declared codes the box cannot emit: {missing}"
    return True, f"{len(emitted)} codes, all declared, none missing"


# ------------------------------------------------------------------ log replay (whole file)

def check_log(rows: list[dict]) -> list[str]:
    violations: list[str] = []
    answered, state = set(), {}
    for rec in rows:
        mid, event = str(rec.get("id") or ""), str(rec.get("event") or "")
        if event and event not in WORDS:
            violations.append(f"undeclared event '{event}' for {mid}")
        if mid and event in ANSWER_WORDS:
            answered.add(mid)
        elif mid and event in REMINDER_WORDS and mid in answered:
            violations.append(f"reminder after answer: {event} for {mid}")
        if not mid or event not in LADDER:
            continue
        prev = state.get(mid)
        if prev is not None and prev != event and (prev, event) not in TRANSITIONS:
            violations.append(f"illegal transition {prev} -> {event} for {mid}")
        state[mid] = event
    return violations


def summarise(violations: list[str]) -> None:
    grouped: dict[str, int] = {}
    for item in violations:
        key = re.sub(r"for [0-9]+$", "for <id>", item)
        key = re.sub(r"for ticker-selftest", "for <id>", key)
        grouped[key] = grouped.get(key, 0) + 1
    for key, count in sorted(grouped.items(), key=lambda kv: -kv[1]):
        print(f"  {count:6d}  {key}")
    for item in violations[:10]:
        print("  example:", item)
    print(f"{len(violations)} violations in {len(grouped)} classes")


# ------------------------------------------------------------------ runner

def run_box(box: Box, allowed: set[str] | None = None) -> tuple[int, int, int, set[str], set[str]]:
    allowed = allowed or set()
    passed = failed = skipped = 0
    unallowed: set[str] = set()
    red: set[str] = set()
    for arm in ARMS:
        fn = globals().get("arm_" + arm["name"])
        if fn is None:
            print(f"FAIL  {arm['name']:<34} {arm['rule']:<5} declared but not implemented")
            failed += 1
            continue
        try:
            ok, detail = fn(box)
        except Exception as exc:  # an arm that crashes is a failure, not a skip
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        if ok is None:
            mark = "" if arm["rule"] in allowed else "  [not allowed]"
            print(f"SKIP  {arm['name']:<34} {arm['rule']:<5} {detail}{mark}")
            skipped += 1
            if arm["rule"] not in allowed:
                unallowed.add(arm["name"])
        elif ok:
            print(f"PASS  {arm['name']:<34} {arm['rule']:<5} {detail}")
            passed += 1
        else:
            print(f"FAIL  {arm['name']:<34} {arm['rule']:<5} {detail}")
            failed += 1
            red.add(arm["name"])
    return passed, failed, skipped, unallowed, red


def selftest(box_name: str) -> int:
    """Can-fail: mutate one answer at a time and require the suite to notice (C28)."""
    print(f"== baseline: {box_name}")
    base = Box(box_name)
    p0, f0, s0, u0, red0 = run_box(base)
    print(f"box={box_name}  {p0} passed, {f0} failed, {s0} skipped\n")
    problems = []
    if red0:
        # A box may legitimately be red on a real defect. Those arms are excluded from the proof: a mutation must
        # turn an arm that was GREEN red, or the can-fail claim is measuring the box's defect instead of the mutant.
        print(f"already red before mutation, and not counted as a catch: {', '.join(sorted(red0))}\n")
    for mutant in CONTRACT["selftest"]["mutants"]:
        if mutant == "bad_log":
            continue
        print(f"== mutant: {mutant}")
        p, f, s, u, red = run_box(Box(box_name, mutant=mutant))
        print(f"box={box_name}+{mutant}  {p} passed, {f} failed, {s} skipped\n")
        caught = red - red0
        if not caught:
            problems.append(f"mutant {mutant} turned no green arm red")
        else:
            print(f"caught by {len(caught)} arm(s): {', '.join(sorted(caught))}\n")
    print("== mutant: bad_log (a doctored record stream)")
    good = [
        {"ts": _window(), "event": "accepted", "id": "1"},
        {"ts": _window(), "event": "injected", "id": "1"},
        {"ts": _window(), "event": "delivered", "id": "1"},
        {"ts": _window(), "event": "answered-with-receipt", "id": "1"},
    ]
    doctored = good + [{"ts": _window(), "event": "notice60", "id": "1"}, {"ts": _window(), "event": "invented_word", "id": "2"}]
    clean, dirty = check_log(good), check_log(doctored)
    print(f"clean stream: {len(clean)} violations; doctored stream: {len(dirty)} violations")
    if clean:
        problems.append(f"a clean stream was flagged: {clean}")
    if not dirty:
        problems.append("a doctored stream was not flagged")
    for item in dirty:
        print("  caught:", item)
    if problems:
        print("\nSELFTEST FAILED")
        for item in problems:
            print("  -", item)
        return 1
    print("\nSELFTEST PASSED: every mutation was caught")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--box", default=None)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--log", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--allow-skips", default="", help="comma-separated rule ids whose SKIP the command accepts")
    args = ap.parse_args()
    allowed_rules = {r.strip() for r in args.allow_skips.split(",") if r.strip()}

    if args.list:
        print(f"contract v{CONTRACT['version']} — {len(ARMS)} arms")
        for arm in ARMS:
            print(f"  {arm['name']:<34} {arm['rule']:<5} {arm['kind']}")
        return 0

    if args.log:
        rows = []
        for line in Path(args.log).read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        violations = check_log(rows)
        print(f"replayed {len(rows)} records from {args.log}")
        summarise(violations)
        return 0

    if not args.box:
        print(__doc__)
        return 2

    if args.selftest:
        return selftest(args.box)

    p, f, s, unallowed, _red = run_box(Box(args.box), allowed=allowed_rules)
    print(f"\nbox={args.box}  {p} passed, {f} failed, {s} skipped  (contract v{CONTRACT['version']})")
    if f:
        return 1
    if unallowed:
        print(f"UNMEASURED: {len(unallowed)} arm(s) skipped without an allowance: {', '.join(sorted(unallowed))}")
        print("  an unmeasured rule is not a satisfied one; name the rule in --allow-skips to accept the gap")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
