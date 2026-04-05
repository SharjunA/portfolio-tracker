#!/usr/bin/env python3
"""
main.py — entrypoint for the portfolio tracker.

Usage:
    python main.py                        # fetch + terminal + excel report
    python main.py --no-cache             # force fresh prices (skip cache)
    python main.py --report terminal      # terminal only
    python main.py --report excel         # excel only
    python main.py --report all           # terminal + excel (default)
"""

import argparse
import sys

from config.holdings import HOLDINGS
from core.portfolio import Portfolio
from reports import excel, terminal
from utils.logger import get_logger

logger = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="NSE Portfolio Tracker")
    p.add_argument(
        "--report",
        choices=["terminal", "excel", "all"],
        default="all",
        help="Which report(s) to generate (default: all)",
    )
    p.add_argument(
        "--no-cache",
        action="store_true",
        help="Force fresh price fetch, ignoring local cache",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    use_cache = not args.no_cache

    portfolio = Portfolio(HOLDINGS)

    try:
        portfolio.refresh(use_cache=use_cache)
    except Exception as e:
        logger.error(f"Failed to refresh portfolio: {e}")
        sys.exit(1)

    summary = portfolio.summary

    if args.report in ("terminal", "all"):
        terminal.print_report(summary)

    if args.report in ("excel", "all"):
        path = excel.generate(summary)
        print(f"✅  Excel report saved: {path}")


if __name__ == "__main__":
    main()
