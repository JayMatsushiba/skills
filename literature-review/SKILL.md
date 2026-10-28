---
name: literature-review
description: Find, collect and extract published literature for a project question, with every value, method detail or claim traced to a paper that was actually read. Handles three kinds of review — values (parameters, conversion factors, reference ranges), methods (how to measure, estimate or model something, compared on accuracy and fit to the project's data) and theory (frameworks, mechanisms and conceptual models, with the evidence for and against each claim). Scopes what's needed, checks the developer's Zotero library and connectors, searches the web (reviews and standards first, then primary studies, local grey literature, and for key papers their references, citing papers, authors' later work and synthesis databases), adds papers to a Zotero collection by DOI with open-access PDFs and retraction checks, hands paywalled or blocked papers to the developer as DOI links and merges the duplicates that follow, extracts into a table after checking the evidence behind each row, and delivers the table and a short note. Use when an issue or the SPEC asks to "compile published values", "find something in the literature", "do a literature review", "which method should we use", "compare approaches", "find a protocol", "what framework/theory explains", "build a conceptual model", or to look up parameters, conversion factors or reference ranges for an analysis.
argument-hint: "<issue number or topic> [--type values|methods|theory] [--collection <name>] [--open-access-only] [--no-connectors] [--no-browser]"
---

# Literature review

Turns a project question into a table the analysis can use and a short note
saying what to use and why. There are three kinds of review:

| Type | Question | Table | Reference |
|---|---|---|---|
| `values` | "what is the sediment carbon stock of a *Zostera marina* meadow?" | one row per value | [references/values.md](references/values.md) |
| `methods` | "how should we map meadow extent from drone imagery?" | one row per method per study | [references/methods.md](references/methods.md) |
| `theory` | "what explains how disturbance affects seagrass recovery?" | one row per claim, one per test of it | [references/theory.md](references/theory.md) |

Everything in the table comes from a paper read for this review, never from
memory.

**Pick the type** from `--type`, or from the request: numbers, parameters
and ranges are `values`; "how to measure", "which method", protocols and
models are `methods`; "why", frameworks, mechanisms and conceptual models
are `theory`. Say which type you chose. Then read its reference file before
step 1: it gives the type's scoping, search order, extraction columns,
evidence checks, synthesis and deliverables. The steps below are shared.

**Mixed reviews.** A question can need more than one type, for example a
method and the values it produces. Pass `--type methods,values`, read each
reference file, and work in the order theory, methods, values: the theory
says what to measure, the method says how, and the values come from studies
using that method. Use one Zotero collection, one table per type and one
note.

When the request is a GitHub issue, run this inside `/work-item <issue>`: the
table and note are the work item's output, and they go through the usual PR,
review and developer approval.

## 0. Check Zotero

Test the Zotero MCP before anything else, so a broken setup shows up before
papers are collected:

1. **Read:** `zotero_get_collections`. An error naming `YOUR_LIBRARY_ID`
   means the library ID is still a placeholder. The same error from Zotero's
   local API gives the real user ID ("use userID 0 or <id>"); for this
   session, `zotero_switch_library(library_id="0", library_type="user")`
   makes reads work.
2. **Write:** create the review's collection (step 4). "Invalid
   Authorization header format" or a 403 means there's no valid API key.
   Writes go through the Zotero web API even when reads are local.
3. **PDF support:** `zotero_read_pdf_pages` and `zotero_add_from_file` need
   PyMuPDF. Check with
   `~/.local/share/uv/tools/zotero-mcp-server/bin/python -c "import pymupdf"`
   (adjust the path if the MCP was installed another way). If it's missing,
   install it into that environment:
   `uv pip install --python ~/.local/share/uv/tools/zotero-mcp-server/bin/python pymupdf`.
   No reconnect is needed.

If check 1 or 2 fails, stop and give the developer the setup steps below.
Don't read or print the API key: the developer pastes it in themselves. If
they'd rather not set it up, carry on without a library and say so. A
failed check 3 needs no developer action: install PyMuPDF as described.

**Setup (done by the developer):**

1. Create a key at <https://www.zotero.org/settings/keys/new> with "Allow
   library access" and "Allow write access" under Personal Library.
