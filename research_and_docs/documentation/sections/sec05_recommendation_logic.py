"""
Section 5: Agricultural Market Recommendation Logic & Spatial Engine
"""

def get_content():
    return r"""# CHAPTER 6: AGRICULTURAL MARKET RECOMMENDATION LOGIC & SPATIAL ENGINE

### 6.1 Mathematical Formulation of Net Realization ($NR$)

AgriLink replaces subjective heuristic guessing with a deterministic spatial optimization engine. The decision objective is formulated as:

$$\max_{m \in \mathcal{M} \cup \mathcal{B}} \text{Estimated Net Revenue}(m)$$

$$\text{Estimated Net Revenue}(m) = \max\Big(0, \; \text{Gross Revenue}(m) - \text{Estimated Logistics Cost}(m)\Big)$$

Where:
- $\mathcal{M}$: Set of active regional APMC mandis.
- $\mathcal{B}$: Set of active institutional buyer procurement buy orders.
- $Q$: Mass of harvested agricultural produce in kilograms ($\text{kg}$).
- $P_m$: Unit purchasing price offered at destination $m$ in ₹ per kg ($₹/\text{kg}$).

$$\text{Gross Revenue}(m) = \text{round}(P_m \times Q)$$

#### The Logistics Transportation Cost Formula:
Rural freight haulage in India comprises a fixed loading/unloading terminal fee plus variable distance-weight tariffs:

$$\text{Weight}_{\text{tons}} = \max\Big(0.5, \; \frac{Q}{1000}\Big)$$

$$\text{Base Cost} = ₹2,000 \quad \text{(Fixed terminal handling, loading & minimum truck haulage)}$$

$$\text{Rate per Ton-Km} = ₹12/\text{ton}\cdot\text{km}$$

$$\text{Estimated Logistics Cost}(m) = \text{round}\Big(\text{Base Cost} + \big(\text{Distance}_{\text{km}}(m) \times \text{Weight}_{\text{tons}} \times \text{Rate per Ton-Km}\big)\Big)$$

---

### 6.2 Spatial Coordinate Registry: 26 Andhra Pradesh Agricultural Districts

The spatial engine in `backend/utils/calculations.js` integrates a hardcoded, verified coordinate registry covering all 26 restructured districts and major agricultural trade terminals of Andhra Pradesh:

| Region | District / Trade Hub Identifier | Latitude (°N) | Longitude (°E) | Primary Agricultural Produce |
| :--- | :--- | :--- | :--- | :--- |
| **North Coastal** | `VISAKHAPATNAM` / `VIZAG` | 17.6868 | 83.2185 | Export Terminal, Sugarcane |
| **North Coastal** | `ANAKAPALLI` | 17.6896 | 83.0033 | Second largest Jaggery Market in India |
| **North Coastal** | `SRIKAKULAM` | 18.2970 | 83.8967 | Cashew, Paddy, Groundnut |
| **North Coastal** | `VIZIANAGARAM` | 18.1067 | 83.3956 | Jute, Mango, Maize |
| **Coastal Central**| `KAKINADA` | 16.9891 | 82.2475 | Rice Deepwater Port, Coconut |
| **Coastal Central**| `RAJAHMUNDRY` (East Godavari) | 17.0005 | 81.8040 | Tobacco, Banana, Oil Palm |
| **Coastal Central**| `ELURU` (West Godavari) | 16.7107 | 81.0952 | Paddy, Cocoa, Oil Palm |
| **Coastal Central**| `VIJAYAWADA` (NTR District) | 16.5062 | 80.6480 | Regional Commercial Trading Capital |
| **Coastal Central**| `GUNTUR` | 16.3067 | 80.4365 | Asia's Largest Red Chilli Market Yard |
| **Coastal Central**| `TENALI` | 16.2437 | 80.6400 | Turmeric, Paddy, Black Gram |
| **South Coastal**  | `ONGOLE` (Prakasam) | 15.5057 | 80.0499 | Tobacco, Bengal Gram, Cotton |
| **South Coastal**  | `NELLORE` (SPSR Nellore) | 14.4426 | 79.9865 | High-grade Paddy (Masoori), Aqua |
| **Rayalaseema**    | `KURNOOL` | 15.8281 | 78.0373 | Onion, Cotton, Groundnut |
| **Rayalaseema**    | `NANDYAL` | 15.4786 | 78.4836 | Maize, Bengal Gram, Sunflower |
| **Rayalaseema**    | `ANANTAPUR` | 14.6819 | 77.6007 | Groundnut, Sweet Orange, Pomegranate |
| **Rayalaseema**    | `KADAPA` (YSR District) | 14.4673 | 78.8242 | Turmeric, Banana, Lime |
| **Rayalaseema**    | `TIRUPATI` / `CHITTOOR` | 13.6288 | 79.4192 | Jaggery, Tomato, Mango Pulp |
| **Rayalaseema**    | `MADANAPALLE` | 13.5560 | 78.5010 | Asia's Largest Tomato Mandi |
| **Trade Terminals**| `HYDERABAD` (Telangana) | 17.3850 | 78.4867 | Major Inter-State Consumptive Hub |
| **Trade Terminals**| `CHENNAI` (Tamil Nadu) | 13.0827 | 80.2707 | Port Terminal & Southern Metro Hub |

---

### 6.3 Multilingual Telugu Normalization & Typo Resilience

Smallholder farmers often input locations in Telugu script, use historical aliases, or make spelling mistakes on mobile keyboards. AgriLink processes origin strings through a 5-stage canonicalization pipeline (`canonicalizeLocation` in `calculations.js`):

```
RAW USER INPUT STRING (e.g., "గుంటూరు", "Bezawada", "Vishakaptnam")
                   │
                   ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 1: Telugu-to-Canonical Dictionary Matching       │
│ Checks `TELUGU_TO_CANONICAL`: 'గుంటూరు' -> 'GUNTUR'    │
└──────────────────────────┬─────────────────────────────┘
                           │ If not matched
                           ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 2: Direct Alias Dictionary Matching              │
│ Checks `LOCATION_ALIASES`: 'BEZAWADA' -> 'VIJAYAWADA'  │
│ Checks historical names: 'CUDDAPAH' -> 'KADAPA'        │
└──────────────────────────┬─────────────────────────────┘
                           │ If not matched
                           ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 3: Direct Coordinate Registry Key Matching       │
│ Checks uppercase token against COORDINATE_REGISTRY     │
└──────────────────────────┬─────────────────────────────┘
                           │ If not matched
                           ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 4: Substring Ingestion & Token Analysis          │
│ Scans joined string for registry substrings            │
└──────────────────────────┬─────────────────────────────┘
                           │ If not matched
                           ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 5: Levenshtein Distance Fuzzy Matching           │
│ Calculates minimum edit distance matrix.               │
│ If d <= 2 (or d <= 3 for words >= 7 chars), matches!   │
│ 'VISHAKAPTNAM' (d=2) -> 'VISAKHAPATNAM'                │
└────────────────────────────────────────────────────────┘
```

#### Levenshtein String Distance Implementation:
```javascript
const levenshteinDistance = (a, b) => {
  const an = a ? a.length : 0;
  const bn = b ? b.length : 0;
  if (an === 0) return bn;
  if (bn === 0) return an;
  const matrix = Array(bn + 1).fill(0).map(() => Array(an + 1).fill(0));
  for (let i = 0; i <= an; i++) matrix[0][i] = i;
  for (let j = 0; j <= bn; j++) matrix[j][0] = j;
  for (let j = 1; j <= bn; j++) {
    for (let i = 1; i <= an; i++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[j][i] = Math.min(
        matrix[j][i - 1] + 1,      // Deletion
        matrix[j - 1][i] + 1,      // Insertion
        matrix[j - 1][i - 1] + cost // Substitution
      );
    }
  }
  return matrix[bn][an];
};
```

---

### 6.4 Road Haulage Modeling: Haversine Formula with 1.22x Tortuosity

Straight-line Euclidean or Great-Circle distance severely underestimates real-world driving mileage due to river detours (e.g., Krishna and Godavari rivers), mountain ghats, and highway infrastructure. AgriLink resolves road transit distance using a 4-tier hierarchy:

1. **Same-District Default**: If canonical origin equals destination, haulage is set to a realistic local intra-city transit distance of **12 km**.
2. **Verified Highway Distance Matrix**: Uses hardcoded road distances for major verified corridors (e.g., Guntur–Vijayawada = 35 km, Guntur–Kurnool = 260 km, Visakhapatnam–Vijayawada = 350 km).
3. **Haversine Formula with Tortuosity Multiplier**:
   $$\Delta\text{lat} = (\text{lat}_2 - \text{lat}_1) \times \frac{\pi}{180}, \quad \Delta\text{lon} = (\text{lon}_2 - \text{lon}_1) \times \frac{\pi}{180}$$
   $$a = \sin^2\Big(\frac{\Delta\text{lat}}{2}\Big) + \cos\Big(\text{lat}_1 \times \frac{\pi}{180}\Big) \cdot \cos\Big(\text{lat}_2 \times \frac{\pi}{180}\Big) \cdot \sin^2\Big(\frac{\Delta\text{lon}}{2}\Big)$$
   $$c = 2 \times \text{atan2}\big(\sqrt{a}, \sqrt{1-a}\big)$$
   $$\text{Straight-Line Distance} = 6,371 \times c \quad (\text{km})$$
   $$\text{Road Distance} = \text{round}(\text{Straight-Line Distance} \times 1.22)$$
   *Note: $1.22$ represents the empirically verified Indian Highway Road Tortuosity factor.*
4. **Fallback Geographic Centroid**: If an unknown remote location is entered, distance is estimated from the Andhra Pradesh state geographic center at Amaravati/Guntur (`lat: 16.3067, lng: 80.4365`).

---

### 6.5 End-to-End Step-by-Step Numerical Walkthrough

#### Scenario Setup:
- **Farmer**: Kiran Farmer, located at **Guntur** (`16.3067° N, 80.4365° E`).
- **Harvested Produce**: **Red Chilli** (Grade-A Quality).
- **Quantity Available**: **5,000 kg** ($5.0\text{ Metric Tons}$).
- **Freight Rate**: $₹2,000\text{ Base} + (\text{Distance} \times 5.0\text{ Tons} \times ₹12/\text{ton-km})$.

#### Candidate Destinations Available:
1. **Candidate A**: Guntur APMC Mandi (Immediate local market).
2. **Candidate B**: Vijayawada APMC Mandi (Neighboring regional hub, 35 km away).
3. **Candidate C**: Visakhapatnam APMC Mandi (Distant coastal terminal, 380 km away).
4. **Candidate D**: Godavari Agro Processing Ltd (Institutional Buyer in Vijayawada, 35 km away).

---

#### Step-by-Step Mathematical Computation:

#### Candidate A: Guntur APMC Mandi (Local)
- Offered Price: **₹185 / kg**
- Road Distance: **12 km** (Local intra-district transit)
- Gross Revenue:
  $$\text{Gross} = 5,000\text{ kg} \times ₹185 = ₹925,000$$
- Logistics Haulage Cost:
  $$\text{Logistics} = 2,000 + (12\text{ km} \times 5.0\text{ tons} \times ₹12) = 2,000 + 720 = ₹2,720$$
- Estimated Net Revenue:
  $$\text{Net Revenue} = ₹925,000 - ₹2,720 = \mathbf{₹922,280}$$

---

#### Candidate B: Vijayawada APMC Mandi (Regional Mandi)
- Offered Price: **₹195 / kg** (+₹10/kg spatial premium over local Guntur mandi)
- Road Distance: **35 km** (via NH16 Guntur–Vijayawada expressway)
- Gross Revenue:
  $$\text{Gross} = 5,000\text{ kg} \times ₹195 = ₹975,000$$
- Logistics Haulage Cost:
  $$\text{Logistics} = 2,000 + (35\text{ km} \times 5.0\text{ tons} \times ₹12) = 2,000 + 2,100 = ₹4,100$$
- Estimated Net Revenue:
  $$\text{Net Revenue} = ₹975,000 - ₹4,100 = \mathbf{₹970,900}$$
- **Economic Evaluation**: Net gain over local Guntur mandi = $₹970,900 - ₹922,280 = \mathbf{+₹48,620}$! Moving 35 km is highly profitable.

---

#### Candidate C: Visakhapatnam APMC Mandi (Distant Mandi - Naive Heuristic Trap!)
- Offered Price: **₹210 / kg** (+₹25/kg nominal premium — looks tempting!)
- Road Distance: **380 km** (via NH16 coastal corridor)
- Gross Revenue:
  $$\text{Gross} = 5,000\text{ kg} \times ₹210 = ₹1,050,000$$
- Logistics Haulage Cost:
  $$\text{Logistics} = 2,000 + (380\text{ km} \times 5.0\text{ tons} \times ₹12) = 2,000 + 22,800 = ₹24,800$$
- Estimated Net Revenue:
  $$\text{Net Revenue} = ₹1,050,000 - ₹24,800 = \mathbf{₹1,025,200}$$
- **Economic Evaluation**: Gross revenue jumped by ₹125,000, but ₹24,800 was consumed by trucking. Because the nominal price spread was very high (+₹25/kg), this option still yields a high net return, but carries high long-distance transit risk (spoilage, driver breakdown).

---

#### Candidate D: Buyer: Godavari Agro Processing Ltd (Institutional Buyer in Vijayawada)
- Offered Price: **₹205 / kg**
- Road Distance: **35 km**
- Gross Revenue:
  $$\text{Gross} = 5,000\text{ kg} \times ₹205 = ₹1,025,000$$
- Logistics Haulage Cost:
  $$\text{Logistics} = 2,000 + (35\text{ km} \times 5.0\text{ tons} \times ₹12) = ₹4,100$$
- Estimated Net Revenue:
  $$\text{Net Revenue} = ₹1,025,000 - ₹4,100 = \mathbf{₹1,020,900}$$

---

#### Final Ranked Recommendation Output Table (As Rendered to Farmer):

| Rank | Destination Name | Type | Price/Kg | Distance | Gross Revenue | Logistics Cost | Estimated Net Realization | Status Flag |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **Visakhapatnam APMC** | `MARKET` | ₹210 | 380 km | ₹1,050,000 | ₹24,800 | **₹1,025,200** | 🏆 **Best Net Return** |
| **#2** | **Buyer: Godavari Agro** | `BUYER`  | ₹205 | 35 km  | ₹1,025,000 | ₹4,100  | **₹1,020,900** | Highly Recommended (Near) |
| **#3** | **Vijayawada APMC**    | `MARKET` | ₹195 | 35 km  | ₹975,000   | ₹4,100  | **₹970,900**   | Regional Mandi |
| **#4** | **Guntur APMC**        | `MARKET` | ₹185 | 12 km  | ₹925,000   | ₹2,720  | **₹922,280**   | Local Mandi (Lowest Return) |

#### Critical Engineering Insight to Explain in Interview:
Notice that **Buyer: Godavari Agro** (Rank #2, Net = ₹1,020,900) yields practically the exact same net cash return as **Visakhapatnam APMC** (Rank #1, Net = ₹1,025,200) — a negligible ₹4,300 difference ($<0.4\%$) — but requires only **35 km** of transit versus **380 km** of hazardous interstate highway transit! AgriLink empowers the farmer to make an informed, risk-adjusted decision rather than blindly dispatching produce on an unhedged 380 km journey.
"""
