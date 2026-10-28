# Values review

For questions that need numbers: parameters, conversion factors, reference
ranges, stocks and rates. For example, "what is the sediment carbon stock of
a *Zostera marina* meadow?"

## Scope (step 1)

- **Quantities.** Each value the analysis needs, with its units and
  convention. For example: sediment organic carbon stock (Mg C ha⁻¹, to
  what depth?), shoot density (shoots m⁻²), height-to-biomass relationship,
  carbon fraction of dry mass.
- **Context that makes a value comparable.** Species, region, habitat,
  depth, season, and the method conventions that change the number (core
  depth, dry vs wet mass, above- vs below-ground).
- **Assumptions**, written as questions the literature can answer. For
  example, "one stock per hectare for the whole meadow" assumes the stock
  doesn't vary with shoot density, cover or depth; "is that true?" is part
  of the review.
- **Done when:** at least one sourced value or range per quantity, or a
  clear statement that none was found and what was searched.

## Search (step 3)

1. **Reviews and meta-analyses** for each quantity. They give ranges and
   point to the primary studies.
2. **Regional primary studies:** the same species and the nearest
   comparable sites, then wider regions if nothing close exists.
3. **Citations**, as in the shared step 3.
4. **Local and grey literature** near the site, as in the shared step 3.
   For values this often holds the only site measurements: a core from the
   next bay is worth more than a regional mean.

In step 3a, look first for newer measurements in the same region, deeper
cores or more sites from the same authors, and synthesis databases that can
be filtered to the species and region for a benchmark.

## Extract (step 5)

One row per value:

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

For key papers, also record the relationships the authors tested between
the quantities (including weak or null results, with R², p and n) and
site-level values, not only the headline value.

Rules:

- **Copy numbers exactly** as printed, with their units. Do unit
  conversions in separate columns, with the formula, so they can be
  checked.
- **Don't average across papers** in the extraction table. Synthesis is
  step 6.

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
- **Recalculations.** If a later source recomputes a value with a
  different method, record both and the reason they differ.

## Synthesise (step 6)

1. **Answer first:** the value or range to use for each quantity, and why
   (closest site, same convention, largest sample).
2. **Where the sources disagree,** and what the disagreement depends on
   (core depth, season, method).
3. **The assumptions,** each answered with what the literature found, or
   marked untested.
4. **Gaps:** quantities with no suitable value, what was searched, and what
   would fill the gap (a site measurement, a partner's data, a paywalled
   paper).
5. **Caveats** that carry into the analysis, such as values from other
   regions or from abstracts only.

## Deliver (step 7)

- **Values table** as CSV, for example `data/literature/<topic>.csv`, one
  row per extracted value.
- **The rule:** no number from memory. Every value traces to a paper read
  in this review. If you recall a value but can't find the paper, leave it
  out and say so.
