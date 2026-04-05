"""
helpers.py — small reusable formatting and utility functions.
"""

from config.settings import CURRENCY_SYMBOL


def fmt_inr(value: float) -> str:
    """Format a number as Indian Rupees: ₹ 1,23,456.78"""
    # Indian number system: last 3 digits, then groups of 2
    s = f"{abs(value):,.2f}"
    parts = s.split(".")
    integer = parts[0].replace(",", "")
    if len(integer) > 3:
        last3 = integer[-3:]
        rest = integer[:-3]
        groups = []
        while len(rest) > 2:
            groups.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.append(rest)
        integer = ",".join(reversed(groups)) + "," + last3
    result = f"{integer}.{parts[1]}"
    sign = "-" if value < 0 else ""
    return f"{sign}{CURRENCY_SYMBOL} {result}"


def fmt_pct(value: float) -> str:
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"
