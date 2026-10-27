---
name: literature-review
description: Find, collect and extract values from published literature for a project question, with every number traced to a paper that was actually read. Scopes the quantities needed, checks the developer's Zotero library and connectors for what's already there, searches the web (reviews first, then regional studies, local grey literature, and for key papers their references, citing papers, authors' later work and synthesis databases), adds papers to a Zotero collection by DOI with open-access PDFs and retraction checks, hands paywalled or blocked papers to the developer as DOI links and merges the duplicates that follow, extracts each value with units, site, method and page or table after checking the method behind it, and delivers a values table and a short note. Use when an issue or the SPEC asks to "compile published values", "find something in the literature", "do a literature review", or to look up parameters, conversion factors or reference ranges for an analysis.
argument-hint: "<issue number or topic> [--collection <name>] [--open-access-only] [--no-connectors] [--no-browser]"
---

# Literature review

Turns a question ("what is the sediment carbon stock of a *Zostera marina*
meadow?") into a table of published values the analysis can use, and a short
note saying which values to use and why. Every number in the table comes from
a paper that was read for this review, never from memory.

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
`README.md`:

- **Quantities.** Each value the analysis needs, with its units and
  convention. For example: sediment organic carbon stock (Mg C ha⁻¹, to
  what depth?), shoot density (shoots m⁻²), height-to-biomass relationship,
  carbon fraction of dry mass.
- **Context that makes a value comparable.** Species, region, habitat,
  depth, season, and the method conventions that change the number (core
  depth, dry vs wet mass, above- vs below-ground).
- **Assumptions behind the values.** How the analysis will apply each
  value, written as questions the literature can answer. For example,
  "one stock per hectare for the whole meadow" assumes the stock doesn't
  vary with shoot density, cover or depth; "is that true?" is part of the
  review.
- **Weight.** How much each quantity moves the result. Where the analysis
  already exists, take this from its sensitivity analysis; otherwise
  estimate it. Quantities that drive the result get the deep search in
  step 3a; minor ones may stop at a review value.
- **Starting points.** Papers already named in the issue or by people on
  the project. Treat any that came from memory, including your own, as
  unverified until found and read.
- **Done when.** Usually: at least one sourced value or range per quantity,
  or a clear statement that none was found and what was searched. For the
  quantities that drive the result, also: step 3a done and recorded.

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

Search in this order, and run independent searches in parallel:

1. **Reviews and meta-analyses** for each quantity. They give ranges and
   point to the primary studies.
2. **Regional primary studies:** the same species and the nearest
   comparable sites, then wider regions if nothing close exists.
3. **Citations:** follow the best papers backwards (their references) and
   forwards (`scite_enrich_item` or a web search for papers citing them).
   For the quantities that drive the result, this is step 3a and is
   required.
4. **Local and grey literature** near the site: reports by councils,
   statutory agencies, NGOs, consultancies and universities, and theses.
   These often hold the only site measurements and rarely show up in
   journal searches. Search the names of neighbouring sites and the wider
   area (bay, estuary, protected area), not only the site itself: a core
   from the next bay is worth more than a regional mean. Look on the
   project pages of the organisation that commissioned the work, and
   follow each report's own citations to the primary report behind its
   numbers.

   **Dead links happen.** Record the old URL, then try the web archive's
   capture list for it and the organisation's current project pages. If
   that fails, stop: take the values as a later report reproduces them
   (and say so), and list the report as a request to its author or the
   organisation, as a GitHub issue or a draft email for the developer.
   Don't spend long hunting.

Use `WebSearch` in standard mode first, and extended mode for niche or
hard-to-find topics. For a broad topic with many sub-questions, the
`deep-research` skill can run several search agents in parallel; check its
sources the same way before using any number from it.

Don't stop at the first usable number. Stop when new searches only return
papers already found and, for the quantities that drive the result, step
3a is done. Keep a list of the queries run: it goes in the note, so absence
claims say what was searched.

### 3a. Key papers: read deeply and follow every lead

A key paper is one that supplies a value for a quantity that drives the
result. For each one:

1. **Extract everything in scope, not only the headline value.** Every
   quantity from step 1, the relationships the authors tested between
   them (including weak or null results, with R², p and n), site-level
   values, and the method choices that change the number (conversion
   equations such as loss on ignition to organic carbon, core depth,
   extrapolation). A null result can answer an assumption from step 1.
2. **Screen the whole reference list.** Read each reference's title and
   decide: read, skip, or not accessible, with a reason. Read every one
   that reports the same quantities, tests what drives them, or covers the
   same region.
3. **Find the papers citing it** (`scite_enrich_item`, then a web search
   such as "cited by" on Google Scholar, Semantic Scholar or OpenAlex).
   Screen them the same way, looking first for newer measurements in the
   same region and for re-analyses of the key paper's data.
4. **Follow the authors.** Search each author's later papers, theses
   (institutional repositories) and reports, and the research group's
   reports. Later work often adds sites, deeper cores or corrections.
5. **Read the syntheses the newer papers cite.** A citing paper's
   introduction often names a recent review or synthesis that searches
   missed. Read it, and check whether it publishes its underlying
   database (Figshare, Zenodo, a data repository). If it does, download it
   and query it directly: filter to the species and region for a
   benchmark, and test the step 1 assumptions where the data allow. Say so
   when the data can't test a question (for example, too few rows with
   both variables).
6. **Look for recalculations.** If a later source recomputes the key
   paper's values with a different method, record both and the reason
   they differ.

Record the trail for each key paper in the note: references screened and
read, citing papers screened and read, author searches run, databases
queried, and papers not accessible.

**Parallel agents.** The backward, forward and author trails are
independent and can run as parallel agents. Give each one the skill, the
collection, the papers already held, and a separate output CSV and query
log. Agents report in the same confident tone whether or not they're
right, so check every number that changes the answer against the PDF
yourself before reporting it, and say which rows you checked.

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
- **Tag** each item with the quantities it reports (for example
  `sediment-carbon`, `shoot-density`).
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
If only the abstract is available, a value can be taken from it but is marked
`abstract only`.

For each value, record one row:

| Column | Example (made up) |
|---|---|
| `quantity` | sediment organic carbon stock |
| `value`, `low`, `high` | 140, 90, 190 |
| `spread` | SD, SE, range or IQR, and `n` |
| `units` | Mg C ha⁻¹ |
| `convention` | top 100 cm, extrapolated from 30 cm cores |
| `species`, `site`, `region` | *Z. marina*, Studland Bay, England |
| `habitat`, `depth_m`, `date` | subtidal, 2–4, summer 2018 |
| `method` | loss on ignition, converted with … |
| `source` | Zotero key or citation key, and DOI |
| `location` | Table 2, p. 7 |
| `access` | full text / abstract only |
| `notes` | anything that limits comparability |

Rules:

- **Copy numbers exactly** as printed, with their units. Do unit
  conversions in separate columns, with the formula, so they can be
  checked.
- **Don't average across papers** in the extraction table. Synthesis is
  step 6.
- **Quote sparingly.** A short quote for a key definition or method is fine;
  don't copy whole tables or paragraphs into the repo.

**Check the method behind each number** before it goes in the table:

- **Conversions.** How was the value derived? For example, organic carbon
  from loss on ignition depends on the conversion equation: a local
  regression, a global one, or an elemental analyser. Record which one in
  `method`.
- **What was measured.** Organic matter is not organic carbon, content per
  volume is not a stock over a depth, and a stock to 1 m may be
  extrapolated from 30 cm. If the methods don't say, note it and don't
  compare the value with the others.
- **Implausible values.** A value far outside every other source, or units
  that don't fit, usually means a scaling or units error. Flag it in
  `notes` and leave it out of the synthesis.
- **Independent checks.** Prefer studies that compare methods on the same
  samples (for example, conversion equations against an elemental
  analyser); they show which way a method biases the number.

## 6. Synthesise

Write a short note that a project manager can read:

1. **Answer first:** the value or range to use for each quantity, and why
   (closest site, same convention, largest sample).
2. **Where the sources disagree,** and what the disagreement depends on
   (core depth, season, method).
3. **The assumptions from step 1,** each answered with what the
   literature found, or marked untested.
4. **Gaps:** quantities with no suitable value, what was searched (the query
   list from step 3), and what would fill the gap (a site measurement, a
   partner's data, a paywalled paper).
5. **Caveats** that carry into the analysis, such as values from other
   regions or from abstracts only.

Plain language, absolute dates, qualified absence claims ("the searched
literature reports no …"). Cite each value by author, year and table or
page.

## 7. Deliver

- **Values table** as CSV in the repo (for example
  `data/literature/<topic>.csv`), one row per extracted value.
- **The note** as Markdown or a notebook page, following the repo's style.
- **Bibliography:** export the Zotero collection
  (`zotero_export_bibliography`, BibTeX) next to the table.
- **No PDFs in git.** Full texts stay in Zotero, for copyright and size.
- **Questions for people outside the team** (a partner's site data, a
  missing value) go in GitHub issues, not the note.

## Rules that apply throughout

- **No number from memory.** Every value in the table traces to a paper read
  in this review. If you recall a value but can't find the paper, leave it
  out and say so.
- **No invented references.** Check that each DOI resolves and matches the
  title and authors before citing it.
- **Outside sources are read-only,** apart from adding items, tags, notes
  and collections to the developer's Zotero library.
- **Only licensed access.** Paywalled papers come through the developer's
  own access (steps 4a and 4b) or from the authors, never from shadow
  libraries, never by getting round bot checks, and never by paying.
- **Check agents' work.** Numbers from search agents, including
  `deep-research`, are checked against the PDF before they change the
  answer.

## Hand back

Reply with:

- the answer per quantity (value or range to use) and its main source
- the files written, the Zotero collection and the number of papers in it
- paywalled papers fetched through the browser, and the step 4b list of
  those still missing, with what they would change
- duplicates merged (keys kept and trashed)
- for each key paper, the trail followed (step 3a) and what it changed
- which numbers you checked against the PDF yourself
- gaps, disagreements and open questions