2. In their own terminal, not with `!` in the session, so the key stays out
   of the transcript:

   ```bash
   claude mcp remove zotero -s user
   claude mcp add zotero -s user \
     -e ZOTERO_LOCAL=true \
     -e ZOTERO_LIBRARY_ID=<user ID> \
     -e ZOTERO_LIBRARY_TYPE=user \
     -e ZOTERO_API_KEY=<key> \
     -- zotero-mcp
   ```

3. Add PyMuPDF to the MCP's environment, so PDFs in Zotero can be read:
   `uv pip install --python ~/.local/share/uv/tools/zotero-mcp-server/bin/python pymupdf`
   (for a uv tool install; otherwise install `pymupdf` wherever
   `zotero-mcp` runs, or install `zotero-mcp-server[pdf]`).
4. Keep Zotero desktop open with sync on, then reconnect with `/mcp`.

This is hybrid mode: reads come from the local Zotero app, writes go through
the web API and reach the local app when it syncs.

## 1. Scope the question

Before searching, write down what's needed, from the issue, `SPEC.md` and
`README.md`. The reference file says what to list for the type (quantities,
the job a method must do, or what a theory is for). For every type, also
write down:

- **Assumptions.** How the analysis will use what the review finds,
  written as questions the literature can answer.
- **Weight.** How much each item moves the result. Where the analysis
  already exists, take this from its sensitivity analysis; otherwise
  estimate it. Items that drive the result get the deep search in step
  3a; minor ones may stop at a review.
- **Starting points.** Papers already named in the issue or by people on
  the project. Treat any that came from memory, including your own, as
  unverified until found and read.
- **Done when.** The reference file gives the usual criterion. For the
  items that drive the result, also: step 3a done and recorded.

Put this list at the top of the note (step 6), and in the issue if it
changes the issue's scope.

## 2. Check what's already there

- **Zotero.** Search the developer's library by topic
  (`zotero_semantic_search`) and by author or title
  (`zotero_search_items`). Reuse papers and notes already there.
- **Repo.** `docs/`, earlier notebooks and issues may already cite sources.
- **Connectors** (skip with `--no-connectors`, or if unavailable, and say
  so): search Google Drive and Gmail for partner reports, site data and
  grey literature the web won't find. Read only.

## 3. Search

Search in the order the reference file gives, and run independent searches
in parallel. Every type starts with the sources that summarise a field
(reviews, standards, founding sources) and ends with these two:

- **Citations:** follow the best papers backwards (their references) and
  forwards (`scite_enrich_item` or a web search for papers citing them).
  For the items that drive the result, this is step 3a and is required.
- **Local and grey literature** near the site: reports by councils,
  statutory agencies, NGOs, consultancies and universities, and theses.
  These often hold the only site measurements, the methods actually used
  nearby, and tests in the project's own system, and rarely show up in
  journal searches. Search the names of neighbouring sites and the wider
  area (bay, estuary, protected area), not only the site itself. Look on
  the project pages of the organisation that commissioned the work, and
  follow each report's own citations to the primary report behind it.

   **Dead links happen.** Record the old URL, then try the web archive's
   capture list for it and the organisation's current project pages. If
   that fails, stop: take the values as a later report reproduces them
   (and say so), and list the report as a request to its author or the
   organisation, as a GitHub issue or a draft email for the developer.
   Don't spend long hunting.

Use `WebSearch` in standard mode first, and extended mode for niche or
hard-to-find topics. For a broad topic with many sub-questions, the
`deep-research` skill can run several search agents in parallel; check its
sources the same way before using anything from it.

Don't stop at the first usable source. Stop when new searches only return
papers already found and, for the items that drive the result, step 3a is
done. Keep a list of the queries run: it goes in the note, so absence
claims say what was searched.

### 3a. Key papers: read deeply and follow every lead

A key paper is one that supplies a value, method or claim the result
depends on; the reference file says which papers count for its type. For
each one:

1. **Extract everything in scope, not only the headline.** Everything from
   step 1 the paper reports, including weak or null results. A null result
   can answer an assumption from step 1.
2. **Screen the whole reference list.** Read each reference's title and
   decide: read, skip, or not accessible, with a reason. Read every one
   that covers the same items, tests what drives them, or covers the same
   region or system.
