"""
Basilisk Toolkit — IC-compatible date utilities.

``datetime`` / ``calendar`` from CPython's stdlib are not reliably
available in the WASM environment used by Basilisk.  This module
provides pure-arithmetic helpers for date manipulation inside canisters.

All functions work with:
  - **epoch seconds** (int) — seconds since 1970-01-01 00:00:00 UTC
  - **date strings** — ``"YYYY-MM-DD"`` ISO format
  - **IC time** — nanoseconds from ``ic.time()``

Usage::

    from ic_basilisk_toolkit.date_utils import (
        epoch_to_date_str, date_str_to_epoch, ic_time_to_epoch,
        add_days, days_in_month, day_of_year,
    )
"""


def is_leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def days_in_month(year: int, month: int) -> int:
    """Return number of days in the given month."""
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if month in (4, 6, 9, 11):
        return 30
    return 29 if is_leap_year(year) else 28


def days_in_year(year: int) -> int:
    return 366 if is_leap_year(year) else 365


def _days_from_epoch(year: int, month: int, day: int) -> int:
    """Total days from 1970-01-01 to the given date."""
    d = 0
    for y in range(1970, year):
        d += days_in_year(y)
    for m in range(1, month):
        d += days_in_month(year, m)
    d += day - 1
    return d


def _date_from_epoch_days(total_days: int):
    """Convert total days since epoch to (year, month, day)."""
    y = 1970
    while True:
        dy = days_in_year(y)
        if total_days < dy:
            break
        total_days -= dy
        y += 1
    m = 1
    while True:
        dm = days_in_month(y, m)
        if total_days < dm:
            break
        total_days -= dm
        m += 1
    return y, m, total_days + 1


# ── Conversions ──────────────────────────────────────────────────────

def epoch_to_date_str(epoch_seconds: int) -> str:
    """Convert epoch seconds to ``"YYYY-MM-DD"``."""
    total_days = epoch_seconds // 86400
    y, m, d = _date_from_epoch_days(total_days)
    return f"{y:04d}-{m:02d}-{d:02d}"


def epoch_to_datetime_str(epoch_seconds: int) -> str:
    """Convert epoch seconds to ``"YYYY-MM-DD HH:MM:SS"``."""
    total_days = epoch_seconds // 86400
    remainder = epoch_seconds % 86400
    y, m, d = _date_from_epoch_days(total_days)
    h = remainder // 3600
    remainder %= 3600
    mi = remainder // 60
    s = remainder % 60
    return f"{y:04d}-{m:02d}-{d:02d} {h:02d}:{mi:02d}:{s:02d}"


def date_str_to_epoch(date_str: str) -> int:
    """Convert ``"YYYY-MM-DD"`` to epoch seconds (midnight UTC)."""
    parts = date_str.split("-")
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    return _days_from_epoch(y, m, d) * 86400


def ic_time_to_epoch(ic_time_ns: int) -> int:
    """Convert ``ic.time()`` nanoseconds to epoch seconds."""
    return ic_time_ns // 1_000_000_000


def epoch_to_ic_time(epoch_seconds: int) -> int:
    """Convert epoch seconds to nanosecond IC time."""
    return epoch_seconds * 1_000_000_000


# ── Arithmetic ───────────────────────────────────────────────────────

def add_days(date_str: str, n: int) -> str:
    """Add *n* days to a ``"YYYY-MM-DD"`` string (negative = subtract)."""
    epoch = date_str_to_epoch(date_str)
    return epoch_to_date_str(epoch + n * 86400)


def add_months(date_str: str, n: int) -> str:
    """Add *n* months, clamping day to valid range."""
    parts = date_str.split("-")
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    m += n
    while m > 12:
        m -= 12
        y += 1
    while m < 1:
        m += 12
        y -= 1
    max_d = days_in_month(y, m)
    d = min(d, max_d)
    return f"{y:04d}-{m:02d}-{d:02d}"


def day_of_year(date_str: str) -> int:
    """1-based day of year for a ``"YYYY-MM-DD"`` string."""
    parts = date_str.split("-")
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    total = d
    for mon in range(1, m):
        total += days_in_month(y, mon)
    return total


def day_of_week(date_str: str) -> int:
    """Day of week: 0=Monday … 6=Sunday (ISO 8601)."""
    epoch = date_str_to_epoch(date_str)
    # 1970-01-01 was a Thursday (3 in 0=Mon scheme)
    return (epoch // 86400 + 3) % 7


def diff_days(date_a: str, date_b: str) -> int:
    """Signed difference *date_a - date_b* in days."""
    return (date_str_to_epoch(date_a) - date_str_to_epoch(date_b)) // 86400
