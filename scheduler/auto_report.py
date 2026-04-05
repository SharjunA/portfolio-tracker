"""
auto_report.py — runs a full portfolio refresh and saves reports on a schedule.

Run manually:
    python scheduler/auto_report.py

Schedule via cron (every weekday at 4:00 PM IST = 10:30 UTC):
    30 10 * * 1-5 /path/to/.venv/bin/python /path/to/portfolio_tracker/scheduler/auto_report.py

Or use the built-in loop (runs every N minutes while the process is alive):
    python scheduler/auto_report.py --loop --interval 30
"""

import argparse
import sys
import time
from pathlib import Path

# Ensure project root is on the path when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.holdings import HOLDINGS
from core.portfolio import Portfolio
from reports import excel, terminal
from utils.logger import get_logger

logger = get_logger(__name__)


def run_once() -> None:
    logger.info("Starting scheduled portfolio refresh...")
    portfolio = Portfolio(HOLDINGS)
    portfolio.refresh(use_cache=False)   # always fresh on scheduled runs
    summary = portfolio.summary

    terminal.print_report(summary)
    path = excel.generate(summary)
    logger.info(f"Report saved: {path}")

    try:
        from reports.charts import allocation_pie, pnl_bar
        pie_path = allocation_pie(summary)
        bar_path = pnl_bar(summary)
        logger.info(f"Charts saved: {pie_path}, {bar_path}")
    except ImportError:
        logger.warning("matplotlib not installed — skipping charts.")


def run_loop(interval_minutes: int) -> None:
    logger.info(f"Scheduler loop started — running every {interval_minutes} min.")
    while True:
        try:
            run_once()
        except Exception as e:
            logger.error(f"Scheduled run failed: {e}")
        time.sleep(interval_minutes * 60)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Scheduled portfolio report runner")
    p.add_argument("--loop", action="store_true", help="Run on a repeating interval")
    p.add_argument("--interval", type=int, default=30, help="Interval in minutes (default: 30)")
    args = p.parse_args()

    if args.loop:
        run_loop(args.interval)
    else:
        run_once()
