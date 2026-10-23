---
name: literature-review
description: Find, collect and extract values from published literature for a project question, with every number traced to a paper that was actually read. Scopes the quantities needed, checks the developer's Zotero library and connectors for what's already there, searches the web (reviews first, then regional studies, then citations), adds papers to a Zotero collection by DOI with open-access PDFs and retraction checks, extracts each value with units, site, method and page or table, and delivers a values table and a short note. Use when an issue or the SPEC asks to "compile published values", "find something in the literature", "do a literature review", or to look up parameters, conversion factors or reference ranges for an analysis.
argument-hint: "<issue number or topic> [--collection <name>] [--open-access-only] [--no-connectors]"
---

# Literature review

Turns a question ("what is the sediment carbon stock of a *Zostera marina*
meadow?") into a table of published values the analysis can use, and a short
note saying which values to use and why. Every number in the table comes from
a paper that was read for this review, never from memory.

When the request is a GitHub issue, run this inside `/work-item <issue>`: the
table and note are the work item's output, and they go through the usual PR,
review and developer approval.

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
- **Tag** each item with the quantities it reports (for example
  `sediment-carbon`, `shoot-density`).
- **Check retractions:** `scite_check_retractions` on the collection. Drop
  retracted papers from the table and say so.
- **Find missing full texts:** `zotero_library_coverage` on the collection.
  List the paywalled papers for the developer, who may have institutional
  access and can add the PDFs to Zotero. With `--open-access-only`, skip
  them and say which values that leaves out.

Zotero is the developer's own library: add items, tags, notes and
collections, but don't delete, merge or edit existing items without asking.

## 5. Read and extract

Read each paper's full text: `zotero_get_item_fulltext` or
`zotero_read_pdf_pages` for PDFs in Zotero, `WebFetch` for open-access pages.
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

## Hand back

Reply with:

- the answer per quantity (value or range to use) and its main source
- the files written, the Zotero collection and the number of papers in it
- paywalled papers the developer could add, and what they would change
- gaps, disagreements and open questions
