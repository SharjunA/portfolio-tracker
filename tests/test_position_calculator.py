"""
Unit tests for core.position_calculator — pure logic, no DB needed.
This is exactly the point of moving aggregation out of the repository:
these tests run in milliseconds with no Postgres instance required.
"""
from decimal import Decimal

import pytest

from core.position_calculator import (
    TransactionRow,
    aggregate_transactions,
    InvalidTransactionHistoryError,
)


def row(ticker, txn_type, qty, price, charges=0):
    return TransactionRow(
        ticker=ticker,
        transaction_type=txn_type,
        quantity=Decimal(str(qty)),
        price=Decimal(str(price)),
        charges=Decimal(str(charges)),
    )


class TestAggregateTransactions:
    def test_single_buy(self):
        result = aggregate_transactions([row("ITC", "BUY", 10, 400)])
        pos = result["ITC"]
        assert pos.quantity == Decimal("10")
        assert pos.avg_price == Decimal("400")

    def test_multiple_buys_weighted_average(self):
        # 10 @ 400 + 10 @ 600 -> 20 shares @ avg 500
        result = aggregate_transactions([
            row("ITC", "BUY", 10, 400),
            row("ITC", "BUY", 10, 600),
        ])
        pos = result["ITC"]
        assert pos.quantity == Decimal("20")
        assert pos.avg_price == Decimal("500")

    def test_charges_included_in_cost_by_default(self):
        # 10 @ 400 + 20 charges -> total cost 4020, avg 402
        result = aggregate_transactions([row("ITC", "BUY", 10, 400, charges=20)])
        pos = result["ITC"]
        assert pos.avg_price == Decimal("402")

    def test_sell_reduces_quantity_not_avg_price(self):
        # buy 20 @ 500, sell 5 -> 15 remaining, avg price unchanged
        result = aggregate_transactions([
            row("ITC", "BUY", 10, 400),
            row("ITC", "BUY", 10, 600),
            row("ITC", "SELL", 5, 700),  # sell price shouldn't affect avg cost
        ])
        pos = result["ITC"]
        assert pos.quantity == Decimal("15")
        assert pos.avg_price == Decimal("500")

    def test_fully_closed_position_is_dropped(self):
        result = aggregate_transactions([
            row("ITC", "BUY", 10, 400),
            row("ITC", "SELL", 10, 500),
        ])
        assert "ITC" not in result

    def test_sell_exceeding_quantity_raises(self):
        with pytest.raises(InvalidTransactionHistoryError, match="exceeds tracked quantity"):
            aggregate_transactions([
                row("ITC", "BUY", 10, 400),
                row("ITC", "SELL", 15, 500),  # more than held
            ])

    def test_unknown_transaction_type_raises(self):
        with pytest.raises(InvalidTransactionHistoryError, match="Unknown transaction_type"):
            aggregate_transactions([
                row("ITC", "BUY", 10, 400),
                row("ITC", "SPLIT", 10, 0),  # not BUY/SELL
            ])

    def test_multiple_tickers_independent(self):
        result = aggregate_transactions([
            row("ITC", "BUY", 10, 400),
            row("RELIANCE", "BUY", 5, 1200),
        ])
        assert set(result.keys()) == {"ITC", "RELIANCE"}
        assert result["RELIANCE"].quantity == Decimal("5")

    def test_zero_quantity_avg_price_is_zero_not_error(self):
        # An empty position (e.g. never bought) has a well-defined avg_price
        # of 0 rather than raising a ZeroDivisionError.
        result = aggregate_transactions([])
        assert result == {}
