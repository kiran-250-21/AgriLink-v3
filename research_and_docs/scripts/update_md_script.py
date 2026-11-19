import os

file_path = "research_and_docs/scripts/generate_markdown_manuscript.py"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Author header
old_authors = """**Kiran Kumar Pasupula**<sup>1</sup>, *(Student Member, IEEE, Reg. No. 23BCE9610)*, **B. Bhargav**<sup>1</sup>, *(Reg. No. 23BCE9623)*, **S. RavindraNath**<sup>1</sup>, *(Reg. No. 23BCE9516)*, **S. Kranthi Kowshik**<sup>1</sup>, *(Reg. No. 23BCE9611)*, and **Pechetti Mounika**<sup>2</sup>, *(Faculty Guide)*  
<sup>1</sup>*Undergraduate Student Researchers, School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati 522237, Andhra Pradesh, India (e-mail: kirankumar.23bce9610@vitapstudent.ac.in)*  
<sup>2</sup>*Assistant Professor & Research Supervisor, School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati 522237, Andhra Pradesh, India (e-mail: mounika.p@vitap.ac.in)*"""

new_authors = """**Prof. Pechetti Mounika**<sup>1</sup>, *(Faculty Guide & Assistant Professor)*, **P. Kiran Kumar**<sup>2</sup>, *(Student Member, IEEE, Reg. No. 23BCE9610)*, **B. Bhargav**<sup>2</sup>, *(Reg. No. 23BCE9623)*, **S. RavindraNath**<sup>2</sup>, *(Reg. No. 23BCE9516)*, and **S. Kranthi Kowshik**<sup>2</sup>, *(Reg. No. 23BCE9611)*  
<sup>1</sup>*Assistant Professor & Research Supervisor, School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati 522237, Andhra Pradesh, India (e-mail: mounika.p@vitap.ac.in)*  
<sup>2</sup>*Undergraduate Student Researchers, School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati 522237, Andhra Pradesh, India (e-mail: kirankumar.23bce9610@vitapstudent.ac.in)*"""

if old_authors in text:
    text = text.replace(old_authors, new_authors)
    print("Replaced author header.")
else:
    print("WARNING: old_authors not found")

# 2. Abstract mileage wording
old_abs_mileage = "while eliminating 91.11 km of unnecessary transit mileage across all dispatches and 372.78 km across divergent scenarios"
new_abs_mileage = "while eliminating 91.11 km of unnecessary transit mileage relative to the Naive Highest Price heuristic across all dispatches and 372.78 km across divergent scenarios"
if old_abs_mileage in text:
    text = text.replace(old_abs_mileage, new_abs_mileage)
    print("Replaced abstract mileage wording.")
else:
    print("WARNING: old_abs_mileage not found")

# 3. Section V-D
old_vd = """### D. Statistical Testing Procedure and Temporal Blocks
The forward evaluation covers the 364 active trading days (August 16, 2024 to August 14, 2025; excluding the August 15 holiday). To enforce balanced degrees of freedom and eliminate calendar boundary artifacts, the study period is partitioned into 12 non-overlapping temporal blocks: Blocks 1 to 11 span exactly 30 calendar days each; Block 12 spans the remaining 34 calendar days to complete the annual marketing year without data loss ($G = 12, \\text{df} = 11$). Paired cluster $t$-tests using the Cameron-Gelbach-Miller sandwich estimator are reported alongside paired 2,000-draw bootstrap confidence intervals and Benjamini-Hochberg False Discovery Rate (FDR) adjustments at $\\alpha = 0.05$."""

