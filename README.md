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
