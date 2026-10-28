# Methods review

For questions about how to measure, estimate or model something. For
example, "how should we map meadow extent from drone imagery?" or "which
loss-on-ignition to organic carbon conversion should we use?"

## Scope (step 1)

- **The job.** What the method has to produce, in what units, at what
  resolution and over what area or period. For example: meadow extent in
  hectares, to ±10 %, for a 40 ha bay, once a year.
- **Constraints.** The data, equipment, staff time, budget and software the
  project has or can get. A method that needs an elemental analyser is out
  if the project only has a muffle furnace.
- **Required standard.** Any protocol, methodology or reporting framework
  the result must meet (for example a carbon crediting methodology, a
  national inventory guideline, a funder's monitoring protocol). It may
  rule methods in or out before any comparison.
- **Candidate methods.** The ones already named in the issue, `SPEC.md` or
  by people on the project, and the ones the search turns up. Treat any
  named from memory as unverified until found and read.
- **Assumptions**, written as questions the literature can answer. For
  example, "a global LOI to OC equation is good enough" assumes the local
  sediment's carbon fraction of organic matter is close to the global one.
- **Done when:** each candidate method has been described from its source,
  its accuracy against a reference is known or marked untested, and one
  method is recommended for the project's data, or the note says why none
  fits.

## Search (step 3)

1. **Standards and protocol manuals** that apply to the job. They name the
   accepted methods and their minimum requirements.
2. **Comparison studies:** papers that apply two or more methods to the
   same samples, sites or images. These are the strongest evidence, because
   only the method differs.
3. **Validation studies:** a method checked against an independent
   reference (ground truth, a reference instrument, a known standard).
4. **Applications in the region or habitat:** studies that used a method
   under conditions like the project's, including grey literature and
   theses. They show whether it works there and what went wrong.
5. **Code and data:** software, scripts, trained models and benchmark
   datasets that come with the method (GitHub, Zenodo, Figshare, package
   registries). Record the version and licence.

In step 3a, a key paper is the one that proposes or validates the
recommended method. Forward citations matter most: look for later
validations, failures in other conditions, corrections, and newer versions
of the method.

## Extract (step 5)

One row per method per study:

| Column | Example (made up) |
|---|---|
| `method` | random forest classification of RGB drone orthomosaics |
| `variant` | 3 cm resolution, 500 training points, texture features |
| `measures` | seagrass presence/absence per pixel |
| `inputs` | RGB imagery at low tide, ground-truth quadrats |
| `assumptions` | clear water, seagrass visible at survey tide |
| `reference` | 120 quadrats, visual cover |
| `accuracy` | overall 91 %, seagrass user's accuracy 84 % |
| `error_metric`, `n` | confusion matrix, 120 |
| `conditions` | intertidal, *Z. noltei*, Brittany, Sept 2021 |
| `failed_when` | patchy cover < 20 %, macroalgae present |
| `effort` | 2 days field, 1 day processing per site |
| `software` | R `ranger` 0.15, code on Zenodo (DOI …) |
| `standard` | meets / doesn't meet / not stated |
| `validated_by` | authors / independent |
| `source` | Zotero key or citation key, and DOI |
| `location` | Methods, p. 4; Table 3 |
| `access` | full text / abstract only |
| `notes` | anything that limits comparability |

Rules:

- **Copy accuracy figures exactly**, with the metric they're stated in.
  Overall accuracy, kappa, RMSE and R² are not interchangeable; don't
  convert one into another.
- **Describe the method from the paper,** not from what the method is
  usually understood to be. Variants matter: the same name often covers
  different settings, equations or sampling designs.
- **Don't rank methods** in the extraction table. Comparison is step 6.

**Check the evidence behind each method:**

- **Who validated it.** A method's own paper usually reports its best
  case. Record whether a check was done by the authors or independently,
  and prefer independent ones.
- **What it was checked against.** A reference that is itself an estimate
  (another model, a coarser survey) is weaker than a direct measurement.
  If there was no independent reference, say so in `notes`.
- **Same data or not.** Accuracy figures from different studies, sites or
  references can't be compared directly. Only comparison studies (search
  step 2) rank methods on equal terms.
- **Overfitting and leakage.** For fitted or trained methods, check that
  the accuracy comes from data not used to fit the model (a held-out set,
  cross-validation by site). Flag accuracy measured on the training data.
- **Transfer.** Note where the conditions differ from the project's
  (species, sediment, water clarity, sensor). A method that works in one
  place may not work in another, and the note must say which assumptions
  can be checked at the project's site.

## Synthesise (step 6)

1. **Answer first:** the method to use with the project's data, its
   expected accuracy, and why (validated under similar conditions, meets
   the standard, fits the budget).
2. **Comparison table:** the candidate methods side by side on accuracy,
   data needs, effort, standard and transfer to the site. Only rank them
   where a comparison study supports it; otherwise say the figures come
   from different studies.
3. **Where the sources disagree,** and what the disagreement depends on
   (site conditions, settings, reference used).
4. **The assumptions,** each answered with what the literature found,
   marked untested, or marked "test at the site", with how.
5. **Gaps:** methods with no independent validation, conditions nobody has
   tested, and what would fill the gap (a pilot comparison, a validation
   set).
6. **Caveats** that carry into the analysis, such as the error to carry
   into uncertainty estimates.

## Deliver (step 7)

- **Methods table** as CSV, for example `data/literature/<topic>_methods.csv`,
  one row per method per study.
- **A protocol note:** the recommended method as steps the analysis can
  follow, with the settings, software versions and source for each step,
  and the checks to run on the project's data. It goes in the repo next to
  the note, or as a draft section of `SPEC.md` if the developer prefers.
- **The rule:** no method detail from memory. Every setting, equation and
  accuracy figure traces to a paper or manual read in this review.
