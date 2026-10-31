#!/usr/bin/env python3
"""One file, checked against the code that claims to obey it (C28, C29).

    python3 tools/check.py                 # declaratations vs implementations, prose vs registry
    python3 tools/check.py --manifest      # the arm manifest, printed (never written to disk)
    python3 tools/check.py --source FILE    # a box source file: every refusal code it names is declared

Why this exists and why it is small: v1-v6 kept a prose document and a hand-maintained list of arms, and
the two disagreed three ways across three boxes. There is one file now, so a checker can be sixty lines
instead of a code generator plus a generated artefact plus a comparator.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "CONTRACT.md"
RUN = ROOT / "conformance" / "run.py"

#: The documents a reviewer is told to trust. The checker could not see them, which is how a sheet can claim 28 arms
#: beside a suite of 37 and an abolished code beside a contract that abolished it (independent review, 2026-10-25).
DOCS = ["REVIEW.md", "CHECKLIST.md", "BOXES.md", "PROPOSAL.md", "RULINGS.md"]

#: A line may name an arm that no longer exists, or a code that was abolished, only while *recording* it. The marker is
#: one of four words, chosen because a narrower list was measured to fail: "no longer" appeared in a row about the
#: length defect and exempted the whole line, which is the same accidental pass this checker exists to prevent.
HISTORY = ("historical", "(history)", "abolished", "withdrawn")

#: Prefixes our arms use. A token with one of these prefixes in a document is an arm reference and must resolve; a
#: contract key with the same shape (`line_template`) resolves against the block, so names and keys cannot be confused.
ARM_PREFIXES = ("gate", "log", "notice", "line", "codes", "vocabulary", "manifest", "unaddressed", "reminder",
                "one_message", "terminal", "supervision", "directive", "no_orphan", "ack_once", "identity")


def _values(node) -> set:
    """Identifier-shaped string *values* in the block: log words and codes are named in prose as often as keys."""
    out: set = set()
    if isinstance(node, dict):
        for v in node.values():
            out |= _values(v)
    elif isinstance(node, list):
        for v in node:
            out |= _values(v)
    elif isinstance(node, str) and re.fullmatch(r"[a-z][a-z0-9_]{2,}", node):
        out.add(node)
    return out


def _keys(node) -> set:
    """Every key in the block, recursively: a document may name a field without naming an arm."""
    out: set = set()
    if isinstance(node, dict):
        for k, v in node.items():
            out.add(k)
            out |= _keys(v)
    elif isinstance(node, list):
        for v in node:
            out |= _keys(v)
    return out


def check_documents(c: dict, problems: list) -> int:
    """The facts the prose states must be the facts the block and the suite hold, or the prose is a claim.

    Three checks, each able to fail on a real defect seen in this package on 2026-10-25:

    * a count — `N arms`, `N rules`, `N codes` — must equal the block's, unless the line records history;
    * an arm name must exist, and a code must not be one the contract abolished, under the same exemption;
    * a measurement — `box=… P passed, F failed, S skipped` — must carry a time and a code identity on its own line,
      because a number without a vantage is the defect this package exists to stop.
    """
    arms = {a["name"] for a in c["arm"]}
    keys = _keys(c) | _values(c)
    abolished = set(c["codes"].get("abolished") or {})
    counts = {"arms": len(c["arm"]), "rules": len(c["rules"]),
              "codes": len([k for k, v in c["codes"].items() if isinstance(v, str) and k not in ("rule", "abolished")])}
    findings = 0
    for name in DOCS:
        path = ROOT / name
        if not path.exists():
            problems.append(f"{name} is named as a document to review but does not exist")
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            where = f"{name}:{lineno}"
            recording = any(marker in line.lower() for marker in HISTORY)
            # Another box's own suite is a different unit: "23 arms" for `debugger` is a fact about that box, not a
            # claim about this suite. Only a claim about *this* suite is checked.
            other_unit = any(word in line.lower() for word in
                             ("own test suite", "box suite", "selftest.py", "debugger", "bugger",
                              "skipped", "allow-skips"))
            for unit, real in counts.items():
                for got in re.findall(rf"\b(\d+)\s+{unit}\b", line):
                    if int(got) != real and not recording and not other_unit:
                        problems.append(f"{where}: says {got} {unit}, the block and suite hold {real}")
                        findings += 1
            for token in re.findall(rf"\b((?:{'|'.join(ARM_PREFIXES)})_[a-z0-9_]+)\b", line):
                if token in arms or token in keys or recording:
                    continue
                problems.append(f"{where}: names {token!r}, which is not an arm in the block")
                findings += 1
            for code in sorted(abolished):
                if re.search(rf"`{code}`|\b{code}\b", line) and not recording:
                    problems.append(f"{where}: presents {code!r} as current; the block abolishes it")
                    findings += 1
            if re.search(r"\b\d+ passed, \d+ failed, \d+ skipped\b", line):
                if not re.search(r"\d\d:\d\dZ|\d{4}-\d\d-\d\d", line) or "identity" not in line:
                    problems.append(f"{where}: a measurement without a time and a code identity on its own line")
                    findings += 1
    # One run, one result: a suite result quoted in two documents must be the same result. This is the check that
    # would have caught 28/0/9 in REVIEW.md beside 26/3/9 in PROPOSAL.md for the same box on the same evening.
    results: dict = {}
    for name in DOCS:
        path = ROOT / name
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if any(marker in line.lower() for marker in HISTORY):
                continue  # a dated historical result may differ from today's; that is what recording it means
            for got in re.findall(r"(?:box=(\w+)\s+)?(\d+) passed, (\d+) failed, (\d+) skipped", line):
                who, triple = got[0] or "unnamed", got[1:]
                results.setdefault(who, []).append((f"{name}:{lineno}", triple))
    for who, seen in results.items():
        triples = {t for _, t in seen}
        if len(triples) > 1:
            problems.append(f"{who}: documents disagree about the same run — " +
                            ", ".join(f"{where} says {t[0]}/{t[1]}/{t[2]}" for where, t in seen))

    # CHECKLIST.md states a tally of its own table. A tally that is not recounted from the table is how "six of
    # thirty-nine unmeasured" was said out loud while the table held twelve (2026-10-25).
    checklist = ROOT / "CHECKLIST.md"
    if checklist.exists():
        rows = [l for l in checklist.read_text(encoding="utf-8").splitlines() if re.match(r"\| \d+ \|", l)]
        tally: dict = {}
        for line in rows:
            cells = [c.strip() for c in line.strip("|").split("|")]
            tag = cells[3] if len(cells) > 3 else ""
            key = ("red" if tag.startswith("**red") else "skip" if tag.startswith("skip") else
                   "unarmed" if tag.startswith("unarmed") else
                   "hand" if tag.startswith(("hand", "box suite")) else "measured")
            tally[key] = tally.get(key, 0) + 1
        claimed = re.search(r"the (\d+) divide:(.*)", checklist.read_text(encoding="utf-8"))
        if not claimed:
            problems.append("CHECKLIST.md states no tally, so its table cannot be checked")
        else:
            if int(claimed.group(1)) != len(rows):
                problems.append(f"CHECKLIST.md states {claimed.group(1)} items; the table holds {len(rows)}")
            for got, unit in re.findall(r"\*\*(\d+) (\w+)\*\*", claimed.group(2)):
                if tally.get(unit, 0) != int(got):
                    problems.append(f"CHECKLIST.md tally says {got} {unit}; the table holds {tally.get(unit, 0)}")
    return findings


def block() -> dict:
    import tomllib

    text = DOC.read_text(encoding="utf-8")
    m = re.search(r"```toml\n(.*?)\n```", text, re.S)
    if not m:
        raise SystemExit("CONTRACT.md has no ```toml block: the machine form is missing")
    return tomllib.loads(m.group(1))


def _call(adapter: Path, req: dict) -> dict | None:
    import subprocess

    r = subprocess.run([sys.executable, str(adapter)], input=json.dumps(req), capture_output=True, text=True,
                       timeout=120, cwd=str(ROOT))
    try:
        return json.loads(r.stdout)
    except Exception:
        return None


def _probe(op: str, cfg: dict) -> dict:
    """A minimal well-formed request per op: the probe asks whether the seam answers, not whether it is right."""
    bot = str(cfg.get("bot_id") or "1")
    operator = str(cfg.get("operator_id") or "2")
    msg = {"id": "1563900000000000001", "content": f"<@{bot}> probe", "mentions": [{"id": bot}], "mention_roles": [],
           "author": {"id": operator, "bot": False}, "guild_id": str(cfg.get("guild_id") or "3"),
           "channel_id": str(cfg.get("channel_id") or "4"), "dm": False}
    base = {"msg_id": "1563900000000000001", "minutes": 20, "ts": 1792710000, "key_hex": None, "text": "probe",
            "line": "[BRIDGE kind=notice msg=1 minutes=20 ts=1792710000 sig=none] probe", "msg": msg, "cfg": cfg}
    return {"op": op, **base}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", action="store_true")
    ap.add_argument("--source", default=None)
    ap.add_argument("--adapters", action="store_true", help="every adapter answers every declared op")
    args = ap.parse_args()
    c = block()
    problems: list[str] = []

    declared = {a["name"] for a in c["arm"]}
    implemented = set(re.findall(r"^def arm_(\w+)\(", RUN.read_text(encoding="utf-8"), re.M))
    problems += [f"declared arm has no implementation: {n}" for n in sorted(declared - implemented)]
    problems += [f"implemented arm is not declared: {n}" for n in sorted(implemented - declared)]

    rules = set(c["rules"])
    problems += [f"arm {a['name']} cites {a['rule']}, not in [rules]" for a in c["arm"] if a["rule"] not in rules]

    armed = {a["rule"] for a in c["arm"]}
    excused = c.get("scope", {}).get("not_measured_by_an_arm", {})
    withdrawn = {r for r, text in c["rules"].items() if str(text).startswith("[X]")}
    problems += [f"rule {r} has no arm: a rule nobody measures is a rule nobody obeys"
                 for r in sorted(rules - armed - set(excused) - withdrawn)]
    # A withdrawn rule must say who withdrew it and when, or it is not a record, it is an omission.
    problems += [f"withdrawn rule {r} does not name the operator and a date" for r in sorted(withdrawn)
                 if "2026-" not in str(c["rules"][r]) or "operator" not in str(c["rules"][r]).lower()]
    problems += [f"rule {r} is withdrawn and still has an arm" for r in sorted(withdrawn & armed)]
    problems += [f"scope excuse for {r} is too thin to review: {why!r}"
                 for r, why in excused.items() if len(str(why)) < 40]
    problems += [f"scope excuse names {r}, which no arm needs excusing" for r in excused if r in armed]
    for r in excused:
        if r not in rules:
            problems.append(f"scope excuse names {r}, not a rule in [rules]")

    prose = DOC.read_text(encoding="utf-8").split("```toml")[0]
    problems += [f"rule {r} is not named in the prose" for r in sorted(rules) if r not in prose]

    codes = {k for k, v in c["codes"].items() if isinstance(v, str) and k != "rule"}
    abolished_codes = set(c["codes"].get("abolished") or {})
    problems += [f"code {k} is abolished and still declared as writable" for k in sorted(abolished_codes & codes)]
    problems += [f"code {k} is abolished and still in [addressing].order" for k in sorted(abolished_codes & set(c["addressing"]["order"]))]
    order = [t for t in c["addressing"]["order"] if t != "addressed"]
    problems += [f"addressing.order names {t}, not a declared code" for t in order if t not in codes]
    problems += [f"code {k} is declared but never ordered" for k in sorted(codes) if k not in order]

    forward = set(c["receipts"]["forward"])
    events = set(c["receipts"]["event"])
    problems += [f"forward word {w} is not in [receipts].event" for w in sorted(forward) if w not in events]

    for state in c["states"]["terminal"]:
        if state not in events:
            problems.append(f"terminal state {state} is not a declared event word")

    check_documents(c, problems)

    if args.source:
        src = Path(args.source).read_text(encoding="utf-8")
        # The same measurement the adapters use: the literals in the box's refusal pairs, whatever they say. A fixed
        # token list passed a box whose refusals were prose, which is the defect this replaces.
        print(f"--source: text scan of {args.source} (heuristic). The measurement is the box's own `codes` op, "
              f"which arm codes_are_declared (C29) runs against the box itself.")
        found = set(re.findall(r"False, '([a-z_]+)'", src))
        if not found:
            problems.append(f"{args.source}: no refusal codes found at all, so nothing was measured")
        problems += [f"{args.source}: undeclared refusal code {code!r}" for code in sorted(found - codes)]

    if args.adapters:
        import subprocess

        ops = c["adapter"]["ops"]
        skips: list[str] = []
        for ad in sorted((ROOT / "conformance" / "adapters").glob("*.py")):
            if ad.name.startswith("_"):
                continue
            cfg = _call(ad, {"op": "config"}) or {}
            for op in ops:
                req = _probe(op, cfg)
                r = subprocess.run([sys.executable, str(ad)], input=json.dumps(req), capture_output=True,
                                   text=True, timeout=120, cwd=str(ROOT))
                try:
                    out = json.loads(r.stdout)
                except Exception:
                    problems.append(f"{ad.name} {op}: not a JSON answer (rc {r.returncode}) {r.stderr.strip()[:90]}")
                    continue
                if "error" in out:
                    why = str(out["error"])
                    if "PI_PEER_HOME" in why or "no bridge.py" in why or "no such file" in why:
                        # The box is not on this host. That is a fact about the deployment sheet, not an adapter
                        # defect, and it is reported as a skip so a missing mount cannot masquerade as success.
                        skips.append(f"{ad.name} {op}: box not reachable here")
                    else:
                        problems.append(f"{ad.name} {op}: {why}")
        print(f"adapters: {len([a for a in (ROOT / 'conformance' / 'adapters').glob('*.py') if not a.name.startswith('_')])} "
              f"x {len(ops)} ops, {len(skips)} unreachable")
        for line in skips:
            print("  SKIP", line)

    # C1: the one rule about this file's own history. Verified where a commit lives, not asserted in prose.
    if "C1" in excused:
        import subprocess

        log = subprocess.run(["git", "log", "-1", "--format=%h %ad -- CONTRACT.md"], cwd=str(ROOT),
                             capture_output=True, text=True)
        if log.returncode != 0 or not log.stdout.strip():
            problems.append("C1: CONTRACT.md has no commit history, so its changes were not commits")
        else:
            print(f"C1: {DOC.name} tracked, last change {log.stdout.split()[0]}")

    if args.manifest:
        print(json.dumps({"version": c["version"], "arms": c["arm"]}, indent=2))

    if problems:
        print("CHECK FAILED")
        for p in problems:
            print("  -", p)
        return 1
    print(f"CHECK PASSED: {len(c['arm'])} arms, {len(rules)} rules, {len(codes)} codes, one file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
