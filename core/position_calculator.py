"""
core/position_calculator.py — pure transaction-to-position calculation.

No DB or I/O dependency on purpose: this is business logic (how a stream
of BUY/SELL rows becomes a current position) and should be testable with
plain Python data, independent of where the rows came from.

Method: weighted-average cost. A BUY changes both quantity and average
cost. A SELL reduces quantity at the *current* average cost and leaves
average cost unchanged. This is a simplifying choice for personal
tracking, not a tax-lot (FIFO) calculation.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

INCLUDE_CHARGES_IN_COST = True


class InvalidTransactionHistoryError(Exception):
    """Raised when the transaction log itself is inconsistent — an oversell
    or an unrecognized transaction type. These indicate broken or
    incomplete data (e.g. a missing BUY row, or a typo'd transaction_type
    that slipped past the DB CHECK constraint on an older row). Clamping
    or skipping would silently produce a wrong position instead of
    surfacing the bad data — worse than a personal tracker being briefly
    unusable until the underlying row is fixed."""


@dataclass
class Position:
    ticker: str
    quantity: Decimal
    total_cost: Decimal

    @property
    def avg_price(self) -> Decimal:
        if self.quantity == 0:
            return Decimal("0")
        return self.total_cost / self.quantity


@dataclass
class TransactionRow:
    ticker: str
    transaction_type: str  # "BUY" | "SELL"
    quantity: Decimal
    price: Decimal
    charges: Decimal


def aggregate_transactions(rows: list[TransactionRow]) -> dict[str, Position]:
    """
    rows must be pre-sorted by (ticker, transaction_date) — this function
    does not sort, since ordering is a query concern, not a calculation
    concern. Returns {ticker: Position} for tickers with quantity > 0;
    fully-closed positions are dropped, since there's nothing to report.

    Raises InvalidTransactionHistoryError on an oversell or an unknown
    transaction_type — see the exception's docstring for why this is a
    hard failure rather than a clamp/skip.
    """
    positions: dict[str, Position] = {}

    for row in rows:
        pos = positions.setdefault(
            row.ticker, Position(row.ticker, Decimal("0"), Decimal("0"))
        )

        if row.transaction_type == "BUY":
            cost = row.quantity * row.price
            if INCLUDE_CHARGES_IN_COST:
                cost += row.charges
            pos.quantity += row.quantity
            pos.total_cost += cost

        elif row.transaction_type == "SELL":
            if row.quantity > pos.quantity:
                raise InvalidTransactionHistoryError(
                    f"SELL of {row.quantity} {row.ticker} exceeds tracked "
                    f"quantity {pos.quantity}. Check transaction history "
                    f"for a missing BUY row before trusting this position."
                )
            avg = pos.avg_price  # avg cost is unchanged by a SELL
            pos.quantity -= row.quantity
            pos.total_cost -= row.quantity * avg

        else:
            raise InvalidTransactionHistoryError(
                f"Unknown transaction_type {row.transaction_type!r} for "
                f"{row.ticker}. Expected 'BUY' or 'SELL'."
            )

    return {t: p for t, p in positions.items() if p.quantity > 0}
