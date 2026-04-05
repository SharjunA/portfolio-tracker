from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Holding:
    name: str
    ticker: str
    qty: int
    avg_price: float
    category: str = "stock"  # "stock" | "etf"

    # Populated after price fetch
    market_price: Optional[float] = None
    fetch_error: Optional[str] = None

    @property
    def invested(self) -> float:
        return round(self.qty * self.avg_price, 2)

    @property
    def market_value(self) -> Optional[float]:
        if self.market_price is None:
            return None
        return round(self.qty * self.market_price, 2)

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
        return round(self.total_market_value - self.total_invested, 2)

    @property
    def total_pnl_pct(self) -> float:
        if self.total_invested == 0:
            return 0.0
        return round((self.total_pnl / self.total_invested) * 100, 2)

    @property
    def stocks(self) -> list[Holding]:
        return [h for h in self.holdings if h.category == "stock"]

    @property
    def etfs(self) -> list[Holding]:
        return [h for h in self.holdings if h.category == "etf"]

    @property
    def failed(self) -> list[Holding]:
        return [h for h in self.holdings if h.fetch_error is not None]
