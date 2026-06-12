
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ── STOCK SCREENER ──────────────────────────────────────

universe = [
    "AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","BRK-B","JPM","JNJ",
    "V","UNH","XOM","WMT","MA","PG","HD","CVX","MRK","ABBV",
    "PEP","KO","AVGO","COST","TMO","MCD","ACN","BAC","LIN","ABT",
    "CRM","DHR","NEE","CMCSA","NFLX","TXN","PM","RTX","AMGN","UNP",
    "HON","LOW","QCOM","CAT","SPGI","GS","BLK","AXP","SBUX","PLD",
    "DE","MMM","IBM","GILD","BA","ISRG","SYK","ADI","REGN","VRTX",
    "MDLZ","CI","CB","SO","DUK","MO","ZTS","EOG","SLB",
    "COP","OXY","MPC","PSX","VLO","WFC","USB","TFC","PNC","SCHW",
    "MS","BK","COF","AIG","PRU","MET","ALL","TRV","AFL","HIG",
    "SPY","QQQ","IWM","VTI","VEA","VWO",
    "XLF","XLK","XLE","XLV","XLI","XLP",
    "AGG","TLT","HYG","LQD",
    "VNQ","O","AMT","WELL","SPG","PSA",
    "GLD","SLV","USO",
]

def run_screener():
    print("Running daily screener...")
    prices = yf.download(universe, period="1y", auto_adjust=True, progress=False)["Close"]
    prices = prices.dropna(axis=1, thresh=int(len(prices)*0.8))
    records = []
    for ticker in prices.columns:
        try:
            info = yf.Ticker(ticker).info
            pe     = info.get("trailingPE")
            pb     = info.get("priceToBook")
            ev_eb  = info.get("enterpriseToEbitda")
            roe    = info.get("returnOnEquity")
            margin = info.get("profitMargins")
            de     = info.get("debtToEquity")
            mom    = (prices[ticker].iloc[-1] / prices[ticker].iloc[0] - 1) * 100 if len(prices[ticker].dropna()) > 50 else None
            records.append({"ticker": ticker, "pe": pe, "pb": pb, "ev_ebitda": ev_eb,
                            "roe": roe, "margin": margin, "de": de, "momentum": mom})
        except:
            pass
    df = pd.DataFrame(records).set_index("ticker")
    def rank_score(series, ascending=True):
        return series.rank(ascending=ascending, pct=True) * 100
    scored = df.copy()
    scored["val_score"] = rank_score(df["pe"]) * 0.33 + rank_score(df["pb"]) * 0.33 + rank_score(df["ev_ebitda"]) * 0.34
    scored["q_score"]   = rank_score(df["roe"], False) * 0.33 + rank_score(df["margin"], False) * 0.33 + rank_score(df["de"]) * 0.34
    scored["mom_score"] = rank_score(df["momentum"], False)
    scored["composite"] = scored["val_score"] * 0.33 + scored["q_score"] * 0.33 + scored["mom_score"] * 0.34
    leaderboard = scored[["composite","val_score","q_score","mom_score","pe","pb","roe","margin","momentum"]].sort_values("composite", ascending=False).round(1)
    watchlist = leaderboard.head(15).copy()
    watchlist["flags"] = ""
    watchlist.loc[watchlist["momentum"] < -20, "flags"] += "📉 oversold  "
    watchlist.loc[watchlist["momentum"] > 20,  "flags"] += "📈 momentum  "
    watchlist.loc[watchlist["pe"] > 100,        "flags"] += "⚠️ high PE  "
    watchlist.loc[watchlist["pb"] < 0,          "flags"] += "⚠️ neg book  "
    watchlist.loc[watchlist["roe"] > 0.3,       "flags"] += "⭐ high ROE  "
    watchlist.loc[watchlist["margin"] > 0.25,   "flags"] += "⭐ fat margin  "
    display = pd.DataFrame({
        "Score"    : watchlist["composite"],
        "Valuation": watchlist["val_score"],
        "Quality"  : watchlist["q_score"],
        "Momentum" : watchlist["mom_score"],
        "P/E"      : watchlist["pe"],
        "ROE"      : (watchlist["roe"] * 100).round(1).astype(str) + "%",
        "Margin"   : (watchlist["margin"] * 100).round(1).astype(str) + "%",
        "1Y Ret"   : watchlist["momentum"].round(1).astype(str) + "%",
        "Flags"    : watchlist["flags"],
    })
    print(f"\n📊 DAILY WATCHLIST — {datetime.today().strftime('%B %d, %Y')}")
    print("=" * 100)
    print(display.to_string())

# ── INVESTMENT BRIEF ─────────────────────────────────────

