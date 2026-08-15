"""Unit tests for price-fetch state transitions."""

from core.fetcher import fetch_all
from core.models import Holding


def test_fetch_all_clears_stale_error_after_success(monkeypatch):
    holding = Holding("Test", "TEST.NS", 1, 100.0)
    holding.fetch_error = "previous failure"
    holding.market_price = 90.0

    monkeypatch.setattr("core.fetcher.fetch_price", lambda ticker, use_cache: 110.0)

    result = fetch_all([holding], use_cache=False)

    assert result[0].market_price == 110.0
    assert result[0].fetch_error is None


def test_fetch_all_marks_unpriceable_instrument_without_fetching(monkeypatch):
    holding = Holding("Unpriced", "UNPRICED", 1, 100.0, priceable=False)
    fetch_called = False

    def unexpected_fetch(*args, **kwargs):
        nonlocal fetch_called
        fetch_called = True
        raise AssertionError("unpriceable instruments must not be fetched")

    monkeypatch.setattr("core.fetcher.fetch_price", unexpected_fetch)

    fetch_all([holding])

    assert fetch_called is False
    assert holding.market_price is None
    assert holding.fetch_error == "No market data source configured for this instrument"
