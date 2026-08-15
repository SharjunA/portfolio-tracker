"""
db/portfolio_repository.py — I/O boundary between PostgreSQL and the rest
of the app. Deliberately thin: this module's job is fetching rows and
shaping them into core.models.Holding. All calculation (weighted-average
cost) lives in core.position_calculator, which has no DB dependency and
can be unit-tested without a database.

Source of truth: `transactions` for quantity/avg_price, `instruments`
for name/category/market_ticker. `holdings` is not read here — see
README/migration notes for why it was retired as a dimension table.

Missing metadata fails loudly. A ticker with transactions but no
`instruments` row is a data-completeness bug, not a case to paper over —
silently excluding it would under-report the portfolio exactly like the
stale `config/holdings.py` did. Add the missing instrument row and rerun.

A known instrument with no `market_ticker` is NOT excluded — it still
has real invested capital and appears in the report as an unpriced
holding (`Holding.priceable = False`). Excluding it would under-report
invested capital the same way stale quantities did.

An oversell or unrecognized transaction_type in the ledger itself raises
core.position_calculator.InvalidTransactionHistoryError rather than
being clamped or skipped — see that module for why.
"""

from __future__ import annotations

from decimal import Decimal
import logging

from db.connection import get_connection
from core.models import Holding
from core.position_calculator import TransactionRow, aggregate_transactions

logger = logging.getLogger(__name__)


class MissingInstrumentMetadataError(Exception):
    """Raised when transactions reference tickers with no matching row in
    `instruments`. Message lists every affected ticker so it can be fixed
    in one pass rather than discovered one ticker at a time."""


def _fetch_transaction_rows(cur) -> list[TransactionRow]:
    cur.execute(
        """
        SELECT ticker, transaction_type, quantity, price, charges
        FROM transactions
        ORDER BY ticker, transaction_date, id
        """
    )
    return [
        TransactionRow(
            ticker=ticker,
            transaction_type=txn_type,
            quantity=Decimal(str(qty)),
            price=Decimal(str(price)),
            charges=Decimal(str(charges)) if charges is not None else Decimal("0"),
        )
        for ticker, txn_type, qty, price, charges in cur.fetchall()
    ]


def _fetch_instrument_metadata(cur, tickers: list[str]) -> dict[str, tuple[str, str, str | None]]:
    """{ticker: (name, category, market_ticker)} for the given tickers."""
    if not tickers:
        return {}
    cur.execute(
        "SELECT ticker, name, category, market_ticker FROM instruments WHERE ticker = ANY(%s)",
        (tickers,),
    )
    return {row[0]: (row[1], row[2], row[3]) for row in cur.fetchall()}


def load_holdings() -> list[Holding]:
    """
    Build core.models.Holding objects from `transactions`, shaped to drop
    into core.portfolio.Portfolio exactly like the static HOLDINGS list.

    Raises MissingInstrumentMetadataError if any ticker with transactions
    has no `instruments` row — see module docstring for why this is a
    hard failure rather than a skip-and-warn.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            rows = _fetch_transaction_rows(cur)
            positions = aggregate_transactions(rows)
            metadata = _fetch_instrument_metadata(cur, list(positions.keys()))

    missing = sorted(set(positions) - set(metadata))
    if missing:
        raise MissingInstrumentMetadataError(
            f"{len(missing)} ticker(s) have transactions but no row in "
            f"`instruments`: {', '.join(missing)}. Add a row to "
            f"db/seed/instruments.sql (or INSERT directly) with name, "
            f"category, and market_ticker for each before loading holdings "
            f"from the DB."
        )

    holdings: list[Holding] = []
    unpriceable: list[str] = []
    for ticker, pos in sorted(positions.items()):
        name, category, market_ticker = metadata[ticker]

        qty = pos.quantity
        # A known instrument with no market_ticker still has real invested
        # capital and belongs in the report — it just can't be priced.
        # Excluding it would under-report total invested capital the same
        # way the stale config/holdings.py under-reported quantities.
        priceable = bool(market_ticker)
        if not priceable:
            unpriceable.append(ticker)

        holdings.append(
            Holding(
                name=name,
                ticker=market_ticker if priceable else ticker,
                qty=qty,
                avg_price=pos.avg_price,
                category=category,
                priceable=priceable,
            )
        )

    if unpriceable:
        logger.warning(
            "No market_ticker configured — included with invested value "
            "but no live price: %s",
            ", ".join(sorted(unpriceable)),
        )
    return holdings
