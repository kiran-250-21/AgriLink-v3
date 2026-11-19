# Reproducibility & Replication Guide
## AgriLink: An Empirical, Logistics-Aware Decision Framework for Agricultural Wholesale Market Selection

**Document Version:** 2.0  
**Target Venue:** *IEEE Access*  
**Date:** October 31, 2026  
**Investigator:** P.B.V. Kiran Kumar (VIT-AP University)  

---

### 1. Hardware & Software Environment

All computational benchmarks, simulations, and statistical inference tests reported in the AgriLink manuscript were executed and validated in the following environment:

- **Operating System:** Microsoft Windows 11 Enterprise (x86_64) / Linux Ubuntu 22.04 LTS compatible
- **Processor:** Intel Core i7 / AMD Ryzen 7 (8 cores, 16 threads)
- **RAM:** 16 GB DDR4/DDR5
- **Python Version:** 3.10.x or higher
- **Required Libraries & Versions:**
  - `pandas` $\ge 2.0.0$
  - `numpy` $\ge 1.24.0$
  - `scipy` $\ge 1.10.0$
  - `matplotlib` $\ge 3.7.0$
  - Google Chrome (v115+ with Headless New engine) or `wkhtmltopdf` / `pdflatex` for PDF compilation

---

### 2. Repository & File Manifest

To reproduce all results from scratch, verify that the following files are present in the project directory:

```text
AgriLink/
│
├── research_and_docs/
│   ├── data/
│   │   ├── agmarknet_india_historical_prices_2024_2025.csv   # Raw AGMARKNET scrape (97.7 MB)
│   │   ├── market_coordinates.csv                           # Verified APMC geocodes (18 mandis)
│   │   ├── primary_freight_survey_quotes.csv                 # 25 primary transporter quotes
│   │   └── real_farmer_dispatch_case_studies.csv             # 60 observational field dispatches
│   │
│   ├── scripts/
│   │   ├── run_comprehensive_agrilink_experiment.py         # Full experimental simulation engine
│   │   ├── generate_agrilink_figures.py                     # High-resolution figure generator
│   │   └── build_ieee_access_paper.py                       # Manuscript rendering & PDF compiler
│   │
│   ├── results/
│   │   ├── pooled_5seeds_5000.csv                           # Simulation logs (N = 5,000)
│   │   ├── master_empirical_results.json                    # Reconciled metrics & CIs
│   │   └── figures/                                         # Output 300 DPI publication plots
│   │       ├── fig1_system_architecture.png
│   │       ├── fig2_spatial_price_dispersion.png
│   │       ├── fig3_comparative_net_realization.png
│   │       ├── fig4_commodity_breakdown.png
│   │       ├── fig5_independent_freight_scoring.png
│   │       └── fig6_switching_and_breakeven.png
│   │
│   └── deliverables/
│       ├── AGRILINK_RESEARCH_AUDIT.md
│       ├── AGRILINK_EXPERIMENTAL_VALIDATION.md
│       ├── AGRILINK_REFERENCES.bib
│       ├── AGRILINK_REPRODUCIBILITY.md
│       ├── AGRILINK_CHANGELOG.md
│       ├── AGRILINK_PUBLICATION_READINESS_CHECKLIST.md
│       ├── AGRILINK_RESEARCH_PAPER_REVISED.pdf
│       └── AGRILINK_RESEARCH_PAPER_REVISED.tex
```

---

### 3. Step-by-Step Replication Pipeline

#### Step 1: Python Virtual Environment Setup
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install --upgrade pip
pip install pandas numpy scipy matplotlib
```

#### Step 2: Execute Master Simulation Battery
Execute the comprehensive simulation battery, which processes raw AGMARKNET records, parameterizes 5,000 dispatches across 5 independent random spatial seeds (Seeds 42, 101, 2024, 777, 999), evaluates all 9 baseline strategies, runs independent freight scoring, and outputs summary statistics:

```bash
cd d:\zz2\AgriLink
python research_and_docs/scripts/run_comprehensive_agrilink_experiment.py
```
*Expected Execution Time:* ~45–60 seconds.  
*Outputs Generated:*
- `research_and_docs/results/pooled_5seeds_5000.csv`
- `research_and_docs/results/master_empirical_results.json`
- High-resolution figures 1–6 in `research_and_docs/results/figures/`

#### Step 3: Verify Independent Freight Scoring Across All 5,000 Scenarios
To independently verify the circularity-free robustness results across the pooled 5,000 dispatches without re-running the full battery:

```bash
python -c "
import pandas as pd, numpy as np, sys
sys.path.append('research_and_docs/scripts')
from run_comprehensive_agrilink_experiment import compute_independent_freight

