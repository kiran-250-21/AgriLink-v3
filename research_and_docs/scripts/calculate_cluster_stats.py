import sys
import pandas as pd
import numpy as np
import scipy.stats as stats

# Load pooled 5000 scenarios
df = pd.read_csv('research_and_docs/results/pooled_5seeds_5000.csv')

# Temporal clustering into 12 30-day blocks
df['date'] = pd.to_datetime(df['decision_date'])
min_date = df['date'].min()
df['temp_block'] = ((df['date'] - min_date).dt.days // 30).clip(0, 11)

strategies = [
    ('S1', 'S1_Nearest', 'Nearest Market'),
    ('S2', 'S2_HighestPrice', 'Naive Highest Price'),
    ('S3', 'S3_DistanceCap', 'Distance-Capped Nearest (40km)'),
    ('S4', 'S4_Hurdle', 'Fixed Cost Hurdle (+Rs 2.5/kg)'),
    ('S5', 'S5_LongRunAvg', 'Long-Run Historical Mean'),
    ('S6', 'S6_MovingAvg', '7-Day Moving Average'),
    ('S7', 'S7_RobustWorstCase', 'Robust Worst-Case Minimax'),
    ('S8', 'S8_Top3Portfolio', 'Top-3 Restricted Portfolio'),
    ('Oracle', 'Oracle', 'Ex-Post Oracle Frontier')
]

print("=== PAIRED CLUSTERED T-TESTS ACROSS 12 TEMPORAL BLOCKS (G=12, df=11) ===")
results = []
for code, col, name in strategies:
    diff = df['AgriLink_net_realization'] - df[f'{col}_net_realization']
    df['temp_diff'] = diff
    cluster_means = df.groupby('temp_block')['temp_diff'].mean()
    mean_diff = float(cluster_means.mean())
    se = float(cluster_means.std(ddof=1) / np.sqrt(len(cluster_means)))
    t_val = float(mean_diff / se) if se > 0 else 0.0
    p_val = float(2 * (1 - stats.t.cdf(abs(t_val), df=11)))
    ci_low = float(mean_diff - stats.t.ppf(0.975, df=11) * se)
    ci_high = float(mean_diff + stats.t.ppf(0.975, df=11) * se)
    strat_mean = float(df[f'{col}_net_realization'].mean())
    agri_mean = float(df['AgriLink_net_realization'].mean())
    pct_gain = ((agri_mean - strat_mean) / strat_mean) * 100.0 if strat_mean != 0 else 0.0
    
    results.append({
        'code': code,
        'name': name,
        'strat_mean': strat_mean,
        'diff': mean_diff,
        'pct_gain': pct_gain,
        'se': se,
        't_stat': t_val,
        'p_val': p_val,
        'ci_low': ci_low,
        'ci_high': ci_high
    })

res_df = pd.DataFrame(results)
print(res_df.to_string())

# Also check Freight Models A-E comparisons
print("\n=== FREIGHT MODELS COMPARISONS (Table 6/7) ===")
with open('research_and_docs/results/master_empirical_results.json') as f:
    import json
    master = json.load(f)
    if 'independent_freight_models' in master:
        print(json.dumps(master['independent_freight_models'], indent=2))

