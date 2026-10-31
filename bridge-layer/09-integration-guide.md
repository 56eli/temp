# 09 — Integration guide: build one yourself

*[agent: 2026-10-31 — sb3. Target reader: someone who has a Discord bot token and an agent in a
terminal, and wants the layer described in this pack. Nothing here is br1-specific except the
example values.]*

## 0. Decide three things first

| decision | why it matters | default worth copying |
|---|---|---|
| **What receives the line?** | the pane must be a live agent session, never a shell | one tmux pane per agent, anchored target |
| **Who may instruct?** | this is the security boundary | one operator id, pinned in code, plus one channel |
| **Where does state live?** | it must survive a restart of the process, not of the machine | one directory, mode 0700, two JSONL files |

If you only need "post messages to Discord", you do not need this layer. The layer exists to carry
an *instruction* in and an *answer* out, with a record and a refusal code for everything else.

## 1. Discord application

In the developer portal, for the bot's application:

1. **Bot → Privileged Gateway Intents → Message Content: ON.** Without it `message.content` is empty
   and every addressed prompt is refused `empty`.
2. Invite the bot with `bot` scope and, in the eligible channel: **View Channel**, **Send Messages**,
   **Read Message History**. Add **Attach Files** only if you implement C33.
3. The operator must be able to DM the bot. The bot does not need to DM first.

Record three ids: the **bot user id**, the **guild id**, the **eligible channel id**, and the
**operator's user id**. Bot/user/channel ids are snowflakes (17–20 digits); the guild id doubles as
the `@everyone` role id, which is why the implementation filters it out of the role set.

## 2. Lay out the box

```
/opt/bridge/                 code (bridge.js, bot.js, state.js, reply.js, adapter.js)
/opt/bridge/contract/        CONTRACT.md
/opt/bridge/config.json      0600, no secrets
/opt/bridge/state/           0700: events.jsonl, answers.jsonl, supervisor.log, loop.lock, attachments/
/etc/bridge/bot.token        0600, the token (never in config, never on a command line)
```

`state/` must be on a filesystem that survives a restart of the *process*. On br1 it is
`/root/.pi/bridge/state`, on the mounted home, so it survives a container recreate.

## 3. Install code and dependencies

The reference installer (`install.sh`) copies code, copies `CONTRACT.md` into `contract/`, seeds
`config.json` from an example with placeholders, and runs `npm ci --omit=dev`. It never reads,
writes or echoes the token. If you write your own, keep those properties.

```
node >= 20        # discord.js 14.27, @iarna/toml 2.2.5
```

## 4. Seat the token (a human step)

```sh
install -d -m 700 /etc/bridge
umask 077
read -r -s -p 'bot token: ' BOT_TOKEN; echo
printf '%s' "$BOT_TOKEN" > /etc/bridge/bot.token
unset BOT_TOKEN
wc -c < /etc/bridge/bot.token      # sanity: a token is ~70 bytes
```

Do not put the token in `config.json`, in a shell history, in a systemd `Environment=` line that is
world-readable, or on a command line. The loop reads the file the config names, or
`BRIDGE_BOT_TOKEN` from its own environment.

## 5. Config

`config.json` (mode 0600). Only the first six fields are load-bearing for the gate:

```json
{
  "operator_id": "847445853584883712",
  "bot_id": "1564946284094292069",
  "role_ids": ["1564948507779923980"],
  "guild_id": "1489236876736069662",
  "channel_id": "1561512381480181860",
  "pane": "=agent:0.0",
  "peers": [],
  "token_file": "/etc/bridge/bot.token",
  "notice_key": "/etc/spacebridge/notice.key",
  "state_dir": "/opt/bridge/state",
  "log": "/opt/bridge/state/events.jsonl",
  "answers": "/opt/bridge/state/answers.jsonl"
}
```

