---
name: literature-review
description: Find, collect and extract values from published literature for a project question, with every number traced to a paper that was actually read. Scopes the quantities needed, checks the developer's Zotero library and connectors for what's already there, searches the web (reviews first, then regional studies, then citations), adds papers to a Zotero collection by DOI with open-access PDFs and retraction checks, fetches paywalled papers through Claude in Chrome when the developer has legitimate access, extracts each value with units, site, method and page or table, and delivers a values table and a short note. Use when an issue or the SPEC asks to "compile published values", "find something in the literature", "do a literature review", or to look up parameters, conversion factors or reference ranges for an analysis.
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
- **Starting points.** Papers already named in the issue or by people on
  the project. Treat any that came from memory, including your own, as
  unverified until found and read.
- **Done when.** Usually: at least one sourced value or range per quantity,
  or a clear statement that none was found and what was searched.

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

Use `WebSearch` in standard mode first, and extended mode for niche or
hard-to-find topics. For a broad topic with many sub-questions, the
`deep-research` skill can run several search agents in parallel; check its
sources the same way before using any number from it.

Stop when new searches only return papers already found. Keep a list of the
queries run: it goes in the note, so absence claims say what was searched.

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
  developer has access. Otherwise list them for the developer, who can ask
  the authors or a partner with access, or add the PDFs to Zotero by hand.

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

Zotero is the developer's own library: add items, tags, notes and
collections, but don't delete, merge or edit existing items without asking.
Items this review created by mistake (duplicates, failed imports) may be
moved to the Zotero trash with `zotero_delete_item`. Say which ones, and
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

## 6. Synthesise

Write a short note that a project manager can read:

1. **Answer first:** the value or range to use for each quantity, and why
   (closest site, same convention, largest sample).
2. **Where the sources disagree,** and what the disagreement depends on
   (core depth, season, method).
3. **Gaps:** quantities with no suitable value, what was searched (the query
   list from step 3), and what would fill the gap (a site measurement, a
   partner's data, a paywalled paper).
4. **Caveats** that carry into the analysis, such as values from other
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
  own access (step 4a) or from the authors, never from shadow libraries,
  and never by paying.

## Hand back

Reply with:

- the answer per quantity (value or range to use) and its main source
- the files written, the Zotero collection and the number of papers in it
- paywalled papers fetched through the browser, and those still missing
  with what they would change
- gaps, disagreements and open questions