3. **Find the papers citing it** (`scite_enrich_item`, then a web search
   such as "cited by" on Google Scholar, Semantic Scholar or OpenAlex).
   Screen them the same way. The reference file says what to look for
   first.
4. **Follow the authors.** Search each author's later papers, theses
   (institutional repositories) and reports, and the research group's
   reports. Later work often adds sites, revises a method or answers
   critics.
5. **Read the syntheses the newer papers cite.** A citing paper's
   introduction often names a recent review or synthesis that searches
   missed. Read it, and check whether it publishes its underlying
   database (Figshare, Zenodo, a data repository). If it does, download it
   and query it directly: filter to the species and region, and test the
   step 1 assumptions where the data allow. Say so when the data can't
   test a question (for example, too few rows with both variables).
6. **Look for revisions.** If a later source recomputes the key paper's
   values, revises its method or restates its claims, record both and the
   reason they differ.

Record the trail for each key paper in the note: references screened and
read, citing papers screened and read, author searches run, databases
queried, and papers not accessible.

**Parallel agents.** The backward, forward and author trails are
independent and can run as parallel agents. Give each one the skill, the
collection, the papers already held, and a separate output CSV and query
log. Agents report in the same confident tone whether or not they're
right, so check every row that changes the answer against the PDF yourself
before reporting it, and say which rows you checked.

## 4. Collect in Zotero

- **One collection per review,** named after the project and topic (for
  example `Ambrosia – seagrass carbon`), or `--collection <name>`.
- **Add by identifier:** `zotero_add_by_doi` (it tries to download an
  open-access PDF), `zotero_add_by_isbn` for books, `zotero_add_by_url` for
  reports. Check the DOI resolves to the paper you meant before adding.
- **Wait for sync.** In hybrid mode a new collection or item is visible to
  reads, and can be filed into, only after Zotero desktop syncs (a few
  seconds). If a call says the collection isn't found, check with
  `zotero_search_collections` and retry.
- **Every paper read has its PDF in Zotero.** That includes papers read as
  HTML or through the browser, and supplements. `zotero_add_by_doi` often
  finds no PDF, even for open-access papers. Don't use
  `zotero_add_from_file` to attach files: it reports "File attached", but
  the upload is rejected and nothing reaches Zotero. Instead:
  1. Create the item with `zotero_add_by_doi(attach_mode="none")`. For a
     report with no DOI, use `zotero_add_by_url`, or
     `zotero_add_from_file` with `title` and `item_type="report"`, which
     creates the item (still without the file).
  2. Download the PDF into its own directory and give it a readable name
     (`Author_Year_topic.pdf`).
  3. Upload it to the item with `scripts/upload_attachments.py` in this
     skill. It reads a manifest of `<item key> <path>` lines and uses the
     Zotero MCP's own Python and credentials, which it reads from the MCP
     configuration without printing them:

     ```bash
     eval "$(claude mcp get zotero | sed -n 's/^ *\(ZOTERO_API_KEY\|ZOTERO_LIBRARY_ID\)=\(.*\)$/export \1="\2"/p')"
     ~/.local/share/uv/tools/zotero-mcp-server/bin/python -I \
       ~/.claude/skills/literature-review/scripts/upload_attachments.py manifest.txt
     ```

     Each line should end `ok`, or `unchanged` (Zotero already stores an
     identical file and links to it). Uploads take several seconds each,
     so run a long batch in the background.
  4. Check with `zotero_library_coverage` once Zotero desktop has synced,
     and read page 1 of one PDF with `zotero_read_pdf_pages` to confirm
     the file itself arrived.
- **Tag** each item with the review type and what it covers (for example
  `values`, `sediment-carbon`; `methods`, `drone-mapping`; `theory`,
  `alternative-stable-states`).
- **Check retractions:** `scite_check_retractions` on the collection. Drop
  retracted papers from the table and say so.
- **Find missing full texts:** `zotero_library_coverage` on the collection.
  For each paper without a PDF, try the legal open routes first: the
  author's manuscript in an institutional repository or preprint server,
  then the publisher's open-access version. With `--open-access-only`,
  stop there and say which values that leaves out.
