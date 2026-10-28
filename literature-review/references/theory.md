# Theory review

For questions about why something happens or how to frame it: theories,
frameworks, mechanisms and conceptual models. For example, "what explains
how disturbance affects seagrass recovery?" or "which ecosystem services
framework should the valuation follow?"

## Scope (step 1)

- **What the theory is for.** How the analysis will use it: choosing
  which variables to measure, setting a causal structure for a model,
  defining terms for a report, or justifying an assumption. This decides
  how deep the review goes.
- **The phenomenon.** What has to be explained or framed, in the project's
  terms. For example: "recovery time of a meadow after a mooring is
  removed", not "seagrass resilience".
- **Candidate theories.** The ones already named in the issue, `SPEC.md` or
  by people on the project, and the ones the search turns up. Treat any
  named from memory, including your own, as unverified until the founding
  source is found and read.
- **Assumptions**, written as questions the literature can answer. For
  example, "recovery follows the same path as loss" assumes no hysteresis;
  "has that been tested for this species?" is part of the review.
- **Done when:** each candidate theory's core claims are stated from its
  founding source, the evidence for and against each claim the analysis
  relies on is summarised, and one framework is recommended, or the note
  says why the evidence doesn't settle it.

## Search (step 3)

1. **Founding sources:** the paper, book or chapter that first set out each
   theory, and any later restatement by the same authors. Read these
   rather than a summary of them.
2. **Reviews and critiques:** papers that assess the theory as a whole,
   name its limits, or propose revisions.
3. **Empirical tests:** studies that test a claim of the theory, ideally in
   the same system (species, habitat, region). Experiments and long time
   series test causal claims more strongly than one-off correlations.
4. **Rival theories:** other explanations of the same phenomenon, and
   papers that test one against another.
5. **Applied frameworks:** guidance documents, standards and agency
   reports that use the theory in practice (for example a management
   framework built on it). They show how it has been put into numbers.

In step 3a, a key paper is the founding source of the recommended theory,
or the strongest test of a claim the analysis relies on. Forward citations
matter more than backward ones here: that's where the tests, critiques and
revisions are. For founding sources with thousands of citing papers, screen
the citing papers that also match the phenomenon or system, not all of
them, and say how the list was narrowed.

## Extract (step 5)

Two tables. **Claims**, one row per claim per theory, taken from the
founding source:

| Column | Example (made up) |
|---|---|
| `theory` | alternative stable states |
| `claim` | loss and recovery follow different paths (hysteresis) |
| `terms` | "stable state": … (definition as given, p. 3) |
| `prediction` | recovery needs conditions better than those at loss |
| `scope` | systems with strong feedbacks between plants and sediment |
| `source` | Zotero key or citation key, and DOI |
| `location` | p. 3, para. 2 |

**Evidence**, one row per test of a claim:

| Column | Example (made up) |
|---|---|
| `theory`, `claim` | alternative stable states, hysteresis |
| `result` | supports / contradicts / mixed / not tested directly |
| `design` | 12-year time series, 4 meadows; or transplant experiment |
| `measured_as` | how the terms were turned into variables |
| `effect` | size, uncertainty and `n`, as printed |
| `system` | *Z. marina*, Wadden Sea |
| `rival` | the competing explanation the study considered, if any |
| `source`, `location`, `access` | as above |
| `notes` | anything that weakens the test |

Rules:

- **State claims as the source states them.** Paraphrase closely and give
  the page; quote the key definitions. Don't sharpen a hedged claim or
  generalise its scope.
- **Don't score theories** in the extraction tables. Weighing the evidence
  is step 6.
- **Quote sparingly.** Short quotes for definitions and core claims are
  fine; don't copy passages.

**Check the evidence behind each claim:**

- **Citation drift.** Later papers often summarise a theory more strongly,
  more broadly or differently than its founding source. When a paper cites
  the theory for a claim, check the claim against the founding source, and
  record in `notes` where the two differ.
- **What was tested.** A study that fits the theory's pattern isn't always
  a test of it: check whether a rival explanation would predict the same
  result. Record the rival in `rival` and mark the result `not tested
  directly` if both predict it.
- **How the terms were measured.** Two studies can test "resilience" with
  different variables and reach different answers. Record each in
  `measured_as`, and only compare tests that measured the same thing.
- **Scope.** Note where the tested system differs from the project's.
  Evidence from another system supports the claim there, not here.
- **Publication bias.** Supporting results are published more often than
  null ones. Search for null results and failed replications by name, and
  say if none were found.

## Synthesise (step 6)

1. **Answer first:** the framework to use, in one or two sentences, and
   why (best supported in this system, fits the analysis's question, used
   by the standard or partner).
2. **What it implies for the analysis:** the variables to measure, the
   causal links to model, and the assumptions it adds. This is the part
   the next work item will use.
3. **How well tested each relied-on claim is:** tested in this system,
   tested elsewhere, or untested, with the main studies.
4. **Where the rivals differ:** what a rival theory would predict
   differently for this project, and whether the project's data could tell
   them apart.
5. **Gaps and caveats:** claims with no test, terms with no agreed
   measurement, and drift between the founding source and how it's cited.

Where it helps, add a short causal diagram (Mermaid in the note) showing
the variables and links the framework implies, each link labelled with its
evidence level.

## Deliver (step 7)

- **Claims and evidence tables** as CSV, for example
  `data/literature/<topic>_claims.csv` and `<topic>_evidence.csv`.
- **The note**, with the diagram if there is one.
- **Follow-ups:** the quantities and methods the framework says the
  analysis needs, listed for a values or methods review if they aren't
  already covered.
- **The rule:** no claim from memory. Every claim and every "this theory
  says" traces to a passage read in this review, with its page.
