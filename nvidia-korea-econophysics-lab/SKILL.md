---
name: nvidia-korea-econophysics-lab
description: Build rigorous economic-physics and social-physics studies from NVIDIA Nemotron-Personas-Korea, including privacy-preserving demographic aggregation, Korean official-statistics calibration, network or agent-based models, Monte Carlo and phase-transition experiments, journal-ready papers, policy briefs, and React/TypeScript/Three.js simulators. Use when a user mentions NVIDIA Korean personas, Korean synthetic agents, sovereign/public AI inequality, econophysics, sociophysics, Korean policy ABMs, distributional simulations, or interactive inequality laboratories. Do not treat synthetic personas as surveys, real people, causal evidence, or nationally representative joint distributions.
---

# NVIDIA Korea Econophysics Lab

Create one reproducible research system in which the data contract, equations, batch experiments, paper, and interactive simulator agree.

## Start with a research contract

Write `research-contract.md` before coding. Record:

- research question and falsifiable hypotheses;
- target population, unit of analysis, time step, and horizon;
- mechanisms and competing explanations;
- interventions and baseline;
- primary outcomes and inequality or polarization metrics;
- calibration, validation, uncertainty, and falsification plans;
- permitted claims and prohibited claims.

If the user provides a paper or repository, inspect its equations, assumptions, tests, and data lineage before extending it. Preserve existing work and isolate new changes on a feature branch.

## Apply the data boundary

Read [references/data-governance.md](references/data-governance.md) whenever data are downloaded, transformed, calibrated, or described.

Treat `nvidia/Nemotron-Personas-Korea` as fully synthetic microdata. Use it to construct heterogeneous strata, test rare scenarios, or generate interface examples. Never infer public opinion, causal policy effects, or real individual behavior from it.

Before analysis:

1. Fetch the current NVIDIA dataset card and record version, date, license, fields, and stated limitations.
2. Stream only required rows; do not download the full corpus unless the task requires it.
3. Exclude UUIDs, names, personas, goals, hobbies, biographies, and other narrative fields from analytical outputs.
4. Aggregate to age × sex × region × education × broad occupation.
5. Validate the aggregate profile with `scripts/validate_nvidia_korea_profile.py`.
6. Audit and reweight joint distributions against current KOSIS, Regional Employment Survey, KLIPS, and Bank of Korea evidence.
7. Preserve attribution required by CC BY 4.0.

Use the bundled preparation script:

```bash
python scripts/prepare_nvidia_korea_profile.py \
  --rows 100000 \
  --region-mode province \
  --occupation-mode broad \
  --output data/nvidia-korea-profile.json

python scripts/validate_nvidia_korea_profile.py \
  data/nvidia-korea-profile.json --strict
```

Install `datasets` only when Hugging Face streaming is needed. For tests or secured environments, pass `--input-jsonl` instead.

## Design the mechanism model

Read [references/model-and-experiments.md](references/model-and-experiments.md) for equations, metrics, calibration, and experiment design.

Separate observed or calibrated inputs from model assumptions. Keep all tunable constants in one typed configuration. At minimum model:

- heterogeneous resources, AI capability, occupation exposure and complementarity;
- access, premium-quality gaps, adoption, trust, and effective use;
- skill accumulation and peer learning on a homophilous network;
- job displacement, mobility, junior career-ladder loss, and regional frictions;
- labor income, transfers, AI-capital ownership, returns, and wealth accumulation;
- policy costs, financing, and welfare or distributional outcomes.

Use the same initial population and random-number streams for paired policy comparisons. Keep the Python research engine authoritative; expose versioned JSON inputs and outputs to the frontend.

## Run publication-grade experiments

Do not stop at one attractive trajectory. Run:

1. deterministic smoke tests and accounting identities;
2. paired Monte Carlo replications with confidence intervals;
3. ablations for each proposed mechanism;
4. global sensitivity analysis using Morris or Sobol methods;
5. finite-size and time-horizon checks;
6. phase-boundary scans and hysteresis tests when claiming econophysics;
7. alternative network topologies and homophily levels;
8. out-of-sample moment checks against Korean official data.

Report null results and policy failure regions. Label results as model-conditional comparative statics unless an explicit causal design supports stronger language.

## Build the simulator and paper

Read [references/simulation-and-publication.md](references/simulation-and-publication.md) when creating a React/Three.js app, paper, policy brief, or journal submission package.

For the simulator:

- use React, TypeScript, Vite, and Three.js;
- provide presets, parameter ranges, seed control, playback, comparisons, CSV/JSON export, and a 2D accessible fallback;
- show data provenance and limitations next to the upload control;
- keep heavy Monte Carlo computation outside the browser;
- configure the Vite base path and GitHub Actions Pages deployment for the repository name;
- test calculations separately from rendering and run typecheck, unit tests, and production build.

For the paper:

- include an ODD-style model description and equation-to-code crosswalk;
- distinguish calibration targets, assumptions, and estimated parameters;
- report uncertainty, sensitivity, ablation, finite-size, and robustness results;
- include a data statement, license attribution, ethics statement, and reproducibility checklist;
- select a journal by actual contribution, not by vocabulary.

## Choose the correct publication claim

- Target economic-interaction or computational-economics journals when the contribution is heterogeneous agents, policy, welfare, and distribution.
- Target JASSS or computational social-science journals when generative explanation, network mechanisms, and transparent ABM validation dominate.
- Target Physica A or a social-physics venue only when the study establishes order parameters, scaling, critical regions, clustering, universality, or hysteresis rather than merely displaying an ABM.

Read [references/experiment-recipes.md](references/experiment-recipes.md) for reusable prompts and study designs. Read [references/sources.md](references/sources.md) before writing the literature review or bibliography, then refresh time-sensitive facts from current primary or official sources.

## Enforce completion gates

Do not call the work complete until all applicable gates pass:

- dataset card and license captured;
- aggregate profile validated and forbidden narrative fields absent;
- Korean joint-distribution audit documented;
- deterministic seeds and configuration snapshot saved;
- tests, Monte Carlo uncertainty, ablations, and sensitivity reported;
- claims match evidence strength;
- paper, code, figures, and UI use the same model version;
- README contains exact reproduction and deployment commands;
- repository status is clean and the requested branch or pull request is published.
