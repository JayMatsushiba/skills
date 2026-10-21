---
name: content-review
description: Review the prose of an analysis report (Quarto .qmd, Markdown, README) as a project manager would read it, not the code. Checks that main findings are clear and up front, cuts technical detail the reader doesn't need, shortens wording, replaces jargon and metaphors with plain language, removes absolute statements, and makes claims that something doesn't exist say what was searched. Use when asked to "content review", "PM review", review report wording, or tighten notebook text. Pass file paths to review; pass --fix to apply the edits.
argument-hint: "[paths...] [--fix]"
---

# Content review

Read the target documents as a project manager (PM) reading a data-analysis
report. The PM wants to know what was found, how confident we are, and what it
means for the project. The PM does not read code and does not need method
details unless they change how a finding should be read.

This is not a code review. Do not comment on code correctness, style, or
performance.

## Scope

**Targets.** Review the paths in the arguments. With no paths, review `.qmd`
and `.md` files changed on the current branch versus `main`
(`git diff --name-only main...HEAD` plus uncommitted changes). If there are
none, ask which files to review.

**Review this text** (what appears in the rendered report):

- Markdown prose, headings, and lists
- YAML `title` and `subtitle`
- Figure and table captions (`#| fig-cap:`, `#| tbl-cap:`, `: Caption {#tbl-…}`)
- Callout boxes
- Strings that code renders as text, such as `Markdown(f"...")` output or table
  column labels. Edit only the string literal, never the surrounding code.

**Skip** code, code comments, and YAML options other than title and subtitle.
Code comments are where technical detail moved out of the prose belongs.

## Checks

Apply each check to every passage in scope.

1. **Main findings first.** The opening section (summary or key findings)
   should state the results in a few short bullets or sentences. Each finding
   should say what was found and, if it matters, how sure we are. Flag findings
   that are buried later in the document, missing from the summary, or
   phrased so the result is unclear.

2. **Cut detail the PM doesn't need.** Remove or move to a code comment:
   processing steps, parameter values, file formats, library names,
   intermediate statistics, and caveats that don't change how a finding should
   be read. Keep a method detail only if the reader needs it to judge the
   finding (for example, "values are model estimates, so results are
   descriptive").

3. **Fewer words.** Prefer the shortest wording that keeps the meaning.
   Remove filler ("it is worth noting that", "in order to", "as can be seen"),
   repeated points, and sentences that restate a figure without adding a
   conclusion. Split long sentences.

4. **Plain language.** Replace jargon with everyday words where a plain word
   exists ("averaged to coarser cells" over "upscaled via block aggregation").
   If a technical term is unavoidable, define it briefly at first use and use
   it the same way afterwards. Spell out acronyms at first use.

5. **No metaphors or analogies.** Replace figurative language with a literal
   statement ("the signal is lost" not "the signal drowns"; "a small part of
   one cell" not "a speck in the cell").

6. **No absolute statements.** Flag words such as *never, always, all, none,
   every, no, only, entirely, completely, impossible, guaranteed, clearly,
   obviously* when they generalise beyond what was measured. Rewrite with the
   actual scope ("in the four surveys examined", "in 9 of 10 blocks", "rarely").
   A count of what was measured is fine ("higher in all 10 blocks"), because it
   is a result, not a generalisation.

7. **Qualify claims that something doesn't exist.** Statements like "there is
   no relevant data", "no relationship was found", or "this isn't available"
   must say what was searched or tested. Example: "There is no relevant data"
   → "Neither the CMEMS catalogue nor the HydroSurv deliverables include
   nitrate measurements for the site." If the document doesn't say what was
   searched and you can't tell from the code or data, flag it as a question
   for the author instead of inventing the scope.

## Output

Report findings grouped by file, in document order. For each finding give:

- **Where:** `path:line`
- **Check:** which check (1–7)
- **Current:** the passage, quoted (trim long passages with `…`)
- **Suggested:** the rewrite, or "delete", or "move to code comment"

Keep explanations to one short clause. The rewrite should make the reason
obvious. Group repeated instances of the same issue into one finding with a
list of locations.

End with:

- Word count of the reviewed prose before, and the estimate after the
  suggested edits.
- Open questions for the author, such as absence claims (check 7) whose
  search scope you couldn't determine.

## Applying edits (`--fix`)

With `--fix`, apply the suggested rewrites directly with the Edit tool, then
report a short list of what changed and the open questions. Do not change
numbers, units, or the meaning of a finding. If a rewrite would need a fact you
don't have (for example, what was searched), leave the passage and list it as
an open question. If the document is a Quarto file, render it afterwards
(`quarto render <file>`) when the environment allows, to confirm it still
builds.
