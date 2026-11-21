from datetime import date
from decimal import Decimal

import pytest

from scripts.generate_synthetic_data import main, money, random_date


def test_money_returns_decimal():
    result = money(50, 900)

    assert isinstance(result, Decimal)


def test_money_stays_within_range():
    result = money(50, 900)

    assert Decimal("50") <= result <= Decimal("900")


def test_money_returns_exact_value_when_bounds_are_equal():
    result = money(Decimal("125.50"), Decimal("125.50"))

    assert result == Decimal("125.50")


def test_random_date_returns_date():
    result = random_date(date(2025, 1, 1), date(2026, 1, 1))

    assert isinstance(result, date)


def test_random_date_stays_within_range():
    start = date(2025, 1, 1)
    end = date(2026, 1, 1)

    result = random_date(start, end)

    assert start <= result <= end


def test_random_date_supports_same_start_and_end():
    target = date(2026, 1, 1)

    assert random_date(target, target) == target


def test_random_date_rejects_end_before_start():
    with pytest.raises(ValueError):
        random_date(date(2026, 1, 2), date(2026, 1, 1))


def test_main_requires_database_password(monkeypatch):
    monkeypatch.delenv("PGPASSWORD", raising=False)

    with pytest.raises(RuntimeError, match="PGPASSWORD is not set"):
        main()
