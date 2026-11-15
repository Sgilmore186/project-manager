# Repo standard

How every Seph repo is organized. `project-manager` is the model repo.

**Goal:** any AI opens a repo, reads one file, and knows what to do.

## Principles
- One rules file per repo, found automatically by every AI tool.
- A short README, tidy docs, tests, and CI on every PR.
- Changes go through reviewed PRs. Seph merges.
- Nothing private in Git.

## Required files
| File | Job |
| --- | --- |
| `AGENTS.md` | The rules. The single source of truth for the repo. |
| `CLAUDE.md` | Two lines: an `@AGENTS.md` import and a link. No rules here. |
| `.gemini/settings.json` | Points Gemini CLI at AGENTS.md. |
| `README.md` | Short overview for humans. Links to AGENTS.md and docs. |
| `docs/` | Guides. Add `docs/README.md` as an index once there are several. |
| `docs/history/` | Finished reports. Kept, not rewritten. |
| `tests/` and `.github/workflows/` | Tests, run by CI on every PR and push to main. |
| `.gitignore` | Keeps secrets, personal data, models and environments out. |

## How each AI finds the rules
| Tool | How |
| --- | --- |
| Codex | Reads AGENTS.md natively. |
| Claude Code | Reads CLAUDE.md, which imports AGENTS.md. Newer versions also fall back to AGENTS.md when no CLAUDE.md exists, but the import is more reliable. |
| Gemini CLI | Reads `.gemini/settings.json`, which names AGENTS.md. |
| Cursor, Copilot, Windsurf and others | Most read AGENTS.md natively. Check the tool's docs. |
| Chat sessions with a GitHub connector | Nothing loads automatically. Tell the AI to read AGENTS.md first. |

## AGENTS.md outline
Keep each section short. Use bullets, not paragraphs.
1. **What this repo is:** one paragraph, plus what it must never become.
2. **Files:** a map of the repo.
3. **How it works:** only if it isn't obvious.
4. **Definitions:** terms that have a precise meaning here.
5. **Rules:** grouped (privacy, safety, quality).
6. **How to change things:** steps, checks, and a never-commit list.
7. **Repo standard:** a pointer to this doc (text below).
8. **Current status:** link to one place. Never copy status into several files.
9. **Writing style:** short, scannable, plain words, no em dashes.

Paste this as section 7:
```md
## Repo standard
This repo follows the Seph repo standard:
https://github.com/Sgilmore186/project-manager/blob/main/docs/REPO_STANDARD.md
Short version: AGENTS.md holds the rules, CLAUDE.md only imports it, README stays short,
docs have one index, changes go through a branch and PR, nothing private is committed.
```

## Change rules
1. Work on a branch and open a PR. Never commit to main directly.
   Exception: a data repo whose script is the only writer (project-manager data goes through `pm.py`).
2. Add or update tests for every behavior change.
3. Run the repo's checks before opening a PR. CI must be green.
4. Seph merges. An AI never merges unless he asks.
5. Stage explicit paths and review what is staged.
6. Never force-push or rewrite main.

## Never commit
Secrets, tokens, keys, personal audio, transcripts or memories, databases, model weights,
environments and private logs. `.gitignore` is a guard, not proof.

## README rules
- What it is, how to run it, and links. Aim for under 50 lines.
- Details go in `docs/`.

## Checklist
- [ ] AGENTS.md has the rules, and CLAUDE.md only imports it
- [ ] `.gemini/settings.json` names AGENTS.md
- [ ] README is short and links to the details
- [ ] Docs are organized, with finished reports in `docs/history/`
- [ ] Tests exist and CI runs them on every PR
- [ ] `.gitignore` covers secrets and personal data
- [ ] Changes arrive by PR
- [ ] Status lives in one place

## Starting a new repo
Copy these files, then fill in AGENTS.md from the outline.

`CLAUDE.md`:
```md
@AGENTS.md

All rules for this repo are in [AGENTS.md](AGENTS.md). Don't add rules here.
```

`.gemini/settings.json`:
```json
{
  "context": {
    "fileName": "AGENTS.md"
  }
}
```
