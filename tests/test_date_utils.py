"""Unit tests for ic_basilisk_toolkit.date_utils — IC-compatible date utilities.

These are pure-Python unit tests (no canister required).
Run: pytest tests/test_date_utils.py -v
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ic_basilisk_toolkit.date_utils import (
    add_days,
    add_months,
    date_str_to_epoch,
    day_of_week,
    day_of_year,
    days_in_month,
    days_in_year,
    diff_days,
    epoch_to_date_str,
    epoch_to_datetime_str,
    epoch_to_ic_time,
    ic_time_to_epoch,
    is_leap_year,
)

# ---------------------------------------------------------------------------
# Leap year
# ---------------------------------------------------------------------------


class TestLeapYear:
    def test_common_years(self):
        assert not is_leap_year(1970)
        assert not is_leap_year(2023)
        assert not is_leap_year(2025)
        assert not is_leap_year(1900)  # divisible by 100 but not 400

    def test_leap_years(self):
        assert is_leap_year(2000)  # divisible by 400
        assert is_leap_year(2024)
        assert is_leap_year(2028)
        assert is_leap_year(1972)

    def test_days_in_year(self):
        assert days_in_year(2024) == 366
        assert days_in_year(2023) == 365


# ---------------------------------------------------------------------------
# days_in_month
# ---------------------------------------------------------------------------


class TestDaysInMonth:
    def test_january(self):
        assert days_in_month(2025, 1) == 31

    def test_february_common(self):
        assert days_in_month(2023, 2) == 28

    def test_february_leap(self):
        assert days_in_month(2024, 2) == 29

    def test_april(self):
        assert days_in_month(2025, 4) == 30

    def test_all_months_2025(self):
        expected = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for m, exp in enumerate(expected, 1):
            assert days_in_month(2025, m) == exp, f"month {m}"

    def test_all_months_2024_leap(self):
        expected = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for m, exp in enumerate(expected, 1):
            assert days_in_month(2024, m) == exp, f"month {m}"


# ---------------------------------------------------------------------------
# epoch ↔ date string conversions
# ---------------------------------------------------------------------------


class TestEpochConversions:
    def test_unix_epoch(self):
        assert epoch_to_date_str(0) == "1970-01-01"

    def test_known_date(self):
        # 2024-01-01 00:00:00 UTC = 1704067200
        assert epoch_to_date_str(1704067200) == "2024-01-01"

    def test_roundtrip(self):
        for date_str in [
            "1970-01-01",
            "2000-02-29",
            "2024-12-31",
            "1999-12-31",
            "2025-06-15",
            "2030-01-01",
        ]:
            epoch = date_str_to_epoch(date_str)
            assert (
                epoch_to_date_str(epoch) == date_str
            ), f"roundtrip failed for {date_str}"

    def test_date_str_to_epoch_midnight(self):
        epoch = date_str_to_epoch("1970-01-02")
        assert epoch == 86400

    def test_leap_day(self):
        date = "2024-02-29"
        epoch = date_str_to_epoch(date)
        assert epoch_to_date_str(epoch) == date

    def test_end_of_year(self):
        date = "2025-12-31"
        epoch = date_str_to_epoch(date)
        assert epoch_to_date_str(epoch) == date

    def test_many_years_roundtrip(self):
        """Test every Jan 1 from 1970 to 2100."""
        for year in range(1970, 2101):
            date_str = f"{year}-01-01"
            epoch = date_str_to_epoch(date_str)
            assert epoch_to_date_str(epoch) == date_str, f"failed for {date_str}"


class TestDatetimeStr:
    def test_epoch_zero(self):
        assert epoch_to_datetime_str(0) == "1970-01-01 00:00:00"

    def test_known_datetime(self):
        # 2024-01-15 13:30:45 UTC
        epoch = date_str_to_epoch("2024-01-15") + 13 * 3600 + 30 * 60 + 45
        assert epoch_to_datetime_str(epoch) == "2024-01-15 13:30:45"

    def test_end_of_day(self):
        epoch = date_str_to_epoch("2025-06-15") + 23 * 3600 + 59 * 60 + 59
        assert epoch_to_datetime_str(epoch) == "2025-06-15 23:59:59"


# ---------------------------------------------------------------------------
# IC time conversions
# ---------------------------------------------------------------------------


class TestICTime:
    def test_ic_time_to_epoch(self):
        # 1 second in nanoseconds
        assert ic_time_to_epoch(1_000_000_000) == 1

    def test_epoch_to_ic_time(self):
        assert epoch_to_ic_time(1) == 1_000_000_000

    def test_roundtrip(self):
        epoch = 1704067200
        assert ic_time_to_epoch(epoch_to_ic_time(epoch)) == epoch

    def test_realistic_ic_time(self):
        # Typical IC time: ~1.7 trillion nanoseconds (year ~2024)
        ic_ns = 1_704_067_200_000_000_000
        epoch = ic_time_to_epoch(ic_ns)
        assert epoch_to_date_str(epoch) == "2024-01-01"


# ---------------------------------------------------------------------------
# add_days
# ---------------------------------------------------------------------------


class TestAddDays:
    def test_add_one_day(self):
        assert add_days("2025-01-01", 1) == "2025-01-02"

    def test_subtract_one_day(self):
        assert add_days("2025-01-01", -1) == "2024-12-31"

    def test_cross_month_boundary(self):
        assert add_days("2025-01-31", 1) == "2025-02-01"

    def test_cross_year_boundary(self):
        assert add_days("2024-12-31", 1) == "2025-01-01"

    def test_add_365_days_non_leap(self):
        assert add_days("2025-01-01", 365) == "2026-01-01"

    def test_add_366_days_leap(self):
        assert add_days("2024-01-01", 366) == "2025-01-01"

    def test_add_zero(self):
        assert add_days("2025-06-15", 0) == "2025-06-15"

    def test_add_large_number(self):
        result = add_days("2025-01-01", 3650)  # ~10 years
        epoch = date_str_to_epoch(result)
        assert epoch > date_str_to_epoch("2034-01-01")

    def test_leap_day_to_next_day(self):
        assert add_days("2024-02-29", 1) == "2024-03-01"

    def test_subtract_from_march_to_leap_feb(self):
        assert add_days("2024-03-01", -1) == "2024-02-29"


# ---------------------------------------------------------------------------
# add_months
# ---------------------------------------------------------------------------


class TestAddMonths:
    def test_add_one_month(self):
        assert add_months("2025-01-15", 1) == "2025-02-15"

    def test_add_twelve_months(self):
        assert add_months("2025-01-15", 12) == "2026-01-15"

    def test_subtract_one_month(self):
        assert add_months("2025-03-15", -1) == "2025-02-15"

    def test_day_clamping_feb(self):
        # Jan 31 + 1 month → Feb 28 (2025 is not leap)
        assert add_months("2025-01-31", 1) == "2025-02-28"

    def test_day_clamping_feb_leap(self):
        # Jan 31 + 1 month → Feb 29 (2024 is leap)
        assert add_months("2024-01-31", 1) == "2024-02-29"

    def test_cross_year_forward(self):
        assert add_months("2025-11-15", 3) == "2026-02-15"

    def test_cross_year_backward(self):
        assert add_months("2025-02-15", -3) == "2024-11-15"

    def test_add_zero_months(self):
        assert add_months("2025-06-15", 0) == "2025-06-15"

    def test_add_24_months(self):
        assert add_months("2025-06-15", 24) == "2027-06-15"


# ---------------------------------------------------------------------------
# day_of_year
# ---------------------------------------------------------------------------


class TestDayOfYear:
    def test_jan_1(self):
        assert day_of_year("2025-01-01") == 1

    def test_dec_31_non_leap(self):
        assert day_of_year("2025-12-31") == 365

    def test_dec_31_leap(self):
        assert day_of_year("2024-12-31") == 366

    def test_march_1_non_leap(self):
        assert day_of_year("2025-03-01") == 60  # 31 + 28 + 1

    def test_march_1_leap(self):
        assert day_of_year("2024-03-01") == 61  # 31 + 29 + 1

    def test_feb_29_leap(self):
        assert day_of_year("2024-02-29") == 60


# ---------------------------------------------------------------------------
# day_of_week
# ---------------------------------------------------------------------------


class TestDayOfWeek:
    def test_epoch_thursday(self):
        # 1970-01-01 was a Thursday
        assert day_of_week("1970-01-01") == 3  # 0=Mon, 3=Thu

    def test_known_monday(self):
        # 2025-04-28 is a Monday
        assert day_of_week("2025-04-28") == 0

    def test_known_sunday(self):
        # 2025-04-27 is a Sunday
        assert day_of_week("2025-04-27") == 6

    def test_known_saturday(self):
        # 2025-04-26 is a Saturday
        assert day_of_week("2025-04-26") == 5

    def test_known_wednesday(self):
        # 2025-01-01 is a Wednesday
        assert day_of_week("2025-01-01") == 2

    def test_range_always_0_to_6(self):
        """Check 365 consecutive days all produce 0..6."""
        base_epoch = date_str_to_epoch("2025-01-01")
        for d in range(365):
            date = epoch_to_date_str(base_epoch + d * 86400)
            dow = day_of_week(date)
            assert 0 <= dow <= 6, f"{date} gave {dow}"

    def test_week_cycle(self):
        """7 consecutive days should produce 0,1,2,3,4,5,6 in some rotation."""
        base_epoch = date_str_to_epoch("2025-01-06")  # Monday
        days = []
        for d in range(7):
            date = epoch_to_date_str(base_epoch + d * 86400)
            days.append(day_of_week(date))
        assert days == [0, 1, 2, 3, 4, 5, 6]


# ---------------------------------------------------------------------------
# diff_days
# ---------------------------------------------------------------------------


class TestDiffDays:
    def test_same_date(self):
        assert diff_days("2025-01-01", "2025-01-01") == 0

    def test_one_day(self):
        assert diff_days("2025-01-02", "2025-01-01") == 1

    def test_negative(self):
        assert diff_days("2025-01-01", "2025-01-02") == -1

    def test_full_year(self):
        assert diff_days("2026-01-01", "2025-01-01") == 365

    def test_leap_year(self):
        assert diff_days("2025-01-01", "2024-01-01") == 366

    def test_cross_century(self):
        assert diff_days("2001-01-01", "2000-01-01") == 366  # 2000 is leap


# ---------------------------------------------------------------------------
# Edge cases / consistency
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_feb_28_to_march_1_non_leap(self):
        assert add_days("2025-02-28", 1) == "2025-03-01"

    def test_feb_28_to_feb_29_leap(self):
        assert add_days("2024-02-28", 1) == "2024-02-29"

    def test_consistency_add_days_and_diff(self):
        """add_days(d, n) and diff_days should be inverse operations."""
        base = "2025-03-15"
        for n in [-365, -30, -1, 0, 1, 30, 365, 730]:
            result = add_days(base, n)
            assert diff_days(result, base) == n, f"n={n}"

    def test_century_boundary(self):
        assert epoch_to_date_str(date_str_to_epoch("1999-12-31")) == "1999-12-31"
        assert epoch_to_date_str(date_str_to_epoch("2000-01-01")) == "2000-01-01"

    def test_distant_future(self):
        date = "2100-12-31"
        assert epoch_to_date_str(date_str_to_epoch(date)) == date

    def test_many_months_roundtrip(self):
        """Adding 12 months to every month-start should give next year."""
        for m in range(1, 13):
            date = f"2025-{m:02d}-01"
            result = add_months(date, 12)
            assert result == f"2026-{m:02d}-01", f"failed for {date}"
