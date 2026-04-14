# settings.py — global configuration for the portfolio tracker.

from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT_DIR    = Path(__file__).parent.parent
DATA_DIR    = ROOT_DIR / "data"
CACHE_DIR   = DATA_DIR / "cache"
EXPORTS_DIR = DATA_DIR / "exports"
HISTORY_DIR = DATA_DIR / "history"

# Ensure dirs exist at import time
for _d in (CACHE_DIR, EXPORTS_DIR, HISTORY_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ── Fetcher ───────────────────────────────────────────────────────────────────
CACHE_TTL_MINUTES   = 15        # How long to reuse a cached price
FETCH_TIMEOUT_SEC   = 10        # Per-ticker timeout
MAX_RETRIES         = 2         # Retry failed tickers once

# ── Reports ───────────────────────────────────────────────────────────────────
CURRENCY_SYMBOL     = "₹"
EXCEL_SHEET_NAME    = "Portfolio Report"

# Excel color scheme (hex, no #)
COLORS = {
    "header_bg":   "1F3864",
    "header_fg":   "FFFFFF",
    "profit_bg":   "C6EFCE",
    "loss_bg":     "FFC7CE",
    "summary_bg":  "D9E1F2",
    "title_fg":    "1F3864",
}

# ── History ───────────────────────────────────────────────────────────────────
SAVE_HISTORY        = True      # Append daily snapshot to history/
HISTORY_FILE        = HISTORY_DIR / "portfolio_history.csv"

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_LEVEL           = "INFO"    # DEBUG | INFO | WARNING | ERROR
LOG_FILE            = ROOT_DIR / "portfolio_tracker.log"