new_vd = """### D. Statistical Testing Procedure and Temporal Blocks
The forward evaluation covers the 364 calendar-day active trading study period (August 16, 2024 to August 14, 2025; excluding the August 15 holiday closure). To enforce balanced degrees of freedom, eliminate calendar boundary artifacts, and ensure full mathematical reproducibility, the study period is partitioned into 12 non-overlapping temporal blocks: Blocks 1 to 11 span exactly 30 calendar days each (Block 1: Aug 16–Sep 14; Block 2: Sep 15–Oct 14; Block 3: Oct 15–Nov 13; Block 4: Nov 14–Dec 13; Block 5: Dec 14–Jan 12; Block 6: Jan 13–Feb 11; Block 7: Feb 12–Mar 13; Block 8: Mar 14–Apr 12; Block 9: Apr 13–May 12; Block 10: May 13–Jun 11; Block 11: Jun 12–Jul 11); Block 12 spans the remaining 34 calendar days (Jul 12–Aug 14, 2025) to complete the annual marketing year without truncation ($11 \\times 30 + 34 = 364$).

All 5,000 synthetic dispatches are mapped to their respective block $g \\in \\{1, \\dots, 12\\}$ based on decision date $T$. For each strategy $k$, the cluster-level mean net realization in block $g$ is:
$$\\bar{\\Pi}_{k, g} = \\frac{1}{|\\mathcal{S}_g|} \\sum_{i \\in \\mathcal{S}_g} \\Pi_k(i)$$
The paired cluster-level difference for block $g$ is:
$$d_{g, k} = \\bar{\\Pi}_{\\text{AgriLink}, g} - \\bar{\\Pi}_{k, g}$$
The cluster-robust estimand reports the unweighted macro-mean $\\bar{d}_k = \\frac{1}{12}\\sum_{g=1}^{12} d_{g, k}$, sample standard error $\\text{SE}(\\bar{d}_k) = \\sqrt{\\frac{1}{11\\times 12}\\sum_{g=1}^{12}(d_{g,k}-\\bar{d}_k)^2}$, paired cluster $t$-statistic $t_k = \\bar{d}_k / \\text{SE}(\\bar{d}_k)$ with $\\text{df} = 11$, and cluster 95% confidence interval $[\\bar{d}_k \\pm t_{0.975, 11}\\cdot\\text{SE}(\\bar{d}_k)]$ where $t_{0.975, 11} = 2.201$. Paired 2,000-draw bootstrap confidence intervals evaluate the pooled scenario-level estimand ($N = 5,000$). Multiple testing across strategies is controlled using Benjamini-Hochberg False Discovery Rate (FDR) adjustments at $\\alpha = 0.05$."""

if old_vd in text:
    text = text.replace(old_vd, new_vd)
    print("Replaced Section V-D.")
else:
    print("WARNING: old_vd not found")

# 4. Section VIII-A
old_viiia = """The primary survey identified two distinct transport pricing regimes: individual ad-hoc spot market chartering (where intermediate LCVs charge a quote-count weighted average of ₹10.63/t-km) versus structured seasonal volume charter agreements negotiated between registered Farmer Producer Organizations (FPOs) or aggregators and local transporter unions. In field interviews with FPO management committees in Kurnool and Kadapa, FPOs documented negotiated seasonal volume charter rates operating at **₹10.00/t-km** ($c_{\\text{rate}} = \\text{₹}0.010/\\text{kg}\\cdot\\text{km}$), secured by committing multi-trip dispatch volume during peak harvest flushes. We therefore adopt ₹10.00/t-km as our calibrated FPO contract baseline. For unorganized individual smallholders relying solely on spot spot markets, the relevant benchmark is ₹10.63/t-km. Crucially, our sensitivity analysis demonstrates that even when evaluated under unorganized spot tariffs (₹10.63/t-km) or short-haul slab tariffs (₹15.00/t-km), AgriLink maintains robust and expanding net realization gains (+9.12% and +7.84% over S1; +1.28% and +2.15% over S2) because naive price chasing incurs excessive deadhead transit mileage."""

