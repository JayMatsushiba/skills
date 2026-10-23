# Skills

Claude Code skills for how I run projects with Claude. The workflow goes from
an idea to merged work: README, then SPEC, then GitHub issues, then one
branch and one PR per work item, with agent reviews before each merge.

It is based on the [Ambrosia](https://github.com/OceanOS-MVP/Ambrosia)
project, where it was first used.

## Workflow

```
 docs/ + notes ──┐
 Obsidian ───────┼──► /project-readme ──► README.md
 Connectors ─────┘                            │
 (Drive, Gmail, Slack)                        │
                                              ▼
                       /project-spec ◄──► SPEC.md   (iterate until it's right)
                                              │
                                              ▼
                       /spec-issues ──► GitHub labels + one issue per work item
                                              │
                         ┌────────────────────┘   one agent per issue
                         ▼
   /work-item #N ──► branch ──► commits ──► PR "Closes #N"
         ▲                                     │
         │                                     ▼
         │                      /pr-review #PR (two new agents)
         │                        ├─ /content-review → PR review comments
         │                        └─ /code-review max → PR review comments
         │                                     │
         └──── feedback goes back to the ──────┘
               same work-item agent
                         │
                         ▼
   developer review ◄──► same agent incorporates feedback
                         │  (repeat until the developer approves)
                         ▼
          rebase on main if needed ──► squash-merge ──► issue closes
```

1. **README.** Write `README.md` myself, or put key files (reports, meeting
   notes, papers, emails) in `docs/` and run `/project-readme`. It reads my
   Obsidian vault, if there is one, for the project's notes, meeting
   write-ups, writing and brainstorms. It also searches Google Drive, Gmail
   and Slack, and records where each fact came from.
2. **SPEC.** `/project-spec` drafts `SPEC.md` from the README: purpose,
   scope, assumptions, then work split into phases and numbered workstreams
   (WS0, WS1, …), each with a goal, steps and a "done when" line. I go back
   and forth with Claude on it until it describes the intended work
   accurately.
3. **Issues.** `/spec-issues` turns each workstream into GitHub issues with
   context, a task checklist and acceptance criteria, and labels them by
   phase and workstream. From here on GitHub tracks progress, not chat.
4. **Work.** `/work-item <issue>` gives one agent one issue. It creates a
   branch when work starts and opens a PR when the work is nearly done. The
   agent stays on that one item until it is merged. Switching between items
   or PRs isn't allowed: the work item is the unit of delegation between
   agents, and switching causes conflicts.
5. **Review.** When the PR is open, `/pr-review <PR>` starts two new
   agents: one runs `/content-review` on the prose, the other runs
   `/code-review` at max effort. Both post their findings on the PR as review
   comments.
6. **Feedback.** The review goes back to the agent that wrote the PR. It
   works through the comments, replies to each one and pushes fixes.
7. **Developer review.** Every PR gets a human review before merging, even
   when the agent reviews found nothing. The agent brings the branch up to
   date with `main`, then asks me to review, with a short summary of the
   results, what changed after the agent reviews, and open questions. My
   feedback (on the PR or in the session) goes back to the same agent, which
   incorporates it the same way. This repeats until I approve explicitly.
8. **Merge.** If `main` has moved on since then, the agent rebases the branch
   onto `main` again, and shows me any conflict fixes that change what I
   approved. Then the PR is squash-merged, which closes the issue.

## Skills

| Skill | Stage | What it does |
|---|---|---|
| [`project-readme`](project-readme/SKILL.md) | 1 | Drafts or updates `README.md` from `docs/`, my notes, my Obsidian vault, and Drive, Gmail and Slack |
| [`project-spec`](project-spec/SKILL.md) | 2 | Drafts and revises `SPEC.md` with phases and workstreams |
| [`spec-issues`](spec-issues/SKILL.md) | 3 | Creates labels and one issue per work item from `SPEC.md`, and keeps them in sync |
| [`work-item`](work-item/SKILL.md) | 4, 6, 7, 8 | Takes one issue through branch, PR, agent and developer feedback, rebase and squash-merge |
| [`pr-review`](pr-review/SKILL.md) | 5 | Starts the content and code review agents on a PR and posts their findings |
| [`content-review`](content-review/SKILL.md) | 5 | Reviews report prose as a project manager would read it |
| [`literature-review`](literature-review/SKILL.md) | 4 | Collects published values for a work item: searches, adds papers to Zotero, extracts each number with its source and page, and writes a values table and note |

`/code-review` is built into Claude Code, so it isn't in this repo.

## Rules that apply throughout

- **One agent, one work item.** An agent works on one issue, one branch and
  one PR. It doesn't check out, edit or push to another item's branch.
- **Each agent gets its own worktree,** so agents working in parallel don't
  share a working directory.
- **Neat, readable commits.** Each commit is one logical step with a brief,
  human-readable description of the work done ("Add WS3 fetch of ~100 m
  ocean-colour maps"), so the history reads as a record of the project.
- **GitHub is the record.** Progress, decisions and review feedback go in
  issues and PRs, so a new agent can pick up the work from GitHub alone.
- **Outside sources are read-only.** The skills read the developer's
  Obsidian vault and search Drive, Gmail and Slack, but never edit the vault
  or send, post, share or edit anything through a connector. In the vault
  they open only notes about the project.
- **No merge without developer approval.** Every PR goes through the
  developer review stage, and only an explicit approval ("merge it", or an
  approving PR review) allows the squash-merge.

## Install

Link each skill into the user skills folder so it's available in every
project:

```bash
for d in */; do
  [ -f "$d/SKILL.md" ] && ln -sfn "$PWD/${d%/}" ~/.claude/skills/"${d%/}"
done
```

The skills need:

- the [GitHub CLI](https://cli.github.com) (`gh`), signed in
- the Google Drive, Gmail and Slack connectors, for `/project-readme`. Without
  them it uses `docs/`, Obsidian and my notes only, and says so.
- optionally, an Obsidian vault. See [Personal settings](#personal-settings).
- for `/literature-review`: web search, and a Zotero MCP server connected to
  the developer's library (for adding papers, reading PDFs and checking
  retractions). Without Zotero it can still search and read open-access
  papers, but keeps no library and says so. Optionally, Claude in Chrome
  fetches paywalled papers through the developer's own journal access, one
  at a time, stopping at sign-ins and payment pages.

## Personal settings

The skills are shared, so they contain no one's paths or accounts. Each
person keeps their own settings in their personal `~/.claude/CLAUDE.md`,
which Claude Code loads in every session and which isn't in this repo.

| Setting | Line in `~/.claude/CLAUDE.md` | Used by | If not set |
|---|---|---|---|
| Obsidian vault | `Obsidian vault: ~/Documents/Notes` | `/project-readme`, `/project-spec` | Taken from Obsidian's own vault list if there's only one, otherwise the skill asks and offers to save the answer |

A `--vault <path>` argument overrides the setting for one run. Each vault is
read using its own `CLAUDE.md` or `README.md` to learn its layout, so
different folder structures work. Connectors (Drive, Gmail, Slack) use each
person's own claude.ai connections, so they need no setting.
