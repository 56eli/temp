#!/usr/bin/env python3
"""A deliberately broken box, for the can-fail proof (C28).

It forwards the request to a real adapter and flips one answer. Three mutations, three defects:

    accept_all  every message is an instruction        -> the gate arms must go red
    bad_sig     every signature verifies               -> the notice arms must go red
    bad_log     a doctored record stream (run.py)      -> the log arms must go red

The suite must catch each. If it cannot, the suite is decoration, and `--selftest` says so.
"""
import json
import os
import subprocess
import sys

target = os.environ["PI_TARGET"]
mode = os.environ["PI_MUTANT"]
req = json.load(sys.stdin)
proc = subprocess.run([sys.executable, target], input=json.dumps(req), capture_output=True, text=True, timeout=120)
try:
    out = json.loads(proc.stdout or "{}")
except json.JSONDecodeError:
    out = {"error": proc.stdout[:200]}

if mode == "accept_all" and req["op"] == "classify":
    out = {"action": "accept", "code": None, "instruction": (req.get("msg") or {}).get("content") or "x"}
elif mode == "bad_sig":
    if req["op"] == "verify":
        out = {"rc": 0, "status": "ok (mutant: accepts any signature)"}
    elif req["op"] == "sign":
        out = {"line": "[BRIDGE kind=notice msg=1 minutes=20 ts=1 sig=" + "0" * 64 + "]\n"}

print(json.dumps(out))
