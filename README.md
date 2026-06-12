# 📊 Stock Investment Brief Tool

## Overview
A Python-based fundamental analysis tool that generates a one-page investment brief 
for any stock or ETF. Input a ticker, get a structured Buy/Hold/Sell signal backed 
by real market data and quantitative scoring.

---

## How It Works

### Step 1 — Data Fetch
Pulls ~25 live data points from Yahoo Finance across four dimensions:
- **Valuation** — P/E, Forward P/E, PEG, EV/EBITDA, Price/Book
- **Quality** — ROE, ROA, Gross/Operating/Net Margins, Debt/Equity, Current Ratio, FCF
- **Growth** — Revenue Growth, Earnings Growth
- **Momentum** — 52-week range position, 50D & 200D moving averages

### Step 2 — Scoring
Each metric is converted to a 0–100 score using institutional thresholds:

| Metric     | Score 100      | Score 70       | Score 40       | Score 15    |
|------------|----------------|----------------|----------------|-------------|
| P/E        | < 15           | 15–25          | 25–35          | > 35        |
| ROE        | > 30%          | 15–30%         | 8–15%          | < 8%        |
| Net Margin | > 25%          | 15–25%         | 8–15%          | < 8%        |
| PEG        | < 1            | 1–2            | 2–3            | > 3         |
| D/E Ratio  | < 50           | 50–100         | 100–200        | > 200       |

Scores are averaged within each category, then combined into a composite:
Composite = Valuation×30% + Quality×30% + Growth×20% + Momentum×20%
### Step 3 — Signal
| Composite Score | Signal       |
|-----------------|--------------|
| 65 – 100        | 🟢 BUY       |
| 45 – 64         | 🟡 HOLD      |
| 0 – 44          | 🔴 SELL      |

---

## Why These Weights?

**Valuation & Quality (30% each)** — Most reliable long-term return predictors, 
consistent with academic factor research and CFA curriculum frameworks.

**Growth (20%)** — Matters but harder to predict consistently; used as a 
supporting factor rather than a primary driver.

**Momentum (20%)** — Price trends carry information. The market is often right 
about direction even when wrong about magnitude.

---

## Example Output — Mastercard (MA)

| Category   | Score    | Insight                                      |
|------------|----------|----------------------------------------------|
| Valuation  | 52.5/100 | Fair — P/E 28x, EV/EBITDA 20x               |
| Quality    | 58.8/100 | Strong — ROE 232%, Net Margin 45.9%, FCF $16B|
| Growth     | 87.5/100 | Excellent — Revenue +15.8%, Earnings +21.2%  |
| Momentum   | 20.0/100 | Weak — 18.8% off 52W high, below 200D MA     |

**Signal: 🟡 HOLD (54.9/100)**

> Great business at a fair price, but price trend is working against entry. 
> Momentum needs to stabilize before initiating a position.

---

## How to Use

```python
# Analyze any ticker
analyze('AAPL')
analyze('NVDA')
analyze('VNQ')
```

---

## Tech Stack
- `yfinance` — live market & fundamental data
- `pandas` / `numpy` — data processing & scoring
- `datetime` — dynamic report dating

---

## Disclaimer
This tool generates quantitative signals only. Always conduct independent 
due diligence before making investment decisions. Not financial advice.
