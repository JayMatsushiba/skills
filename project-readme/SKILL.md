---
name: project-readme
description: Draft or update a project's README.md as the first step of a new project. Reads the developer's notes, the files in docs/ and the developer's Obsidian vault (notes, meetings, writing, brainstorms), searches Google Drive, Gmail and Slack for more context, and writes a README that says what the project is, who is involved, what inputs exist and what is still open, with the source of each fact. Use when starting a project, when asked to "write the README", "set up the project context", "gather context from Obsidian/Drive/email/Slack", or to refresh the README after new documents arrive.
argument-hint: "[project name or search terms] [--vault <path>] [--no-obsidian] [--no-connectors]"
---

# Project README

The README is the shared context for everything that follows: `SPEC.md`, the
GitHub issues, and every agent that picks up a work item. It describes the
project as it is. It does not plan the work; that belongs in `SPEC.md`
(`/project-spec`).

## 1. Collect what's in the repo

- **Existing `README.md`.** If the developer wrote one, it is the main
  source. Keep their framing and wording where it's accurate, and add to it
  rather than rewriting it.
- **`docs/`.** Read everything: reports, proposals, meeting notes and
  transcripts, papers, exported emails. Use the `pdf`, `docx`, `xlsx` and
  `pptx` skills for those formats. Note each file's date and author.
- **Notes in the request.** Anything the developer typed counts as a source.

## 2. Read the Obsidian vault

Many developers keep notes, meeting write-ups, drafts and brainstorms in an
Obsidian vault. These often hold the clearest statement of what the project
is for, and ideas that never made it into an email. Skip this step with
`--no-obsidian`, or if the developer doesn't use Obsidian.

**Find the vault.** Each developer has their own vault in their own place, so
never assume a path. Use the first of these that gives one:

1. `--vault <path>` in the arguments.
2. An `Obsidian vault:` line in the developer's `~/.claude/CLAUDE.md`, for
   example `Obsidian vault: ~/Documents/Notes`. This file is personal and
   isn't in this repo.
3. Obsidian's own list of vaults: `~/.config/obsidian/obsidian.json` on
   Linux, `~/Library/Application Support/obsidian/obsidian.json` on macOS,
   `%APPDATA%\obsidian\obsidian.json` on Windows. Use it only if it lists
   exactly one vault, or exactly one marked `"open": true`.
4. Ask the developer. Offer to save the answer as an `Obsidian vault:` line
   in their `~/.claude/CLAUDE.md`, and only add it if they agree.

**Learn the vault's layout.** Vaults are organised differently. Read the
vault's own `CLAUDE.md`, `README.md` or home note first, and follow the
folders and properties it describes. Common things to look for:

- **A project note or folder:** a note or folder named after the project, or
  a note whose properties link this repository (for example a `repo:`
  property with the git remote URL). Read it, the other notes in its folder,
  and any attached documents.
- **Meeting notes** that name the project, its partners or its people. Link
  properties (such as `project:`) are often empty, so search note text as
  well.
- **People and organisation notes** for everyone linked from the project
  note or the meetings, for their roles.
- **Writing and brainstorms:** thoughts, drafts, daily notes and quick
  notes that mention the project or its key terms.
- **Links:** notes link with `[[wikilinks]]`, so follow links out of the
  project note and search for notes that link to it
  (`grep -rl "\[\[<Project>" <vault>`).

If the vault has no clear structure, search the whole vault by project name,
partner organisations, people and key terms, and read the matching notes.

Rules:

- **Read only.** Don't create, edit, move or rename anything in the vault.
  If a note looks out of date or a link is missing, mention it in the
  summary instead.
- **Stay on the project.** Open only notes that are about the project. Skip
  personal and financial notes (taxes, invoices, CVs, health, journals that
  don't mention the project) and credential files (for example
  `client_secret*.json`, `.env`), even if a search hits them.
- **Brainstorms aren't decisions.** Thoughts, daily notes and braindumps
  hold ideas. Report them as ideas ("the developer's notes from 2026-10-12
  suggest …"), and keep the ones about planning the work for the SPEC.
  Facts confirmed in a meeting note can go in the README, citing the
  meeting.
- Use the note's date (from its date property or file name) when citing
  it.

## 3. Search the connectors

Skip this step with `--no-connectors`, or if a connector isn't available
(then say which ones were skipped in the summary).

Build search terms from the project name, partner organisations, people,
grant or contract numbers, and key technical terms found in steps 1 and 2. Run the
searches in parallel:

- **Google Drive:** `search_files` by name and full text, then
  `read_file_content` on the relevant hits (proposals, plans, reports,
  meeting notes, spreadsheets).
- **Gmail:** `search_threads` (for example `"<project>" OR from:<partner
  domain>`), then `get_thread` on the relevant threads. Look for decisions,
  confirmations, data deliveries and deadlines.
- **Slack:** `slack_search_public_and_private`, then `slack_read_thread` on
  the relevant threads. Look for scope changes, earlier plans and who owns
  what.

Rules:

- **Read only.** Never send, reply, post, share, label, move or edit
  anything through a connector.
- **Newest wins.** When sources disagree, prefer the most recent one, and
  write down the disagreement if it still matters.
- **Don't copy private content into the repo wholesale.** Summarise. Before
  saving a file from Drive or an email attachment into `docs/`, ask the
  developer, because `docs/` is usually committed.
- Stop searching once new results stop adding facts. Report what was searched
  so the developer can point to anything missed.

## 4. Write the README

Use the sections that fit the project, in roughly this order:

1. **Title and one-paragraph summary:** what the project is, for whom, and
   where.
2. **Status:** short bullets, current as of today. What's done, what's
   waiting on whom, what's due next.
3. **Project:** goals, funding or client, duration, the main question or
   problem, and any change of direction and why.
4. **People and partners:** a table of organisation (or person), role and
   what they provide or own.
5. **Inputs:** data sources, systems, documents or APIs the work depends on.
   For each one: what it is, who provides it, what has arrived, what is still
   expected, and known problems.
6. **Timeline:** milestones and deadlines, with dates.
7. **Open questions:** what isn't known yet, and who could answer it.
8. **Running the project:** setup and commands, once code exists.

Writing rules:

- **Say where facts came from** when they aren't obvious, with person,
  organisation, channel and date. For example: "Confirmed by Simon Gibbs
  (HydroSurv) by email on 2026-10-19." Link files in `docs/` by relative
  path.
- **Use absolute dates** (2026-10-19), never "last week".
- **Plain language.** Spell out acronyms at first use. Short sentences. No
  metaphors.
- **Qualify absence claims:** "The HydroSurv deliverables include no
  water-quality data", not "there is no water-quality data".
- Put facts in the README, plans in the SPEC. If you find a plan or a
  decision about the work, keep it for the SPEC and mention it in the
  summary.

## 5. Hand back

Don't commit unless asked. Reply with:

- what was added or changed in the README
- sources used, grouped by Obsidian, Drive, Gmail, Slack and `docs/`, and any
  source that was skipped
- conflicts between sources, and open questions for the developer
- plans or decisions found that should go into `SPEC.md`

The next step is `/project-spec`.
