"""
charts.py — generates portfolio charts using matplotlib.

Install extra dep:  pip install matplotlib
"""

from pathlib import Path

from config.settings import EXPORTS_DIR
from core.models import PortfolioSummary


def _check_matplotlib():
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        raise ImportError(
            "matplotlib is required for charts.\n"
            "Install it with:  pip install matplotlib"
        )


def allocation_pie(summary: PortfolioSummary, output_path: Path | None = None) -> Path:
    """Pie chart of portfolio allocation by market value."""
    plt = _check_matplotlib()

    holdings = [h for h in summary.holdings if h.market_value]
    labels = [h.name for h in holdings]
    sizes  = [h.market_value for h in holdings]

    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.82,
    )
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9)
    ax.set_title(
        f"Portfolio Allocation — {summary.generated_at.strftime('%d %b %Y')}",
        fontsize=13, pad=20,
    )
    plt.tight_layout()

    if output_path is None:
        ts = summary.generated_at.strftime("%Y%m%d_%H%M")
        output_path = EXPORTS_DIR / f"Allocation_{ts}.png"

    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def pnl_bar(summary: PortfolioSummary, output_path: Path | None = None) -> Path:
    """Horizontal bar chart of P&L % per holding."""
    plt = _check_matplotlib()

    holdings = [h for h in summary.holdings if h.pnl_pct is not None and h.avg_price > 0]
    holdings.sort(key=lambda h: h.pnl_pct)

    names  = [h.name for h in holdings]
    values = [h.pnl_pct for h in holdings]
    colors = ["#C6EFCE" if v >= 0 else "#FFC7CE" for v in values]

    fig, ax = plt.subplots(figsize=(10, max(4, len(names) * 0.45)))
    bars = ax.barh(names, values, color=colors, edgecolor="gray", linewidth=0.5)
    ax.axvline(0, color="gray", linewidth=0.8, linestyle="--")
    ax.set_xlabel("P&L (%)")
    ax.set_title(
        f"P&L by Holding — {summary.generated_at.strftime('%d %b %Y')}",
        fontsize=13, pad=12,
    )
    for bar, val in zip(bars, values):
        ax.text(
            val + (0.3 if val >= 0 else -0.3),
            bar.get_y() + bar.get_height() / 2,
            f"{val:+.1f}%",
            va="center", ha="left" if val >= 0 else "right", fontsize=8,
        )
    plt.tight_layout()

    if output_path is None:
        ts = summary.generated_at.strftime("%Y%m%d_%H%M")
        output_path = EXPORTS_DIR / f"PnL_Bar_{ts}.png"

    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path
