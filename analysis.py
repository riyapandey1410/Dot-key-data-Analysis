"""
Dot & Key D2C Brand — Business Analyst Report
Revenue Growth, Pricing & Channel Analysis | FY 2021-22 to FY 2023-24
Analyst: [Your Name]
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings, os
warnings.filterwarnings('ignore')

# ── Brand palette (matches Dot & Key visual identity) ──────────────────────
CORAL   = '#E8604A'
TEAL    = '#3A9E8F'
YELLOW  = '#F5C842'
NAVY    = '#1C2B3A'
PINK    = '#E8799A'
LAVENDER= '#9B82C2'
SAGE    = '#7BAE8E'
LIGHT   = '#FAF6F2'
GREY    = '#64748B'
WHITE   = '#FFFFFF'

FY_COLORS = {'FY21-22': '#9B82C2', 'FY22-23': '#3A9E8F', 'FY23-24': '#E8604A'}
CAT_COLORS = [CORAL, TEAL, YELLOW, PINK, LAVENDER]
CHAN_COLORS = ['#E8604A', '#3A9E8F', '#F5C842', '#E8799A', '#9B82C2']

plt.rcParams.update({
    'font.family':        'DejaVu Sans',
    'axes.facecolor':     LIGHT,
    'figure.facecolor':   WHITE,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.grid':          True,
    'grid.color':         '#E2E8F0',
    'grid.linewidth':     0.6,
    'axes.labelcolor':    NAVY,
    'xtick.color':        GREY,
    'ytick.color':        GREY,
    'figure.dpi':         150,
})

OUT = '/home/claude/dotandkey/outputs'
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv('/home/claude/dotandkey/data/dotandkey_orders.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

FYS = ['FY21-22', 'FY22-23', 'FY23-24']

def cr(val):
    return f"₹{val/1e7:.2f} Cr"

def lakh(val):
    return f"₹{val/1e5:.1f}L"


# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 — 3-YEAR REVENUE GROWTH OVERVIEW (Hero slide)
# ══════════════════════════════════════════════════════════════════════════════
fy_summary = df.groupby('fiscal_year').agg(
    Orders=('order_id', 'count'),
    GMV=('gmv', 'sum'),
    Net_Revenue=('net_revenue', 'sum'),
    Gross_Profit=('gross_profit', 'sum'),
    Discount_Total=('discount_amount', 'sum'),
    Marketing_Cost=('marketing_cost', 'sum'),
).reindex(FYS)
fy_summary['GP_Margin']       = (fy_summary['Gross_Profit'] / fy_summary['Net_Revenue'] * 100).round(1)
fy_summary['Discount_Leakage']= (fy_summary['Discount_Total'] / fy_summary['GMV'] * 100).round(1)
fy_summary['Revenue_Growth']  = fy_summary['Net_Revenue'].pct_change() * 100

fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor(WHITE)
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38)

ax_main = fig.add_subplot(gs[0, :2])
ax_gp   = fig.add_subplot(gs[0, 2])
ax_ord  = fig.add_subplot(gs[1, 0])
ax_aov  = fig.add_subplot(gs[1, 1])
ax_leak = fig.add_subplot(gs[1, 2])

# ── Main: GMV vs Net Revenue vs Gross Profit bars ──
x = np.arange(3)
w = 0.26
bars1 = ax_main.bar(x - w,  fy_summary['GMV']/1e7,          width=w, color=NAVY,    label='GMV',          alpha=0.85)
bars2 = ax_main.bar(x,      fy_summary['Net_Revenue']/1e7,   width=w, color=TEAL,    label='Net Revenue',  alpha=0.90)
bars3 = ax_main.bar(x + w,  fy_summary['Gross_Profit']/1e7,  width=w, color=CORAL,   label='Gross Profit', alpha=0.90)

for bars, vals in [(bars1, fy_summary['GMV']), (bars2, fy_summary['Net_Revenue']), (bars3, fy_summary['Gross_Profit'])]:
    for bar, v in zip(bars, vals):
        ax_main.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                     f'₹{v/1e7:.2f}Cr', ha='center', fontsize=8.5, fontweight='bold', color=NAVY)

ax_main.set_xticks(x)
ax_main.set_xticklabels(FYS, fontsize=12, fontweight='bold')
ax_main.set_ylabel('₹ Crore', fontsize=11)
ax_main.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v:.0f}Cr'))
ax_main.legend(fontsize=10, loc='upper left')
ax_main.set_title('Dot & Key: 3-Year Revenue Growth (FY 2021–2024)', fontsize=14, fontweight='bold', color=NAVY, pad=10)

# Growth badge
for i, (fy, row) in enumerate(fy_summary.iterrows()):
    if i > 0:
        g = row['Revenue_Growth']
        ax_main.annotate(f'+{g:.0f}%', xy=(i, row['Net_Revenue']/1e7 + 0.25),
                         fontsize=12, fontweight='bold', color=SAGE, ha='center')

# ── GP Margin trend ──
bars_gp = ax_gp.bar(FYS, fy_summary['GP_Margin'], color=[FY_COLORS[f] for f in FYS], edgecolor='white', width=0.5)
for bar, v in zip(bars_gp, fy_summary['GP_Margin']):
    ax_gp.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{v}%', ha='center', fontsize=11, fontweight='bold', color=NAVY)
ax_gp.set_title('Gross Profit Margin', fontsize=12, fontweight='bold', color=NAVY)
ax_gp.set_ylim(0, 60)
ax_gp.set_ylabel('%', fontsize=10)
ax_gp.tick_params(axis='x', labelsize=9)

# ── Order volume ──
ax_ord.bar(FYS, fy_summary['Orders']/1000, color=[FY_COLORS[f] for f in FYS], edgecolor='white', width=0.5)
for i, (fy, v) in enumerate(fy_summary['Orders'].items()):
    ax_ord.text(i, v/1000+0.8, f'{v/1000:.0f}K', ha='center', fontsize=10, fontweight='bold', color=NAVY)
ax_ord.set_title('Total Orders (\'000)', fontsize=12, fontweight='bold', color=NAVY)
ax_ord.set_ylabel("Orders ('000)", fontsize=10)
ax_ord.tick_params(axis='x', labelsize=9)

# ── AOV ──
aov = fy_summary['Net_Revenue'] / fy_summary['Orders']
ax_aov.plot(FYS, aov, marker='o', color=CORAL, linewidth=3, markersize=10)
for i, (fy, v) in enumerate(aov.items()):
    ax_aov.text(i, v+3, f'₹{v:.0f}', ha='center', fontsize=10, fontweight='bold', color=NAVY)
ax_aov.set_title('Avg Order Value (₹)', fontsize=12, fontweight='bold', color=NAVY)
ax_aov.set_ylabel('₹', fontsize=10)
ax_aov.set_ylim(aov.min()-30, aov.max()+30)
ax_aov.tick_params(axis='x', labelsize=9)

# ── Discount leakage ──
ax_leak.bar(FYS, fy_summary['Discount_Leakage'], color=[FY_COLORS[f] for f in FYS], edgecolor='white', width=0.5)
for i, (fy, v) in enumerate(fy_summary['Discount_Leakage'].items()):
    ax_leak.text(i, v+0.2, f'{v}%', ha='center', fontsize=10, fontweight='bold', color=NAVY)
ax_leak.set_title('Discount Leakage % of GMV', fontsize=12, fontweight='bold', color=NAVY)
ax_leak.set_ylabel('% of GMV', fontsize=10)
ax_leak.axhline(14, color=CORAL, linestyle='--', alpha=0.5, linewidth=1.2)
ax_leak.tick_params(axis='x', labelsize=9)

fig.suptitle('Dot & Key D2C Brand — Executive Revenue Dashboard | FY 2021–2024',
             fontsize=16, fontweight='bold', color=NAVY, y=1.01)
plt.savefig(f'{OUT}/01_revenue_growth_overview.png', bbox_inches='tight', facecolor=WHITE)
plt.close()
print("✓ Chart 1 — Revenue Growth Overview")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 2 — MONTHLY REVENUE TREND (seasonality & YoY comparison)
# ══════════════════════════════════════════════════════════════════════════════
# Map calendar month to fiscal month (Apr=1 ... Mar=12)
df['fiscal_month'] = ((df['month'] - 4) % 12) + 1
FMONTH_LABELS = ['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar']

monthly = df.groupby(['fiscal_year','fiscal_month'])['net_revenue'].sum().reset_index()
monthly['net_rev_lakh'] = monthly['net_revenue'] / 1e5

fig, axes = plt.subplots(2, 1, figsize=(15, 9), facecolor=WHITE)

# Top: Line chart YoY
ax = axes[0]
for fy, color in FY_COLORS.items():
    sub = monthly[monthly['fiscal_year']==fy].sort_values('fiscal_month')
    ax.plot(sub['fiscal_month'], sub['net_rev_lakh'], marker='o', color=color,
            linewidth=2.5, markersize=6, label=fy)
    # Shade area under curve
    ax.fill_between(sub['fiscal_month'], sub['net_rev_lakh'], alpha=0.08, color=color)

ax.set_xticks(range(1, 13))
ax.set_xticklabels(FMONTH_LABELS, fontsize=11)
ax.set_ylabel('Net Revenue (₹ Lakhs)', fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v:.0f}L'))
ax.legend(fontsize=11)
ax.set_title('Monthly Net Revenue Trend — YoY Comparison (Fiscal Year Apr–Mar)', fontsize=13, fontweight='bold', color=NAVY)

# Annotations for peaks
for fy, color in FY_COLORS.items():
    sub = monthly[monthly['fiscal_year']==fy].sort_values('fiscal_month')
    peak_row = sub.loc[sub['net_rev_lakh'].idxmax()]
    ax.annotate(f"Peak\n₹{peak_row['net_rev_lakh']:.0f}L",
                xy=(peak_row['fiscal_month'], peak_row['net_rev_lakh']),
                xytext=(peak_row['fiscal_month']+0.3, peak_row['net_rev_lakh']+15),
                fontsize=8.5, color=color, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=color, lw=1.2))

# Festive season shading
ax.axvspan(6.5, 9.5, alpha=0.07, color=YELLOW, label='Festive Season')
ax.text(7.5, ax.get_ylim()[1]*0.85, '🎉 Festive\nSeason', fontsize=9, color='#B8860B', ha='center')

# Bottom: MoM growth rate for FY23-24 (most recent year)
ax2 = axes[1]
sub24 = monthly[monthly['fiscal_year']=='FY23-24'].sort_values('fiscal_month').copy()
sub23 = monthly[monthly['fiscal_year']=='FY22-23'].sort_values('fiscal_month').set_index('fiscal_month')['net_rev_lakh']
sub24['yoy_growth'] = sub24.apply(lambda r: (r['net_rev_lakh'] / sub23.get(r['fiscal_month'], np.nan) - 1)*100, axis=1)

bar_colors = [TEAL if v >= 0 else CORAL for v in sub24['yoy_growth']]
bars = ax2.bar(sub24['fiscal_month'], sub24['yoy_growth'], color=bar_colors, edgecolor='white', width=0.7)
ax2.axhline(0, color=NAVY, linewidth=1.2)
ax2.axhline(sub24['yoy_growth'].mean(), color=GREY, linewidth=1, linestyle='--', alpha=0.6)
for bar, v in zip(bars, sub24['yoy_growth']):
    ax2.text(bar.get_x()+bar.get_width()/2,
             bar.get_height()+(1 if v>=0 else -3.5),
             f'{v:.0f}%', ha='center', fontsize=9, fontweight='bold',
             color=TEAL if v>=0 else CORAL)
ax2.set_xticks(range(1,13))
ax2.set_xticklabels(FMONTH_LABELS, fontsize=11)
ax2.set_ylabel('YoY Growth %', fontsize=11)
ax2.set_title('FY 2023-24 vs FY 2022-23 — Month-on-Month Revenue Growth (%)', fontsize=13, fontweight='bold', color=NAVY)
ax2.text(11.5, sub24['yoy_growth'].mean()+1, f'Avg: {sub24["yoy_growth"].mean():.0f}%', fontsize=9, color=GREY)

fig.tight_layout(pad=2)
plt.savefig(f'{OUT}/02_monthly_seasonality_yoy.png', bbox_inches='tight', facecolor=WHITE)
plt.close()
print("✓ Chart 2 — Monthly Seasonality & YoY")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 3 — CATEGORY ANALYSIS (Revenue, Margin, Growth)
# ══════════════════════════════════════════════════════════════════════════════
cats = df['category'].unique()
cat_fy = df.groupby(['fiscal_year','category']).agg(
    Net_Revenue=('net_revenue','sum'),
    GP=('gross_profit','sum'),
    Orders=('order_id','count'),
    Avg_Disc=('discount_pct','mean'),
).reset_index()
cat_fy['GP_Margin'] = (cat_fy['GP'] / cat_fy['Net_Revenue'] * 100).round(1)

fig, axes = plt.subplots(1, 3, figsize=(17, 6), facecolor=WHITE)

# Left: Stacked bar revenue by category per FY
cat_pivot = cat_fy.pivot(index='fiscal_year', columns='category', values='Net_Revenue').reindex(FYS).fillna(0)
cat_pivot_cr = cat_pivot / 1e7
cat_pivot_cr.plot(kind='bar', stacked=True, ax=axes[0],
                  color=CAT_COLORS, edgecolor='white', width=0.55)
axes[0].set_xticklabels(FYS, rotation=0, fontsize=11)
axes[0].set_ylabel('Net Revenue (₹ Cr)', fontsize=11)
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v:.1f}Cr'))
axes[0].set_title('Revenue by Category per FY\n(Stacked)', fontsize=12, fontweight='bold', color=NAVY)
axes[0].legend(fontsize=8.5, bbox_to_anchor=(1,1), title='Category')
axes[0].set_xlabel('')

# Middle: Category GP Margin across FYs
cat_margin = cat_fy.pivot(index='category', columns='fiscal_year', values='GP_Margin').fillna(0)
cat_margin = cat_margin.sort_values('FY23-24', ascending=True)
x = np.arange(len(cat_margin))
w = 0.26
for i, (fy, color) in enumerate(FY_COLORS.items()):
    axes[1].barh(x + (i-1)*w, cat_margin[fy], height=w, color=color, label=fy, edgecolor='white')
axes[1].set_yticks(x)
axes[1].set_yticklabels(cat_margin.index, fontsize=10)
axes[1].set_xlabel('Gross Profit Margin (%)', fontsize=11)
axes[1].set_title('GP Margin by Category\n(Across FYs)', fontsize=12, fontweight='bold', color=NAVY)
axes[1].legend(fontsize=10)
axes[1].axvline(42, color=CORAL, linestyle='--', alpha=0.5, linewidth=1.2)
axes[1].text(42.2, -0.5, 'Target\n42%', fontsize=8, color=CORAL)

# Right: Category growth FY21→FY24
cat23 = cat_fy[cat_fy['fiscal_year']=='FY21-22'].set_index('category')['Net_Revenue']
cat24 = cat_fy[cat_fy['fiscal_year']=='FY23-24'].set_index('category')['Net_Revenue']
growth = ((cat24 / cat23) - 1) * 100
growth = growth.sort_values(ascending=True)
bar_c = [TEAL if v > 80 else CORAL for v in growth]
bars = axes[2].barh(growth.index, growth.values, color=bar_c, edgecolor='white')
for bar, v in zip(bars, growth.values):
    axes[2].text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
                 f'+{v:.0f}%', va='center', fontsize=11, fontweight='bold', color=NAVY)
axes[2].set_xlabel('Revenue Growth FY21-22 → FY23-24 (%)', fontsize=11)
axes[2].set_title('3-Year Category Growth\n(FY21-22 → FY23-24)', fontsize=12, fontweight='bold', color=NAVY)
axes[2].set_xlim(0, growth.max() + 40)

fig.suptitle('Category Performance Analysis — Revenue, Margin & Growth', fontsize=14, fontweight='bold', color=NAVY, y=1.01)
fig.tight_layout()
plt.savefig(f'{OUT}/03_category_analysis.png', bbox_inches='tight', facecolor=WHITE)
plt.close()
print("✓ Chart 3 — Category Analysis")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 4 — CHANNEL STRATEGY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
chan_fy = df.groupby(['fiscal_year','channel']).agg(
    Net_Revenue=('net_revenue','sum'),
    GMV=('gmv','sum'),
    GP=('gross_profit','sum'),
    Disc=('discount_amount','sum'),
    Orders=('order_id','count'),
    Mktg=('marketing_cost','sum'),
    Returns=('is_returned','mean'),
).reset_index()
chan_fy['GP_Margin']   = (chan_fy['GP'] / chan_fy['Net_Revenue'] * 100).round(1)
chan_fy['Disc_Pct']    = (chan_fy['Disc'] / chan_fy['GMV'] * 100).round(1)
chan_fy['ROI']         = ((chan_fy['GP'] - chan_fy['Mktg']) / chan_fy['Mktg'] * 100).round(1)

chan_latest = chan_fy[chan_fy['fiscal_year']=='FY23-24'].sort_values('Net_Revenue', ascending=False)

fig, axes = plt.subplots(2, 2, figsize=(15, 10), facecolor=WHITE)

# Top-left: Revenue share pie
wedge_colors = CHAN_COLORS
wedges, texts, autotexts = axes[0,0].pie(
    chan_latest['Net_Revenue'], labels=chan_latest['channel'],
    colors=wedge_colors, autopct='%1.1f%%', startangle=140,
    wedgeprops={'edgecolor':'white','linewidth':2},
    pctdistance=0.78, labeldistance=1.08
)
for t in autotexts: t.set_fontsize(10); t.set_fontweight('bold')
axes[0,0].set_title('Channel Revenue Share\n(FY 2023-24)', fontsize=12, fontweight='bold', color=NAVY)

# Top-right: Channel revenue growth across 3 FYs
chan_pivot = chan_fy.pivot(index='channel', columns='fiscal_year', values='Net_Revenue').fillna(0)
chan_pivot = chan_pivot.reindex(columns=FYS)
chan_pivot_lakh = chan_pivot / 1e5
x = np.arange(len(chan_pivot))
w = 0.26
for i, (fy, color) in enumerate(FY_COLORS.items()):
    bars = axes[0,1].bar(x + (i-1)*w, chan_pivot_lakh[fy], width=w, color=color, label=fy, edgecolor='white', alpha=0.9)
axes[0,1].set_xticks(x)
axes[0,1].set_xticklabels(chan_pivot.index, rotation=15, ha='right', fontsize=10)
axes[0,1].set_ylabel('Net Revenue (₹ Lakhs)', fontsize=11)
axes[0,1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v:.0f}L'))
axes[0,1].legend(fontsize=10)
axes[0,1].set_title('Channel Revenue Growth — FY 2021–2024', fontsize=12, fontweight='bold', color=NAVY)

# Bottom-left: Discount leakage vs GP Margin scatter
sc = axes[1,0].scatter(chan_latest['Disc_Pct'], chan_latest['GP_Margin'],
                        s=chan_latest['Net_Revenue']/8000,
                        c=CHAN_COLORS, edgecolors='white', linewidths=2, zorder=5)
for _, row in chan_latest.iterrows():
    axes[1,0].annotate(row['channel'],
                       (row['Disc_Pct']+0.3, row['GP_Margin']+0.3),
                       fontsize=10, color=NAVY)
axes[1,0].set_xlabel('Discount Leakage (% of GMV)', fontsize=11)
axes[1,0].set_ylabel('Gross Profit Margin (%)', fontsize=11)
axes[1,0].set_title('Discount vs Margin by Channel\n(bubble = revenue size | FY23-24)', fontsize=12, fontweight='bold', color=NAVY)
axes[1,0].axhline(chan_latest['GP_Margin'].mean(), color=GREY, linestyle='--', alpha=0.5)

# Bottom-right: Return rate & Marketing ROI
ax_r = axes[1,1]
x2 = np.arange(len(chan_latest))
bars_roi = ax_r.bar(x2, chan_latest['ROI'], color=[FY_COLORS['FY23-24']]*5, edgecolor='white', alpha=0.8, label='Marketing ROI %')
ax_r2 = ax_r.twinx()
ax_r2.plot(x2, chan_latest['Returns']*100, marker='s', color=CORAL, linewidth=2.5,
           markersize=9, label='Return Rate %', zorder=5)
ax_r.set_xticks(x2)
ax_r.set_xticklabels(chan_latest['channel'], rotation=15, ha='right', fontsize=10)
ax_r.set_ylabel('Marketing ROI (%)', fontsize=11)
ax_r2.set_ylabel('Return Rate (%)', fontsize=11, color=CORAL)
ax_r2.tick_params(axis='y', colors=CORAL)
ax_r2.spines['right'].set_visible(True); ax_r2.spines['right'].set_color(CORAL)
for bar, v in zip(bars_roi, chan_latest['ROI']):
    ax_r.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2, f'{v:.0f}%', ha='center', fontsize=9.5, fontweight='bold', color=NAVY)
lines1, labels1 = ax_r.get_legend_handles_labels()
lines2, labels2 = ax_r2.get_legend_handles_labels()
ax_r.legend(lines1+lines2, labels1+labels2, fontsize=9, loc='upper right')
ax_r.set_title('Marketing ROI vs Return Rate by Channel\n(FY 2023-24)', fontsize=12, fontweight='bold', color=NAVY)

fig.suptitle('Channel Strategy Analysis — Revenue, Discount & Profitability', fontsize=14, fontweight='bold', color=NAVY, y=1.01)
fig.tight_layout()
plt.savefig(f'{OUT}/04_channel_strategy.png', bbox_inches='tight', facecolor=WHITE)
plt.close()
print("✓ Chart 4 — Channel Strategy")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 5 — CUSTOMER COHORT & RETENTION ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
cust_fy = df.groupby(['fiscal_year','customer_type']).agg(
    Orders=('order_id','count'),
    Revenue=('net_revenue','sum'),
    AOV=('net_revenue','mean'),
    GP=('gross_profit','sum'),
).reset_index()
cust_fy['GP_Margin'] = (cust_fy['GP'] / cust_fy['Revenue'] * 100).round(1)

fig, axes = plt.subplots(1, 3, figsize=(16, 6), facecolor=WHITE)

# Left: Revenue mix by customer type per FY
cust_pivot = cust_fy.pivot(index='fiscal_year', columns='customer_type', values='Revenue').reindex(FYS).fillna(0)
cust_pct = cust_pivot.div(cust_pivot.sum(axis=1), axis=0) * 100
ctype_colors = {'New': CORAL, 'Repeat': TEAL, 'Loyal': YELLOW}
bottom = np.zeros(3)
for ctype, color in ctype_colors.items():
    vals = cust_pct[ctype].values
    bars = axes[0].bar(FYS, vals, bottom=bottom, color=color, label=ctype, edgecolor='white', width=0.55)
    for bar, v, b in zip(bars, vals, bottom):
        if v > 5:
            axes[0].text(bar.get_x()+bar.get_width()/2, b+v/2, f'{v:.0f}%',
                         ha='center', va='center', fontsize=11, fontweight='bold', color=NAVY)
    bottom += vals
axes[0].set_ylim(0, 110)
axes[0].set_ylabel('Revenue Share (%)', fontsize=11)
axes[0].set_title('Revenue Mix by Customer Type\n(New vs Repeat vs Loyal)', fontsize=12, fontweight='bold', color=NAVY)
axes[0].legend(fontsize=10)
axes[0].tick_params(axis='x', labelsize=11)

# Middle: AOV by customer type and FY
aov_pivot = cust_fy.pivot(index='customer_type', columns='fiscal_year', values='AOV').fillna(0)
x = np.arange(3)
w = 0.26
for i, (fy, color) in enumerate(FY_COLORS.items()):
    axes[1].bar(x+(i-1)*w, aov_pivot[fy], width=w, color=color, label=fy, edgecolor='white', alpha=0.9)
axes[1].set_xticks(x)
axes[1].set_xticklabels(['Loyal','New','Repeat'], fontsize=11)
axes[1].set_ylabel('Avg Order Value (₹)', fontsize=11)
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v:.0f}'))
axes[1].set_title('AOV by Customer Type — YoY\n(Loyal customers spend most)', fontsize=12, fontweight='bold', color=NAVY)
axes[1].legend(fontsize=10)

# Right: Loyal customer revenue growth
loyal_rev = cust_fy[cust_fy['customer_type']=='Loyal'].set_index('fiscal_year')['Revenue'].reindex(FYS)
repeat_rev = cust_fy[cust_fy['customer_type']=='Repeat'].set_index('fiscal_year')['Revenue'].reindex(FYS)
new_rev    = cust_fy[cust_fy['customer_type']=='New'].set_index('fiscal_year')['Revenue'].reindex(FYS)
axes[2].plot(FYS, loyal_rev/1e5,  marker='o', color=YELLOW,  linewidth=3, markersize=10, label='Loyal')
axes[2].plot(FYS, repeat_rev/1e5, marker='s', color=TEAL,    linewidth=3, markersize=10, label='Repeat')
axes[2].plot(FYS, new_rev/1e5,    marker='^', color=CORAL,   linewidth=3, markersize=10, label='New')
axes[2].fill_between(FYS, loyal_rev/1e5,  alpha=0.1, color=YELLOW)
axes[2].fill_between(FYS, repeat_rev/1e5, alpha=0.08, color=TEAL)
axes[2].fill_between(FYS, new_rev/1e5,    alpha=0.08, color=CORAL)
axes[2].set_ylabel('Net Revenue (₹ Lakhs)', fontsize=11)
axes[2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v:.0f}L'))
axes[2].set_title('Revenue Growth by Customer Segment\n(Repeat & Loyal = Retention Quality)', fontsize=12, fontweight='bold', color=NAVY)
axes[2].legend(fontsize=10)
axes[2].tick_params(axis='x', labelsize=11)

fig.suptitle('Customer Retention & LTV Analysis — FY 2021–2024', fontsize=14, fontweight='bold', color=NAVY, y=1.01)
fig.tight_layout()
plt.savefig(f'{OUT}/05_customer_retention.png', bbox_inches='tight', facecolor=WHITE)
plt.close()
print("✓ Chart 5 — Customer Retention")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 6 — DISCOUNT EFFICIENCY & PRICING SWEET SPOT
# ══════════════════════════════════════════════════════════════════════════════
bins   = [0, 5, 10, 15, 20, 25, 100]
labels = ['0–5%','5–10%','10–15%','15–20%','20–25%','25%+']
df['disc_band'] = pd.cut(df['discount_pct'], bins=bins, labels=labels, right=True)

band_fy = df.groupby(['fiscal_year','disc_band'], observed=True).agg(
    Orders=('order_id','count'),
    Revenue=('net_revenue','sum'),
    GP=('gross_profit','sum'),
    AOV=('net_revenue','mean'),
).reset_index()
band_fy['GP_Margin'] = (band_fy['GP'] / band_fy['Revenue'] * 100).round(1)

# Overall band summary
band_all = df.groupby('disc_band', observed=True).agg(
    Orders=('order_id','count'),
    Revenue=('net_revenue','sum'),
    GP=('gross_profit','sum'),
    AOV=('net_revenue','mean'),
    Disc_Amt=('discount_amount','sum'),
).reset_index()
band_all['GP_Margin']    = (band_all['GP'] / band_all['Revenue'] * 100).round(1)
band_all['Rev_Share']    = (band_all['Revenue'] / band_all['Revenue'].sum() * 100).round(1)

fig, axes = plt.subplots(1, 3, figsize=(17, 6), facecolor=WHITE)

# Left: Volume vs Revenue share per band
ax2t = axes[0].twinx()
bar_c = [TEAL if i < 2 else (YELLOW if i == 2 else CORAL) for i in range(len(band_all))]
bars = axes[0].bar(band_all['disc_band'], band_all['Orders']/1000, color=bar_c, edgecolor='white', alpha=0.85)
ax2t.plot(band_all['disc_band'], band_all['Rev_Share'], color=NAVY, marker='D', linewidth=2.5, markersize=8, label='Revenue Share %')
axes[0].set_ylabel("Orders ('000)", fontsize=11)
ax2t.set_ylabel('Revenue Share (%)', fontsize=11, color=NAVY)
for bar, n in zip(bars, band_all['Orders']):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{n/1000:.0f}K', ha='center', fontsize=9.5)
axes[0].set_title('Order Volume & Revenue Share\nby Discount Band', fontsize=12, fontweight='bold', color=NAVY)
axes[0].set_xlabel('Discount Band', fontsize=11)
green_patch = mpatches.Patch(color=TEAL, label='Healthy Zone')
red_patch   = mpatches.Patch(color=CORAL, label='Over-discounting')
axes[0].legend(handles=[green_patch, red_patch], fontsize=9)

# Middle: GP Margin per band
grad_colors = [TEAL, TEAL, YELLOW, YELLOW, CORAL, CORAL]
bars2 = axes[1].bar(band_all['disc_band'], band_all['GP_Margin'], color=grad_colors, edgecolor='white')
for bar, v, aov in zip(bars2, band_all['GP_Margin'], band_all['AOV']):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                 f'{v:.1f}%\nAOV ₹{aov:.0f}', ha='center', fontsize=9.5, fontweight='bold', color=NAVY)
axes[1].set_ylabel('Gross Profit Margin (%)', fontsize=11)
axes[1].set_title('GP Margin & AOV by Discount Band\n(Sweet spot: 5–15%)', fontsize=12, fontweight='bold', color=NAVY)
axes[1].axhline(band_all['GP_Margin'].mean(), color=GREY, linestyle='--', alpha=0.6, label=f'Avg {band_all["GP_Margin"].mean():.1f}%')
axes[1].legend(fontsize=9)
axes[1].set_ylim(0, band_all['GP_Margin'].max()+12)
axes[1].set_xlabel('Discount Band', fontsize=11)

# Right: Band GP Margin trend across FYs (shows disciplined pricing?)
band_margin_fy = band_fy.pivot(index='disc_band', columns='fiscal_year', values='GP_Margin').fillna(0)
for fy, color in FY_COLORS.items():
    if fy in band_margin_fy.columns:
        axes[2].plot(range(len(band_margin_fy)), band_margin_fy[fy],
                     marker='o', color=color, linewidth=2.5, markersize=8, label=fy)
axes[2].set_xticks(range(len(labels)))
axes[2].set_xticklabels(labels, rotation=15, ha='right', fontsize=10)
axes[2].set_ylabel('Gross Profit Margin (%)', fontsize=11)
axes[2].set_title('GP Margin per Discount Band — YoY\n(Is pricing discipline improving?)', fontsize=12, fontweight='bold', color=NAVY)
axes[2].legend(fontsize=10)

fig.suptitle('Discount Efficiency & Pricing Sweet Spot Analysis', fontsize=14, fontweight='bold', color=NAVY, y=1.01)
fig.tight_layout()
plt.savefig(f'{OUT}/06_discount_pricing_analysis.png', bbox_inches='tight', facecolor=WHITE)
plt.close()
print("✓ Chart 6 — Discount & Pricing")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 7 — GEOGRAPHIC PERFORMANCE HEATMAP
# ══════════════════════════════════════════════════════════════════════════════
city_fy = df.groupby(['fiscal_year','city']).agg(
    Revenue=('net_revenue','sum'),
    Orders=('order_id','count'),
    GP=('gross_profit','sum'),
).reset_index()
city_fy['GP_Margin'] = (city_fy['GP'] / city_fy['Revenue'] * 100).round(1)
city_fy['AOV']       = (city_fy['Revenue'] / city_fy['Orders']).round(0)

pivot_rev = city_fy.pivot(index='city', columns='fiscal_year', values='Revenue').fillna(0)
pivot_rev = pivot_rev.reindex(columns=FYS)
# Sort by total revenue
pivot_rev['total'] = pivot_rev.sum(axis=1)
pivot_rev = pivot_rev.sort_values('total', ascending=False).drop(columns='total')
pivot_lakh = pivot_rev / 1e5

pivot_gp = city_fy.pivot(index='city', columns='fiscal_year', values='GP_Margin').reindex(pivot_rev.index).fillna(0)

fig, axes = plt.subplots(1, 2, figsize=(15, 6), facecolor=WHITE)

sns.heatmap(pivot_lakh, annot=True, fmt='.0f', cmap='YlOrRd',
            linewidths=0.5, ax=axes[0],
            cbar_kws={'label': 'Net Revenue (₹ Lakhs)', 'shrink': 0.8},
            annot_kws={'size': 11, 'weight': 'bold'})
axes[0].set_title('City Revenue Heatmap (₹ Lakhs)\nFY 2021–2024', fontsize=13, fontweight='bold', color=NAVY)
axes[0].set_ylabel('City', fontsize=11)
axes[0].set_xlabel('Fiscal Year', fontsize=11)
axes[0].tick_params(axis='x', rotation=0)

sns.heatmap(pivot_gp, annot=True, fmt='.1f', cmap='RdYlGn',
            linewidths=0.5, ax=axes[1],
            cbar_kws={'label': 'Gross Profit Margin (%)', 'shrink': 0.8},
            annot_kws={'size': 11, 'weight': 'bold'})
axes[1].set_title('City GP Margin Heatmap (%)\nFY 2021–2024', fontsize=13, fontweight='bold', color=NAVY)
axes[1].set_ylabel('')
axes[1].set_xlabel('Fiscal Year', fontsize=11)
axes[1].tick_params(axis='x', rotation=0)

fig.suptitle('Geographic Performance: Revenue & Margin Across Cities', fontsize=14, fontweight='bold', color=NAVY, y=1.01)
fig.tight_layout()
plt.savefig(f'{OUT}/07_geo_heatmap.png', bbox_inches='tight', facecolor=WHITE)
plt.close()
print("✓ Chart 7 — Geographic Heatmap")


# ══════════════════════════════════════════════════════════════════════════════
# PRINT FULL SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("   DOT & KEY — BUSINESS ANALYSIS SUMMARY")
print("═"*60)
for fy in FYS:
    row = fy_summary.loc[fy]
    print(f"\n  {fy}")
    print(f"    Orders       : {row['Orders']:,.0f}")
    print(f"    GMV          : {cr(row['GMV'])}")
    print(f"    Net Revenue  : {cr(row['Net_Revenue'])}")
    print(f"    Gross Profit : {cr(row['Gross_Profit'])} ({row['GP_Margin']}% margin)")
    print(f"    Disc Leakage : {row['Discount_Leakage']}% of GMV")

rev_cagr = ((fy_summary.loc['FY23-24','Net_Revenue'] / fy_summary.loc['FY21-22','Net_Revenue'])**0.5 - 1)*100
ord_cagr = ((fy_summary.loc['FY23-24','Orders'] / fy_summary.loc['FY21-22','Orders'])**0.5 - 1)*100
print(f"\n  Revenue CAGR (2Y): {rev_cagr:.1f}%")
print(f"  Order CAGR  (2Y): {ord_cagr:.1f}%")
print(f"\n  Top category (FY23-24): {df[df['fiscal_year']=='FY23-24'].groupby('category')['net_revenue'].sum().idxmax()}")
print(f"  Top city (FY23-24)    : {df[df['fiscal_year']=='FY23-24'].groupby('city')['net_revenue'].sum().idxmax()}")
print(f"  Best margin channel   : {chan_latest.sort_values('GP_Margin',ascending=False).iloc[0]['channel']}")
print("═"*60)
print("\n✅  All 7 charts saved to outputs/")