def get_fundamentals(ticker):
    info = yf.Ticker(ticker).info
    return {
        "name": info.get("longName", ticker),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "mktcap": info.get("marketCap"),
        "beta": info.get("beta"),
        "pe": info.get("trailingPE"),
        "fwd_pe": info.get("forwardPE"),
        "pb": info.get("priceToBook"),
        "peg": info.get("pegRatio"),
        "ev_ebitda": info.get("enterpriseToEbitda"),
        "div_yield": info.get("dividendYield"),
        "roe": info.get("returnOnEquity"),
        "roa": info.get("returnOnAssets"),
        "gross_margin": info.get("grossMargins"),
        "op_margin": info.get("operatingMargins"),
        "net_margin": info.get("profitMargins"),
        "de_ratio": info.get("debtToEquity"),
        "current_r": info.get("currentRatio"),
        "fcf": info.get("freeCashflow"),
        "rev_growth": info.get("revenueGrowth"),
        "earn_growth": info.get("earningsGrowth"),
        "week52_high": info.get("fiftyTwoWeekHigh"),
        "week52_low": info.get("fiftyTwoWeekLow"),
        "ma50": info.get("fiftyDayAverage"),
        "ma200": info.get("twoHundredDayAverage"),
    }

def generate_signal(data):
    scores = {}
    reasons = []
    def score_metric(v, thresholds, labels):
        for threshold, score, label in thresholds:
            if v is not None and v < threshold:
                return score, label
        return thresholds[-1][1], thresholds[-1][2]

    val, count = 0, 0
    if data["pe"]:
        v = 100 if data["pe"]<15 else 70 if data["pe"]<25 else 40 if data["pe"]<35 else 15
        val += v; count += 1
        reasons.append(f"P/E of {data['pe']:.1f} — {'attractive' if v>=70 else 'fair' if v>=40 else 'stretched'}")
    if data["fwd_pe"]:
        val += 100 if data["fwd_pe"]<15 else 70 if data["fwd_pe"]<25 else 40 if data["fwd_pe"]<35 else 15; count += 1
    if data["peg"]:
        v = 100 if data["peg"]<1 else 65 if data["peg"]<2 else 35 if data["peg"]<3 else 10
        val += v; count += 1
        reasons.append(f"PEG of {data['peg']:.1f} — {'growth at reasonable price' if v>=65 else 'expensive relative to growth'}")
    if data["ev_ebitda"]:
        val += 100 if data["ev_ebitda"]<10 else 65 if data["ev_ebitda"]<20 else 35 if data["ev_ebitda"]<30 else 10; count += 1
    scores["valuation"] = val / count if count else 50

    qual, count = 0, 0
    if data["roe"]:
        v = 100 if data["roe"]>0.30 else 70 if data["roe"]>0.15 else 40 if data["roe"]>0.08 else 15
        qual += v; count += 1
        reasons.append(f"ROE of {data['roe']*100:.1f}% — {'exceptional' if v>=100 else 'solid' if v>=70 else 'weak'}")
    if data["net_margin"]:
        v = 100 if data["net_margin"]>0.25 else 75 if data["net_margin"]>0.15 else 45 if data["net_margin"]>0.08 else 15
        qual += v; count += 1
        reasons.append(f"Net margin of {data['net_margin']*100:.1f}% — {'best-in-class' if v>=100 else 'healthy' if v>=75 else 'thin'}")
    if data["de_ratio"]:
        v = 100 if data["de_ratio"]<50 else 70 if data["de_ratio"]<100 else 40 if data["de_ratio"]<200 else 15
        qual += v; count += 1
        reasons.append(f"D/E ratio of {data['de_ratio']:.0f} — {'conservative balance sheet' if v>=70 else 'leveraged'}")
    if data["current_r"]:
        qual += 100 if data["current_r"]>2 else 65 if data["current_r"]>1 else 20; count += 1
    scores["quality"] = qual / count if count else 50

    grow, count = 0, 0
    if data["rev_growth"]:
        v = 100 if data["rev_growth"]>0.20 else 75 if data["rev_growth"]>0.10 else 50 if data["rev_growth"]>0.05 else 30 if data["rev_growth"]>0 else 10
        grow += v; count += 1
        reasons.append(f"Revenue growth of {data['rev_growth']*100:.1f}% — {'strong' if v>=75 else 'moderate' if v>=50 else 'slowing'}")
    if data["earn_growth"]:
        v = 100 if data["earn_growth"]>0.20 else 75 if data["earn_growth"]>0.10 else 40 if data["earn_growth"]>0 else 10
        grow += v; count += 1
        reasons.append(f"Earnings growth of {data['earn_growth']*100:.1f}% — {'accelerating' if v>=75 else 'modest' if v>=40 else 'declining'}")
    scores["growth"] = grow / count if count else 50

    mom, count = 0, 0
    if data["price"] and data["week52_high"] and data["week52_low"]:
        rp = (data["price"] - data["week52_low"]) / (data["week52_high"] - data["week52_low"])
        v = 90 if rp>0.75 else 65 if rp>0.50 else 40 if rp>0.25 else 20
        mom += v; count += 1
        reasons.append(f"Trading at {rp*100:.0f}% of 52-week range — {'near highs' if v>=90 else 'mid-range' if v>=65 else 'near lows'}")
    if data["price"] and data["ma50"] and data["ma200"]:
        v = 100 if data["price"]>data["ma50"]>data["ma200"] else 65 if data["price"]>data["ma200"] else 50 if data["price"]>data["ma50"] else 20
        mom += v; count += 1
        reasons.append(f"Price vs MAs — {'bullish trend' if v>=100 else 'above 200MA' if v>=65 else 'weak trend'}")
    scores["momentum"] = mom / count if count else 50

    composite = scores["valuation"]*0.30 + scores["quality"]*0.30 + scores["growth"]*0.20 + scores["momentum"]*0.20
    signal, color = ("BUY","🟢") if composite>=65 else ("HOLD","🟡") if composite>=45 else ("SELL","🔴")
    return scores, composite, signal, color, reasons