- **Fetch paywalled papers through the browser** (step 4a), if the
  developer has access. Otherwise hand them to the developer (step 4b).
- **Don't get round bot checks.** If a repository or publisher returns a
  bot check, CAPTCHA or 403, don't retry with a spoofed user agent,
  browser headers or another trick. List the paper for the developer
  (step 4b).

### 4a. Paywalled papers through Claude in Chrome

Use this only when Claude in Chrome is connected (its tools are named
`mcp__claude-in-chrome__*`; read the `chrome-browser` skill first) and the
developer has confirmed they have legitimate access: an institutional or
library login, a library proxy, or a personal subscription. Skip it with
`--no-browser`. This uses the developer's own access; it never gets round a
paywall.

1. **Ask once which access route to use** (for example "University library
   proxy" or "publisher login"), and which tool shows it on article pages
   (for example the LibKey Nomad extension's "Download PDF" link). Note the
   answer for the rest of the review.
2. **One paper at a time,** in a new tab: open the article page through
   that route and download the PDF, after the developer has approved
   downloading it. Read it locally and check it's the right paper, then
   add it to Zotero as in step 4 ("Every paper read has its PDF in
   Zotero"). Claude in Chrome can't use the Zotero Connector: its toolbar
   button and keyboard shortcut are handled by Chrome, outside the page.
   - Don't use the download button in Chrome's PDF viewer: it always opens
     a "Save as" dialog, which Claude can't operate. Instead, with the PDF
     open in a tab, start a normal link download with `javascript_tool`:
     `const a = document.createElement('a'); a.href = location.href;
     a.download = 'paper.pdf'; document.body.appendChild(a); a.click();`
     The file lands in the default downloads folder without a dialog
     (provided Chrome's "Ask where to save each file" setting is off). Move
     it into the review's own download directory before reading it.
   - Reading the full text on the publisher's HTML page is fine, but
     download the PDF too.
3. **Stop and hand over to the developer** at any sign-in, single sign-on,
   two-factor or CAPTCHA page. Continue after they have signed in.
4. **Never pay.** Stop at any purchase, "buy article" or rental page and
   list the paper as not accessible.
5. **Stay small.** Fetch only the papers this review needs, at the pace a
   person would. Publisher licences usually forbid automated bulk
   downloading, and too many downloads can get the developer's institution
   blocked. No crawling, no downloading whole issues or reference lists.
6. **Record the route** for each PDF in the extraction table's `access`
   column (`full text via library proxy`).

Never use shadow libraries or other unlicensed copies (for example
Sci-Hub or LibGen), even if a search result points to one.

### 4b. Hand missing papers to the developer

When the legal open routes fail and the browser route isn't available,
give the developer a list they can work through with their own access:

- **One link per paper:** `https://doi.org/<DOI>`, with author, year, a
  few words on what it would add, and the existing Zotero item key, so
  they attach the PDF to that item instead of creating a new one.
- **Check each DOI against Crossref** (`api.crossref.org/works/<DOI>`)
  before listing it. Citing papers sometimes print a wrong DOI; give the
  correct one and say so.
- **Group the list:** paywalled; blocked by a bot check (often open access
  in a normal browser); no DOI (reports, with title, publisher and the
  last known URL). Put first the papers that would change the answer.
- **Signed or expiring download links** (for example cloud storage URLs
  with `X-Amz-Expires`) stop working within minutes. Identify the document
  from the filename in the link instead of downloading it, and ask the
  developer to add it to Zotero if it's needed.

When the developer says they've added PDFs, list the collection again
before reading: the PDF may sit on the developer's own copy of the item,
not on the key you created (step 4c).

### 4c. Clean up duplicates

Adding PDFs through the Zotero Connector creates new items next to the
ones this review created. After each round of additions, and before
saying any item lacks a PDF:

1. **Find them:** `zotero_find_duplicates(collection_key=..., method="both")`.
   A library-wide scan can include items already in the trash; check the
   `deleted` flag before acting on one.
2. **Pick the keeper:** the copy with the PDF and fuller metadata, or the
   one with supplementary files if both have the main PDF.
3. **Merge:** `zotero_merge_duplicates` as a dry run first, then with
   `confirm=True`. Tags, collections, notes and attachments move to the
   keeper; the other copies go to the trash, where they can be restored.
4. **Check skipped attachments.** If the merge reports "duplicate
   attachments skipped", compare the files' MD5 (`md5` in the attachment
   data) to confirm nothing was lost.
5. **Check again after sync** with `zotero_find_duplicates`, and list the
   item keys kept and trashed in the hand-back.

Zotero is the developer's own library: add items, tags, notes and
collections freely. Merge duplicates inside the review's collection, and
items this review created, as above. Don't delete, merge or edit other
existing items, including duplicates outside the collection, unless the
developer asks. Items this review created by mistake (failed imports) may
be moved to the Zotero trash with `zotero_delete_item`. Say which ones, and
never empty the trash.

## 5. Read and extract

Read each paper's full text: `zotero_get_item_fulltext` or
`zotero_read_pdf_pages` for PDFs in Zotero (including those fetched in step
4a), `WebFetch` for open-access pages.
If only the abstract is available, a row can be taken from it but is marked
`abstract only`.

Record one row per item in the columns the reference file gives. Every
table has `source` (Zotero key or citation key, and DOI), `location` (table,
figure or page), `access` (full text, abstract only, or the route used) and
`notes` (anything that limits comparability).

Rules for every type:

- **Copy as printed.** Numbers with their units and metrics, definitions
  and claims as the source states them. Conversions and paraphrases go in
  separate columns, so they can be checked.
- **Don't combine across papers** in the extraction table. Averaging,
  ranking and weighing evidence are step 6.
- **Quote sparingly.** A short quote for a key definition, method or claim
  is fine; don't copy whole tables or paragraphs into the repo.
- **Check the evidence behind each row** before it goes in the table, with
  the checks in the reference file: how a number was derived, how a method
  was validated, or whether a study really tested a claim. A row that fails
  a check stays in the table with the reason in `notes`, and is left out of
  the synthesis.

## 6. Synthesise

Write a short note that a project manager can read, in the order the
reference file gives. For every type it covers:

1. **Answer first:** what to use (value, method or framework) and why.
2. **Where the sources disagree,** and what the disagreement depends on.
3. **The assumptions from step 1,** each answered with what the
   literature found, or marked untested.
4. **Gaps:** what has no suitable source, what was searched (the query list
   from step 3), and what would fill the gap.
5. **Caveats** that carry into the analysis.

For a mixed review, give one answer per type, in the order theory,
methods, values, and say how they connect.

Plain language, absolute dates, qualified absence claims ("the searched
literature reports no …"). Cite each row by author, year and table or
page.

## 7. Deliver

- **Tables** as CSV in the repo (for example `data/literature/<topic>.csv`),
  named and laid out as the reference file says.
- **The note** as Markdown or a notebook page, following the repo's style,
  with any extra deliverable the reference file names (a protocol note, a
  causal diagram).
- **Bibliography:** export the Zotero collection
  (`zotero_export_bibliography`, BibTeX) next to the table.
- **No PDFs in git.** Full texts stay in Zotero, for copyright and size.
- **Questions for people outside the team** (a partner's site data, a
  missing value) go in GitHub issues, not the note.

## Rules that apply throughout

- **Nothing from memory.** Every value, method detail and claim in the
  tables traces to a paper read in this review. If you recall one but
  can't find the paper, leave it out and say so.
- **No invented references.** Check that each DOI resolves and matches the
  title and authors before citing it.
- **Outside sources are read-only,** apart from adding items, tags, notes
  and collections to the developer's Zotero library.
- **Only licensed access.** Paywalled papers come through the developer's
  own access (steps 4a and 4b) or from the authors, never from shadow
  libraries, never by getting round bot checks, and never by paying.
- **Check agents' work.** Rows from search agents, including
  `deep-research`, are checked against the PDF before they change the
  answer.

## Hand back

Reply with:

- the review type, and the answer per item (value or range, method, or
  framework to use) and its main source
- the files written, the Zotero collection and the number of papers in it
- paywalled papers fetched through the browser, and the step 4b list of
  those still missing, with what they would change
- duplicates merged (keys kept and trashed)
- for each key paper, the trail followed (step 3a) and what it changed
- which rows you checked against the PDF yourself
- gaps, disagreements and open questions
