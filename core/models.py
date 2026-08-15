from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Optional
from datetime import datetime


@dataclass
class Holding:
    name: str
    ticker: str
    qty: Decimal
    avg_price: Decimal
    category: str = "stock"

    # False for instruments with no configured market data source (e.g. no
    # market_ticker in the instruments table yet). Such holdings still show
    # invested value — they just never get a market_price, by design, not
    # because a fetch failed. See core.fetcher.fetch_all.
    priceable: bool = True

    # Populated after price fetch
    market_price: Optional[float] = None
    fetch_error: Optional[str] = None

    def __post_init__(self):
        try:
            self.qty = Decimal(str(self.qty))
            self.avg_price = Decimal(str(self.avg_price))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Quantity and average price must be numeric") from exc

        if self.qty <= 0:
            raise ValueError("Quantity must be positive")

        if self.avg_price < 0:
            raise ValueError("Average price cannot be negative")

    @property
    def invested(self) -> float:
        return round(float(self.qty * self.avg_price), 2)

    @property
    def market_value(self) -> Optional[float]:
        if self.market_price is None:
            return None
        return round(float(self.qty * Decimal(str(self.market_price))), 2)

    @property
    def pnl(self) -> Optional[float]:
        if self.market_value is None:
            return None
        return round(self.market_value - self.invested, 2)

    @property
    def pnl_pct(self) -> Optional[float]:
        if self.pnl is None or self.invested == 0:
            return None
        return round((self.pnl / self.invested) * 100, 2)

    @property
    def is_profit(self) -> Optional[bool]:
        if self.pnl is None:
            return None
        return self.pnl >= 0


@dataclass
class PortfolioSummary:
    holdings: list[Holding]
    generated_at: datetime = field(default_factory=datetime.now)

    @property
    def total_invested(self) -> float:
        return round(sum(h.invested for h in self.holdings), 2)

    @property
    def total_market_value(self) -> float:
        return round(sum(h.market_value for h in self.holdings if h.market_value is not None), 2)

    @property
    def total_pnl(self) -> float:
        # A missing price means that the holding's P&L is unknown. Treating
        # its invested value as a complete loss would materially distort the
        # portfolio result when one data source is unavailable.
        return round(sum(h.pnl for h in self.holdings if h.pnl is not None), 2)

    @property
    def total_pnl_pct(self) -> float:
        priced_invested = sum(
            h.invested for h in self.holdings if h.pnl is not None
        )
        if priced_invested == 0:
            return 0.0
        return round((self.total_pnl / priced_invested) * 100, 2)

    @property
    def stocks(self) -> list[Holding]:
        return [h for h in self.holdings if h.category == "stock"]

    @property
    def etfs(self) -> list[Holding]:
        return [h for h in self.holdings if h.category == "etf"]

    @property
    def failed(self) -> list[Holding]:
        return [h for h in self.holdings if h.fetch_error is not None]
