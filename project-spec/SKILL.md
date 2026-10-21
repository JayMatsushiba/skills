---
name: project-spec
description: Draft or revise SPEC.md, the execution plan for a project, from README.md and the context gathered for it. The spec sets the purpose, key decisions, scope, assumptions, and the work split into phases and numbered workstreams (WS0, WS1, …), each with a goal, steps and a "done when" line. Use after /project-readme, when asked to "write the spec", "plan the phases", or to revise the spec after feedback. Iterates with the developer until the spec is accurate; pass a section or a change request to revise part of it.
argument-hint: "[change request or section to revise]"
---

# Project SPEC

`SPEC.md` says what work will be done, in what order, and when each piece is
finished. It is written to be split into GitHub issues: each workstream
becomes one or more issues (`/spec-issues`), and each issue becomes one
agent's branch and PR. So every workstream must be a piece of work one agent
can finish on its own.

## Inputs

- `README.md` (required; if it's missing, run `/project-readme` first)
- `docs/`, and the decisions or plans `/project-readme` reported
- the developer's Obsidian notes on the project: the project note, meeting
  notes, and brainstorms and drafts (find the vault and notes as in
  `/project-readme` step 2). Brainstorms are ideas, not decisions: put an
  idea in the spec only if the developer confirms it, or list it under Open
  questions.
  Read only; don't edit the vault.
- the developer's instructions and feedback in this conversation
- if the spec already exists and issues have been created, the GitHub issues
  (`gh issue list --state all`), so the spec reflects what's done

## Structure

```markdown
# <Project>: Execution Spec (Draft)

**Status:** Draft, updated YYYY-MM-DD
**Owner:** <name>
**Reviewers:** <names>

## 1. Purpose and framing
One or two paragraphs: what will be delivered and what won't.

**Key decisions:** short bullets, each one decided (with who and when, if known).

### Phasing
- **Phase A: <name>.** What it covers and what it needs to start.
- **Phase B: <name>.** …

### Out of scope
Bullets, each with the reason.

### Assumptions
Bullets: what we're taking as true, and who confirmed it.

## 2. Setup
### WS0: Repository and environment

## 3. Phase A: <name>
### WS1: <name>
**Goal:** one or two lines.

1. Numbered steps, specific enough to turn into a task checklist.
   - Sub-points for detail, choices and caveats.

**Done when:** a checkable result (for example, "a notebook produces the
per-survey metric table and the change maps").

## 4. Phase B: <name>
…

## N. Dependencies and blockers
What each workstream waits on: other workstreams, partners, data.

## N+1. Risks
## N+2. Open questions
Each with who can answer it.

## N+3. Implementation notes
Libraries, file formats, parameters and other technical detail, grouped by
workstream. This keeps the sections above readable for non-developers.
```

## Rules for workstreams

- **Phases group work by what it depends on,** not by topic. Work that can
  start now goes in an earlier phase than work waiting on data, a partner or
  another phase.
- **Number workstreams in order across the whole spec** (WS0, WS1, …). The
  numbers become issue labels and branch names, so when renumbering, say so
  in the summary so labels and issues can be updated.
- **One workstream, one deliverable.** If a workstream needs several
  separate PRs, split it, or mark the step boundaries where it splits into
  issues.
- **Every workstream has a "Done when"** that someone else can check.
- **Optional or time-boxed work** says so in the heading, for example
  "(optional, time-boxed: 3 days)".
- Steps say what to do and why, not how to code it. Code-level detail goes
  in Implementation notes.

## Writing rules

- Plain language, short sentences, acronyms spelled out at first use, no
  metaphors.
- Absolute dates. Name who made each decision or confirmation.
- Link to README sections instead of repeating them (for example the
  timeline), and to issues once they exist (`[#5](…/issues/5)`).

## Iterating

The developer will revise the spec over several rounds. In each round:

1. Make the requested change, and any edits elsewhere that it implies (for
   example, a scope change that affects Out of scope, Assumptions and the
   affected workstreams).
2. Update the **Status** date.
3. Reply with a short list of what changed and the open questions that
   remain. Ask at most a few questions, most important first, and only ones
   the developer has to answer. Pick sensible defaults for the rest and say
   what you picked.

Don't create issues while the spec is still changing. When the developer
says the spec is ready, the next step is `/spec-issues`. If issues already
exist, tell the developer which ones the change affects.