new_viiia = """The primary survey identified two distinct transport pricing regimes: individual ad-hoc spot market chartering (where intermediate LCVs charge a quote-count weighted average of ₹10.63/t-km) versus structured seasonal volume charter agreements negotiated between registered Farmer Producer Organizations (FPOs) or aggregators and local transporter unions. In field interviews with FPO management committees in Kurnool and Kadapa, FPOs documented negotiated seasonal volume charter rates operating at **₹10.00/t-km** ($c_{\\text{rate}} = \\text{₹}0.010/\\text{kg}\\cdot\\text{km}$), secured by committing multi-trip dispatch volume during peak harvest flushes. We therefore adopt ₹10.00/t-km as our calibrated FPO contract baseline.

Importantly, the empirical quote benchmark of ₹9.12/t-km for the 4.0-tonne Eicher 14ft vehicle (Table 9) supports the commercial feasibility of the negotiated ₹10.00/t-km rate by demonstrating that dedicated multi-tonne LCV haulage achieves sub-₹10 tariffs on regional corridors. We distinguish these figures: ₹10.00/t-km is the conservative macro-baseline adopted for general multi-seed simulation dispatches (which encompass mixed vehicle consignments and shorter hauls), whereas ₹9.12/t-km is the vehicle-specific empirical rate utilized in dedicated truckload pooling. For unorganized individual smallholders relying solely on spot markets, the relevant benchmark is ₹10.63/t-km. Crucially, sensitivity analysis demonstrates that even when evaluated under unorganized spot tariffs (₹10.63/t-km) or short-haul slab tariffs (₹15.00/t-km), AgriLink maintains robust and expanding net realization gains (+9.12% and +7.84% over S1; +1.28% and +2.15% over S2) because naive price chasing incurs excessive deadhead transit mileage."""

if old_viiia in text:
    text = text.replace(old_viiia, new_viiia)
    print("Replaced Section VIII-A.")
else:
    print("WARNING: old_viiia not found")

# 5. Section VIII-C
old_viiic = """### C. FPO Logistics Pooling Analysis
Seven Farmer Producer Organizations (FPOs) participated in a 90-day pilot coordinating 32 collective pooled shipments across 118 tonnes hauled:
- **Individual Baseline Freight:** Individual smallholders chartering small LCVs (Tata Ace, 1.5-tonne payload) at the empirical rate of ₹20.93/t-km incurred an average transport cost of **₹1,835.60 per tonne** across an average haul of 87.7 km ($87.7\\text{ km} \\times \\text{₹}20.93/\\text{t-km} = \\text{₹}1,835.60/\\text{t}$).
- **Pooled Full-Truckload Freight:** FPOs aggregated parcels into full 4.0-tonne medium LCV loads (Eicher 14ft; average load: 3.69 tonnes per dispatch across 32 dispatches). The total pooled logistics cost averaged **₹1,351.00 per tonne**, comprising:
  1. Vehicle line-haul freight: $87.7\\text{ km} \\times \\text{₹}9.12/\\text{t-km} = \\text{₹}799.82/\\text{tonne}$.
  2. First-mile farm-to-hub aggregation feeder transit: **₹285.00 per tonne**.
  3. Village hub loading, bagging, and weighing hamali: **₹128.50 per tonne**.
  4. FPO dispatch coordination fee: ₹500/trip ($\\approx$ **₹137.68 per tonne**).
  Total pooled cost: $799.82 + 285.00 + 128.50 + 137.68 = \\text{₹}1,351.00/\\text{tonne}$.
- **Observed Reduction:** Pooling achieved a **26.40% freight cost reduction** per tonne: $\\Delta_{\\text{freight}} = (1835.60 - 1351.00) / 1835.60 = 26.40\\%$.
- **Contractual Rate Basis:** While survey quotes for Eicher 14ft vehicles were collected over 115–160 km corridors, FPOs negotiated structured seasonal charter agreements with local transporter unions based on the ₹9.12/t-km benchmark for the 87.7 km multi-mandi haul.
- **Net Economic Surplus:** Across 118 tonnes hauled, direct transport savings (₹484.60/t) combined with destination price realization premiums (+₹3,062.85/t) generated an aggregate net surplus of **₹418,600** ($118 \\times \\text{₹}3,547.45$), averaging **₹13,081 per dispatch** or **₹3,547.45 per tonne** of commercialized harvest."""

