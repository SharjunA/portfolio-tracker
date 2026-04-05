"""
test_calculator.py — unit tests for Holding and PortfolioSummary calculations.
No network calls; all values are hardcoded.
"""

import pytest
from core.models import Holding, PortfolioSummary


def make_holding(name="Test", ticker="TEST.NS", qty=10, avg=100.0, market=120.0):
    h = Holding(name=name, ticker=ticker, qty=qty, avg_price=avg)
    h.market_price = market
    return h


class TestHolding:
    def test_invested(self):
        h = make_holding(qty=5, avg=200.0)
        assert h.invested == 1000.0

    def test_market_value(self):
        h = make_holding(qty=5, avg=200.0, market=250.0)
        assert h.market_value == 1250.0

    def test_pnl_profit(self):
        h = make_holding(qty=10, avg=100.0, market=120.0)
        assert h.pnl == 200.0
        assert h.pnl_pct == 20.0
        assert h.is_profit is True

    def test_pnl_loss(self):
        h = make_holding(qty=10, avg=100.0, market=80.0)
        assert h.pnl == -200.0
        assert h.pnl_pct == -20.0
        assert h.is_profit is False

    def test_pnl_no_price(self):
        h = Holding("X", "X.NS", 5, 100.0)
        assert h.market_value is None
        assert h.pnl is None
        assert h.pnl_pct is None

    def test_zero_avg_price(self):
        h = make_holding(qty=1, avg=0.0, market=50.0)
        assert h.invested == 0.0
        assert h.pnl_pct is None  # avoid division by zero


class TestPortfolioSummary:
    def test_totals(self):
        h1 = make_holding(qty=10, avg=100.0, market=120.0)
        h2 = make_holding(qty=5,  avg=200.0, market=180.0)
        s = PortfolioSummary([h1, h2])
        assert s.total_invested    == 2000.0
        assert s.total_market_value == 2100.0
        assert s.total_pnl         == 100.0

    def test_failed_excluded_from_value(self):
        h1 = make_holding(qty=10, avg=100.0, market=110.0)
        h2 = Holding("Bad", "BAD.NS", 5, 100.0)
        h2.fetch_error = "Timeout"
        s = PortfolioSummary([h1, h2])
        assert s.total_market_value == 1100.0   # h2 excluded
        assert len(s.failed) == 1
