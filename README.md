# 📊 Stock Analysis Toolkit
**Built by Yashvi Shah | CFA Level 3 | Finance Professional**

A Python-based quantitative research toolkit for daily investment research. 
Built to bridge the gap between institutional-grade investment frameworks 
and accessible, automated analysis tools.

---

## 🧰 What's Inside

### 1. Daily Stock Screener
Scans a universe of 114 stocks, ETFs, and REITs every morning and ranks 
them using a composite factor score across valuation, quality, and momentum.
Outputs a top-15 watchlist with flags to guide where to focus research time.

### 2. Investment Brief Generator
Input any ticker and get a one-page fundamental analysis brief with a 
quantitative Buy/Hold/Sell signal. Pulls ~25 live data points from Yahoo 
Finance and scores them using institutional thresholds.

### 3. Investment Memo Generator
Input any ticker and generate a structured, institutional-style investment 
memo with a full trade setup. Automatically pulls live data, runs the 
quantitative scoring model, and outputs a ready-to-use research document.

Each memo includes:
- Company overview & key metrics
- Quantitative signal from the screener
- Full valuation, quality, growth & momentum snapshot
- Key observations in plain English
- Trade setup — entry, price target, stop loss, risk/reward, position size

**Sample:** See `ABT_investment_memo.md` for a live example — 
Abbott Laboratories (Long), generated June 14, 2026.

---

## ⚙️ How the Scoring Works

Each metric is converted to a 0–100 score using institutional thresholds,
then combined into four category scores and one composite:

Composite = Valuation×30% + Quality×30% + Growth×20% + Momentum×20%

| Metric     | Score 100 | Score 70 | Score 40 | Score 15 |
|------------|-----------|----------|----------|----------|
| P/E        | < 15      | 15–25    | 25–35    | > 35     |
| ROE        | > 30%     | 15–30%   | 8–15%    | < 8%     |
| Net Margin | > 25%     | 15–25%   | 8–15%    | < 8%     |
| PEG        | < 1       | 1–2      | 2–3      | > 3      |
| D/E Ratio  | < 50      | 50–100   | 100–200  | > 200    |

| Composite Score | Signal    |
|-----------------|-----------|
| 65 – 100        | 🟢 BUY    |
| 45 – 64         | 🟡 HOLD   |
| 0 – 44          | 🔴 SELL   |

**Why these weights?**
Valuation and quality carry the most weight (30% each) — consistent with 
academic factor research and CFA curriculum frameworks. Growth (20%) is a 
supporting factor. Momentum (20%) reflects that price trends carry real 
information about market sentiment.

---

## 🚀 How to Use

### Run the daily screener
```bash
python stock_tools.py
```

### Get an investment brief for any ticker
```bash
python stock_tools.py AAPL
```

### Generate an investment memo (in Jupyter)
```python
generate_memo('ABT')

# With custom assumptions
generate_memo('NVDA', target_multiple=25, stop_pct=0.08, position_size="5%")
```

---

## 📁 Files

| File | Description |
|------|-------------|
| `stock_tools.py` | Screener + investment brief — run daily from terminal |
| `Stock Screener.ipynb` | Step-by-step Jupyter notebook — daily screener |
| `Stock Research.ipynb` | Step-by-step Jupyter notebook — investment brief & memo |
| `ABT_investment_memo.md` | Sample investment memo — Abbott Laboratories (Long) |

---

## 🔍 Sample Output — Investment Brief
============================================================

Mastercard Incorporated (MA)

Financial Services | Credit Services

Price: $488.64  |  Mkt Cap: $431.8B  |  Beta: 0.7

SIGNAL: 🟡 HOLD  (54.9 / 100)
Valuation  : 52.5/100  █████

Quality    : 58.8/100  █████

Growth     : 87.5/100  ████████

Momentum   : 20.0/100  ██

---

## 🔍 Sample Output — Daily Screener
📊 DAILY WATCHLIST — June 14, 2026

──────────────────────────────────────────────────────────────────

Score  Valuation  Quality  Momentum   P/E    ROE  Flags

ticker

COST     76.4       93.2     56.4      79.6  49.1  30.0%

COF      75.6       52.1     89.3      85.0  56.0   0.0%

NFLX     67.1       76.2     26.7      97.3  26.2  50.0%  📉 oversold

---

## 🛠️ Tech Stack

- `yfinance` — live market & fundamental data
- `pandas` / `numpy` — data processing & scoring
- `plotly` — interactive charts
- `datetime` — dynamic report dating

---

## 📌 Methodology Notes

- **Percentile ranking** is used in the screener to normalize scores 
  across the universe, making cross-stock comparisons fair regardless of sector
- **Threshold scoring** is used in the brief generator to evaluate each 
  metric against absolute benchmarks used by institutional investors
- **Forward P/E** is used for price target calculation — trailing P/E 
  can be distorted by one-time items

---

## ⚠️ Disclaimer
This toolkit generates quantitative signals only and is intended for 
research and educational purposes. Always conduct independent due diligence 
before making investment decisions. Not financial advice.