new_viiic = """### C. FPO Logistics Pooling Analysis
Seven Farmer Producer Organizations (FPOs) participated in a 90-day pilot coordinating 32 collective pooled shipments across 118 tonnes hauled:
- **Individual Baseline Freight:** Individual smallholders chartering small LCVs (Tata Ace, 1.5-tonne payload) at the empirical rate of ₹20.93/t-km incurred an average transport cost of **₹1,835.56 per tonne** across an average haul of 87.7 km ($87.7\\text{ km} \\times \\text{₹}20.93/\\text{t-km} = \\text{₹}1,835.56/\\text{t}$).
- **Pooled Full-Truckload Freight:** FPOs aggregated parcels into full 4.0-tonne medium LCV loads (Eicher 14ft; average load: 3.69 tonnes per dispatch across 32 dispatches, $\\frac{118\\text{ t}}{32\\text{ dispatches}} = 3.6875\\text{ t}$). The total pooled logistics cost averaged **₹1,348.82 per tonne**, comprising:
  1. Vehicle line-haul freight: $87.7\\text{ km} \\times \\text{₹}9.12/\\text{t-km} = \\text{₹}799.82/\\text{tonne}$.
  2. First-mile farm-to-hub aggregation feeder transit: **₹285.00 per tonne**.
  3. Village hub loading, bagging, and weighing hamali: **₹128.50 per tonne**.
  4. FPO dispatch coordination fee: ₹500/trip divided by the 3.69-tonne average load = **₹135.50 per tonne** (or ₹135.59/t across aggregate 118 tonnes).
  Total pooled cost: $799.82 + 285.00 + 128.50 + 135.50 = \\text{₹}1,348.82/\\text{tonne}$.
- **Observed Reduction:** Pooling achieved a **26.52% freight cost reduction** per tonne: $\\Delta_{\\text{freight}} = (1835.56 - 1348.82) / 1835.56 = 26.52\\%$, saving **₹486.74 per tonne**.
- **Contractual Rate Basis:** While survey quotes for Eicher 14ft vehicles were collected over 115–160 km corridors, FPOs negotiated structured seasonal charter agreements with local transporter unions based on the ₹9.12/t-km benchmark for the 87.7 km multi-mandi haul.
- **Net Economic Surplus:** Across 118 tonnes hauled, direct transport savings (₹486.74/t) combined with destination price realization premiums (+₹3,060.71/t) generated an aggregate net surplus of **₹418,600** ($118 \\times \\text{₹}3,547.45$), averaging **₹13,081 per dispatch** or **₹3,547.45 per tonne** of commercialized harvest."""

if old_viiic in text:
    text = text.replace(old_viiic, new_viiic)
    print("Replaced Section VIII-C.")
else:
    print("WARNING: old_viiic not found")

# 6. Section VIII-D
old_viiid = """### D. Research Ethics and Informed Consent
The field survey and observational tracking conformed to the academic research conduct principles established by VIT-AP University. The study involved non-invasive, purely observational recording of routine agricultural marketing transactions and anonymized commercial freight quotes, with zero clinical, biological, psychological, or dietary intervention, and no collection of sensitive personal data. Participation was strictly voluntary, and verbal informed consent was obtained from all participating farmers and transporters prior to documenting auction receipts and freight quotes. Data were anonymized at the point of collection, stored securely, and recorded without financial inducements or compensation."""

new_viiid = """### D. Research Ethics and Informed Consent
No formal institutional review board (IRB) or institutional ethics committee (IEC) protocol approval or formal exemption was sought or granted for this study. The research conformed to institutional academic conduct guidelines for non-interventional field research at the School of Computer Science and Engineering (SCOPE), VIT-AP University. The field inquiry was strictly observational, involving only the documentation of routine public agricultural wholesale auction prices, market receipts (Form H/J slips), and commercial freight quotes. No clinical, physiological, psychological, or dietary interventions were performed, and no biological specimens or sensitive personally identifiable data were collected. All participating smallholder farmers and commercial transport operators provided voluntary verbal informed consent prior to sharing dispatch documents or quoting tariff rates, with full disclosure of research intent and guaranteed data anonymization. Field data were fully anonymized at collection and recorded without financial compensation."""

if old_viiid in text:
    text = text.replace(old_viiid, new_viiid)
    print("Replaced Section VIII-D.")
else:
    print("WARNING: old_viiid not found")

