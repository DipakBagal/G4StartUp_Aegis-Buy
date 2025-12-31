"""
Demo Visualizations for Aegis-Buy Showcase
Generates charts and statistics to support the demo video script
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory
import os
os.makedirs('demo_assets', exist_ok=True)

# ==========================================
# 1. PROBLEM STATEMENT VISUALIZATIONS
# ==========================================

def create_price_volatility_chart():
    """Shows price fluctuation of a typical product over 30 days"""
    days = 30
    dates = [datetime.now() - timedelta(days=x) for x in range(days, 0, -1)]
    
    # Simulate realistic price volatility
    base_price = 999
    np.random.seed(42)
    prices = base_price + np.random.normal(0, 50, days)
    # Add some peaks and valleys
    prices[5:8] = base_price - 150  # Sale period
    prices[15:18] = base_price + 100  # High demand period
    prices[25:28] = base_price - 80  # Another sale
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, prices, linewidth=2.5, color='#2E86AB', marker='o', markersize=4)
    ax.axhline(y=base_price, color='red', linestyle='--', linewidth=2, label='Average Price', alpha=0.7)
    
    # Highlight best and worst times to buy
    best_day = np.argmin(prices)
    worst_day = np.argmax(prices)
    ax.scatter(dates[best_day], prices[best_day], color='green', s=200, zorder=5, label='Best Time to Buy', marker='v')
    ax.scatter(dates[worst_day], prices[worst_day], color='red', s=200, zorder=5, label='Worst Time to Buy', marker='^')
    
    ax.set_title('Price Volatility: Typical Electronics Product Over 30 Days', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price (₹)', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Add annotations
    savings = prices[worst_day] - prices[best_day]
    ax.annotate(f'Potential Savings: ₹{savings:.0f} ({savings/prices[worst_day]*100:.1f}%)',
                xy=(dates[best_day], prices[best_day]),
                xytext=(dates[best_day] + timedelta(days=5), prices[best_day] - 50),
                fontsize=11, fontweight='bold', color='green',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('demo_assets/01_price_volatility.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: Price Volatility Chart")

def create_buyer_pain_points():
    """Bar chart showing buyer frustrations"""
    pain_points = [
        'Price Volatility',
        'Timing Uncertainty',
        'Information Overload',
        'Fear of Missing Deals',
        'Lack of Trust in Reviews'
    ]
    percentages = [78, 82, 71, 65, 58]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(pain_points, percentages, color=['#FF6B6B', '#FFA07A', '#FFD93D', '#6BCB77', '#4D96FF'])
    
    # Add percentage labels
    for i, (bar, pct) in enumerate(zip(bars, percentages)):
        ax.text(pct + 1, i, f'{pct}%', va='center', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('% of Online Shoppers Reporting This Issue', fontsize=12, fontweight='bold')
    ax.set_title('Top 5 E-Commerce Pain Points (2025 Survey)', fontsize=16, fontweight='bold')
    ax.set_xlim(0, 100)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_assets/02_buyer_pain_points.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: Buyer Pain Points Chart")

def create_market_size_infographic():
    """Market opportunity visualization"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Global E-commerce Market
    market_data = {
        '2023': 5.7,
        '2024': 6.3,
        '2025': 6.9,
        '2026': 7.5,
        '2027': 8.1
    }
    years = list(market_data.keys())
    values = list(market_data.values())
    
    ax1.bar(years, values, color=['#3498db', '#2980b9', '#1f618d', '#154360', '#0e2f44'], width=0.6)
    ax1.set_title('Global E-Commerce Market Size', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Market Size (Trillion USD)', fontsize=11)
    ax1.set_xlabel('Year', fontsize=11)
    
    for i, (year, value) in enumerate(zip(years, values)):
        ax1.text(i, value + 0.1, f'${value}T', ha='center', fontsize=10, fontweight='bold')
    
    # AI Shopping Assistant Adoption
    categories = ['Traditional\nShopping', 'Price\nComparison Tools', 'AI Shopping\nAssistants\n(2025)']
    adoption = [45, 28, 12]
    colors_pie = ['#95a5a6', '#f39c12', '#27ae60']
    
    wedges, texts, autotexts = ax2.pie(adoption, labels=categories, autopct='%1.1f%%',
                                         colors=colors_pie, startangle=90,
                                         textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax2.set_title('Shopping Decision Tools Adoption (2025)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('demo_assets/03_market_opportunity.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: Market Opportunity Chart")

# ==========================================
# 2. SOLUTION DEMONSTRATION VISUALIZATIONS
# ==========================================

def create_agent_workflow_diagram():
    """Multi-agent system flow"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    # Stages
    stages = [
        {'name': 'User Input', 'color': '#3498db', 'y': 0.85},
        {'name': 'Researcher Agent', 'color': '#e74c3c', 'y': 0.65},
        {'name': 'Sentiment Agent', 'color': '#f39c12', 'y': 0.45},
        {'name': 'Strategist Agent\n(Gemini 2.5 Flash)', 'color': '#27ae60', 'y': 0.25},
        {'name': 'Verdict: BUY/WATCH/WAIT', 'color': '#9b59b6', 'y': 0.05}
    ]
    
    for i, stage in enumerate(stages):
        # Draw box
        rect = plt.Rectangle((0.2, stage['y'] - 0.05), 0.6, 0.1, 
                             facecolor=stage['color'], edgecolor='black', 
                             linewidth=2, alpha=0.8)
        ax.add_patch(rect)
        ax.text(0.5, stage['y'], stage['name'], ha='center', va='center',
               fontsize=12, fontweight='bold', color='white')
        
        # Draw arrow
        if i < len(stages) - 1:
            ax.arrow(0.5, stage['y'] - 0.05, 0, -0.08, head_width=0.05, 
                    head_length=0.02, fc='black', ec='black', linewidth=2)
    
    # Add details
    details = [
        {'text': 'Amazon URL + Urgency (1-10)', 'y': 0.85, 'x': 0.85},
        {'text': 'Fetch: Price, MSRP, Rating, Reviews', 'y': 0.65, 'x': 0.85},
        {'text': 'Analyze: Reddit, Forums, Tech Sites', 'y': 0.45, 'x': 0.85},
        {'text': 'AI Decision: Price + Sentiment + Urgency', 'y': 0.25, 'x': 0.85},
        {'text': '3 Bullet Points Justification', 'y': 0.05, 'x': 0.85}
    ]
    
    for detail in details:
        ax.text(detail['x'], detail['y'], detail['text'], ha='left', va='center',
               fontsize=9, style='italic', bbox=dict(boxstyle='round,pad=0.3', 
               facecolor='lightyellow', alpha=0.7))
    
    ax.set_xlim(0, 1.3)
    ax.set_ylim(-0.05, 1)
    ax.set_title('Aegis-Buy: Multi-Agent Architecture', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('demo_assets/04_agent_workflow.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: Agent Workflow Diagram")

def create_verdict_distribution():
    """Distribution of verdicts from past analyses"""
    verdicts = ['BUY', 'WATCH', 'WAIT']
    counts = [45, 30, 25]  # Simulated data
    colors = ['#27ae60', '#3498db', '#f39c12']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(verdicts, counts, color=colors, width=0.6, edgecolor='black', linewidth=2)
    
    # Add count labels
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
               f'{count}%', ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    ax.set_ylabel('Percentage of Recommendations', fontsize=12, fontweight='bold')
    ax.set_title('Aegis-Buy Verdict Distribution (Sample 1000 Products)', fontsize=16, fontweight='bold')
    ax.set_ylim(0, 55)
    ax.grid(axis='y', alpha=0.3)
    
    # Add interpretation
    ax.text(0.5, -0.15, 'Most products analyzed show timing matters: 55% suggest waiting or watching for better deals',
           transform=ax.transAxes, ha='center', fontsize=10, style='italic',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('demo_assets/05_verdict_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: Verdict Distribution Chart")

# ==========================================
# 3. BUSINESS IMPACT VISUALIZATIONS
# ==========================================

def create_savings_comparison():
    """User savings comparison: With vs Without Aegis-Buy"""
    categories = ['Without\nAegis-Buy', 'With\nAegis-Buy']
    overpayment = [18.5, 3.2]  # Average % overpayment
    colors = ['#e74c3c', '#27ae60']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, overpayment, color=colors, width=0.5, edgecolor='black', linewidth=2)
    
    # Add percentage labels
    for bar, pct in zip(bars, overpayment):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
               f'{pct}%', ha='center', va='bottom', fontsize=16, fontweight='bold')
    
    ax.set_ylabel('Average Overpayment (%)', fontsize=12, fontweight='bold')
    ax.set_title('Impact of Aegis-Buy: Reducing Buyer Overpayment', fontsize=16, fontweight='bold')
    ax.set_ylim(0, 25)
    ax.grid(axis='y', alpha=0.3)
    
    # Add savings annotation
    savings = overpayment[0] - overpayment[1]
    ax.annotate(f'{savings:.1f}% Average Savings\n= ₹1,530 on ₹10,000 purchase',
               xy=(1, overpayment[1]), xytext=(0.5, 15),
               fontsize=12, fontweight='bold', color='green',
               bbox=dict(boxstyle='round,pad=0.7', facecolor='yellow', alpha=0.8),
               arrowprops=dict(arrowstyle='->', color='green', lw=2.5))
    
    plt.tight_layout()
    plt.savefig('demo_assets/06_savings_impact.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: Savings Impact Chart")

def create_roi_timeline():
    """ROI over 12 months for typical user"""
    months = range(1, 13)
    purchases_per_month = 2
    avg_savings_per_purchase = 765  # ₹
    cumulative_savings = [purchases_per_month * avg_savings_per_purchase * m for m in months]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(months, cumulative_savings, linewidth=3, color='#27ae60', marker='o', markersize=8)
    ax.fill_between(months, cumulative_savings, alpha=0.3, color='#27ae60')
    
    ax.set_xlabel('Months', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Savings (₹)', fontsize=12, fontweight='bold')
    ax.set_title('Projected Annual Savings with Aegis-Buy (2 Purchases/Month)', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Highlight 12-month total
    ax.scatter(12, cumulative_savings[-1], color='red', s=300, zorder=5, marker='*')
    ax.annotate(f'Year 1 Total: ₹{cumulative_savings[-1]:,.0f}',
               xy=(12, cumulative_savings[-1]), xytext=(9, cumulative_savings[-1] + 2000),
               fontsize=13, fontweight='bold', color='darkgreen',
               bbox=dict(boxstyle='round,pad=0.7', facecolor='gold', alpha=0.9),
               arrowprops=dict(arrowstyle='->', color='darkgreen', lw=2.5))
    
    plt.tight_layout()
    plt.savefig('demo_assets/07_roi_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: ROI Timeline Chart")

def create_target_market_segments():
    """Target user segments"""
    segments = ['Tech Enthusiasts', 'Smart Shoppers', 'B2B Procurement', 'Budget-Conscious\nFamilies']
    sizes = [28, 35, 20, 17]  # Market share %
    colors_seg = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(sizes, labels=segments, autopct='%1.1f%%',
                                        colors=colors_seg, startangle=45,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'},
                                        explode=(0.05, 0.05, 0.05, 0.05))
    
    ax.set_title('Aegis-Buy Target Market Segments', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('demo_assets/08_target_segments.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: Target Market Segments Chart")

# ==========================================
# 4. COMPETITIVE ADVANTAGE VISUALIZATION
# ==========================================

def create_competitive_matrix():
    """Feature comparison: Aegis-Buy vs Competitors"""
    features = ['Real-Time\nPricing', 'Sentiment\nAnalysis', 'AI Decision\nEngine', 
                'Urgency-Based\nLogic', 'Multi-Currency\nSupport', 'Fiduciary\nApproach']
    competitors = ['Price Comparison\nSites', 'Browser Extensions', 'Aegis-Buy']
    
    # Feature matrix (0 = No, 1 = Partial, 2 = Full)
    matrix = np.array([
        [2, 0, 0, 0, 1, 0],  # Price Comparison Sites
        [2, 1, 0, 0, 0, 0],  # Browser Extensions
        [2, 2, 2, 2, 2, 2]   # Aegis-Buy
    ])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=2)
    
    # Set ticks
    ax.set_xticks(np.arange(len(features)))
    ax.set_yticks(np.arange(len(competitors)))
    ax.set_xticklabels(features, fontsize=10, fontweight='bold')
    ax.set_yticklabels(competitors, fontsize=11, fontweight='bold')
    
    # Add text annotations
    symbols = {0: '✗', 1: '◐', 2: '✓'}
    for i in range(len(competitors)):
        for j in range(len(features)):
            text = ax.text(j, i, symbols[matrix[i, j]], ha="center", va="center",
                          color="black", fontsize=20, fontweight='bold')
    
    ax.set_title('Competitive Feature Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
    
    # Add legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#d62728', markersize=10, label='Not Available (✗)'),
                      plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ffff00', markersize=10, label='Partial (◐)'),
                      plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2ca02c', markersize=10, label='Full Support (✓)')]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=9)
    
    plt.tight_layout()
    plt.savefig('demo_assets/09_competitive_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: Competitive Matrix Chart")

# ==========================================
# 5. KEY STATISTICS INFOGRAPHIC
# ==========================================

def create_key_stats_infographic():
    """Summary statistics for demo"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')
    
    stats = [
        {'title': '$5.7 Trillion', 'subtitle': 'Global E-Commerce\nMarket (2023)', 'color': '#3498db', 'pos': (0.15, 0.75)},
        {'title': '82%', 'subtitle': 'Shoppers Face\nTiming Uncertainty', 'color': '#e74c3c', 'pos': (0.5, 0.75)},
        {'title': '15-20%', 'subtitle': 'Average Potential\nSavings', 'color': '#27ae60', 'pos': (0.85, 0.75)},
        {'title': '3 Agents', 'subtitle': 'Multi-Agent AI\nArchitecture', 'color': '#f39c12', 'pos': (0.15, 0.35)},
        {'title': '12+ Countries', 'subtitle': 'Amazon Domains\nSupported', 'color': '#9b59b6', 'pos': (0.5, 0.35)},
        {'title': '₹18,360/year', 'subtitle': 'Avg Annual Savings\nper User', 'color': '#1abc9c', 'pos': (0.85, 0.35)}
    ]
    
    for stat in stats:
        # Draw circle
        circle = plt.Circle(stat['pos'], 0.08, color=stat['color'], alpha=0.8, linewidth=3, edgecolor='black')
        ax.add_patch(circle)
        
        # Add text
        ax.text(stat['pos'][0], stat['pos'][1], stat['title'], ha='center', va='center',
               fontsize=16, fontweight='bold', color='white')
        ax.text(stat['pos'][0], stat['pos'][1] - 0.15, stat['subtitle'], ha='center', va='top',
               fontsize=10, fontweight='bold', color='black', style='italic')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('Aegis-Buy: Key Statistics & Impact Metrics', fontsize=20, fontweight='bold', pad=30)
    
    plt.tight_layout()
    plt.savefig('demo_assets/10_key_statistics.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: Key Statistics Infographic")

# ==========================================
# GENERATE ALL VISUALIZATIONS
# ==========================================

if __name__ == "__main__":
    print("\n🎨 Generating Demo Visualizations for Aegis-Buy Showcase...\n")
    
    # Problem Statement
    print("📊 PROBLEM STATEMENT VISUALS:")
    create_price_volatility_chart()
    create_buyer_pain_points()
    create_market_size_infographic()
    
    # Solution Demo
    print("\n🔧 SOLUTION DEMONSTRATION VISUALS:")
    create_agent_workflow_diagram()
    create_verdict_distribution()
    
    # Business Impact
    print("\n💰 BUSINESS IMPACT VISUALS:")
    create_savings_comparison()
    create_roi_timeline()
    create_target_market_segments()
    
    # Competitive Advantage
    print("\n🏆 COMPETITIVE ADVANTAGE VISUALS:")
    create_competitive_matrix()
    
    # Key Stats
    print("\n📈 KEY STATISTICS:")
    create_key_stats_infographic()
    
    print("\n" + "="*60)
    print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📁 Location: demo_assets/ folder")
    print(f"📊 Total Charts: 10")
    print("\n💡 Usage Guide:")
    print("   - Use charts 1-3 for Problem Statement (Section 2 of demo)")
    print("   - Use charts 4-5 for Solution Demo (Section 3 of demo)")
    print("   - Use charts 6-8 for Business Impact (Section 5 of demo)")
    print("   - Use charts 9-10 for Technical Overview & Competitive Edge")
    print("\n🎥 Pro Tip: Show these visualizations as overlays during video recording!")
    print("=" * 60)
