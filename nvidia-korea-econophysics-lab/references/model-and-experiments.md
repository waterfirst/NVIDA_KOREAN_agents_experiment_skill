# Model and experiment design

## Contents

1. State variables
2. Mechanism skeleton
3. Networks
4. Policies
5. Metrics
6. Calibration and identification
7. Experiments and falsification

## 1. State variables

Keep synthetic demographic strata distinct from simulated economic states. A useful agent state is:

\[
X_i(t)=\{d_i,r_i,o_i,e_i,s_i(t),a_i(t),y_i(t),w_i(t),k_i(t),q_i(t),c_i\},
\]

where demographics \(d_i\), region \(r_i\), occupation \(o_i\), and education \(e_i\) initialize heterogeneity; skill \(s\), adoption \(a\), income \(y\), wealth \(w\), AI-capital ownership \(k\), and employment quality \(q\) evolve; care or time constraint \(c\) is slow-moving.

Keep every coefficient in a versioned configuration. Attach a provenance label to each value: `estimated`, `calibrated`, `literature`, `scenario`, or `normalization`.

## 2. Mechanism skeleton

Use an effective-AI-service term rather than equating free access with equal benefit:

\[
z_i(t)=A_i(t)Q_i(t)a_i(t)\left[s_i(t)+\lambda \sum_j \widetilde{G}_{ij}s_j(t)\right].
\]

Here \(A\) is access, \(Q\) effective quality and reliability, \(a\) adoption intensity, \(s\) capability, and \(\widetilde G\) a row-normalized network. Allow premium quality, organizational support, and regional infrastructure to affect \(Q\).

One transparent skill equation is:

\[
s_i(t+1)=\operatorname{clip}\left[s_i(t)+\eta_i T_i(t)(1-s_i(t))+\lambda_s\sum_j\widetilde G_{ij}(s_j-s_i)-\delta_s s_i,0,1\right].
\]

Labor income can separate complementarity and displacement:

\[
y_i^L(t+1)=y_i^L(t)\{1+g_0+\beta_c C_i z_i-\beta_d E_i a_i-\beta_j J_i+\beta_m M_i\}+\varepsilon_i,
\]

where \(C\) is AI complementarity, \(E\) exposure, \(J\) junior-career shock, and \(M\) mobility or transition support.

Wealth and AI capital should be explicit:

\[
w_i(t+1)=(1+r_i^K)w_i(t)+\sigma_i y_i(t)+D_i(t)-\tau_i(t),
\]

with dividends or citizen ownership \(D\), taxes \(\tau\), and heterogeneous capital returns. Enforce budget identities for every policy.

These equations are templates, not empirical facts. Change them when the research question demands, and document the change.

## 3. Networks

Generate links from a declared topology:

- homophilous k-nearest neighbors for region, occupation, education, or income;
- small-world rewiring for cross-cluster diffusion;
- scale-free links only with a defensible institutional interpretation;
- empirical networks when available.

Report degree distribution, clustering, path length, assortativity, modularity, isolated nodes, and sensitivity to topology. Never present a visually appealing Three.js graph as validated network evidence.

## 4. Policies

Compare at least:

- market-only AI;
- universal free access;
- access plus progressive capability training;
- job-transition and junior-career protection;
- regional infrastructure and organizational support;
- care-time support;
- cash recycling;
- citizen or worker AI-capital ownership;
- an integrated package;
- a deliberately weak or low-quality public-AI failure case.

Where possible, equalize fiscal cost across policies. Report both gross and net outcomes.

## 5. Metrics

Use a preregistered primary set and a broader diagnostic set.

Distribution:

- Gini, Atkinson with declared aversion, Theil, Palma;
- Wolfson polarization and middle-income share;
- Esteban-Ray polarization only with declared group construction and alpha;
- equally distributed equivalent income and social welfare.

Dynamics:

- income and occupation transition matrices;
- absolute and relative mobility;
- vulnerable employment and junior entry rates;
- regional and education gaps in effective AI service;
- adoption, output, policy cost, and cost effectiveness;
- top-decile AI-capital share.

Network and physics:

- adoption or skill cluster size;
- assortativity and modularity;
- candidate order parameter such as normalized polarization change;
- susceptibility or variance near a transition;
- critical threshold, finite-size scaling, and hysteresis area.

## 6. Calibration and identification

Map each target moment to one parameter or a clearly identified block. Avoid tuning many coefficients to one headline outcome. Use independent validation moments not used in calibration.

Distinguish:

- demographic initialization from NVIDIA plus official reweighting;
- Korean empirical targets from official surveys or papers;
- structural assumptions required by the model;
- policy scenarios chosen for stress tests.

Provide uncertainty intervals for empirical targets and parameter distributions. Do not collapse all uncertainty into a single seed.

## 7. Experiments and falsification

Run paired policies with common random numbers. Use multiple seeds and report Monte Carlo intervals. Add:

- factorial or Latin-hypercube coverage of the parameter space;
- Morris screening before Sobol analysis when dimensionality is high;
- mechanism ablations;
- alternative network topology and homophily;
- finite populations such as 250, 500, 1,000, and 2,000 agents;
- alternative horizons and initial inequality;
- negative controls and parameter recovery on synthetic truth;
- phase diagrams over quality gap × mobility, exposure × training, and homophily × peer learning;
- policy withdrawal paths for hysteresis.

A phase-transition claim requires convergence evidence, critical-region uncertainty, and finite-size behavior. A threshold visible in one heatmap is only a candidate phase boundary.
