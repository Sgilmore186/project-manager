---
name: pm-update
description: After Seph says anything about his ideas or projects, decide what changed in his project-manager repo and save it with scripts/pm.py, one push per message.
---

# pm-update

Repo: Sgilmore186/project-manager. `scripts/pm.py` is the only way to change data. Never hand-edit JSON or log.md. AGENTS.md has the full rules; this is the short path.

## Keep it cheap
- Don't read the whole repo. Run `python3 scripts/pm.py get ID` for the items the message touches. Use `list` only when you can't tell which id he means.
- No AI work inside the script. Your job is only to pick the command.
- One message from Seph = one push. Each command commits itself; push once at the end.

## 1. Did anything change?
Scan his message for these. If none, stop. Save nothing.

| He says | Run |
|---|---|
| New outcome he wants, not committed | `add idea --id ID --name N --description D [--goal G]` |
| He commits to an idea | `move ID --to project --goal G` |
| Something isn't committed after all | `move ID --to idea --reason R` |
| Finished the current next step | `done ID --next "new next step"` |
| Finished something else | `done ID --step "what was done"` (add `--item "open item"` if the wording differs) |
| New next step only | `update ID --set next_step="..."` |
| Stage moved | `update ID --set stage="..."` |
| Add or drop one open item | `update ID --add open_items="..."` or `--remove open_items="..."` |
| Sets focus | `update ID --set focus=primary` (or `secondary`; `none` needs `--reason R`) |
| Goal reached | `update ID --set status=done --set focus=none` |
| Steps away (pause, archive, drop) | ask his reason first, then `update ID --set status=S --reason R` |
| Wants it gone for good | `delete ID --reason R` |
| Depends on another item, no goal of its own | `add part --id ID --name N --part-of P1,P2` |

## 2. Ask, don't guess
Ask Seph one short question, and save nothing yet, when:
- you can't tell if it's an idea, project or part
- a new idea has no description, or a project would have no goal
- he's leaving a project without a reason (name what's left on it)
- it's a new idea (ask how it ranks against his current focus first)

## 3. Run it
0. `python3 scripts/pm.py sync`
1. `--dry-run` first if unsure of the effect.
2. Run each command. Pass his reason with `--reason` whenever he gives one.
3. If any line prints `error:`, nothing was saved. Fix the input or ask him. Never force it.
4. `python3 scripts/pm.py check`
5. `python3 scripts/pm.py commit --push`

## 4. Tell him
One or two lines: what changed, and the next step if it moved. Then one challenge if it fits (vague goal, drifting off the primary, too many open things). No em dashes.
