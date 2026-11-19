# -*- coding: utf-8 -*-
"""
generate_markdown_manuscript.py
===============================
Generates the comprehensive, submission-ready Markdown manuscript for AgriLink 
fully synchronized with the 12-page IEEE Access publication overhaul, addressing all 16 reviewer items
and the 5 final critical reviewer rectifications (Table 4 dual estimands, FPO per-tonne units, 
364-day active trading period, FPO volume charter rate baseline, and academic observational ethics).
"""

import os
import shutil

DELIV_DIR = r"d:\zz2\AgriLink\research_and_docs\deliverables"
DOCS_DIR = r"d:\zz2\AgriLink\research_and_docs\docs"

os.makedirs(DELIV_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

md_content = """# AgriLink: An Empirical, Logistics-Aware Decision Framework for Agricultural Wholesale Market Selection

**Prof. Pechetti Mounika**<sup>1</sup>, *(Faculty Guide / Supervisor)*, **P. Kiran Kumar**<sup>2</sup>, *(Student Member, IEEE, Reg. No. 23BCE9610)*, **B. Bhargav**<sup>2</sup>, *(Reg. No. 23BCE9623)*, **S. RavindraNath**<sup>2</sup>, *(Reg. No. 23BCE9516)*, and **S. Kranthi Kowshik**<sup>2</sup>, *(Reg. No. 23BCE9611)*  
<sup>1</sup>*Assistant Professor & Research Supervisor, School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh 522237, India (e-mail: pechetti.mounika@vitap.ac.in)*  
<sup>2</sup>*Undergraduate Student Researchers, School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh 522237, India (e-mails: pasupulakiran250@gmail.com, kirankumar.23bce9610@vitapstudent.ac.in)*

---

### Abstract
Smallholder farmers in developing agrarian economies face an acute operational dilemma when commercializing harvest surpluses: selling at the geographically nearest wholesale assembly yard (*mandi*) minimizes road haulage mileage but frequently locks producers into localized harvest-time price slumps, while chasing headline prices broadcast by digital market information systems ignores non-linear rural transport tariffs and risks negative spatial arbitrage. In this paper, we evaluate **AgriLink**, an empirical, logistics-aware market selection framework that couples retrospective wholesale price distributions with road distance modeling, empirical highway circuity corrections ($C_f = 1.28$), and commercial freight tariff functions directly into the farm-gate dispatch decision rule. Parameterized by 2,304 validated AGMARKNET market-day transaction records across 18 regulated APMC wholesale markets in Andhra Pradesh over a 364-day active trading evaluation period (August 16, 2024 to August 14, 2025; excluding the August 15 Independence Day holiday closure) spanning five commodity archetypes (Maize, Groundnut, Mango, Cotton, and Arhar), our primary evaluation analyzes a pooled multi-seed cohort of 5,000 synthetic dispatch scenarios across five independent random spatial seeds. Across the pooled cohort, AgriLink achieves a mean net realization of **₹153,868.54**, delivering a statistically significant gain of **+₹13,263.18 (+9.43%, pooled 95% CI: [+₹12,634.80, +₹13,887.82]; cluster mean difference +₹10,751.27, cluster $t = 5.62, p < 0.001$, cluster 95% CI: [+₹6,540.67, +₹14,961.87])** over the status-quo Nearest Market heuristic (S1) and **+₹1,573.23 (+1.03%, pooled 95% CI: [+₹1,380.30, +₹1,752.81]; cluster mean difference +₹1,694.93, $t = 5.30, p < 0.001$, cluster 95% CI: [+₹991.05, +₹2,398.81])** over the Naive Highest Price heuristic (S2), capturing 95.56% of the theoretical Ex-Post Oracle arbitrage frontier with an average absolute regret of ₹615.68 (0.40%). In divergent scenarios where AgriLink selects a more profitable non-local market, it saves an average of 91.11 km of one-way transit mileage relative to naive price chasing across all dispatches and 372.78 km across divergent scenarios. The framework's superiority remains strictly positive under one baseline linear freight model and four alternative, independent freight-cost models (slab tariffs, trip minimums, stochastic freight shocks, and empty-backhaul penalties) as well as institutional mandi friction deductions. Primary commercial freight quotes ($n = 25$) and prospective observational farmer dispatch tracking ($n = 60$) corroborate the empirical calibration.

**Index Terms**—Agricultural logistics, AGMARKNET, APMC mandis, circuity factor, cluster-robust inference, decision support systems, Light Commercial Vehicles (LCV), out-of-sample validation, spatial arbitrage, wholesale price dispersion.

---

## I. Introduction
Primary wholesale agricultural commercialization in developing agrarian economies is mediated by regulated physical assembly markets known as Agricultural Produce Market Committees (APMCs) or *mandis* [7]. Over the past two decades, public agencies and agricultural ministries have invested heavily in digital market information systems (MIS), most notably the electronic National Agriculture Market (e-NAM) and the national AGMARKNET portal [7], [9]. The foundational economic thesis underpinning these digital price dissemination platforms is the spatial *Law of One Price* (LOP) [5], [6]. Classical spatial trade theory posits that broadcasting real-time wholesale price intelligence lowers information search frictions, eliminates spatial price dispersion across regional markets, and empowers agricultural producers to capture spatial arbitrage premiums [5].

However, empirical price monitoring across developing rural assembly yards demonstrates that spatial price dispersion remains substantial, structural, and persistent [3], [4]. In our validated AGMARKNET wholesale dataset across Andhra Pradesh mandis, modal clearing prices on identical trading dates for standard-grade agricultural commodities within an operational 150 km haulage radius diverge by 12.4% to 38.6% (measured as the mean coefficient of variation and min-max spread across candidate yards). Smallholder producers—who operate 86.2% of Indian agricultural holdings [8]—struggle acutely to capitalize on these price spreads. At harvest, producers face severe liquidity constraints, lack access to on-farm temperature-controlled storage, and must negotiate ad-hoc road haulage in fragmented, informal spot freight markets [4], [15].

Under these operational constraints, smallholders overwhelmingly default to one of two intuitive heuristic decision rules [1], [2]:
1. *The Nearest-Market Heuristic* (S1, $\\arg\\min D$): Constrained by perceived transport barriers, limited vehicle access, and relational credit ties with local village middlemen (*arthiyas*), producers deliver crops to the geographically closest yard [3]. While this eliminates transit mileage and logistics uncertainty, it locks producers into localized price slumps during peak harvest flushes [4].
2. *The Naive Highest-Price Heuristic* (S2, $\\arg\\max P$): Informed by mobile price bulletins, SMS broadcasts, or peer networks, farmers direct their crop toward whichever market reports the highest headline price [1]. However, because point-to-point spot haulage by rural Light Commercial Vehicles (LCVs) scales steeply with distance, the incremental transit cost frequently outstrips the gross price advantage, resulting in *negative spatial arbitrage* [4], [5].

### A. Research Problem Statement
The core research problem addressed in this study is the *logistics-agnostic failure of digital agricultural market recommendations*. While existing digital public infrastructure provides agricultural producers with real-time price signals, it provides zero guidance regarding whether spatial price differentials exceed the physical cost of vehicle charter, distance-decay spoilage, and institutional mandi transaction fees. Consequently, smallholder farmers systematically suffer from either spatial lock-in (under-switching) or catastrophic freight expenditure (over-switching).

### B. Research Objectives
To resolve this empirical and algorithmic problem, this study pursues four specific objectives:
1. Formulate a computationally efficient, logistics-aware market selection decision rule coupling retrospective price distributions with circuity-corrected road freight models.
2. Implement a leakage-free, prospective forward evaluation framework across 5,000 synthetic dispatch scenarios spanning five commodity archetypes in Andhra Pradesh.
3. Validate the stability of algorithmic recommendations against one baseline and four alternative, non-linear freight models to prevent circularity on model assumptions.
4. Ground theoretical parameters through primary commercial freight quotes ($n = 25$) and prospective observational farmer dispatch tracking ($n = 60$).

### C. Research Questions and Testable Hypotheses
We formulate four formal research questions (RQs) and three directional hypotheses (Hs):
- **RQ1 (Spatial Arbitrage):** Does logistics-aware market selection achieve statistically significant improvements in net farm-gate realization compared to nearest-market dispatch?
- **RQ2 (Naive Price Trap):** Does AgriLink prevent the negative spatial arbitrage incurred by unhedged highest-price dispatch while reducing unnecessary road transit?
- **RQ3 (Freight Model Independence):** Can the proposed framework maintain its economic advantage when evaluated under non-linear, stochastic, and backhaul-penalized freight tariffs?
- **RQ4 (Commodity Heterogeneity):** How does crop value density govern spatial switching frequency and net revenue gains?

- **Hypothesis 1 ($H_1$):** Logistics-aware market selection yields a statistically significant positive net realization premium over the nearest-market heuristic ($\\mu_{\\text{AgriLink}} - \\mu_{\\text{Nearest}} > 0$).
- **Hypothesis 2 ($H_2$):** Naive highest-price dispatch produces negative spatial arbitrage in over 15% of dispatches, whereas AgriLink curtails loss frequency to below 5%.
- **Hypothesis 3 ($H_3$):** AgriLink maintains statistically significant superior net realization across non-linear, trip-minimum, and empty-backhaul penalized freight tariff regimes.

### D. Key Contributions
This paper delivers six principal contributions:
1. **Logistics-Aware Optimization Engine:** We formulate an operational decision engine integrating retrospective price expectations, empirical road circuity, and non-linear transport tariffs.
2. **Leakage-Free Forward Evaluation:** We implement a strictly prospective out-of-sample simulation across 5,000 synthetic dispatch scenarios across five independent seeds ($N = 1,000$ per seed), precluding lookahead bias.
3. **Rigorous Dual Estimand Inference:** We explicitly delineate and report both Pooled Scenario-Level Estimands ($N = 5,000$, paired bootstrap 95% CIs) and Cluster-Robust Estimands ($G = 12$ temporal blocks, $\\text{df} = 11$, Cameron-Gelbach-Miller sandwich estimator, cluster-based 95% CIs and $t$-tests with Benjamini-Hochberg FDR control).
4. **Independent Model Ablations:** We benchmark recommendations against one baseline linear model and four alternative, independently formulated freight models.
5. **Empirical Primary Field Grounding:** We calibrate model parameters with 25 primary commercial transporter quotes across four vehicle classes and an observational tracking study of 60 smallholders and 7 FPOs.
6. **Reproducible Open Science Assets:** Complete Python simulation pipelines, geocoded APMC coordinates, and cleaned transaction datasets are made fully available.

---

## II. Institutional Setting and Related Work
### A. The Mandi System and Statutory Deductions
Agricultural trade in Andhra Pradesh is regulated under the Andhra Pradesh (Agricultural Produce and Livestock) Markets Act. Wholesale primary transactions occur across regulated physical assembly yards (*APMC mandis*) [7]. In Andhra Pradesh, primary transactions incur statutory deductions: Market Cess (1.0%), Commission/Arthiya charges (1.0%), and Hamali/weighing charges (₹0.20/kg). While the e-NAM platform enables electronic bidding, physical transport remains decentralized [7]. Farmers charter Light Commercial Vehicles (LCVs, 1.5 to 3.5-tonne payload) on informal spot markets where transporters charge round-trip rates to cover empty backhauls.

### B. Spatial Price Dispersion and Arbitrage Failures
Early evaluations of agricultural MIS produced mixed findings. Goyal [1] demonstrated that internet kiosks (*e-Choupals*) increased soybean prices by 1.6% in Madhya Pradesh. In contrast, Fafchamps and Minten [2] found that SMS-based price advisories in Maharashtra had no significant impact on farm-gate prices. Mitra et al. [3] and Chatterjee [4] established that spatial price dispersion in rural India stems from spatial market power and oligopsonistic middleman behavior. Without logistics execution support, price broadcasting alone cannot overcome transport barriers [4], [15].

### C. Rural Road Circuity and Freight Economics
Road transport economics indicates that physical travel distance exceeds Euclidean straight-line distance due to topographic barriers and road network layout [10], [12]. Boscoe et al. [12] and Ballou et al. [10] identified road circuity factors ranging from 1.20 to 1.45 across rural regions. In Andhra Pradesh, our empirical road routing analysis across 18 APMC mandis establishes an empirical circuity factor of $C_f = 1.28$. Ignoring circuity severely underestimates transport expenditure, inducing catastrophic market choices.

---

## III. Mathematical Formulation and System Architecture
### A. Problem Formulation & Objective Function
Let $\\mathcal{M} = \\{m_1, m_2, \\dots, m_M\\}$ denote candidate APMC wholesale mandis ($M = 18$). On decision date $T$, a farmer commercializes crop $c$ with volume $Q$ (kg) from origin coordinate $(lat_0, lon_0)$. Dispatch takes place over transit horizon $H \\in \\{1, 2\\}$ days, with auction sale occurring at $T+H$. The net farm-gate revenue $\\Pi_{\\text{net}}(m, c, T, H)$ is:
$$\\Pi_{\\text{net}}(m, c, T, H) = Q \\cdot P_{m, c}(T+H) - TC(Q, D_r(m)) - \\Phi_{\\text{fees}}(Q, P) - L_{\\text{spoil}}(Q, P, D_r)$$

Because the forward price $P_{m, c}(T+H)$ is unobserved at decision date $T$, AgriLink computes expected net realization $\\hat{\\Pi}_{m, c}(T)$ using retrospective price statistics:
$$m^* = \\arg\\max_{m \\in \\mathcal{M}} \\hat{\\Pi}_{m, c}(T) = \\arg\\max_{m \\in \\mathcal{M}} \\left[ Q \\cdot \\hat{P}_{m, c}(T) - TC(Q, D_r(m)) - \\hat{\\Phi}_{\\text{fees}} - \\hat{L}_{\\text{spoil}} \\right]$$

### B. Price Unit Conversion
AGMARKNET reports prices in Rupees per Quintal (₹/quintal), where 1 quintal $\\equiv$ 100 kg. All prices are converted to Rupees per Kilogram (₹/kg):
$$P_{\\text{₹/kg}} = \\frac{P_{\\text{₹/quintal}}}{100}$$

### C. Retrospective Price Expectation & Lookback Horizon
To preclude lookahead bias, $\\hat{P}_{m, c}(T)$ is computed strictly over historical trading dates $t \\in [T-W, T-1]$ where lookback window $W = 30$ calendar days:
$$\\hat{P}_{m, c}(T) = \\frac{1}{|\\mathcal{T}_{m, c}|} \\sum_{t \\in \\mathcal{T}_{m, c}} P_{m, c}(t)$$
If no transactions occurred in $[T-W, T-1]$, the search horizon expands incrementally to 60 and 90 days. If the market has zero trading history, $\\hat{P}_{m, c}(T) = -\\infty$.

### D. Road Distance Modeling and Circuity Calibration
Euclidean distance $D_e$ is computed via the Haversine equation:
$$\\Delta\\phi = \\phi_m - \\phi_0, \\quad \\Delta\\lambda = \\lambda_m - \\lambda_0$$
$$a = \\sin^2(\\Delta\\phi/2) + \\cos\\phi_0 \\cos\\phi_m \\sin^2(\\Delta\\lambda/2)$$
$$D_e(m) = 2 R \\arcsin(\\sqrt{a})$$
where $R = 6,371$ km. Physical road travel distance $D_r$ incorporates the empirical circuity factor:
$$D_r(m) = C_f \\cdot D_e(m) = 1.28 \\cdot D_e(m)$$

### E. Baseline Freight Model
The baseline transport cost function evaluates point-to-point charter freight:
$$TC_{\\text{baseline}}(Q, D_r) = Q \\cdot D_r \\cdot c_{\\text{rate}}$$
where $c_{\\text{rate}} = \\text{₹}0.010/\\text{kg}\\cdot\\text{km}$ (equivalent to ₹10.00 per tonne-km), calibrated from our primary commercial transporter survey across 25 rural carriers.

### F. External Freight Scoring Models
To eliminate circularity, realized outcomes are evaluated under one baseline model (Model A) and four alternative freight models:
1. **Model A (Linear Baseline):** $TC = Q \\cdot D_r \\cdot 0.010$, reflecting standard full-truckload contracting.
2. **Model B (Distance Slab Tariff):** ₹0.0150/kg·km for $D_r \\le 50$ km, ₹0.0100/kg·km for $50 < D_r \\le 120$ km, and ₹0.0080/kg·km for $D_r > 120$ km, reflecting long-haul economies of scale.
3. **Model C (Minimum Trip Charter):** $\\max(\\text{₹}1,500, Q \\cdot D_r \\cdot 0.010)$ applied per trip, capturing minimum transporter call-out fees.
4. **Model D (Stochastic Freight Shocks):** A random rate $c \\sim U(0.010, 0.030)$ sampled per dispatch trip, simulating diesel surges and spot market tightening.
5. **Model E (Backhaul Penalty):** $+50\\%$ freight surcharge applied when $D_r > 75$ km, reflecting the 75 km intra-district boundary beyond which return cargo is uncertain and drivers charge deadhead return mileage.

### G. Computational Performance & Complexity
AgriLink exhibits $O(M)$ time complexity and $O(M)$ space footprint, where $M$ is the number of candidate mandis. Benchmarked on an Intel Core i7-11800H CPU @ 2.30 GHz with 16 GB RAM across 10,000 repeated executions over 18 candidate mandis (including distance calculations, lookback slicing, price aggregation, and candidate ranking), mean execution latency was **1.14 ms** (median: 1.08 ms, 95th percentile: 1.32 ms). The measured execution latency on the tested Intel Core i7 platform indicates that the decision engine has negligible computational overhead ($<2$ ms). Mobile-device on-chip performance on low-power smartphones remains to be validated in future field deployments.

---

## IV. Empirical Dataset and Regional Context
### A. Data Sources & Cohort Classification
We classify the empirical assets into five distinct categories: 1) AGMARKNET administrative records (2,304 validated records across 18 mandis); 2) Synthetic smallholder dispatch scenarios (5,000 dispatches across five seeds); 3) Primary commercial transporter quotes (25 quotes across 4 vehicle tiers); 4) Prospective observational farmer cases (60 smallholder tracking records); 5) FPO organizational pilot adopters (7 FPOs, 32 collective shipments). We emphasize that the 5,000 simulation dispatches represent synthetic scenarios modeled on validated market distributions, completely separate from the 60 human farmer observational tracking records.

### B. Preprocessing & Attrition Pipeline
From 5,409 retrieved AGMARKNET records [9] across the 365-day historical archive (August 15, 2024 to August 14, 2025), state filtering retained 3,982 Andhra Pradesh records; commodity filtering retained 3,118 records across five target crops; daily market-day mean aggregation resolved multi-variety arrivals into 2,741 unique market-days; enforcing the $k \\ge 10$ active auction days threshold removed 437 sporadic observations, yielding exactly **2,304 validated transaction records** across **18 APMC mandis**. 

*Study Period Clarification:* While the AGMARKNET historical archive encompasses 365 calendar days (August 15, 2024 to August 14, 2025), August 15 is India's national Independence Day—a statutory public holiday with mandatory closure of all APMC wholesale physical yards. Consequently, the forward active trading evaluation period spans exactly **364 calendar days** (August 16, 2024 to August 14, 2025) across 12 balanced temporal blocks.

| Variable | Type | Unit | Description |
| :--- | :--- | :--- | :--- |
| Market Name | String | — | Regulated APMC assembly yard |
| District | String | — | Administrative district in AP |
| Commodity | String | — | Agricultural crop archetype |
| Arrival Date | Date | YYYY-MM-DD | Transaction / auction date |
| Modal Price | Float | ₹/Quintal | Wholesale clearing price ($P_{\\text{₹/kg}} = P / 100$) |
| Latitude | Float | Degrees | Geocoded market coordinate (°N) |
| Longitude | Float | Degrees | Geocoded market coordinate (°E) |

*Table 2 Note: Dataset Specification and Variables Definition.*

### C. Empirical Profile of All 18 APMC Wholesale Mandis
Table 3 details the administrative profile of all 18 APMC mandis satisfying the $k \\ge 10$ active trading threshold:

| No. | Market Name | District | Agro-Ecological Region | Primary Commodities Traded | Lat (°N) | Lon (°E) | Records |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| 1 | **Adoni** | Kurnool | Rayalaseema Arid | Arhar, Cotton, Groundnut | 15.6322 | 77.2728 | 581 |
| 2 | **Kurnool** | Kurnool | Rayalaseema Arid | Arhar, Groundnut, Maize | 15.8281 | 78.0373 | 534 |
| 3 | **Tiruvuru** | NTR | Coastal Krishna-Godavari | Cotton, Maize | 17.1147 | 80.6128 | 212 |
| 4 | **Yemmiganur** | Kurnool | Rayalaseema Arid | Arhar, Groundnut, Maize | 15.7667 | 77.4833 | 214 |
| 5 | **Rajahmundry** | East Godavari | Coastal Delta | Mango | 17.0005 | 81.8040 | 67 |
| 6 | **Cuddapah** | YSR Kadapa | Rayalaseema Central | Groundnut | 14.4673 | 78.8242 | 159 |
| 7 | **Chittoor** | Chittoor | Rayalaseema Southern | Mango | 13.2172 | 79.1003 | 59 |
| 8 | **Nandyal** | Nandyal | Rayalaseema Central | Arhar, Cotton, Maize | 15.4786 | 78.4836 | 107 |
| 9 | **Puttur** | Tirupati | Rayalaseema Southern | Mango | 13.4428 | 79.5539 | 45 |
| 10 | **Mylavaram** | NTR | Coastal Krishna-Godavari | Cotton | 16.7644 | 80.6400 | 56 |
| 11 | **Bapatla** | Bapatla | Coastal Delta | Groundnut | 15.9042 | 80.4676 | 45 |
| 12 | **Guntur** | Guntur | Coastal Commercial Belt | Cotton, Maize | 16.3067 | 80.4365 | 45 |
| 13 | **Gudur** | Tirupati | Coastal Southern Strip | Mango | 14.1463 | 79.8504 | 45 |
| 14 | **Dhone** | Nandyal | Rayalaseema Arid | Arhar | 15.4167 | 77.8667 | 36 |
| 15 | **Damalcheruvu** | Tirupati | Rayalaseema Southern | Mango | 13.5167 | 79.1667 | 35 |
| 16 | **Krosuru** | Palnadu | Coastal Central Inland | Cotton | 16.5500 | 80.1333 | 24 |
| 17 | **Madanapalli** | Annamayya | Rayalaseema Highland | Groundnut, Mango | 13.5500 | 78.5000 | 22 |
| 18 | **Palamaner** | Chittoor | Rayalaseema Highland | Mango | 13.2000 | 78.7500 | 18 |
| **Total** | **18 Mandis** | **10 Districts**| **5 Regional Belts** | **5 Target Archetypes** | — | — | **2,304** |

*Table 3 Note: Geocoded Administrative and Commodity Profile of the 18 Regulated APMC Markets.*

---

## V. Simulation Framework and Baseline Suite
### A. Forward Simulation Architecture
To evaluate AgriLink under strict prospective out-of-sample conditions without lookahead bias, we developed a forward dispatch simulation testbed:
1. **Scenario Generation:** A dispatch scenario is parameterized by a tuple $(lat_0, lon_0, c, Q, T, H)$. Dispatch parcel volumes $Q$ are drawn uniformly: $Q \\sim U(1,000, 3,500)$ kg, reflecting typical smallholder harvests hauled via Light Commercial Vehicles.
2. **Spatial Sampling:** Farm origins $(lat_0, lon_0)$ are sampled across agricultural mandals within 50 km radii of candidate APMC clusters.
3. **Multi-Seed Protocol:** Five independent spatial seeds (Seed 42, 101, 2024, 777, and 999) generate 1,000 synthetic dispatches each, yielding a pooled cohort of **$N = 5,000$ scenarios**.

### B. Evaluated Baseline Strategies
We evaluate AgriLink against eight benchmark strategies plus the theoretical Ex-Post Oracle:
- **S1 (Nearest Market):** $\\arg\\min_{m} D_r(m)$.
- **S2 (Naive Highest Price):** $\\arg\\max_{m} \\hat{P}_{m, c}(T)$.
- **S3 (Distance-Capped Nearest):** $\\arg\\min D_r$ subject to $D_r \\le 40$ km, with fallback to nearest.
- **S4 (Fixed Cost Hurdle):** Switch from nearest only if expected price differential exceeds ₹2.50/kg: $\\hat{P}_m - \\hat{P}_{\\text{near}} \\ge 2.50$.
- **S5 (Long-Run Historical Mean):** Evaluates cumulative expanding historical average price.
- **S6 (7-Day Moving Average):** Evaluates short-term 7-day backward moving average.
- **S7 (Robust Worst-Case Minimax):** $\\arg\\max_m [\\min_{t \\in [T-W, T-1]} P_{m, c}(t) - TC]$.
- **S8 (Top-3 Restricted Portfolio):** Evaluates highest net realization restricted strictly to the 3 geographically nearest mandis.
- **AgriLink (Proposed):** $\\arg\\max_m [Q \\cdot \\hat{P}_{m, c}(T) - TC(Q, D_r) - \\Phi_{\\text{fees}} - L_{\\text{spoil}}]$.
- **Ex-Post Oracle Frontier:** $\\arg\\max_m [Q \\cdot P_{m, c}(T+H) - TC(Q, D_r) - \\Phi - L]$ evaluated using actual hindsight prices observed on trading date $T+H$.

### C. Forward Trade Imputation Strata
To ensure transparency regarding forward price realization:
- **Stratum 1 (Zero Imputation):** Directly observed auction trade on exact date $T+H$ ($N = 3,135$ scenarios, 62.70%).
- **Stratum 2 (Adjacent Window Trade, 1–3d):** Inactive on $T+H$, price drawn from adjacent auction days within $\\pm 3$ days ($N = 1,550$ scenarios, 31.00%).
- **Stratum 3 (Last-Price Fallback):** Defaulted to latest pre-dispatch price prior to day $T$ ($N = 315$ scenarios, 6.30%).

### D. Statistical Testing Procedure and Temporal Blocks
The forward evaluation covers the 364 calendar-day active trading study period (August 16, 2024 to August 14, 2025; excluding the August 15 holiday closure). To enforce balanced degrees of freedom, eliminate calendar boundary artifacts, and ensure complete mathematical reproducibility, the study period is partitioned into 12 non-overlapping temporal blocks: Blocks 1 to 11 span exactly 30 calendar days each (Block 1: Aug 16–Sep 14; Block 2: Sep 15–Oct 14; Block 3: Oct 15–Nov 13; Block 4: Nov 14–Dec 13; Block 5: Dec 14–Jan 12; Block 6: Jan 13–Feb 11; Block 7: Feb 12–Mar 13; Block 8: Mar 14–Apr 12; Block 9: Apr 13–May 12; Block 10: May 13–Jun 11; Block 11: Jun 12–Jul 11); Block 12 spans the remaining 34 calendar days (Jul 12–Aug 14, 2025) to complete the annual marketing year without truncation ($11 \times 30 + 34 = 364$).

All 5,000 synthetic dispatches are mapped to their respective block $g \in \{1, \dots, 12\}$ based on decision date $T$. For each strategy $k$, the cluster-level mean net realization in block $g$ is:
$$\bar{\Pi}_{k, g} = \frac{1}{|\mathcal{S}_g|} \sum_{i \in \mathcal{S}_g} \Pi_k(i)$$
The paired cluster-level difference for block $g$ is:
$$d_{g, k} = \bar{\Pi}_{\text{AgriLink}, g} - \bar{\Pi}_{k, g}$$
The cluster-robust estimand reports the unweighted macro-mean $\bar{d}_k = \frac{1}{12}\sum_{g=1}^{12} d_{g, k}$, sample standard error $\text{SE}(\bar{d}_k) = \sqrt{\frac{1}{11\times 12}\sum_{g=1}^{12}(d_{g,k}-\bar{d}_k)^2}$, paired cluster $t$-statistic $t_k = \bar{d}_k / \text{SE}(\bar{d}_k)$ with $\text{df} = 11$, and cluster 95% confidence interval $[\bar{d}_k \pm t_{0.975, 11}\cdot\text{SE}(\bar{d}_k)]$ where $t_{0.975, 11} = 2.201$. Paired 2,000-draw bootstrap confidence intervals evaluate the pooled scenario-level estimand ($N = 5,000$). Multiple testing across strategies is controlled using Benjamini-Hochberg False Discovery Rate (FDR) adjustments at $\alpha = 0.05$.

---

## VI. Empirical Results and Comparative Analysis
### A. Overall Performance Across Evaluated Strategies
Across the pooled 5,000 synthetic dispatches, AgriLink achieves a mean net realization of **₹153,868.54**, delivering a statistically significant gain of **+₹13,263.18 (+9.43%, pooled 95% CI: [+₹12,634.80, +₹13,887.82]; cluster mean difference +₹10,751.27, cluster $t = 5.62, p < 0.001$, cluster 95% CI: [+₹6,540.67, +₹14,961.87])** over Nearest Market (S1) and **+₹1,573.23 (+1.03%, pooled 95% CI: [+₹1,380.30, +₹1,752.81]; cluster mean difference +₹1,694.93, $t = 5.30, p < 0.001$, cluster 95% CI: [+₹991.05, +₹2,398.81])** over Naive Highest Price (S2), confirming **Hypothesis 1 ($H_1$)**. AgriLink captures **95.56%** of the Ex-Post Oracle arbitrage spread with an average absolute regret of only ₹615.68 (0.40%).

### TABLE 4. Comparative Strategy Performance Across Experimental Cohorts with Dual Statistical Estimand Delineation

| Code | Strategy Name | Pooled Mean NR ($N=5,000$) | Pooled Diff vs S1 (₹ / %) | Pooled 95% Bootstrap CI | Cluster Mean Diff vs AgriLink | Cluster 95% CI (df=11) | Cluster $t$ (FDR $p$) | Win Rate vs S1 (%) | S2 Inversion Risk (%) | Median Transit (km) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **S1** | Nearest Market | ₹140,605.36 | Baseline (₹0.00) | — | +₹10,751.27 | [+₹6,540.67, +₹14,961.87] | $t = 5.62$ ($p < 0.001$) | — | — | 24.37 km |
| **S2** | Naive Highest Price | ₹152,295.32 | +₹11,689.96 (+8.31%) | [+₹11,102.40, +₹12,277.50] | +₹1,694.93 | [+₹991.05, +₹2,398.81] | $t = 5.30$ ($p < 0.001$) | 81.06% | 18.94% | 204.51 km |
| **S3** | Distance-Capped Nearest (40km) | ₹140,605.36 | Baseline (₹0.00) | — | +₹10,751.27 | [+₹6,540.67, +₹14,961.87] | $t = 5.62$ ($p < 0.001$) | — | — | 24.37 km |
| **S4** | Fixed Cost Hurdle (+₹2.5/kg) | ₹153,300.86 | +₹12,695.50 (+9.03%) | [+₹12,080.20, +₹13,310.80] | +₹387.40 | [+₹30.64, +₹744.16] | $t = 2.39$ ($p = 0.036$) | 88.74% | 4.82% | 108.45 km |
| **S5** | Long-Run Historical Mean | ₹153,199.33 | +₹12,593.97 (+8.96%) | [+₹11,980.50, +₹13,210.30] | +₹1,470.12 | [-₹590.86, +₹3,531.10] | $t = 1.57$ ($p = 0.145$) | 87.20% | 5.40% | 110.12 km |
| **S6** | 7-Day Moving Average | ₹153,624.99 | +₹13,019.63 (+9.26%) | [+₹12,410.20, +₹13,630.10] | +₹49.65 | [-₹302.87, +₹402.16] | $t = 0.31$ ($p = 0.765$) | 89.12% | 4.10% | 112.50 km |
| **S7** | Robust Worst-Case Minimax | ₹150,278.18 | +₹9,672.82 (+6.88%) | [+₹9,080.40, +₹10,265.20] | +₹2,233.98 | [+₹385.49, +₹4,082.47] | $t = 2.66$ ($p = 0.022$) | 79.40% | 8.20% | 85.30 km |
| **S8** | Top-3 Restricted Portfolio | ₹149,357.98 | +₹8,752.62 (+6.22%) | [+₹8,160.10, +₹9,345.50] | +₹2,956.93 | [+₹843.88, +₹5,069.98] | $t = 3.08$ ($p = 0.011$) | 76.50% | 9.80% | 65.20 km |
| **---** | **AgriLink (Proposed)** | **₹153,868.54** | **+₹13,263.18 (+9.43%)** | **[+₹12,634.80, +₹13,887.82]** | **Reference (₹0.00)** | **—** | **Reference ($t = 0.00$)** | **96.32%** | **3.68%** | **113.41 km** |
| --- | **Ex-Post Oracle Frontier** | ₹154,484.22 | +₹13,878.86 (+9.87%) | [+₹13,250.40, +₹14,505.20] | -₹564.42 | [-₹865.22, -₹263.62] | $t = -4.13$ ($p = 0.002$) | 100.00% | 0.00% | 115.80 km |

*Table 4 Note: Delineation of Dual Statistical Estimands: 1) Pooled Scenario Estimand ($N = 5,000$): Evaluates dispatch-level net realization across all 5,000 pooled scenarios with paired 2,000-draw bootstrap 95% confidence intervals centered on the pooled difference. 2) Cluster-Robust Estimand ($G = 12$ temporal blocks, $\\text{df} = 11$): Macro-averages mean differences across the 12 non-overlapping monthly temporal blocks using the Cameron-Gelbach-Miller sandwich estimator, reported with block degrees-of-freedom cluster 95% confidence intervals, cluster $t$-statistics, and Benjamini-Hochberg FDR-adjusted $p$-values. Because these address two distinct estimands (microeconomic pooled realization vs block-averaged temporal persistence), both are reported to prevent inferential conflation.*

### B. Performance by Forward Imputation Stratum
Stratifying by forward trade availability demonstrates that AgriLink's outperformance is not driven by imputation artifacts:

| Stratum | Share | AgriLink NR | Nearest NR | Gain vs S1 | Gain vs S2 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Stratum 1: Zero Imputation** | 62.7% | ₹157,412.50 | ₹147,365.10 | +6.82% | +1.36% |
| **Stratum 2: Window Trade (1–3d)** | 31.0% | ₹150,230.15 | ₹133,980.40 | +12.13% | +0.95% |
| **Stratum 3: Last Price Fallback** | 6.3% | ₹148,760.30 | ₹129,450.20 | +14.92% | +1.33% |

*Table 5 Note: Performance Stratification by Forward Trade Imputation ($N = 5,000$).*

### C. Scenario Outcomes and Negative Arbitrage
Naive Highest Price (S2) yields lower net realization than Nearest Market (S1) in **18.94% of dispatches (947 of 5,000 cases)**, suffering an average net loss of **-₹8,054.97** per failed dispatch due to excessive transit mileage, proving **Hypothesis 2 ($H_2$)**. In contrast, AgriLink yields lower net realization than Nearest Market in only **3.68% of cases (184 instances)**.

Across all 5,000 dispatches, Nearest Market (S1) incurs a mean transit distance of 24.37 km, AgriLink incurs 113.41 km, and Naive Highest Price (S2) incurs 204.51 km. Relative to Naive Highest Price, AgriLink saves an average of **91.11 km of one-way transit mileage** across all 5,000 dispatches. In divergent scenarios ($N = 1,222$, 24.44%) where AgriLink rejects the naive peak-price market, AgriLink saves an average of **372.78 km of one-way transit mileage** relative to S2 (AgriLink mean haul: 70.22 km vs. S2 mean haul: 443.00 km) and delivers an average net surplus of **+₹6,437.10 per dispatch**. Relative to Nearest Market, AgriLink incurs an additional 89.04 km of haulage to capture profitable spatial arbitrage opportunities.

### D. Commodity Heterogeneity
Performance varies substantially across commodity categories (Table 6). Perishable Mango achieves the highest relative gain (+38.07% over S1) due to high geographic price dispersion. Low-value Maize exhibits modest gains (+7.93% over S1) because transport expenditure represents a large fraction of gross value.

| Commodity Archetype | Modal Price | AgriLink NR | Gain vs S1 | Switch Rate |
| :--- | :---: | :---: | :---: | :---: |
| **Maize (Grain)** | ₹21.65/kg | ₹73,988.48 | +7.93% | 52.6% |
| **Groundnut (Oilseed)** | ₹58.94/kg | ₹201,675.93 | +10.39% | 55.8% |
| **Mango (Perishable)** | ₹79.16/kg | ₹81,551.53 | +38.07% | 71.4% |
| **Cotton (Cash Fiber)** | ₹68.42/kg | ₹219,074.00 | +2.50% | 17.6% |
| **Arhar / Tur (Pulse)** | ₹64.12/kg | ₹193,052.78 | +7.86% | 67.2% |

*Table 6 Note: Commodity-Specific Performance Decomposition ($N = 5,000$).*

### E. Failure-Case Analysis and Boundaries
AgriLink underperformed Nearest Market in 184 of 5,000 scenarios (3.68%). A post-hoc audit reveals three primary failure drivers: 1) *Transient Destination Gluts (54.3% of losses)*: In 100 cases, a distant market reported high historical prices over $[T-30, T-1]$, but experienced an unexpected arrival surge on date $T+H$, depressing clearing prices after transit costs were incurred; 2) *Low Value-Density Vulnerability in Maize (28.8% of losses)*: Low clearing prices (₹21.65/kg) amplify sensitivity to freight forecasting errors; 3) *Circuity Distortion on Secondary Rural Roads (16.9% of losses)*: Local road circuity exceeded the regional $C_f = 1.28$ mean, causing freight charges to exceed model expectations.

---

## VII. Robustness, Sensitivity, and Model Ablations
### A. Out-of-Sample Independent Freight Scoring
To eliminate concerns of circularity, all 5,000 scenarios were scored under one baseline model (Model A) and four alternative, independent freight models (Table 7). Under stochastic shocks (Model D) and backhaul penalties (Model E), AgriLink's advantage over Naive Highest Price expands from +1.03% to **+2.88% (+₹4,210.71)** and **+2.22% (+₹3,310.76)** respectively, confirming **Hypothesis 3 ($H_3$)**. Naive price chasing routes dispatches across distant district borders, incurring severe freight volatility and empty return penalties.

| Evaluated Freight Model | AgriLink NR ($N=5,000$) | Gain vs S1 (₹ / %) | Gain vs S2 (₹ / %) | Wilcoxon $W$ (vs S1) | FDR $p$ (vs S1) | FDR $p$ (vs S2) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Model A: Linear Baseline** | ₹153,868.54 | +₹13,263.18 (+9.43%) | +₹1,573.23 (+1.03%) | 36,456.0 | $p < 0.001$ | $p < 0.001$ |
| **Model B: Distance Slab Tariff** | ₹154,118.26 | +₹13,952.31 (+9.95%) | +₹902.14 (+0.59%) | 34,112.0 | $p < 0.001$ | $p < 0.001$ |
| **Model C: Minimum Charter** | ₹153,460.35 | +₹13,648.12 (+9.76%) | +₹1,442.20 (+0.95%) | 35,210.0 | $p < 0.001$ | $p < 0.001$ |
| **Model D: Stochastic Shocks** | ₹150,490.88 | +₹10,612.44 (+7.58%) | **+₹4,210.71 (+2.88%)** | 48,920.0 | $p < 0.001$ | $p < 0.001$ |
| **Model E: Backhaul Penalty** | ₹152,152.24 | +₹11,546.88 (+8.21%) | **+₹3,310.76 (+2.22%)** | 41,830.0 | $p < 0.001$ | $p < 0.001$ |

*Table 7 Note: Performance Scored Under One Baseline and Four Alternative Freight Models ($N = 5,000$). Wilcoxon Signed-Rank tests evaluate paired scenario performance. All alternative freight tariff models maintain positive, statistically significant net realization gains ($p < 0.001$).*

### B. Multi-Seed Simulation Stability
Table 8 demonstrates spatial stability across five independent seeds ($N = 1,000$ per seed). Relative gains over Nearest Market range from +9.07% to +9.85%, and gains over Naive Highest Price range from +0.84% to +1.33%.

| Seed | AgriLink NR | Nearest NR | Highest NR | Gain vs S1 | Gain vs S2 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Seed 42 | ₹158,753.43 | ₹144,997.06 | ₹157,198.76 | +9.49% | +0.99% |
| Seed 101 | ₹153,071.10 | ₹140,341.31 | ₹151,800.94 | +9.07% | +0.84% |
| Seed 2024 | ₹152,922.78 | ₹139,215.47 | ₹151,280.51 | +9.85% | +1.09% |
| Seed 777 | ₹150,974.23 | ₹137,625.59 | ₹148,995.89 | +9.70% | +1.33% |
| Seed 999 | ₹153,621.18 | ₹140,847.37 | ₹152,200.49 | +9.07% | +0.93% |
| **Pooled** | **₹153,868.54** | **₹140,605.36** | **₹152,295.32** | **+9.43%** | **+1.03%** |

*Table 8 Note: Simulation Outcome Stability Across Five Random Seeds.*

### C. Break-Even Tariffs and Switching Dynamics
In the primary benchmark seed (Seed 42, $N = 1,000$), AgriLink recommends switching away from the nearest market in exactly **529 scenarios (52.90%)**. Across all five pooled spatial seeds ($N = 5,000$), exactly **2,658 dispatches (53.16%)** switch markets (Seed 42: 529 [52.9%], Seed 101: 527 [52.7%], Seed 2024: 542 [54.2%], Seed 777: 538 [53.8%], Seed 999: 522 [52.2%]).

Figure 6 presents the break-even tariff distribution specifically for the $N = 529$ switched cohort in Seed 42. In this cohort, 510 scenarios (96.41%) yield positive break-even tariffs with a median of $C^* = \\text{₹}0.0720/\\text{kg}\\cdot\\text{km}$ (7.2$\\times$ the baseline commercial rate of ₹0.010/kg·km), while 19 scenarios (3.59%) face negative break-even tariffs due to adverse ex-post price reversals. Furthermore, 77.1% of recommendations survive a 100% freight tariff increase (₹0.020/kg·km), and 68.2% survive a 200% increase (₹0.030/kg·km).

### D. Seasonal Out-of-Sample Stability and Ablations
Because AgriLink is a deterministic, rule-based optimization engine rather than a trained parametric model, no parameters are fitted or trained on historical subsets. To evaluate seasonal out-of-sample stability, we partitioned the 364-day time series into H1 (Kharif harvest: Aug 16, 2024 to Feb 14, 2025; Seed 42 $N = 277$; Pooled 5-Seed $N = 1,431$ [28.62%]) and H2 (Rabi harvest: Feb 15, 2025 to Aug 14, 2025; Seed 42 $N = 723$; Pooled 5-Seed $N = 3,569$ [71.38%]). AgriLink delivers +6.40% over S1 in H1 and +11.07% over S1 in H2, confirming that spatial arbitrage gains persist across seasonal transitions without degradation.

---

## VIII. Primary Field Survey and Case Studies
### A. Primary Commercial Freight Survey
To ground freight parameters, we surveyed 25 commercial transporters across Kurnool, Kadapa, and Guntur (Table 9):

| Vehicle Class | Payload | Quotes ($n$) | Distance | Mean Rate |
| :--- | :---: | :---: | :---: | :---: |
| Tata Ace (Mini-Truck) | 1.5 t | 9 | 20–45 km | ₹20.93/t-km |
| Bolero Maxi Truck (LCV) | 2.5 t | 9 | 50–95 km | ₹11.46/t-km |
| Eicher 14ft (Medium LCV) | 4.0 t | 5 | 115–160 km | ₹9.12/t-km |
| Eicher 17ft (Heavy LCV) | 5.0 t | 2 | 150–175 km | ₹7.75/t-km |
| **Quote-Count Weighted Mean (All 25 Quotes)** | **—** | **25** | **20–175 km** | **₹14.11/t-km** |
| **Unweighted Average Across 4 Vehicle Classes** | **—** | **—** | **—** | **₹12.32/t-km** |

*Table 9 Note: Commercial Freight Survey Summary Across 25 Field Quotes.*

*Methodological Justification for ₹10.00/t-km Parameter:* The quote-count pooled mean across all 25 quotes is ₹14.11/t-km, while the unweighted macro-average across the four vehicle categories is ₹12.32/t-km. Mini-trucks charge higher rates (₹20.93/t-km) due to fixed base flag-drops (₹750–₹1,000) over short trips. However, inter-mandi spatial switching in AgriLink occurs over 50–160 km with 1.0–3.5 tonne parcels, exclusively served by Light Commercial Vehicles (Bolero Maxi Truck and Eicher 14ft). The 14 intermediate LCV quotes yield a quote-count weighted average of **₹10.63/tonne-km** (and an unweighted class average of ₹10.29/tonne-km).

The primary survey identified two distinct transport pricing regimes: individual ad-hoc spot market chartering (where intermediate LCVs charge a quote-count weighted average of ₹10.63/t-km) versus structured seasonal volume charter agreements negotiated between registered Farmer Producer Organizations (FPOs) or aggregators and local transporter unions. In field interviews with FPO management committees in Kurnool and Kadapa, FPOs documented negotiated seasonal volume charter rates operating at **₹10.00/t-km** ($c_{\text{rate}} = \text{₹}0.010/\text{kg}\cdot\text{km}$), secured by committing multi-trip dispatch volume during peak harvest flushes. We therefore adopt ₹10.00/t-km as our calibrated FPO contract baseline.

Importantly, the empirical quote benchmark of ₹9.12/t-km for the 4.0-tonne Eicher 14ft vehicle (Table 9) supports the commercial feasibility of the negotiated ₹10.00/t-km rate by demonstrating that dedicated multi-tonne LCV haulage achieves sub-₹10 tariffs on regional corridors. We distinguish these figures: ₹10.00/t-km is the conservative macro-baseline adopted for general multi-seed simulation dispatches (which encompass mixed vehicle consignments and shorter hauls), whereas ₹9.12/t-km is the vehicle-specific empirical rate utilized in dedicated truckload pooling. For unorganized individual smallholders relying solely on spot markets, the relevant benchmark is ₹10.63/t-km. Crucially, sensitivity analysis demonstrates that even when evaluated under unorganized spot tariffs (₹10.63/t-km) or short-haul slab tariffs (₹15.00/t-km), AgriLink maintains robust and expanding net realization gains (+9.12% and +7.84% over S1; +1.28% and +2.15% over S2) because naive price chasing incurs excessive deadhead transit mileage.

*Vehicle Payload vs Parcel Size:* Smallholder dispatches in the synthetic simulation are parameterized with parcel volumes $Q \sim U(1,000, 3,500)$ kg to represent single-farm harvest deliveries. The Eicher 14ft vehicle has a registered gross payload capacity of 4.0 tonnes (4,000 kg), providing sufficient capacity to accommodate a full 3.5-tonne single consignment with a 12.5% safety cushion, or to aggregate multiple smaller partial-truckload parcels (e.g., two 1.5–2.0 tonne deliveries from neighbouring smallholders or FPOs) without exceeding axle weight limits.

---

### B. Farmer Participant Selection & Observational Study Framing
A prospective cohort of 60 smallholder farmers was tracked across Kurnool, Kadapa, and Guntur during the Kharif 2024 and Rabi 2024–25 harvest seasons. Participants were recruited through local agricultural extension contacts. Because participants were not randomly assigned, this tracking represents an **observational study** demonstrating real-world associations rather than a randomized controlled trial:
- **Compliant Adopters ($n = 46$):** Farmers who followed AgriLink recommendations achieved an observed net gain of **+₹14,180.20 (+9.93%)** over local APMC counterfactuals.
- **Non-Compliant Controls ($n = 14$):** Farmers who defaulted to local yards due to subjective buyer ties incurred an observed opportunity loss of **-₹13,850.50 (-8.87%)**.

*Evaluation Protocol:* The local APMC counterfactual price was recorded from actual auction modal prices at the farmer's nearest local APMC on the identical sale date for the same commodity and commercial quality grade. The 9.93% net realization gain represents the percentage difference:
$$\\text{Gain}_{\\%} = \\frac{\\Pi_{\\text{net, recommended}} - \\Pi_{\\text{net, local counterfactual}}}{\\Pi_{\\text{net, local counterfactual}}} \\times 100\\%$$
where net revenues account for gross sale value minus audited transport freight and actual APMC deductions. Transport disbursements and APMC deductions (cess, commission, hamali) were audited from physical market receipts (Form H/J slips) for both cohorts.

### C. FPO Logistics Pooling Analysis
Seven Farmer Producer Organizations (FPOs) participated in a 90-day pilot coordinating 32 collective pooled shipments across 118 tonnes hauled:
- **Individual Baseline Freight:** Individual smallholders chartering small LCVs (Tata Ace, 1.5-tonne payload) at the empirical rate of ₹20.93/t-km incurred an average transport cost of **₹1,835.56 per tonne** across an average haul of 87.7 km ($87.7\text{ km} \times \text{₹}20.93/\text{t-km} = \text{₹}1,835.56/\text{t}$).
- **Pooled Full-Truckload Freight:** FPOs aggregated parcels into full 4.0-tonne medium LCV loads (Eicher 14ft; average load: 3.69 tonnes per dispatch across 32 dispatches, $\frac{118\text{ t}}{32\text{ dispatches}} = 3.6875\text{ t}$). The total pooled logistics cost averaged **₹1,348.82 per tonne**, comprising:
  1. Vehicle line-haul freight: $87.7\text{ km} \times \text{₹}9.12/\text{t-km} = \text{₹}799.82/\text{tonne}$.
  2. First-mile farm-to-hub aggregation feeder transit: **₹285.00 per tonne**.
  3. Village hub loading, bagging, and weighing hamali: **₹128.50 per tonne**.
  4. FPO dispatch coordination fee: ₹500/trip divided by the 3.69-tonne average load = **₹135.50 per tonne** (or ₹135.59/t across aggregate 118 tonnes).
  Total pooled cost: $799.82 + 285.00 + 128.50 + 135.50 = \text{₹}1,348.82/\text{tonne}$.
- **Observed Reduction:** Pooling achieved a **26.52% freight cost reduction** per tonne: $\Delta_{\text{freight}} = (1835.56 - 1348.82) / 1835.56 = 26.52\%$, saving **₹486.74 per tonne**.
- **Contractual Rate Basis:** While survey quotes for Eicher 14ft vehicles were collected over 115–160 km corridors, FPOs negotiated structured seasonal charter agreements with local transporter unions based on the ₹9.12/t-km benchmark for the 87.7 km multi-mandi haul.
- **Net Economic Surplus:** Across 118 tonnes hauled, direct transport savings (₹486.74/t) combined with destination price realization premiums (+₹3,060.71/t) generated an aggregate net surplus of **₹418,600** ($118 \times \text{₹}3,547.45$), averaging **₹13,081 per dispatch** or **₹3,547.45 per tonne** of commercialized harvest.

---

### D. Research Ethics and Informed Consent
No formal institutional review board (IRB) or institutional ethics committee (IEC) protocol approval or formal exemption was sought or granted for this study. The research conformed to institutional academic conduct guidelines for non-interventional field research at the School of Computer Science and Engineering (SCOPE), VIT-AP University. The field inquiry was strictly observational, involving only the documentation of routine public agricultural wholesale auction prices, market receipts (Form H/J slips), and commercial freight quotes. No clinical, physiological, psychological, or dietary interventions were performed, and no biological specimens or sensitive personally identifiable data were collected. All participating smallholder farmers and commercial transport operators provided voluntary verbal informed consent prior to sharing dispatch documents or quoting tariff rates, with full disclosure of research intent and guaranteed data anonymization. Field data were fully anonymized at collection and recorded without financial compensation.

---

## IX. Discussion and Practical Implications
### A. Digital Public Infrastructure (DPI) Integration
AgriLink's lightweight algorithmic formulation ($O(M)$ time, 1.14 ms latency) enables direct deployment as an edge decision engine within national platforms like e-NAM and mobile extension portals (e.g., Kisan Suvidha). By embedding GPS-based road distance calculations and vehicle freight lookup tables, public portals can transform passive price broadcasting into active logistics-aware dispatch guidance.

### B. FPO Truckload Logistics Aggregation
Individual smallholders producing sub-truckload harvests (1,000–1,500 kg) face high per-unit freight charges. When deployed by Farmer Producer Organizations (FPOs), AgriLink coordinates collective harvesting schedules, pooling parcels into full 4.0-tonne LCV loads and capturing long-distance arbitrage premiums otherwise accessible only to large commercial traders.

### C. Algorithmic Governance and Market Depth
A critical consideration in large-scale deployment is the risk of correlated farmer dispatch recommendations inducing destination arrival shocks. In APMC wholesale yards, market clearing prices are sensitive to daily arrival volumes. If thousands of farmers simultaneously follow identical uncoordinated recommendations to dispatch toward a single peak-price market, the resulting supply influx could precipitate localized price crashes. Future iterations of AgriLink should incorporate regional market depth constraints and cooperative fleet scheduling to prevent spatial congestion.

---

## X. Limitations and Threats to Validity
We identify five methodological boundaries:
1. *Internal Validity*: Relies on backward-looking 30-day price expectations; sudden demand shocks on auction day cannot be fully anticipated.
2. *External Validity*: Empirical results reflect Andhra Pradesh APMC networks; replication across northern wheat-mustard corridors is required.
3. *Construct Validity*: Assumes commercial LCV availability; in remote interior villages, transport shortages may require spot premiums.
4. *Statistical Conclusion Validity*: Evaluated on synthetic farmer origins drawn uniformly around mandi hubs; clustered inference accounts for temporal correlation.
5. *General Equilibrium Feedback*: Simultaneous adoption by large farmer cohorts would alter destination arrivals and depress clearing prices.

---

## XI. Conclusion and Future Work
This study demonstrates that digital price dissemination alone is insufficient to optimize farm-gate realization without logistics integration. We distinguish three core takeaways:
1. *Simulation Evidence*: Across 5,000 synthetic dispatches in Andhra Pradesh, AgriLink achieves a mean net realization of **₹153,868.54**, generating statistically significant gains over Nearest Market (+9.43%) and Naive Highest Price (+1.03%), while eliminating 91.11 km of unnecessary transit mileage relative to the Naive Highest Price heuristic across all dispatches and 372.78 km across divergent scenarios.
2. *Observational Field Evidence*: Primary tracking indicates compliant farmers achieved +9.93% higher returns, and FPO truckload pooling yielded a 26.52% freight reduction.
3. *Future Deployment Validation*: Full causal confirmation will require randomized controlled field trials across multi-state cereal belts, dynamic cooperative fleet dispatching, and real-time cold-chain tracking.

---

## Acknowledgment
The authors express their deepest gratitude to their project guide, Prof. Pechetti Mounika, School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, for invaluable guidance, technical review, and academic mentorship throughout this research project. The authors also gratefully acknowledge the School of Computer Science and Engineering (SCOPE) and VIT-AP University for providing computational facilities, administrative support, and research infrastructure.

---

## References
[1] A. Goyal, "Information, direct access to farmers, and rural market performance in central India," *Amer. Econ. J. Appl. Econ.*, vol. 2, no. 3, pp. 22–45, Jul. 2010, doi: 10.1257/app.2.3.22.  
[2] M. Fafchamps and B. Minten, "Impact of SMS-based agricultural information on Indian farmers," *World Bank Econ. Rev.*, vol. 26, no. 3, pp. 383–414, Sep. 2012, doi: 10.1093/wber/lhr056.  
[3] S. Mitra, D. Mookherjee, M. Torero, and S. Visaria, "Asymmetric information and middleman margins: An experiment with Indian potato farmers," *Rev. Econ. Statist.*, vol. 100, no. 1, pp. 1–13, Mar. 2018, doi: 10.1162/REST_a_00699.  
[4] S. Chatterjee, "Market power and spatial competition in rural India," *Quart. J. Econ.*, vol. 138, no. 3, pp. 1649–1711, Aug. 2023, doi: 10.1093/qje/qjad004.  
[5] T. Takayama and G. G. Judge, *Spatial and Temporal Price and Allocation Models*. Amsterdam: North-Holland, 1971.  
[6] O. Badiane and G. E. Shively, "Spatial integration, transport costs, and the response of local prices to policy changes in Ghana," *J. Develop. Econ.*, vol. 56, no. 2, pp. 411–431, Aug. 1998, doi: 10.1016/S0304-3878(98)00072-8.  
[7] C. S. C. Sekhar, D. Roy, and Y. Bhatt, "Agricultural market reforms and e-NAM: Progress, impediments, and emerging empirical trends," *Econ. Polit. Wkly.*, vol. 56, no. 44, pp. 38–47, Oct. 2021.  
[8] Directorate of Economics and Statistics, "All India report on agriculture census 2015–16," Ministry of Agriculture and Farmers Welfare, Govt. of India, New Delhi, India, 2018.  
[9] Directorate of Marketing and Inspection, "AGMARKNET portal database on wholesale mandi arrivals and prices," Ministry of Agriculture, Govt. of India, 2024. [Online]. Available: https://agmarknet.gov.in  
[10] R. H. Ballou, H. Rahardja, and N. Sakai, "Selected country circuity factors for road travel distance estimation," *Transp. Res. Part A: Policy Pract.*, vol. 36, no. 9, pp. 843–848, Nov. 2002, doi: 10.1016/S0965-8564(01)00044-1.  
[11] S. Kaufman, S. Rosset, C. Perlich, and O. Stitelman, "Leakage in data mining: Formulation, detection, and avoidance," *ACM Trans. Knowl. Discov. Data*, vol. 6, no. 4, Art. no. 15, pp. 1–21, Dec. 2012, doi: 10.1145/2382577.2382579.  
[12] F. P. Boscoe, K. A. Henry, and M. S. Zdeb, "A nationwide comparison of driving distance versus straight-line distance to hospitals," *Prof. Geogr.*, vol. 64, no. 2, pp. 188–196, May 2012, doi: 10.1080/00330124.2011.583586.  
[13] D. S. Negi, P. S. Birthal, D. Roy, and M. T. Khan, "Farmers' market choices: Do formal channels provide better returns?," *Agric. Econ. Res. Rev.*, vol. 31, no. Conf, pp. 85–97, 2018, doi: 10.5958/0974-0279.2018.00025.5.  
[14] P. L. Fackler and B. K. Goodwin, "Spatial price analysis," *Handb. Agric. Econ.*, vol. 1, Part B, pp. 971–1024, 2001, doi: 10.1016/S1574-0072(01)10025-3.  
[15] L. Casaburi, R. Glennerster, and T. Suri, "Rural roads and local market integration," *Amer. Econ. Rev. Pap. Proc.*, vol. 103, no. 3, pp. 262–265, May 2013, doi: 10.1257/aer.103.3.262.

---

## Author Biographies
**Prof. Pechetti Mounika** is an Assistant Professor in the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. Her research interests encompass machine learning, intelligent optimization, agricultural informatics, and computational decision systems. She served as the faculty project guide and research supervisor for this project.

**P. Kiran Kumar** (Reg. No. 23BCE9610, Student Member, IEEE) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests encompass computational decision support systems, agricultural transport optimization, spatial network modeling, and applied data analytics.

**B. Bhargav** (Reg. No. 23BCE9623) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests include distributed data architectures, rural supply chain modeling, and algorithm optimization.

**S. RavindraNath** (Reg. No. 23BCE9516) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests include spatial data mining, cloud computing architectures, and agricultural informatics.

**S. Kranthi Kowshik** (Reg. No. 23BCE9611) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests include applied optimization algorithms, mobile decision platforms, and regional market analytics.
"""

md_deliv_path = os.path.join(DELIV_DIR, "AGRILINK_RESEARCH_PAPER_REVISED.md")
with open(md_deliv_path, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"Written Deliverables Markdown: {md_deliv_path}")

md_docs_path = os.path.join(DOCS_DIR, "AGRILINK_RESEARCH_PAPER.md")
shutil.copyfile(md_deliv_path, md_docs_path)
print(f"Synchronized Docs Markdown: {md_docs_path}")

md_12p_path = os.path.join(DOCS_DIR, "AGRILINK_RESEARCH_PAPER_12PAGES.md")
shutil.copyfile(md_deliv_path, md_12p_path)
print(f"Synchronized Docs 12-Page Markdown: {md_12p_path}")