def print_brief(ticker, data, scores, composite, signal, color, reasons):
    def fmt_pct(v): return f"{v*100:.1f}%" if v else "N/A"
    def fmt_x(v):   return f"{v:.1f}x" if v else "N/A"
    def fmt_n(v):   return f"{v:.1f}" if v else "N/A"
    def fmt_fcf(v): return f"${v/1e9:.1f}B" if v else "N/A"
    def fmt_div(v):
        if not v: return "None"
        return f"{v*100:.1f}%" if v < 0.5 else f"{v:.1f}%"
    mktcap_b = f"${data['mktcap']/1e9:.1f}B" if data["mktcap"] else "N/A"
    print(f"""
{"="*60}
  INVESTMENT BRIEF — {datetime.today().strftime("%B %d, %Y")}
{"="*60}
  {data["name"]} ({ticker.upper()})
  {data["sector"]} | {data["industry"]}
  Price: ${data["price"]:.2f}  |  Mkt Cap: {mktcap_b}  |  Beta: {fmt_n(data["beta"])}
  Dividend Yield: {fmt_div(data["div_yield"])}
{"="*60}

  SIGNAL: {color} {signal}  ({composite:.1f} / 100)

{"─"*60}
  SCORES
{"─"*60}
  Valuation  : {scores["valuation"]:.1f}/100  {"█" * int(scores["valuation"]//10)}
  Quality    : {scores["quality"]:.1f}/100  {"█" * int(scores["quality"]//10)}
  Growth     : {scores["growth"]:.1f}/100  {"█" * int(scores["growth"]//10)}
  Momentum   : {scores["momentum"]:.1f}/100  {"█" * int(scores["momentum"]//10)}

{"─"*60}
  VALUATION
{"─"*60}
  Trailing P/E    : {fmt_x(data["pe"])}
  Forward P/E     : {fmt_x(data["fwd_pe"])}
  PEG Ratio       : {fmt_n(data["peg"])}
  EV/EBITDA       : {fmt_x(data["ev_ebitda"])}
  Price/Book      : {fmt_x(data["pb"])}

{"─"*60}
  QUALITY
{"─"*60}
  ROE             : {fmt_pct(data["roe"])}
  ROA             : {fmt_pct(data["roa"])}
  Gross Margin    : {fmt_pct(data["gross_margin"])}
  Operating Margin: {fmt_pct(data["op_margin"])}
  Net Margin      : {fmt_pct(data["net_margin"])}
  Debt/Equity     : {fmt_n(data["de_ratio"])}
  Current Ratio   : {fmt_n(data["current_r"])}
  Free Cash Flow  : {fmt_fcf(data["fcf"])}

{"─"*60}
  GROWTH
{"─"*60}
  Revenue Growth  : {fmt_pct(data["rev_growth"])}
  Earnings Growth : {fmt_pct(data["earn_growth"])}

{"─"*60}
  MOMENTUM
{"─"*60}
  52W High        : ${data["week52_high"]:.2f}
  52W Low         : ${data["week52_low"]:.2f}
  50D MA          : ${data["ma50"]:.2f}
  200D MA         : ${data["ma200"]:.2f}
  vs 52W High     : {((data["price"]/data["week52_high"])-1)*100:.1f}%

{"─"*60}
  KEY OBSERVATIONS
{"─"*60}""")
    for r in reasons:
        print(f"  • {r}")
    print(f"""
{"─"*60}
  ⚠️  This is a quantitative signal only. Always do your
  own due diligence before making investment decisions.
{"="*60}
""")

def analyze(ticker):
    ticker = ticker.strip().upper()
    print(f"Fetching data for {ticker}...")
    try:
        data = get_fundamentals(ticker)
        scores, composite, signal, color, reasons = generate_signal(data)
        print_brief(ticker, data, scores, composite, signal, color, reasons)
    except Exception as e:
        print(f"❌ Could not fetch data for {ticker}. ({e})")

# ── RUN ──────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyze(sys.argv[1])
    else:
        print("Usage: python stock_tools.py AAPL")
        print("Or run the screener:")
        run_screener()
