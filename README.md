# Skills

Claude Code skills for how I run projects with Claude. The workflow goes from
an idea to merged work: README, then SPEC, then GitHub issues, then one
branch and one PR per work item, with agent reviews before each merge.

It is based on the [Ambrosia](https://github.com/OceanOS-MVP/Ambrosia)
project, where it was first used.

## Workflow

```
 docs/ + my notes ──► /project-readme ──► README.md
 Drive, Gmail, Slack ─┘                       │
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
          rebase on main if needed ──► squash-merge ──► issue closes
```

1. **README.** Write `README.md` myself, or put key files (reports, meeting
   notes, papers, emails) in `docs/` and run `/project-readme`. It also
   searches Google Drive, Gmail and Slack for context, and records where each
   fact came from.
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
7. **Merge.** If `main` has moved on since the branch started, the agent
   rebases the branch onto `main`. Then the PR is squash-merged, which closes
   the issue.

## Skills

| Skill | Stage | What it does |
|---|---|---|
| [`project-readme`](project-readme/SKILL.md) | 1 | Drafts or updates `README.md` from `docs/`, my notes, and Drive, Gmail and Slack |
| [`project-spec`](project-spec/SKILL.md) | 2 | Drafts and revises `SPEC.md` with phases and workstreams |
| [`spec-issues`](spec-issues/SKILL.md) | 3 | Creates labels and one issue per work item from `SPEC.md`, and keeps them in sync |
| [`work-item`](work-item/SKILL.md) | 4, 6, 7 | Takes one issue through branch, PR, review feedback, rebase and squash-merge |
| [`pr-review`](pr-review/SKILL.md) | 5 | Starts the content and code review agents on a PR and posts their findings |
| [`content-review`](content-review/SKILL.md) | 5 | Reviews report prose as a project manager would read it |

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
- **Connectors are read-only.** The skills search Drive, Gmail and Slack but
  never send, post, share or edit anything there.
- **Ask before merging.** Squash-merging is the developer's call unless they
  have said otherwise for the project.

## Install

Link each skill into the user skills folder so it's available in every
project:

```bash
for d in */; do
  [ -f "$d/SKILL.md" ] && ln -sfn "$PWD/${d%/}" ~/.claude/skills/"${d%/}"
done
```

`~/.claude/skills/content-review` already exists as a folder. Move it out of
the way first if you want it to point at this repo's copy.

The skills need:

- the [GitHub CLI](https://cli.github.com) (`gh`), signed in
- the Google Drive, Gmail and Slack connectors, for `/project-readme`. Without
  them it uses `docs/` and my notes only, and says so.
