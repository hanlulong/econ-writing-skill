# Writing by Identification Strategy

Different identification strategies and paper types require different narrative structures. Adapt your writing to the method.

---

## Randomized Controlled Trials (RCTs)
- Lead with the intervention and its policy relevance
- Describe randomization mechanism and balance tests early
- Emphasize intent-to-treat (ITT) as main specification; discuss compliance and LATE separately
- Address attrition and spillovers as primary threats to identification
- Report take-up rates -- they are central to interpreting treatment effects
- Pre-analysis plan: if registered, state the registry number in the introduction
- Structure results as: ITT first, then LATE/IV if compliance is imperfect, then heterogeneity
- External validity is often the main concern -- discuss what populations the results generalize to

## Difference-in-Differences (DiD)
- Lead with the policy change or natural experiment that generates treatment variation
- The parallel trends assumption is the core of your identification -- devote a full paragraph to it
- Show pre-trends visually (event study plot is mandatory for modern DiD papers)
- Discuss treatment timing variation and staggered adoption if relevant
- If using staggered DiD, address recent econometric concerns (Goodman-Bacon, Sun and Abraham, Callaway and Sant'Anna)
- Report results with and without covariates to show sensitivity
- Discuss anticipation effects if the policy was announced before implementation
- Address compositional changes in treated vs. control groups over time

## Instrumental Variables (IV)
- Name the instrument in the first paragraph of the introduction
- Devote a full paragraph to instrument relevance (first stage F-statistic; report the Kleibergen-Paap or effective F-statistic)
- Devote a full paragraph to the exclusion restriction -- argue it economically, not just statistically
- Report both OLS and IV estimates; explain why they differ (measurement error, selection, LATE vs. ATE)
- Discuss what the complier population looks like -- who are the marginal individuals whose behavior is shifted by the instrument?
- If the instrument is weak (F < 10), use Anderson-Rubin confidence intervals
- Address the monotonicity assumption if estimating LATE
- Common instruments to discuss carefully: Bartik/shift-share (Goldsmith-Pinkham, Sorkin, and Swift 2020), judge/examiner leniency, historical/geographic instruments

## Regression Discontinuity (RDD)
- Lead with the running variable and the cutoff
- Show the discontinuity visually (RD plot is mandatory -- this is your "figure 1")
- Discuss manipulation of the running variable (McCrary/density test)
- Present bandwidth sensitivity analysis -- results should be stable across reasonable bandwidths
- Report local polynomial estimates with optimal bandwidth (Calonico, Cattaneo, and Titiunik)
- Emphasize that RDD estimates are LOCAL to the cutoff -- discuss external validity explicitly
- For fuzzy RDD: report both reduced form (jump in outcome) and first stage (jump in treatment) separately
- Address any other discontinuities at the cutoff that might confound your estimates

## Synthetic Control
- Lead with the treated unit and the event/policy
- Describe donor pool selection criteria (why these comparison units?)
- Show pre-treatment fit visually -- this is your identification (if pre-treatment fit is poor, the method fails)
- Present placebo tests (permutation inference) as the primary inference tool
- Discuss what the synthetic counterfactual means substantively
- Report donor weights -- which comparison units receive the most weight?
- Address concerns about interpolation bias if donor units are very different from treated unit
- For multiple treated units, consider the augmented/penalized synthetic control or the synthetic DiD

## Structural Estimation
- Clearly state the economic model and its key assumptions in plain English before the math
- Distinguish between identifying assumptions (testable or untestable) and functional form assumptions
- Explain identification intuitively: what variation in the data pins down each parameter?
- Report model fit -- show the model can replicate key moments in the data
- Validate with out-of-sample predictions when possible
- Counterfactual simulations are the payoff -- present them prominently
- Discuss sensitivity to key assumptions: what if risk aversion is different? What if agents have different information?
- Compare structural estimates to reduced-form estimates where possible for credibility

## Descriptive and Measurement Papers
- Lead with why the measurement/description matters for economics
- Be explicit: "This paper does not estimate a causal effect. It documents [pattern/fact/measurement]."
- Describe the data construction process in detail -- this IS the contribution
- Show robustness of descriptive patterns to alternative definitions and samples
- Discuss what causal questions the new facts enable future researchers to answer
- Relate your descriptive findings to existing theoretical predictions

---

## Adapting the Introduction by Paper Type

| Paper Type | Hook Strategy | What Goes in Paragraphs 4-6 | Key Threat to Discuss |
|-----------|--------------|-----------------------------|-----------------------|
| RCT | Policy relevance of intervention | ITT and LATE estimates | Attrition, spillovers, external validity |
| DiD | Policy change or natural experiment | Main DiD estimate + event study | Parallel trends, anticipation |
| IV | The instrument and why it's clever | OLS vs. IV comparison | Exclusion restriction, weak instruments |
| RDD | The cutoff and its stakes | RD estimate + bandwidth sensitivity | Manipulation, other discontinuities |
| Synthetic Control | The treated unit and the event | Synthetic vs. actual trajectory | Pre-treatment fit, donor pool |
| Structural | The economic question that requires a model | Key counterfactual results | Model assumptions, external validity |
| Theory | The puzzle or paradox the model resolves | Main proposition and intuition | Robustness of mechanism to assumptions |
| Descriptive | Why the fact/measurement matters | Key patterns with magnitudes | Measurement validity, sample selection |
