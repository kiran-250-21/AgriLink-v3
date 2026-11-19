import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(14, 11), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#FFFFFF')

    # Color definitions (Modern academic palette)
    c_primary = '#1E3A8A'     # Deep Navy
    c_primary_light = '#EFF6FF'
    c_spatial = '#0369A1'     # Ocean Blue
    c_spatial_light = '#F0F9FF'
    c_price = '#4338CA'       # Indigo
    c_price_light = '#EEF2FF'
    c_optim = '#B45309'       # Warm Amber
    c_optim_light = '#FFFBEB'
    c_eval = '#047857'        # Emerald Green
    c_eval_light = '#F0FDF4'
    c_border = '#CBD5E1'      # Border gray
    c_text = '#0F172A'        # Dark slate text

    def draw_rounded_box(x, y, w, h, bg_color, border_color, border_width=1.5, radius=0.25):
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle=f"round,pad={radius},rounding_size={radius}",
                             facecolor=bg_color, edgecolor=border_color,
                             linewidth=border_width, zorder=2)
        ax.add_patch(box)
        return box

    def draw_header_bar(x, y, w, h, bg_color, title_text, font_size=11, font_color='#FFFFFF'):
        # Header banner inside a box
        bar = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0.15,rounding_size=0.15",
                             facecolor=bg_color, edgecolor=bg_color,
                             linewidth=1, zorder=3)
        ax.add_patch(bar)
        ax.text(x + w / 2, y + h / 2, title_text,
                ha='center', va='center', fontsize=font_size, fontweight='bold',
                color=font_color, family='sans-serif', zorder=4)

    # 1. TOP HEADER BOX: Master Protocol
    draw_rounded_box(0.8, 9.8, 12.4, 0.9, '#1E293B', '#0F172A', border_width=1.8, radius=0.18)
    ax.text(7.0, 10.35, "AGRILINK EMPIRICAL LOGISTICS-AWARE DECISION & EVALUATION PROTOCOL",
            ha='center', va='center', fontsize=13, fontweight='bold', color='#F8FAFC', family='sans-serif', zorder=5)
    ax.text(7.0, 10.02, "End-to-End System Architecture: Spatial Infrastructure, Market Records, Optimization Rule & Forward Evaluation",
            ha='center', va='center', fontsize=9.5, fontstyle='italic', color='#94A3B8', family='sans-serif', zorder=5)

    # Connectors from Top Header to Spatial & Price boxes
    ax.annotate('', xy=(3.8, 9.25), xytext=(3.8, 9.8),
                arrowprops=dict(arrowstyle="-|>", color='#475569', lw=1.8, mutation_scale=15), zorder=1)
    ax.annotate('', xy=(10.2, 9.25), xytext=(10.2, 9.8),
                arrowprops=dict(arrowstyle="-|>", color='#475569', lw=1.8, mutation_scale=15), zorder=1)

    # 2. LEFT BOX: Physical Spatial Logistics Architecture
    draw_rounded_box(0.8, 6.7, 5.8, 2.5, c_spatial_light, '#0284C7', border_width=1.5)
    draw_header_bar(0.95, 8.75, 5.5, 0.45, c_spatial, "PHYSICAL SPATIAL LOGISTICS ARCHITECTURE", font_size=9.5)
    
    spatial_text = (
        "• Geocoded GPS Coordinates of APMC Mandis (18 Mandis across 10 AP Districts)\n"
        "• Great-Circle Geodesic Distance (Dg) via Haversine Spherical Formulation\n"
        "• Calibrated Regional Circuity Factor (Cf = 1.28 Road Winding Multiplier)\n"
        "• Baseline Freight Tariff Benchmark (c = ₹0.010/kg·km = ₹10.00/tonne·km)\n"
        "• Primary Transporter Survey: 25 Quotes across 4 Vehicle Classes (1.5T to 5.0T)"
    )
    ax.text(1.15, 7.7, spatial_text, ha='left', va='center', fontsize=8.2, color=c_text,
            linespacing=1.65, family='sans-serif', zorder=5)

    # 3. RIGHT BOX: Temporal Wholesale Price Record Architecture
    draw_rounded_box(7.4, 6.7, 5.8, 2.5, c_price_light, '#6366F1', border_width=1.5)
    draw_header_bar(7.55, 8.75, 5.5, 0.45, c_price, "TEMPORAL WHOLESALE PRICE RECORD ARCHITECTURE", font_size=9.5)
    
    price_text = (
        "• 2,304 Validated AGMARKNET Official Daily Auction Wholesale Price Records\n"
        "• 18 Regulated APMC Wholesale Assembly Mandis (Coverage Threshold k >= 10)\n"
        "• 5 AP Commodity Archetypes: Maize, Groundnut, Mango, Cotton, Arhar\n"
        "• 364 Active Trading Days Full Empirical Year (Aug 16, 2024 to Aug 14, 2025)\n"
        "• Strict Retrospective Lookback Window [T - 30, T] Eliminating Lookahead Leakage"
    )
    ax.text(7.75, 7.7, price_text, ha='left', va='center', fontsize=8.2, color=c_text,
            linespacing=1.65, family='sans-serif', zorder=5)

    # Connectors from Spatial & Price boxes to Optimization box
    ax.annotate('', xy=(5.0, 5.85), xytext=(3.7, 6.6),
                arrowprops=dict(arrowstyle="-|>", color='#475569', lw=1.8, mutation_scale=15), zorder=1)
    ax.annotate('', xy=(9.0, 5.85), xytext=(10.3, 6.6),
                arrowprops=dict(arrowstyle="-|>", color='#475569', lw=1.8, mutation_scale=15), zorder=1)

    # 4. MIDDLE BOX: Decision-Time Dispatch Optimization Rule
    draw_rounded_box(0.8, 3.45, 12.4, 2.35, c_optim_light, '#D97706', border_width=1.8)
    draw_header_bar(1.0, 5.35, 12.0, 0.45, c_optim, "DECISION-TIME DISPATCH OPTIMIZATION RULE (AT HARVEST DATE T)", font_size=10)

    # Formula callout card
    draw_rounded_box(1.2, 4.35, 11.6, 0.85, '#FFFFFF', '#F59E0B', border_width=1.2, radius=0.1)
    formula_label = "AgriLink Proposed Dispatch Rule:"
    formula_math = "m* = argmax [ Q · P̂m,c(T) - TC(Q, Dr(m)) - Φfees(m) - Lspoil(m) ]"
    ax.text(1.5, 4.9, formula_label, ha='left', va='center', fontsize=9, fontweight='bold', color='#92400E', family='sans-serif', zorder=5)
    ax.text(7.0, 4.58, formula_math, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1E293B', family='monospace', zorder=5)

    baselines_text = (
        "Evaluated Baseline Suite:  S1 Nearest Market (argmin Dr)  |  S2 Naive Highest Price (argmax P̂)  |  S3 Distance-Capped Nearest (40 km)\n"
        "S4 Fixed Cost Hurdle (+₹2.50/kg)  |  S5 Long-Run Historical Mean  |  S6 7-Day Moving Avg  |  S7 Robust Worst-Case  |  S8 Top-3 Restricted Portfolio"
    )
    ax.text(7.0, 3.85, baselines_text, ha='center', va='center', fontsize=8.0, color='#334155', linespacing=1.5, family='sans-serif', zorder=5)

    # Connector to Evaluation Protocol
    ax.annotate('', xy=(7.0, 2.85), xytext=(7.0, 3.4),
                arrowprops=dict(arrowstyle="-|>", color='#475569', lw=2.0, mutation_scale=16), zorder=1)

    # 5. BOTTOM BOX: Out-of-Sample Forward Evaluation Protocol
    draw_rounded_box(0.8, 0.35, 12.4, 2.45, c_eval_light, '#059669', border_width=1.8)
    draw_header_bar(1.0, 2.35, 12.0, 0.45, c_eval, "OUT-OF-SAMPLE FORWARD EVALUATION PROTOCOL (FORWARD HORIZONS T + H, H ∈ {7, 14, 30})", font_size=10)

    # Sub-cards inside evaluation
    card_w = 2.85
    card_h = 1.6
    y_card = 0.55

    # Sub-card 1: Full Cohort
    draw_rounded_box(1.1, y_card, card_w, card_h, '#FFFFFF', '#A7F3D0', border_width=1.0, radius=0.1)
    ax.text(1.1 + card_w/2, y_card + 1.35, "Experimental Cohort", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#065F46', family='sans-serif', zorder=5)
    t1 = "• N = 5,000 Dispatches\n• 5 Independent Spatial Seeds\n  (42, 101, 2024, 777, 999)\n• Parcel Q ~ U(1000, 3500 kg)\n• Origin Radius: 5 to 35 km"
    ax.text(1.25, y_card + 0.65, t1, ha='left', va='center', fontsize=7.2, color='#1E293B', linespacing=1.4, family='sans-serif', zorder=5)

    # Sub-card 2: Imputation Strata
    draw_rounded_box(4.1, y_card, card_w, card_h, '#FFFFFF', '#A7F3D0', border_width=1.0, radius=0.1)
    ax.text(4.1 + card_w/2, y_card + 1.35, "Imputation Strata", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#065F46', family='sans-serif', zorder=5)
    t2 = "• Stratum 1: Zero Imputation\n  (N = 3,135; 62.70%)\n• Stratum 2: Adjacent Window\n  (N = 1,550; 31.00%)\n• Stratum 3: Last-Price Fallback\n  (N = 315; 6.30%)"
    ax.text(4.25, y_card + 0.65, t2, ha='left', va='center', fontsize=7.2, color='#1E293B', linespacing=1.4, family='sans-serif', zorder=5)

    # Sub-card 3: Freight & APMC Frictions
    draw_rounded_box(7.1, y_card, card_w, card_h, '#FFFFFF', '#A7F3D0', border_width=1.0, radius=0.1)
    ax.text(7.1 + card_w/2, y_card + 1.35, "Freight & Frictions", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#065F46', family='sans-serif', zorder=5)
    t3 = "• 4 Tariff Stress-Tests: Distance\n  Slabs, Min Trip, Stochastic,\n  and Backhaul Penalty\n• Statutory Frictions: 1% Cess,\n  1% Commission, Hamali ₹0.20/kg"
    ax.text(7.25, y_card + 0.65, t3, ha='left', va='center', fontsize=7.2, color='#1E293B', linespacing=1.4, family='sans-serif', zorder=5)

    # Sub-card 4: Statistical Estimand & Oracle
    draw_rounded_box(10.1, y_card, card_w, card_h, '#FFFFFF', '#A7F3D0', border_width=1.0, radius=0.1)
    ax.text(10.1 + card_w/2, y_card + 1.35, "Statistical Benchmark", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#065F46', family='sans-serif', zorder=5)
    t4 = "• Dual Estimands: Scenario\n  Bootstrap & Cluster df=11\n• Benjamini-Hochberg FDR\n• S9 Theoretical Oracle Bound\n  (Hindsight Ceiling: 95.56% cap)"
    ax.text(10.25, y_card + 0.65, t4, ha='left', va='center', fontsize=7.2, color='#1E293B', linespacing=1.4, family='sans-serif', zorder=5)

    out_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'figures', 'fig1_system_architecture.png')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"Architecture diagram saved successfully to: {out_path}")

if __name__ == '__main__':
    create_architecture_diagram()

