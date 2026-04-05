"""
test_alerts.py — tests for the alert rule engine. No network calls.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.models import Holding, PortfolioSummary
from scheduler.alerts import AlertRule, _check


def _holding(ticker, avg=100.0, market=100.0, qty=1):
    h = Holding(ticker, ticker, qty, avg)
    h.market_price = market
    return h


class TestAlertRules:
    def test_pnl_pct_above_triggered(self):
        h = _holding("TEST.NS", avg=100.0, market=120.0)
        rule = AlertRule("TEST.NS", "pnl_pct_above", 15.0)
        assert _check(h, rule) is True

    def test_pnl_pct_above_not_triggered(self):
        h = _holding("TEST.NS", avg=100.0, market=110.0)
        rule = AlertRule("TEST.NS", "pnl_pct_above", 15.0)
        assert _check(h, rule) is False

    def test_pnl_pct_below_triggered(self):
        h = _holding("TEST.NS", avg=100.0, market=85.0)
        rule = AlertRule("TEST.NS", "pnl_pct_below", -10.0)
        assert _check(h, rule) is True

    def test_price_above_triggered(self):
        h = _holding("TEST.NS", market=400.0)
        rule = AlertRule("TEST.NS", "price_above", 350.0)
        assert _check(h, rule) is True

    def test_price_below_triggered(self):
        h = _holding("TEST.NS", market=90.0)
        rule = AlertRule("TEST.NS", "price_below", 100.0)
        assert _check(h, rule) is True

    def test_no_price_no_trigger(self):
        h = Holding("TEST.NS", "TEST.NS", 1, 100.0)
        rule = AlertRule("TEST.NS", "price_above", 50.0)
        assert _check(h, rule) is False