| field | meaning | notes |
|---|---|---|
| `operator_id` | the only human author | the reference **pins** it in code; a config naming another id is refused at load |
| `bot_id` | this bot's user id | filled from `client.user.id` at ready; the value in the file is a cache, not authority |
| `role_ids` | roles that address the bot like a mention does | merged at ready with the bot's actual roles |
| `guild_id` | guild the eligible channel lives in | omitted ⇒ C9 skipped |
| `channel_id` | the one channel instructions may arrive in | the operator's DM is a second lane |
| `pane` | tmux target | anchor with `=` (`=agent:0.0`) |
| `peers` | bot authors allowed as peers | empty by default; **empty is the safe default** |
| `token_file` | where the token lives | never inline the token |
| `notice_key` | notice signing key | absent ⇒ `sig=none` (R6) |
| `state_dir` | where the two JSONL files live | mode 0700 |

On first `ready` the loop rewrites the config with the real `bot_id` and merged `role_ids`, mode
0600. That is the only time the bridge writes its own config.

## 6. Start it

Either use the shipped pair:

```sh
tmux new-session -d -s bridge '/opt/bridge/supervise.sh'
sh /opt/bridge/run.sh status
```

or, with systemd:

```ini
[Unit]
Description=agent discord bridge
After=network-online.target

[Service]
Type=simple
User=agent
WorkingDirectory=/opt/bridge
ExecStart=/usr/bin/node /opt/bridge/bot.js
Restart=always
RestartSec=2

[Install]
WantedBy=default.target
```

If you use systemd, you still want the heartbeat: `Restart=always` covers *process gone*, never
*loop stopped*. The bridge does not need to know which supervisor you chose, only that the three
axes each have evidence (C30).

## 7. Smoke test (five minutes, no agent involved)

1. **Gate, accepted.** From the operator account, in the eligible channel:
   `@yourbot status` → the channel gets the ack (`<@operator> on it.`), and the pane receives
   `[discord:addressed <ts> msg=<id>] status`.
2. **Gate, refused.** Post `hello` with no mention → **nothing** appears in the channel; the log gets
   one `refused` record with `pinged_nobody`.
3. **Answer.** `node reply.js <id> "pong"` → the channel gets `pong`; the log gets
   `reply, delivered, answered, receipt-written`.
4. **Reminder.** Leave a request open. After ~20 minutes the channel and the pane get the notice
   line; the log gets `reminder` or `reminder_unsigned`.
5. **Restart.** Stop and start the loop with an open request. The log gets `start`,
   `restart-window`, `abandoned_restart` for that id, `binding`, `baseline` — and nothing older is
   relayed.

Only step 4 takes time; everything else is seconds.

## 8. Measure it

```sh
python3 conformance/run.py --box <your-adapter> --allow-skips C20   # if you have no notice key
python3 conformance/run.py --box <your-adapter> --selftest
python3 tools/check.py
```

Write your adapter in the three-line shape from §08. Expect the first run to be red; that is the
suite doing its job. Do not "fix" the arm.

## 9. Operate it

* Watch the **heartbeat**, not the process (`tail -1 events.jsonl`).
* Watch `supervisor.log` for a restart loop: the same `rc=` line repeating means the loop cannot
  start, and the session being alive is not evidence.
* Watch `refused` counts: thousands is normal in a busy channel with other bots; a sudden burst of
  one code is a gate regression.
* Keep `--force` for mistakes. It records an answer that the loop will not post, so it is a record
  of a decision, not a delivery.

## 10. What "done" looks like

- [ ] one process per token, writer lock in place, second loop exits 2;
- [ ] operator pinned in code, not only in config;
- [ ] gate returns a declared code for every refusal, and nothing else;
- [ ] the pane line matches the grammar and carries the message id;
- [ ] the ack is posted once, before any answer;
- [ ] the reply tool refuses an unknown or closed id, and refuses when the loop is not live;
- [ ] restart closes the backlog and relays nothing older than the process;
- [ ] reminders fire from entry, in both sinks, and are labelled signed/unsigned;
- [ ] `tools/check.py` passes;
- [ ] `--selftest` passes, and you have one real, recorded failure of your own suite to show it can
      fail on your box too.
