"""
alerts.py — simple threshold-based alerts printed to terminal (or emailed).

Define your alert rules in ALERT_RULES below.
This module is called automatically by auto_report.py after each refresh.
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.models import Holding, PortfolioSummary
from utils.logger import get_logger

logger = get_logger(__name__)

AlertType = Literal["pnl_pct_above", "pnl_pct_below", "price_above", "price_below"]


@dataclass
class AlertRule:
    ticker: str
    alert_type: AlertType
    threshold: float
    message: str = ""


# ── Define your alert rules here ─────────────────────────────────────────────
ALERT_RULES: list[AlertRule] = [
    AlertRule("HDFCBANK.NS",  "pnl_pct_above",  15.0,  "HDFC Bank up >15% — consider booking partial profit"),
    AlertRule("ANANTRAJ.NS",  "pnl_pct_below",  -10.0, "Anant Raj down >10% — review position"),
    AlertRule("NIFTYIETF.NS", "price_above",    350.0,  "Nifty 50 ETF above ₹350"),
]


def _check(holding: Holding, rule: AlertRule) -> bool:
    if rule.alert_type == "pnl_pct_above":
        return holding.pnl_pct is not None and holding.pnl_pct >= rule.threshold
    if rule.alert_type == "pnl_pct_below":
        return holding.pnl_pct is not None and holding.pnl_pct <= rule.threshold
    if rule.alert_type == "price_above":
        return holding.market_price is not None and holding.market_price >= rule.threshold
    if rule.alert_type == "price_below":
        return holding.market_price is not None and holding.market_price <= rule.threshold
    return False


def check_alerts(summary: PortfolioSummary) -> list[str]:
    """Check all alert rules and return a list of triggered alert messages."""
    ticker_map = {h.ticker: h for h in summary.holdings}
    triggered = []

    for rule in ALERT_RULES:
        holding = ticker_map.get(rule.ticker)
        if holding is None:
            continue
        if _check(holding, rule):
            msg = rule.message or f"Alert triggered: {rule.ticker} — {rule.alert_type} {rule.threshold}"
            triggered.append(msg)
            logger.warning(f"🔔 ALERT: {msg}")

    return triggered


def print_alerts(summary: PortfolioSummary) -> None:
    alerts = check_alerts(summary)
    if not alerts:
        print("  No alerts triggered.\n")
        return
    print(f"\n{'─' * 50}")
    print(f"  🔔  {len(alerts)} ALERT(S) TRIGGERED")
    print(f"{'─' * 50}")
    for a in alerts:
        print(f"  • {a}")
    print()