df = pd.read_csv('research_and_docs/results/pooled_5seeds_5000.csv')
rng = np.random.RandomState(42)

for m in ['linear', 'slab', 'minimum_charge', 'stochastic', 'backhaul_penalty']:
    a = [r['AgriLink_revenue'] - compute_independent_freight(r['quantity_kg'], r['AgriLink_dist_km'], m, rng) for _, r in df.iterrows()]
    n = [r['S1_Nearest_revenue'] - compute_independent_freight(r['quantity_kg'], r['S1_Nearest_dist_km'], m, rng) for _, r in df.iterrows()]
    h = [r['S2_HighestPrice_revenue'] - compute_independent_freight(r['quantity_kg'], r['S2_HighestPrice_dist_km'], m, rng) for _, r in df.iterrows()]
    print(f'{m:18s} | Agri: ₹{np.mean(a):.2f} | Near Gain: +₹{np.mean(a)-np.mean(n):.2f} ({(np.mean(a)-np.mean(n))/np.mean(n)*100:+.2f}%) | High Gain: +₹{np.mean(a)-np.mean(h):.2f} ({(np.mean(a)-np.mean(h))/np.mean(h)*100:+.2f}%)')
"
```
*Expected Output:*
```text
linear             | Agri: ₹153868.54 | Near Gain: +₹13263.18 (+9.43%) | High Gain: +₹1573.23 (+1.03%)
slab               | Agri: ₹154118.26 | Near Gain: +₹13950.56 (+9.95%) | High Gain: +₹903.87 (+0.59%)
minimum_charge     | Agri: ₹153460.35 | Near Gain: +₹13644.53 (+9.76%) | High Gain: +₹1439.00 (+0.95%)
stochastic         | Agri: ₹150490.88 | Near Gain: +₹10608.25 (+7.58%) | High Gain: +₹4210.71 (+2.88%)
backhaul_penalty   | Agri: ₹152152.24 | Near Gain: +₹11546.88 (+8.21%) | High Gain: +₹3310.76 (+2.22%)
```

#### Step 4: Recompile Manuscript PDF
To compile the revised IEEE Access formatted paper to PDF with high-resolution vector and raster assets:

```bash
python research_and_docs/scripts/build_ieee_access_paper.py
```
*Expected Output:*
- `research_and_docs/deliverables/AGRILINK_RESEARCH_PAPER_REVISED.pdf`
- Perfectly balanced two-column format matching `template.pdf` with zero blank pages.

---

### 4. Random Seeds & Deterministic Guarantees

| Experiment Component | Seed Variable | Fixed Seed Value | Purpose |
| :--- | :--- | :--- | :--- |
| **Reference Calibration Cohort** | `BENCHMARK_SEED` | `42` | Primary baseline tuning, temporal split H1/H2, ablation benchmarks |
| **Multi-Seed Spatial Cohorts** | `SIMULATION_SEEDS` | `[42, 101, 2024, 777, 999]` | Geographic variance invariance; 1,000 dispatches per seed ($N = 5,000$) |
| **Stochastic Freight Shocks** | `STOCHASTIC_SEED` | `42` | Reproducible lognormal noise injection for independent scoring |
| **Bootstrap Standard Errors** | `BOOTSTRAP_SEED` | `12345` | 1,000 block-bootstrap resamples for confidence interval bounds |

---

### 5. Contact & Support
For replication queries or assistance with AGMARKNET API scraping pipelines:
- **Author:** P.B.V. Kiran Kumar
- **Affiliation:** School of Computer Science and Engineering, VIT-AP University, Amaravati, Andhra Pradesh 522237, India.