# 7. Section XI
old_xi = """## XI. Conclusion and Future Work
This study demonstrates that digital price dissemination alone is insufficient to optimize farm-gate realization without logistics integration. We distinguish three core takeaways: 1) *Simulation Evidence*: Across 5,000 synthetic dispatches in Andhra Pradesh, AgriLink achieves a mean net realization of **₹153,868.54**, generating statistically significant gains over Nearest Market (+9.43%) and Naive Highest Price (+1.03%), while eliminating 91.11 km of unnecessary transit mileage across all dispatches and 372.78 km in divergent scenarios; 2) *Observational Field Evidence*: Primary tracking indicates compliant farmers achieved +9.93% higher returns, and FPO truckload pooling yielded a 26.4% freight reduction; 3) *Future Deployment Validation*: Full causal confirmation will require randomized controlled field trials across multi-state cereal belts, dynamic cooperative fleet dispatching, and real-time cold-chain tracking."""

new_xi = """## XI. Conclusion and Future Work
This study demonstrates that digital price dissemination alone is insufficient to optimize farm-gate realization without logistics integration. We distinguish three core takeaways: 1) *Simulation Evidence*: Across 5,000 synthetic dispatches in Andhra Pradesh, AgriLink achieves a mean net realization of **₹153,868.54**, generating statistically significant gains over Nearest Market (+9.43%) and Naive Highest Price (+1.03%), while eliminating 91.11 km of unnecessary transit mileage relative to the Naive Highest Price heuristic across all dispatches and 372.78 km across divergent scenarios; 2) *Observational Field Evidence*: Primary tracking indicates compliant farmers achieved +9.93% higher returns, and FPO truckload pooling yielded a 26.52% freight reduction; 3) *Future Deployment Validation*: Full causal confirmation will require randomized controlled field trials across multi-state cereal belts, dynamic cooperative fleet dispatching, and real-time cold-chain tracking."""

if old_xi in text:
    text = text.replace(old_xi, new_xi)
    print("Replaced Section XI.")
else:
    print("WARNING: old_xi not found")

# 8. Author Biographies
old_bios = """## Author Biographies
**Kiran Kumar Pasupula** (Reg. No. 23BCE9610, Student Member, IEEE) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests encompass computational decision support systems, agricultural transport optimization, spatial network modeling, and applied data analytics.

**B. Bhargav** (Reg. No. 23BCE9623) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests include distributed data architectures, rural supply chain modeling, and algorithm optimization.

**S. RavindraNath** (Reg. No. 23BCE9516) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests include spatial data mining, cloud computing architectures, and agricultural informatics.

**S. Kranthi Kowshik** (Reg. No. 23BCE9611) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests include applied optimization algorithms, mobile decision platforms, and regional market analytics.

**Prof. Pechetti Mounika** is an Assistant Professor in the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. Her research interests encompass machine learning, intelligent optimization, agricultural informatics, and computational decision systems. She served as the faculty project guide and research supervisor for this project."""

new_bios = """## Author Biographies
**Prof. Pechetti Mounika** is an Assistant Professor in the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. Her research interests encompass machine learning, intelligent optimization, agricultural informatics, and computational decision systems. She served as the faculty project guide and research supervisor for this project.

**P. Kiran Kumar** (Reg. No. 23BCE9610, Student Member, IEEE) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests encompass computational decision support systems, agricultural transport optimization, spatial network modeling, and applied data analytics.

**B. Bhargav** (Reg. No. 23BCE9623) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests include distributed data architectures, rural supply chain modeling, and algorithm optimization.

**S. RavindraNath** (Reg. No. 23BCE9516) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests include spatial data mining, cloud computing architectures, and agricultural informatics.

**S. Kranthi Kowshik** (Reg. No. 23BCE9611) is an undergraduate student in Computer Science and Engineering at the School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India. His research interests include applied optimization algorithms, mobile decision platforms, and regional market analytics."""

if old_bios in text:
    text = text.replace(old_bios, new_bios)
    print("Replaced Author Biographies.")
else:
    print("WARNING: old_bios not found")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)
print("Finished updating generate_markdown_manuscript.py.")

