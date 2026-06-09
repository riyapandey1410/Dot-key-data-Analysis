"""
Dot & Key – Realistic D2C Dataset Generator
FY 2021-22 to FY 2023-24 (3 full years)
Reflects real brand growth trajectory & product mix
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random, os

np.random.seed(2024)
random.seed(2024)

# ── Brand context ──────────────────────────────────────────────────────────
# Dot & Key was founded 2018, major growth post-2021 via Nykaa + own DTC site
# Known for: Vitamin C serums, Watermelon range, SPF products, eye creams
# Price band: ₹395–₹895 mostly; some kits up to ₹1,499

CATEGORIES = {
    'Vitamin C & Brightening': {'weight': 0.28, 'price': (495, 895), 'skus': ['Vitamin C Face Serum', 'Vitamin C Eye Cream', 'Brightening Clay Mask', 'Glow Toner']},
    'SPF & Sun Protection':    {'weight': 0.22, 'price': (445, 795), 'skus': ['SPF 50 Sunscreen', 'Invisible Sunscreen Gel', 'Tinted SPF Fluid', 'After-Sun Lotion']},
    'Watermelon Hydration':    {'weight': 0.20, 'price': (395, 695), 'skus': ['Watermelon Sleeping Mask', 'Watermelon Gel Moisturiser', 'Watermelon Face Wash', 'Watermelon Toner']},
    'Acne & Oil Control':      {'weight': 0.15, 'price': (395, 749), 'skus': ['Niacinamide Serum', 'Salicylic Acid Cleanser', 'Oil Control Moisturiser', 'Pore Refining Toner']},
    'Kits & Combos':           {'weight': 0.15, 'price': (799, 1499), 'skus': ['Glow Starter Kit', 'Hydration Duo', 'SPF + Vitamin C Combo', 'AM/PM Routine Kit']},
}

CHANNELS = {
    'Nykaa':          {'weight': 0.35, 'discount_range': (10, 25), 'return_rate': 0.04},
    'Own Website':    {'weight': 0.28, 'discount_range': (5,  18), 'return_rate': 0.025},
    'Amazon':         {'weight': 0.18, 'discount_range': (8,  22), 'return_rate': 0.06},
    'Instagram Shop': {'weight': 0.12, 'discount_range': (5,  15), 'return_rate': 0.02},
    'Blinkit/Zepto':  {'weight': 0.07, 'discount_range': (0,   8), 'return_rate': 0.01},
}

CITIES = {
    'Mumbai': 0.19, 'Delhi': 0.16, 'Bengaluru': 0.15, 'Hyderabad': 0.11,
    'Pune': 0.09, 'Chennai': 0.08, 'Kolkata': 0.07, 'Ahmedabad': 0.06,
    'Jaipur': 0.05, 'Lucknow': 0.04
}

CUSTOMER_TYPES = {'New': 0.55, 'Repeat': 0.35, 'Loyal': 0.10}

# ── Year-wise order volumes (reflects brand growth) ────────────────────────
# FY21-22: brand just scaling, ~8k orders/month avg
# FY22-23: Nykaa bestseller, ~14k orders/month
# FY23-24: matured + quick commerce launch, ~18k orders/month
YEAR_CONFIGS = {
    'FY21-22': {'n_orders': 48000, 'start': '2021-04-01', 'end': '2022-03-31', 'price_multiplier': 1.0},
    'FY22-23': {'n_orders': 75000, 'start': '2022-04-01', 'end': '2023-03-31', 'price_multiplier': 1.08},
    'FY23-24': {'n_orders': 95000, 'start': '2023-04-01', 'end': '2024-03-31', 'price_multiplier': 1.12},
}

# Monthly seasonality weights (Apr=1 … Mar end)
# India skincare peaks: Oct–Jan (festive + winter), Apr–Jun (summer SPF)
MONTH_WEIGHTS = {
    4: 1.1, 5: 1.2, 6: 1.15,  # summer SPF spike
    7: 0.85, 8: 0.8, 9: 0.9,
    10: 1.3, 11: 1.5, 12: 1.6,  # festive season
    1: 1.3, 2: 1.0, 3: 1.1
}

all_rows = []
order_counter = 100001
customer_pool = [f"DNK{str(i).zfill(6)}" for i in range(1, 40001)]

for fy, cfg in YEAR_CONFIGS.items():
    n = cfg['n_orders']
    start = datetime.strptime(cfg['start'], '%Y-%m-%d')
    end   = datetime.strptime(cfg['end'],   '%Y-%m-%d')
    pm    = cfg['price_multiplier']

    # Build weighted date list
    date_pool = []
    d = start
    while d <= end:
        w = MONTH_WEIGHTS.get(d.month, 1.0)
        date_pool.extend([d] * int(w * 10))
        d += timedelta(days=1)

    cats     = list(CATEGORIES.keys())
    cat_w    = [CATEGORIES[c]['weight'] for c in cats]
    chans    = list(CHANNELS.keys())
    chan_w   = [CHANNELS[c]['weight'] for c in chans]
    city_k   = list(CITIES.keys())
    city_w   = list(CITIES.values())
    ctype_k  = list(CUSTOMER_TYPES.keys())
    ctype_w  = list(CUSTOMER_TYPES.values())

    for _ in range(n):
        cat   = random.choices(cats,    weights=cat_w)[0]
        chan  = random.choices(chans,   weights=chan_w)[0]
        city  = random.choices(city_k,  weights=city_w)[0]
        ctype = random.choices(ctype_k, weights=ctype_w)[0]
        date  = random.choice(date_pool)

        sku   = random.choice(CATEGORIES[cat]['skus'])
        lo, hi = CATEGORIES[cat]['price']
        unit_price = round(random.uniform(lo * pm, hi * pm) / 5) * 5  # round to ₹5

        qty = random.choices([1, 2, 3, 4], weights=[0.52, 0.28, 0.13, 0.07])[0]
        # Loyal customers buy more
        if ctype == 'Loyal':
            qty = min(qty + 1, 4)

        disc_lo, disc_hi = CHANNELS[chan]['discount_range']
        # Festive months: higher discounts
        fest_boost = 3 if date.month in [10, 11, 12, 1] else 0
        disc_pct  = round(random.uniform(disc_lo, min(disc_hi + fest_boost, 35)), 1)
        disc_amt  = round(unit_price * qty * disc_pct / 100, 2)
        gmv       = round(unit_price * qty, 2)
        net_rev   = round(gmv - disc_amt, 2)
        # COGS: 38–52% of unit price (kits have lower COGS %)
        cogs_pct  = random.uniform(0.38, 0.52) if cat != 'Kits & Combos' else random.uniform(0.42, 0.55)
        cogs      = round(unit_price * qty * cogs_pct, 2)
        gp        = round(net_rev - cogs, 2)
        returned  = 1 if random.random() < CHANNELS[chan]['return_rate'] else 0
        # Marketing spend per order (approx CAC by channel)
        cac_map   = {'Nykaa': 85, 'Own Website': 120, 'Amazon': 95, 'Instagram Shop': 140, 'Blinkit/Zepto': 60}
        mktg_cost = cac_map[chan] if ctype == 'New' else cac_map[chan] * 0.3

        all_rows.append({
            'order_id':        f"DNK{order_counter}",
            'fiscal_year':     fy,
            'order_date':      date.strftime('%Y-%m-%d'),
            'month':           date.month,
            'month_name':      date.strftime('%b'),
            'fiscal_quarter':  f"Q{((date.month - 4) % 12) // 3 + 1}",
            'category':        cat,
            'sku':             sku,
            'channel':         chan,
            'city':            city,
            'customer_type':   ctype,
            'quantity':        qty,
            'unit_price':      unit_price,
            'discount_pct':    disc_pct,
            'discount_amount': disc_amt,
            'gmv':             gmv,
            'net_revenue':     net_rev,
            'cogs':            cogs,
            'gross_profit':    gp,
            'marketing_cost':  round(mktg_cost, 2),
            'is_returned':     returned,
        })
        order_counter += 1

df = pd.DataFrame(all_rows)
os.makedirs('/home/claude/dotandkey/data', exist_ok=True)
df.to_csv('/home/claude/dotandkey/data/dotandkey_orders.csv', index=False)

print(f"Total orders: {len(df):,}")
for fy in ['FY21-22', 'FY22-23', 'FY23-24']:
    sub = df[df['fiscal_year'] == fy]
    print(f"  {fy}: {len(sub):,} orders | GMV ₹{sub['gmv'].sum()/1e7:.2f}Cr | Net Rev ₹{sub['net_revenue'].sum()/1e7:.2f}Cr | GP ₹{sub['gross_profit'].sum()/1e7:.2f}Cr")
