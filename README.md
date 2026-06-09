# Revenue & Pricing Optimization Analysis
### D2C E-commerce Brand | FY 2023 | Business Analyst Project

---

## 📌 Problem Statement

A D2C skincare & wellness brand was experiencing **growing GMV but shrinking net margins**. Despite increasing order volumes, gross profit margin had declined across several channels and categories in FY 2023.

**Management question:**
> *"Where exactly are we losing revenue — and which discount strategies are hurting us more than helping?"*

---

## 🎯 Objective

1. Identify **revenue drivers and margin leakages** across categories, channels, and geographies
2. Quantify the **impact of discounting** on net revenue and gross profit
3. Pinpoint the **pricing sweet spot** — discount bands that maximize revenue without eroding margins
4. Deliver **actionable recommendations** to recover ₹15–20L in annual margin

---

## 📊 Dataset

| Field | Description |
|---|---|
| Source | Simulated order-level transaction data (reflects real D2C patterns) |
| Records | 12,000 orders across FY 2023 (Jan–Dec) |
| Key Fields | Order ID, Customer ID, Category, Channel, City, Unit Price, Discount %, GMV, Net Revenue, COGS, Gross Profit, Returns |

**Key Metrics:**
- Total GMV: ₹1.83 Cr
- Net Revenue: ₹1.60 Cr
- Gross Profit: ₹65.2L
- Overall GP Margin: **40.3%**
- Total Discount Leakage: **₹22.4L (12.3% of GMV)**

---

## 🔍 Analysis Performed

### 1. Monthly Revenue Trend
Tracked GMV, Net Revenue, and Gross Profit across all 12 months alongside GP Margin % to identify seasonal patterns and margin compression periods.

**Finding:** Q4 (Oct–Dec) drives **~34% of annual revenue** but GP Margin dips due to heavier festival-season discounting via Email and Paid Ads channels.

---

### 2. Category Performance
Broke down revenue share, GP margin, and average discount by product category.

**Finding:** Skincare is the **top revenue contributor (35% share)** but Supplements carries the **highest GP margin (43.1%)** despite lower volume — an under-invested category.

---

### 3. Channel Discount Efficiency
Measured discount leakage (discount as % of GMV) and GP margin across all 5 acquisition channels.

**Finding:**
- **Email channel** offers the highest discounts (avg 22.4%) but yields the **lowest GP margin** — discount depth is not translating to loyalty or quality orders
- **Organic Search** has the healthiest margins with the lowest discount dependency
- **Paid Ads** has the highest return rate (5.8%), inflating GMV but reducing net revenue

---

### 4. Discount Band Analysis (Key Insight)
Segmented all orders into discount bands (0–5%, 5–10%, 10–15%, 15–20%, 20–25%, 25%+) and measured GP margin and Average Order Value per band.

**Finding — The Pricing Sweet Spot:**

| Discount Band | GP Margin | AOV | Verdict |
|---|---|---|---|
| 0–5% | ~42% | ₹949 | ✅ Best |
| 5–10% | ~40% | ₹872 | ✅ Healthy |
| 10–15% | ~39% | ₹831 | ⚠️ Watch |
| 15–20% | ~37% | ₹798 | 🔴 Margin risk |
| 20–25% | ~34% | ₹762 | 🔴 Over-discounting |
| 25%+ | ~30% | ₹710 | ❌ Revenue destroyer |

> Orders with 25%+ discount have GP Margins **12 percentage points lower** than 0–5% orders, yet AOV is only ₹239 lower. The trade-off is not worth it.

---

### 5. Geographic & Seasonal Distribution
Heatmap of city × quarter revenue performance and stacked bar of quarterly category mix.

**Finding:** Mumbai and Bengaluru together contribute **37% of revenue** but show the sharpest Q4 spike — indicating over-dependence on seasonal campaigns in metro cities. Tier-2 cities (Pune, Hyderabad) show steady growth QoQ.

---

## 💡 Business Recommendations

### Rec 1: Cap Email Channel Discounts at 15%
- Current avg: 22.4% | Recommended: ≤15%
- **Estimated recovery: ₹4.2L/year** in margin
- Replace deep discounts with loyalty perks (early access, bundles)

### Rec 2: Increase Investment in Supplements Category
- Highest margin category but only 18% revenue share
- Run targeted campaigns for Supplements on Organic + Instagram
- **Opportunity: ₹6–8L incremental GP** at current margin rates

### Rec 3: Reduce Paid Ads Return Rate
- 5.8% return rate on Paid Ads vs 2.1% on Organic Search
- Root cause: misleading ad creatives setting wrong expectations
- **Action: A/B test product-accurate creatives** to reduce returns by 30%

### Rec 4: Standardize Festival Discount Cap at 20%
- Q4 discounting on Email + Paid Ads goes as high as 28–30%
- Enforce a 20% maximum cap with approval for exceptions
- **Estimated margin protection: ₹3.5L during Oct–Dec**

### Rec 5: Grow Organic Search Share
- Highest GP margin channel with zero discount dependency
- Invest in SEO content for ingredient-led keywords (growing search trend)
- Target organic from 28% → 35% channel mix over 2 quarters

---

## 📁 Project Structure

```
revenue_analysis/
├── data/
│   ├── generate_data.py      # Data generation script
│   └── orders.csv            # 12,000 order records
├── outputs/
│   ├── 01_monthly_revenue_trend.png
│   ├── 02_category_revenue_margin.png
│   ├── 03_channel_discount_margin.png
│   ├── 04_discount_band_analysis.png
│   └── 05_geo_seasonal_heatmap.png
├── analysis.py               # Main analysis & visualization script
└── README.md
```

---

## 🛠️ Tools & Libraries

- **Python 3.x** — core analysis
- **Pandas** — data manipulation, aggregation, pivot tables
- **NumPy** — numerical operations
- **Matplotlib** — custom multi-panel charts, dual-axis plots
- **Seaborn** — heatmap visualizations

---

## 📈 Business Impact Summary

| Problem | Finding | Recommendation | Est. Recovery |
|---|---|---|---|
| Discount leakage | ₹22.4L lost to discounts | Cap Email at 15%, festival at 20% | ₹7.7L/yr |
| Underperforming channel | Email: lowest GP margin | Shift from discounts to loyalty | ₹4.2L/yr |
| Untapped category | Supplements: highest margin, low volume | Increase marketing investment | ₹6–8L/yr |
| High return rate | Paid Ads: 5.8% returns | Fix ad creatives | ₹2.1L/yr |

**Total addressable margin opportunity: ₹18–22L annually**

---

*Project by [Your Name] | Business Analyst | Python · Data Analysis · Revenue Optimization*
