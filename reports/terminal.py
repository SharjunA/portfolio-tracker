"""
terminal.py — prints a formatted portfolio table to the terminal.
"""

from config.settings import CURRENCY_SYMBOL
from core.models import PortfolioSummary


def _fmt_pnl(pnl: float | None, pnl_pct: float | None) -> tuple[str, str]:
    if pnl is None:
        return "N/A", "N/A"
    arrow = "▲" if pnl >= 0 else "▼"
    sign  = "+" if pnl_pct >= 0 else ""
    return f"{arrow} {abs(pnl):,.2f}", f"{sign}{pnl_pct:.2f}%"


def print_report(summary: PortfolioSummary) -> None:
    col = "{:<28} {:<18} {:>5} {:>10} {:>10} {:>12} {:>12} {:>12} {:>8}"
    header = col.format(
        "Stock / ETF", "Ticker", "Qty",
        "Avg (₹)", "Mkt (₹)", "Invested", "Mkt Value", "P&L", "P&L %"
    )
    sep = "─" * len(header)

    print(f"\n📡  Fetched at {summary.generated_at.strftime('%d %b %Y, %I:%M %p')}")
    print(sep)
    print(header)
    print(sep)

    def _section(holdings, label):
        if not holdings:
            return
        print(f"\n  {label}")
        for h in holdings:
            pnl_str, pct_str = _fmt_pnl(h.pnl, h.pnl_pct)
            mkt = f"{h.market_price:,.2f}" if h.market_price else "ERROR"
            print(col.format(
                h.name[:27], h.ticker, h.qty,
                f"{h.avg_price:,.2f}", mkt,
                f"{h.invested:,.2f}",
                f"{h.market_value:,.2f}" if h.market_value else "N/A",
                pnl_str, pct_str,
            ))

    _section(summary.stocks, "Stocks")
    _section(summary.etfs,   "ETFs")

    if summary.failed:
        print(f"\n  ⚠  Failed to fetch ({len(summary.failed)})")
        for h in summary.failed:
            print(f"     {h.name} ({h.ticker}): {h.fetch_error}")

    total_pnl_str, total_pct_str = _fmt_pnl(summary.total_pnl, summary.total_pnl_pct)

    print(f"\n{'═' * 60}")
    print("   📊  PORTFOLIO SUMMARY")
    print(f"{'═' * 60}")
    print(f"   Total Invested       : {CURRENCY_SYMBOL} {summary.total_invested:>12,.2f}")
    print(f"   Current Market Value : {CURRENCY_SYMBOL} {summary.total_market_value:>12,.2f}")
    print(f"   Total P&L            : {CURRENCY_SYMBOL} {total_pnl_str:>12}")
    print(f"   Total Return         :   {total_pct_str:>10}")
    print(f"{'═' * 60}\n")
