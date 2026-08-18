# Simulation and publication workflow

## Contents

1. One model, two runtimes
2. Research engine
3. React and Three.js interface
4. Verification
5. Paper structure
6. Journal fit
7. Korean policy output

## 1. One model, two runtimes

Keep the Python batch engine authoritative. Export:

- `model-version.json` with equation and configuration hashes;
- `population-profile.json` validated against schema version 1;
- `experiment-config.json` with seed, horizon, policies, and parameters;
- tidy `trajectories.csv` and `agent-snapshots.parquet` when appropriate;
- `summary.json` with estimates, intervals, and diagnostics.

The browser may run a lightweight mechanism demonstrator. If browser equations differ, label it explicitly and add parity tests for shared metrics.

## 2. Research engine

Organize a new project around:

```text
configs/
data/derived/
src/model/
src/metrics/
scripts/
tests/
results/
paper/
web/
```

Use deterministic random-number generators, immutable configuration snapshots, tidy outputs, cached experiment IDs, and resumable batches. Store no raw persona narratives in the project.

## 3. React and Three.js interface

Use React + TypeScript + Vite. Separate simulation state, derived metrics, and Three.js rendering. The 3D view should encode declared quantities:

- x: initial resources or skill;
- y: income or welfare change;
- z: region, occupation, or network community;
- color: income group, policy exposure, or effective AI service;
- size: wealth, influence, or another labeled variable;
- links: actual simulated peer edges.

Provide:

- play, pause, reset, and period scrubber;
- scenario presets and bounded parameter controls;
- seed and population-size controls;
- baseline-versus-policy trajectories with uncertainty;
- hover or keyboard-accessible agent summaries;
- 2D table or chart fallback;
- JSON profile import with strict validation;
- CSV and configuration export;
- always-visible synthetic-data and non-forecast labels.

Never imply each point is a real Korean person.

For GitHub Pages, set Vite `base` to `/<repository-name>/`, upload `dist`, and deploy through GitHub Actions with `pages: write` and `id-token: write`. Verify the public URL and every built asset returns HTTP 200.

## 4. Verification

Test:

- fixed-seed reproducibility;
- metric bounds and known toy distributions;
- policy budget identities;
- no NaN, Infinity, negative wealth where prohibited, or invalid probabilities;
- profile schema rejection for malformed and forbidden fields;
- small populations and empty-network edge cases;
- Python-to-TypeScript parity for shared formulas;
- typecheck, unit tests, production build, and a browser smoke test;
- paired-policy invariants and result-file hashes.

## 5. Paper structure

Use this order:

1. problem and contribution;
2. Korean institutional setting and evidence;
3. NVIDIA data role, official calibration, and limitations;
4. agents, network, mechanisms, and policies;
5. ODD protocol and equation-to-code map;
6. calibration and identification;
7. preregistered experiments and metrics;
8. baseline results with uncertainty;
9. ablations, sensitivity, finite-size, and phase behavior;
10. policy welfare and distributional trade-offs;
11. external validity, ethics, and limitations;
12. reproducibility package.

Use `model-conditional`, `mechanism experiment`, and `candidate phase boundary` unless evidence justifies stronger terms. Do not call normalized parameters estimates.

## 6. Journal fit

Choose based on the finished contribution:

- Journal of Economic Interaction and Coordination: interacting heterogeneous agents, complex networks, policy and economic dynamics;
- Journal of Artificial Societies and Social Simulation: transparent generative ABM, ODD description, replication, and social mechanisms;
- Journal of Computational Social Science: Korea-calibrated computational social science and responsible synthetic-data use;
- Computational Economics: calibration, welfare, numerical economics, and benchmarking;
- Physica A: statistical-mechanics contribution with order parameters, scaling, transition behavior, or universality.

Check current aims, article types, data policy, code requirements, and word limits on the official journal site before submission.

## 7. Korean policy output

Translate model results into a policy matrix rather than one ranking. For each policy show:

- target mechanism;
- beneficiary and excluded group;
- fiscal and implementation cost;
- output effect;
- inequality, polarization, mobility, and regional effects;
- rights and safety constraints;
- evidence strength;
- leading indicators and stop rules;
- pilot and scale-up design.

Recommend staged pilots, preregistered evaluation, appeal routes, interoperability, procurement portability, and public reporting. Define sovereign AI by effective capability and shared returns, not only model nationality or account counts.
