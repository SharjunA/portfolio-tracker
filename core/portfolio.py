"""
portfolio.py — high-level Portfolio class: load → fetch → summarise.
"""

import csv
from datetime import datetime

from config.settings import HISTORY_FILE, SAVE_HISTORY
from core.fetcher import fetch_all
from core.models import Holding, PortfolioSummary
from utils.logger import get_logger

logger = get_logger(__name__)


class Portfolio:
    def __init__(self, holdings: list[Holding]):
        self.holdings = holdings
        self._summary: PortfolioSummary | None = None

    def refresh(self, use_cache: bool = True) -> "Portfolio":
        """Fetch live prices and rebuild the summary."""
        fetch_all(self.holdings, use_cache=use_cache)
        self._summary = PortfolioSummary(holdings=self.holdings)
        if SAVE_HISTORY:
            self._append_history()
        return self

    @property
    def summary(self) -> PortfolioSummary:
        if self._summary is None:
            raise RuntimeError("Call portfolio.refresh() before accessing summary.")
        return self._summary

    def _append_history(self) -> None:
        """Append today's total values to the history CSV."""
        s = self._summary
        row = {
            "date": s.generated_at.strftime("%Y-%m-%d %H:%M"),
            "invested": s.total_invested,
            "market_value": s.total_market_value,
            "pnl": s.total_pnl,
            "pnl_pct": s.total_pnl_pct,
        }
        write_header = not HISTORY_FILE.exists()
        with open(HISTORY_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(row)
        logger.debug(f"History appended: {row}")
