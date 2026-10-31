# reference/ — the artefacts, verbatim

Nothing in this directory has been edited. If the prose in this pack and a file here disagree, the
file here wins.

## `contract-v7/` — the standard

Extracted with `git archive origin/agent/bridge-contract-v7-2026-10-25` (head `06a8f26`) from the
private botrunner repository, 2026-10-31. This is byte-identical to what the four br1 bridges load as
`contract/CONTRACT.md` (sha256 `c26551c2…`).

| file | what it is |
|---|---|
| `CONTRACT.md` | **normative.** Prose + one fenced `toml` block. 32 rules, 38 arms, 9 codes |
| `RULINGS.md` | the operator's words, verbatim, with dates and source ids; the only override |
| `BOXES.md` | the per-box deployment sheet — **allowed to differ**; measured/reported marked |
| `REVIEW.md` | the reviewer's page: reading order, what each claim rests on, what is not claimed |
| `CHECKLIST.md` | 39 properties in message order, with what the suite says about the one measured box |
| `PROPOSAL.md` | the plan approved 2026-10-25 and what was built (history) |
| `conformance/run.py` | the black-box suite; 38 arms |
| `conformance/adapters/` | `sb2.py` (in-process), `debugger.py`/`bugger.py` (peer, via `_peer.py`), `_proxy.py` (mutants) |
| `tools/check.py` | block ⇄ arms ⇄ prose ⇄ documents checker |

Not included because it never existed on this branch: a `devcage.py` adapter (it lives on the
devcage branch) and C33/attachments (also devcage branch, commit `16e4acd`).

## `br1-live/` — the code that was running on 2026-10-31

Copied from `/root/.pi/bridge` in the `sb3` cage. No token, key or config contents are included.

| file | note |
|---|---|
| `bridge.js`, `state.js`, `adapter.js` | byte-identical to devcage commit `09859c1` |
| `bot.js` | local delta: writer lock, `@everyone` role filtering |
| `reply.js` | local delta: trailing-only `--force`, heartbeat liveness check (exit 4) |
| `supervise.sh` | local delta: `cd`/`node` guards, 30 s backoff on the lock refusal |
| `run.sh` | seat-local: `start`/`stop`/`status`/`probe` |
| `PROVENANCE` | the estate's own record of what came from where |
| `contract/CONTRACT.md` | the deployed copy (same sha256 as `contract-v7/CONTRACT.md`) |
| `tests/bridge.test.js` | the box's own tests (gate, line, notice, ladder, operator pin) |
| `package.json`, `package-lock.json` | `discord.js 14.27.0`, `@iarna/toml 2.2.5`, node ≥ 20 |
| `config.example.json` | the installer's placeholder config |

## Reproducing the measurements in `../12-measurements-2026-10-31.md`

```sh
# extract the standard (read-only fact from the mounted checkout)
cd /home/ubuntu/botrunner
git archive origin/agent/bridge-contract-v7-2026-10-25 services/bridge-contract | tar -x -C /tmp/bsc --strip-components=1

# checker (needs a git repo for the C1 rule)
cd /tmp/bsc/bridge-contract && git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm x
python3 tools/check.py

# a nine-line adapter for this box, then the suite
cat > conformance/adapters/sb3br1.py <<'PY'
import json, subprocess, sys
req = json.load(sys.stdin)
p = subprocess.run(["node", "/root/.pi/bridge/adapter.js"], input=json.dumps(req),
                   capture_output=True, text=True, timeout=120)
print(p.stdout or json.dumps({"error": p.stderr[:200]}))
PY
python3 conformance/run.py --box sb3br1
python3 conformance/run.py --box sb3br1 --selftest
python3 conformance/run.py --log /root/.pi/bridge/state/events.jsonl
```

Reading the log and running the adapter are read-only. The conformance run does not write to the
box; the `log` op only returns a path.
