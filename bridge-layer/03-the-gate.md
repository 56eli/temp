# 03 — The gate

*[agent: 2026-10-31 — sb3. Rules C2–C13, C33; measured payloads from the live sb3 box.]*

## The question the gate answers

> Is this Discord message an **instruction to this agent**, and if not, exactly why not?

It answers with one of two shapes, and nothing else:

```json
{"action":"accept","code":null,"instruction":"status"}
{"action":"refuse","code":"pinged_nobody","instruction":null}
```

A refusal **carries no instruction**. A refusal produces **no channel message**. Silence is a
feature (C2): the bridge does not argue with the channel, it writes one `refused` record so that
silence leaves a trace.

## Two lanes, then one shared order

`[addressing].order` is normative:

```
bot_author
dm_stranger
other_author
wrong_guild
wrong_channel
thread_not_in_scope      (optional capability)
pinged_nobody
pinged_other_user
empty
```

Read it as: the first four tests establish *who and where*, the last three establish *whether this
bot was addressed and whether anything is left*. The implementation collapses the last two
addressing outcomes into one branch (`others.length ? pinged_other_user : pinged_nobody`) but the
code values are distinct, which is what C13 requires.

The reference implementation, in order:

```js
if (isBot && !peers.has(author))                      return refuse('bot_author');
if (dm && author !== operator)                        return refuse('dm_stranger');
if (!isBot && author !== operator && !peers.has(author)) return refuse('other_author');
if (!dm && cfg.guild_id && guild_id !== cfg.guild_id) return refuse('wrong_guild');
if (!dm && channel_id !== cfg.channel_id)              return refuse('wrong_channel');

const addressed = mentions.includes(botId)
               || mention_roles.some(r => roleIds.includes(r));
if (!addressed) {
  const others = mentions.filter(id => id !== botId && id !== operator);
  return refuse(others.length ? 'pinged_other_user' : 'pinged_nobody');
}
if (!instruction) return refuse('empty');
return { action: 'accept', code: null, instruction };
```

Two details worth copying literally:

* **`author` is tested by id, not by name or discriminator.** The operator id is pinned in code
  (`OPERATOR_ID`), and a config that names a different operator is refused **at load**:
  `config operator_id X is not the pinned operator Y (R9)`. The application owner is never consulted
  as a fallback, because an app transfer or a team change must not add an author.
* **A DM has no guild.** C9 is skipped when `dm` is true; otherwise a DM would fail the guild test
  and the more useful `dm_stranger` diagnosis would never be reached. C10 is placed before C6 for
  the same reason: a stranger's DM should say "stranger DM", not "other author".

## What counts as an address

An address is **either**:

1. the bot's own user id in `mentions` (`<@id>` or `<@!id>`), **or**
2. a role id the bot holds in `mention_roles` (`<@&id>`).

Nothing else. In particular:

* **Other people's mentions are content.** The operator's ruling (R7, 2026-10-25 20:41Z): *"Any ping
  to bot is a valid request further specific with message contents addressing individual parties for
  custom requests."* A message that pings the bot and three humans is one instruction; the humans'
  mentions survive into the instruction *as text*, because the agent may need to know who each part
  is for.
* **A role the bot does not hold is not an address.** `foreign_role` was abolished for this reason —
  "how could a bot be mentioned by a role it doesn't possess?" A message carrying only a foreign role
  is `pinged_nobody`.
* **`@everyone` is not a role mention.** It arrives as `mentions.everyone`, not in `mention_roles`.
  The role cache, however, *does* contain the guild id as an `@everyone` pseudo-role, so the
  reference implementation filters `id === guild_id` out of `role_ids` before merging (a local delta
  on sb3, see `reference/br1-live/PROVENANCE`).
* **Discord populates `mentions` only when the sender allows it.** A message posted with
  `allowed_mentions: { parse: [] }` — which is what this bridge uses for all of **its own** outbound
  messages — will not populate mentions, so it can never be an instruction. That is deliberate:
  answers and reminders must not become new requests.

## Stripping the address

The instruction is the content with every address token for *this bot* removed:

```js
out = content.replace(new RegExp(`<@!?${botId}>`,'g'), ' ')
for (role of roleIds) out = out.replace(new RegExp(`<@&${role}>`,'g'), ' ')
out = out.replace(/[ \t]+/g,' ').trim()
```

Other users' `<@id>` tokens deliberately survive. Then: empty ⇒ `empty`.

## Worked examples (live, 2026-10-31)

These are real calls to the running box's own adapter (`node adapter.js`), not reconstructed:

| input | author | where | result |
|---|---|---|---|
| `<@ugger> status` | operator | eligible channel | `accept` → `"status"` |
| `<@ugger> <@&ugger-role> status` | operator | eligible channel | `accept` (role is also an address) |
| `<@ugger> <@stranger> <@&foreign> do it` | operator | eligible channel | `accept`; stranger id preserved in text |
| `status` (no mention) | operator | eligible channel | `refuse / pinged_nobody` |
| `<@stranger> status` | operator | eligible channel | `refuse / pinged_other_user` |
| `<@&foreign> status` | operator | eligible channel | `refuse / pinged_nobody` |
| `<@ugger> status` | stranger | eligible channel | `refuse / other_author` |
| `<@ugger> status` | any bot | eligible channel | `refuse / bot_author` |
| `<@ugger> status` | operator | other channel | `refuse / wrong_channel` |
| `<@ugger> status` | operator | other guild | `refuse / wrong_guild` |
| `<@ugger> status` | stranger | DM | `refuse / dm_stranger` |
| `<@ugger>` (nothing else) | operator | eligible channel | `refuse / empty` |

`thread_not_in_scope` is a declared **optional** code: a box with no thread surface cannot emit it,
and the code-set arm subtracts the declared optional gap rather than hard-coding an exception. The
Node box has no thread policy: a thread under the eligible channel is simply `wrong_channel`.

## Facts about the channel that the gate depends on

* The bridge must have the **Message Content intent** in the Discord developer portal. Without it,
  `message.content` is empty and every addressed prompt is refused `empty` — a configuration bug
  that looks like a gate bug.
* The bot must be able to **View Channel, Send Messages, Read Message History** in the eligible
  channel, and the operator must be able to DM it (needs `Partials.Channel` for DM events).
* The operator's *own* messages can be a reply to a bot's message (Discord type 19). Discord then
  puts the replied-to author into `mentions`, so a reply to another agent without addressing this
  bot is correctly `pinged_other_user`. That is not a regression; it is the rule working.
* **A second process on the same token** would ack, inject and post twice. The reference loop takes
  a writer lock and exits with code 2 (see §07); on 2026-10-28 the supervisor log shows exactly that
  happening on sb3.

## If you change the gate

* Keep the order. Reordering changes which code a message gets, and the codes are the diagnosis.
* One cause per code, and add the code to `[codes]` **and** `[addressing].order` **and** an arm.
  A code declared but never ordered, or ordered but never declared, fails `tools/check.py`.
* Do not add a length rule. R7 withdrew it: a Discord message is already bounded at 2,000 characters.
  Truncating was a real defect (an 1,801-character instruction delivered as 1,800, silently); the fix
  was to stop truncating, not to add a refusal.
* If you add a "peers" lane (bot authors allowed), remember the loop must then not treat its own id as
  a peer and must still refuse `message.system` events.
