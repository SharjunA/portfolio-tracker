# fetcher.py — fetches live NSE prices via yfinance with local disk cache.

import json
import time
from datetime import datetime, timedelta
from pathlib import Path

import yfinance as yf

from config.settings import CACHE_DIR, CACHE_TTL_MINUTES, MAX_RETRIES
from core.models import Holding
from utils.logger import get_logger

logger = get_logger(__name__)


def _cache_path(ticker: str) -> Path:
    return CACHE_DIR / f"{ticker.replace('.', '_')}.json"


def _load_cache(ticker: str) -> float | None:
    """Return cached price if still fresh, else None."""
    path = _cache_path(ticker)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        cached_at = datetime.fromisoformat(data["cached_at"])
        if datetime.now() - cached_at < timedelta(minutes=CACHE_TTL_MINUTES):
            logger.debug(f"{ticker}: using cached price {data['price']}")
            return data["price"]
    except Exception:
        pass
    return None


def _save_cache(ticker: str, price: float) -> None:
    path = _cache_path(ticker)
    path.write_text(json.dumps({"price": price, "cached_at": datetime.now().isoformat()}))


def fetch_price(ticker: str, use_cache: bool = True) -> float:
    """
    Fetch the latest price for a single ticker.
    Raises ValueError if price cannot be retrieved.
    """
    if use_cache:
        cached = _load_cache(ticker)
        if cached is not None:
            return cached

    for attempt in range(1, MAX_RETRIES + 2):
        try:
            data = yf.Ticker(ticker)
            price = data.fast_info.last_price
            if price is None:
                raise ValueError("Price returned as None")
            price = round(float(price), 2)
            _save_cache(ticker, price)
            logger.debug(f"{ticker}: fetched {price} (attempt {attempt})")
            return price
        except Exception as e:
            logger.warning(f"{ticker}: attempt {attempt} failed — {e}")
            if attempt <= MAX_RETRIES:
                time.sleep(1)

    raise ValueError(f"Could not fetch price for {ticker} after {MAX_RETRIES + 1} attempts")


def fetch_all(holdings: list[Holding], use_cache: bool = True) -> list[Holding]:
    """
    Fetch prices for all holdings in-place.
    Sets market_price or fetch_error on each Holding.
    Returns the same list for convenience.
    """
    logger.info(f"Fetching prices for {len(holdings)} holdings...")
    for h in holdings:
        try:
            h.market_price = fetch_price(h.ticker, use_cache=use_cache)
        except Exception as e:
            h.fetch_error = str(e)
            logger.error(f"{h.name} ({h.ticker}): {e}")
    return holdings
