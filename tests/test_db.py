"""Repository tests using fake cursor/connection objects, not PostgreSQL."""

from decimal import Decimal

import pytest

from db import portfolio_repository
from db.portfolio_repository import MissingInstrumentMetadataError


class FakeCursor:
    def __init__(self, transactions, metadata):
        self.transactions = transactions
        self.metadata = metadata
        self.last_query = ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query, params=None):
        self.last_query = query

    def fetchall(self):
        if "FROM transactions" in self.last_query:
            return self.transactions
        return self.metadata


class FakeConnection:
    def __init__(self, transactions, metadata):
        self.cursor_obj = FakeCursor(transactions, metadata)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def cursor(self):
        return self.cursor_obj


def fake_connection(transactions, metadata):
    return FakeConnection(transactions, metadata)


def test_load_holdings_uses_transactions_and_instrument_metadata(monkeypatch):
    transactions = [
        ("TMPV", "BUY", Decimal("1.5"), Decimal("330.50"), Decimal("1.20")),
        ("TMPV", "BUY", Decimal("0.5"), Decimal("340.50"), Decimal("0.80")),
    ]
    metadata = [("TMPV", "Tata Motors Passenger Vehicles", "stock", "TMPV.NS")]
    monkeypatch.setattr(
        portfolio_repository,
        "get_connection",
        lambda: fake_connection(transactions, metadata),
    )

    holdings = portfolio_repository.load_holdings()

    assert len(holdings) == 1
    assert holdings[0].ticker == "TMPV.NS"
    assert holdings[0].qty == Decimal("2.0")
    assert holdings[0].avg_price == Decimal("334")
    assert holdings[0].priceable is True


def test_load_holdings_fails_when_instrument_metadata_is_missing(monkeypatch):
    transactions = [("TMPV", "BUY", Decimal("1"), Decimal("330.50"), Decimal("0"))]
    monkeypatch.setattr(
        portfolio_repository,
        "get_connection",
        lambda: fake_connection(transactions, []),
    )

    with pytest.raises(MissingInstrumentMetadataError, match="TMPV"):
        portfolio_repository.load_holdings()
