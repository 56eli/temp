#!/usr/bin/env python3
"""A real box: this container's live bridge (sb2), driven through its own interfaces.

Nothing is re-implemented here. `classify` is the box's own `bridge.gate`; `verify` is the
box's own `verify.verify`; `config` is the box's own `operator.json`, read by the box itself.
Where the box exposes no seam — its notice line is built inline in `post_notice`, its log
vocabulary is not a constant, and it has no simulator — the adapter answers null and the suite
records SKIP, because a missing input is never a pass.
"""
import json
import os
import re
import sys
from pathlib import Path

HOME = Path(os.environ.get("SB2_BRIDGE", "/root/.pi/dbg-bot2"))
sys.path.insert(0, str(HOME))
import bridge as live  # noqa: E402
import verify as verifier  # noqa: E402


def main() -> int:
    req = json.load(sys.stdin)
    op = req["op"]
    if op == "config":
        cfg = live.CFG
        out = {
            "operator_id": str(cfg["operator_id"]),
            "bot_id": str(cfg["bot_id"]),
            "role_ids": [str(r) for r in (cfg.get("role_ids") or [])],
            "guild_id": str(cfg.get("guild_id")),
            "channel_id": str(cfg["channel_id"]),
            # C22: the box's own cadence constant, read rather than restated. A box without one answers null and the
            # arm records a SKIP instead of inventing a number.
            "reminder_every_s": getattr(live, "REMINDER_EVERY_S", None),
        }
    elif op == "classify":
        accept, reason, instruction = live.gate(req["msg"], live.CFG, dm=bool(req["msg"].get("dm")))
        out = {
            "action": "accept" if accept else "refuse",
            "code": None if accept else reason,
            "instruction": instruction,
        }
    elif op == "sign":
        if req.get("key_hex"):
            out = {"line": None, "reason": "the box reads its notice key from a file; there is no key-injection seam"}
        else:
            # The box's own line builder, with whatever key it actually has: no key on this host, so the line comes
            # back labelled `sig=none` (C20/R6) rather than withheld.
            sig = live.sign_notice(req["msg_id"], int(req["minutes"]), int(req["ts"]))
            out = {"line": live.notice_line(req["msg_id"], int(req["minutes"]), int(req["ts"]), sig)}
    elif op == "verify":
        key = bytes.fromhex(req["key_hex"]) if req.get("key_hex") else None
        code, why = verifier.verify(req["line"], key, int(req["ts"]))
        out = {"rc": code, "status": why}
    elif op == "log":
        out = {"path": str(HOME / "dbg-bot.log") if (HOME / "dbg-bot.log").exists() else None}
    elif op == "codes":
        # C29: what this box can actually emit. Read from the return statements themselves, so a box whose refusals
        # are prose yields prose and goes red — a fixed token list in the checker could never tell the difference.
        src = Path(getattr(live, "__file__", HOME / "bridge.py")).read_text(encoding="utf-8")
        out = {"codes": sorted(set(re.findall(r"False, '([a-z_]+)'", src))),
               "method": "literals in return statements of the box's own gate"}
    elif op == "supervision":
        # C30. This box is supervised by the runner, not by itself; there is no seam to read, and null says so
        # rather than pretending three axes were checked.
        out = {"axes": None}
    elif op in ("line", "vocabulary"):
        out = {"line" if op == "line" else "words": None}
    else:
        out = {"error": f"unknown op {op}"}
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
