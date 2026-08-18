# Data governance and Korean calibration

## Purpose

Use NVIDIA Nemotron-Personas-Korea for synthetic population engineering and stress testing, not as a survey or behavioral oracle.

## Required dataset facts

Verify the current dataset card before every study. Version 1.0, released on 2026-04-20, documents one million records, seven million persona texts, 26 fields, adult ages 19+, 17 provinces, and 252 districts. The data are completely artificial and licensed CC BY 4.0. The card also states that some demographic factors are assigned under independence assumptions and that interaction effects may be absent.

Do not silently carry these numbers into later years. Record the exact card revision or commit used.

## Allowed analytical fields

Prefer these structural fields:

- `age`
- `sex`
- `province` or `district`
- `education_level`
- `bachelors_field` when a study genuinely needs it
- `occupation`
- `marital_status`, `family_type`, or `housing_type` only when justified

Exclude these from durable analytical outputs:

- `uuid`
- all `*_persona` fields and `persona`
- `cultural_background`
- skills, hobbies, interests, goals, ambitions, and other narrative text

The dataset is synthetic, but minimizing narrative and identifier fields prevents accidental profiling patterns and reduces unnecessary storage.

## Aggregate contract

Use schema version 1 with the following required root keys:

```json
{
  "schemaVersion": 1,
  "source": "NVIDIA Nemotron-Personas-Korea",
  "dataset": "nvidia/Nemotron-Personas-Korea",
  "datasetVersion": "1.0",
  "license": "CC BY 4.0",
  "sampleSize": 100000,
  "retainedSampleSize": 99980,
  "strata": []
}
```

Each stratum must contain only `ageGroup`, `sex`, `region`, `education`, `occupation`, and positive integer `count`. Require `sum(count) == retainedSampleSize <= sampleSize`.

## Korean official-statistics audit

Create `calibration-register.csv` with columns:

- variable or joint margin;
- source agency and table identifier;
- reference period;
- population universe;
- transformation;
- target moment;
- synthetic moment;
- absolute and relative error;
- resulting weight or parameter;
- limitation.

Use current sources appropriate to the question:

- KOSIS for population, education, occupation, industry, and region margins;
- Regional Employment Survey for age × sex × education × occupation × region;
- KLIPS for income, wealth proxies, job transitions, and longitudinal heterogeneity;
- Bank of Korea for AI exposure, complementarity, adoption, productivity, and employment evidence;
- business and ICT-use surveys for firm-size and organizational-capability gaps.

Fit weights with iterative proportional fitting or calibration weighting. Cap extreme weights, report effective sample size, and rerun results under alternative caps. Do not claim the reweighted synthetic rows become observed people.

## Data statement template

State that NVIDIA records are fully synthetic, specify the dataset version and CC BY 4.0 attribution, list fields retained and discarded, identify every official calibration table, describe independence assumptions, and prohibit individual-level or causal interpretation.

## Red flags

Stop and revise if a result:

- calls personas respondents, citizens, survey participants, or observations of behavior;
- quotes persona narratives as evidence;
- predicts elections, opinions, health, credit, crime, or eligibility;
- uses names or UUIDs as model features;
- reports national estimates without official-data calibration and uncertainty;
- infers causality from synthetic associations;
- hides cells, exclusions, weights, or failed validation.
