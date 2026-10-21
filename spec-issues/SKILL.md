---
name: spec-issues
description: Turn the workstreams in SPEC.md into GitHub issues, one per work item, with context, a task checklist and acceptance criteria, labelled by phase and workstream. Also creates issues for open questions that need someone outside the team. Use when the spec is ready and the developer asks to "create the issues", "put the spec in GitHub", or to sync issues after the spec changed. From then on, progress is tracked in GitHub.
argument-hint: "[WS numbers to limit to] [--sync]"
---

# SPEC to GitHub issues

Each issue is one work item: one agent, one branch, one PR. Write each issue
so an agent that has only the issue, `README.md` and `SPEC.md` can do the
work.

## 1. Read the current state

- `SPEC.md` and `README.md`
- the repository: `gh repo view --json nameWithOwner`
- existing labels and issues:
  `gh label list --limit 200` and `gh issue list --state all --limit 200`

If the spec still says it's waiting on decisions the work depends on, list
them and ask before creating anything.

## 2. Plan the issues

Split each workstream into work items:

- **One issue per PR-sized piece of work.** Usually one per workstream. Split
  a workstream when its steps produce separate results that can be reviewed
  and merged on their own (for example "inventory and extraction" and
  "comparison"), or when one part is blocked and another isn't.
- **Questions for people outside the team** (partners, clients, data
  providers) get their own issue, labelled `partner` or `data-request`, so the
  answer is tracked and can be linked from the spec.
- **Don't duplicate.** If an open or closed issue already covers the item,
  reuse it and note it in the plan.

Labels:

- phase: `phase-a`, `phase-b`, …
- workstream: `ws<N>-<short-name>`, for example `ws1-surveys`
- type, where useful: `analysis`, `setup`, `data-quality`, `data-request`,
  `partner`, `reporting`, `optional`
- topic labels the project already uses

Show the developer the plan as a table (title, workstream, labels, blocked
by) and wait for approval before creating labels or issues. Creating issues
is visible to everyone with access to the repository.

## 3. Write each issue

Title: an imperative sentence that says what will be done, for example "Load
HydroSurv survey outputs and reproduce monthly metrics and change maps".

Body:

```markdown
## Context
Why this work is needed and what it builds on, in a few sentences. Who asked
for it and when, if known. Link the SPEC section:
[SPEC WS1](https://github.com/<owner>/<repo>/blob/main/SPEC.md#ws1-…).

## Tasks
- [ ] Specific, checkable steps from the spec.
  - [ ] Sub-steps where useful.

## Acceptance
- The spec's "Done when", plus anything a reviewer should check.

## Blocked by
- #N, or the partner or data it waits on. Leave out if nothing.
```

Rules:

- Plain language, absolute dates, names for who confirmed what.
- Put file and module names in tasks only where the spec decided them.
- Optional or time-boxed work says so in Context, along with what counts as
  an acceptable negative result.

Create labels first (`gh label create <name> --color <hex>`), then issues,
in spec order so the numbers follow the workstreams:

```bash
gh issue create --title "…" --label "phase-a,ws1-surveys,analysis" --body-file /tmp/issue-ws1.md
```

## 4. Sync after spec changes (`--sync`)

Compare the spec with the existing issues and propose:

- new issues for new work items
- edits to open issues whose tasks or acceptance changed
  (`gh issue edit N --body-file …`)
- closing issues for work that was dropped, with a comment that points to
  the spec change (`gh issue close N --reason "not planned" --comment …`)
- label changes after workstreams were renumbered

Don't edit issues that are in progress (with an open PR or a linked branch)
without saying so in the plan, because an agent is working from them.

## 5. Hand back

Reply with the created or changed issues as a table (number, title, labels)
and their links. The next step is `/work-item <issue>` for each issue that
isn't blocked, one agent per issue.
