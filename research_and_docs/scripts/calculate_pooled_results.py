import os, sys, json
import pandas as pd
import numpy as np

from run_comprehensive_agrilink_experiment import (
    load_market_coordinates, load_and_preprocess_agmarknet,
    generate_scenarios, run_evaluation, compute_independent_freight,
    TARGET_CROPS, DATA_DIR, RESULTS_DIR
)

coords = load_market_coordinates()
data_file = os.path.join(DATA_DIR, 'agmarknet_india_historical_prices_2024_2025.csv')
daily_df, audit = load_and_preprocess_agmarknet(data_file, coords)

seeds = [42, 101, 2024, 777, 999]
all_recs = []

for s in seeds:
    sc = generate_scenarios(daily_df, coords, n_total=1000, seed=s)
    rec, _ = run_evaluation(sc, daily_df, coords, seed=s)
    for r in rec:
        r['seed'] = s
    all_recs.extend(rec)

print(f"Done! Total pooled dispatches: {len(all_recs)}")
df = pd.DataFrame(all_recs)
df.to_csv(os.path.join(RESULTS_DIR, 'pooled_5seeds_5000.csv'), index=False)

strats = ['S1_Nearest', 'S2_HighestPrice', 'S4_Hurdle', 'S5_LongRunAvg', 'S6_MovingAvg', 'S7_RobustWorstCase', 'S8_Top3Portfolio', 'AgriLink', 'Oracle']
print("\n=== POOLED STRATEGY MEANS (N=5,000) ===")
agri_mean = df['AgriLink_net_realization'].mean()
for st in strats:
    col = f"{st}_net_realization"
    m = df[col].mean()
    gain = agri_mean - m
    pct = (gain / m) * 100 if m != 0 else 0
    print(f"{st:20s}: Mean NR = INR {m:10.2f} | Gain vs AgriLink = +INR {gain:8.2f} ({pct:5.2f}%)")

print("\n=== POOLED OVERLAP WITH HIGHEST PRICE ===")
df['agri_high_match'] = df['AgriLink_market'] == df['S2_HighestPrice_market']
match_pct = df['agri_high_match'].mean() * 100
div = df[~df['agri_high_match']]
print(f"Match: {match_pct:.2f}% | Divergent: {100-match_pct:.2f}% (N={len(div)})")
div_gain = (div['AgriLink_net_realization'] - div['S2_HighestPrice_net_realization']).mean()
div_dist = (div['S2_HighestPrice_dist_km'] - div['AgriLink_dist_km']).mean()
print(f"Divergent mean gain: +INR {div_gain:.2f} | Divergent distance saved: {div_dist:.1f} km")

# Oracle capture
agri_gain_near = agri_mean - df['S1_Nearest_net_realization'].mean()
oracle_gain_near = df['Oracle_net_realization'].mean() - df['S1_Nearest_net_realization'].mean()
oracle_capture = (agri_gain_near / oracle_gain_near) * 100
regret = df['Oracle_net_realization'].mean() - agri_mean
print(f"Oracle Capture: {oracle_capture:.2f}% | Regret: INR {regret:.2f}")

# Highest Price loses to Nearest
df['high_loses_near'] = df['S2_HighestPrice_net_realization'] < df['S1_Nearest_net_realization']
loss_count = df['high_loses_near'].sum()
mean_loss = (df[df['high_loses_near']]['S2_HighestPrice_net_realization'] - df[df['high_loses_near']]['S1_Nearest_net_realization']).mean()
print(f"Highest loses to Nearest: {df['high_loses_near'].mean()*100:.2f}% (N={loss_count}), mean loss: INR {mean_loss:.2f}")

# AgriLink loses to Nearest
df['agri_loses_near'] = df['AgriLink_net_realization'] < df['S1_Nearest_net_realization']
print(f"AgriLink loses to Nearest: {df['agri_loses_near'].mean()*100:.2f}% (N={df['agri_loses_near'].sum()})")

# Win / Tie / Loss vs baselines
print("\n=== POOLED WIN / TIE / LOSS vs NEAREST & HIGHEST ===")
for base in ['S1_Nearest', 'S2_HighestPrice', 'S4_Hurdle', 'S5_LongRunAvg', 'S6_MovingAvg', 'S7_RobustWorstCase', 'S8_Top3Portfolio']:
    diff = df['AgriLink_net_realization'] - df[f'{base}_net_realization']
    wins = (diff > 0.01).sum()
    ties = (diff.abs() <= 0.01).sum()
    losses = (diff < -0.01).sum()
    win_gain = diff[diff > 0.01].mean() if wins > 0 else 0
    loss_regret = diff[diff < -0.01].mean() if losses > 0 else 0
    print(f"vs {base:18s}: Wins={wins} ({wins/len(df)*100:.1f}%), Ties={ties} ({ties/len(df)*100:.1f}%), Losses={losses} ({losses/len(df)*100:.1f}%) | Mean Win=+INR {win_gain:.2f}, Mean Loss=INR {loss_regret:.2f}, Net=+INR {diff.mean():.2f}")

# Commodity Breakdown across pooled 5,000
print("\n=== POOLED COMMODITY BREAKDOWN (N=5,000) ===")
for crop, g in df.groupby('crop'):
    a_nr = g['AgriLink_net_realization'].mean()
    n_nr = g['S1_Nearest_net_realization'].mean()
    h_nr = g['S2_HighestPrice_net_realization'].mean()
    q_mean = g['quantity_kg'].mean()
    gain_n = a_nr - n_nr
    gain_h = a_nr - h_nr
    print(f"{crop:25s}: N={len(g)} | Q_mean={q_mean:.1f}kg | AgriLink=INR {a_nr:9.2f} | Near=INR {n_nr:9.2f} (+{gain_n/n_nr*100:5.2f}%) | High=INR {h_nr:9.2f} (+{gain_h/h_nr*100:5.2f}%)")

# Month-clustered inference
df['month'] = pd.to_datetime(df['decision_date']).dt.to_period('M')
months = df['month'].unique()
print(f"\nUnique calendar months: {len(months)} ({months})")
month_diffs_near = df.groupby('month').apply(lambda m: (m['AgriLink_net_realization'] - m['S1_Nearest_net_realization']).mean())
month_diffs_high = df.groupby('month').apply(lambda m: (m['AgriLink_net_realization'] - m['S2_HighestPrice_net_realization']).mean())
from scipy import stats
t_near = stats.ttest_1samp(month_diffs_near, 0)
t_high = stats.ttest_1samp(month_diffs_high, 0)
print(f"Month-level t-test vs Nearest: t={t_near.statistic:.3f}, p={t_near.pvalue:.4f}")
print(f"Month-level t-test vs Highest: t={t_high.statistic:.3f}, p={t_high.pvalue:.4f}")
