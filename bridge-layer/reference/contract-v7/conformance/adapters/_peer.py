#!/usr/bin/env python3
"""A peer box: drive that box's own bridge module, unmodified.

Nothing here re-implements a rule. Point `PI_PEER_HOME` at the directory holding the box's `bridge.py`
(a local mount, or a directory copied over ssh) and every operation calls that box's own code, the way
`sb2.py` does for this container. Where the box exposes no such callable, the answer is `null` and the
arm is SKIP.

    PI_PEER_HOME=/mnt/debugger-bridge  python3 run.py --box debugger
"""
import json
import os
import re
import sys
from pathlib import Path


def main(name: str) -> int:
    home = Path(os.environ.get("PI_PEER_HOME", f"/root/.pi/peers/{name}"))
    req = json.load(sys.stdin)
    op = req["op"]
    out: dict = {}
    if not (home / "bridge.py").exists():
        print(json.dumps({"error": f"no bridge.py under {home}: set PI_PEER_HOME"}))
        return 0
    sys.path.insert(0, str(home))
    try:
        import bridge as live  # type: ignore
    except Exception as exc:
        print(json.dumps({"error": f"import bridge failed: {exc}"}))
        return 0
    cfg = getattr(live, "CFG", {})
    if op == "config":
        out = {
            "operator_id": str(cfg.get("operator_id")),
            "bot_id": str(cfg.get("bot_id")),
            "role_ids": [str(r) for r in (cfg.get("role_ids") or [])],
            "guild_id": str(cfg.get("guild_id")),
            "channel_id": str(cfg.get("channel_id")),
            "reminder_every_s": getattr(live, "REMINDER_EVERY_S", None),
        }
    elif op == "classify" and hasattr(live, "gate"):
        accept, reason, instruction = live.gate(req["msg"], cfg, dm=bool(req["msg"].get("dm")))
        out = {"action": "accept" if accept else "refuse", "code": None if accept else reason, "instruction": instruction}
    elif op == "log":
        path = home / "dbg-bot.log"
        out = {"path": str(path) if path.exists() else None}
    elif op == "codes":
        src = Path(live.__file__).read_text(encoding="utf-8")
        out = {"codes": sorted(set(re.findall(r"False, '([a-z_]+)'", src))),
               "method": "literals in return statements of the box's own gate"}
    else:
        key = {"classify": "action", "sign": "line", "verify": "rc", "line": "line", "vocabulary": "words", "log": "path", "codes": "codes"}.get(op)
        out = {key: None} if key else {"error": f"unknown op {op}"}
    print(json.dumps(out))
    return 0
