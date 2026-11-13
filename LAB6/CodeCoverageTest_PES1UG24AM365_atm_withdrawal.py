"""
Code Coverage Test Suite for atm_withdrawal.py
Software Engineering Lab 6: Code and Branch Coverage
Student: Dishanth (PES1UG24AM365)
"""

import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ============================================================================
# Tests for withdraw()
# ============================================================================

def test_withdraw_unknown_account():
    """Verify that an unknown account type raises a ValueError."""
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(10000, 1000, "credit", True)


def test_withdraw_zero_amount():
    """Verify that a zero amount raises a ValueError."""
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(10000, 0, "savings", True)


def test_withdraw_negative_amount():
    """Verify that a negative amount raises a ValueError."""
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(10000, -500, "savings", True)


def test_withdraw_not_multiple_of_100():
    """Verify that an amount not divisible by 100 raises a ValueError."""
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(10000, 250, "savings", True)


def test_withdraw_exceeds_daily_limit_savings():
    """Verify savings daily limit (25000) is enforced."""
    assert withdraw(50000, 26000, "savings", True) == "limit exceeded"


def test_withdraw_exceeds_daily_limit_current():
    """Verify current daily limit (50000) is enforced."""
    assert withdraw(100000, 51000, "current", True) == "limit exceeded"


def test_withdraw_own_bank_no_fee():
    """Verify no fee is charged for own-bank withdrawals."""
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_withdraw_other_bank_small_amount_fee():
    """Verify flat ₹20 fee for other-bank withdrawals up to ₹10000."""
    assert withdraw(5000, 1000, "savings", False) == 3980


def test_withdraw_other_bank_large_amount_fee():
    """Verify additional ₹10 fee for other-bank withdrawals above ₹10000."""
    # fee = 20 + 10 = 30; result = 20000 - 15000 - 30 = 4970
    assert withdraw(20000, 15000, "savings", False) == 4970


def test_withdraw_insufficient_funds():
    """Verify insufficient funds when balance cannot cover amount + fee."""
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


def test_withdraw_successful_current_account():
    """Verify successful withdrawal from current account."""
    assert withdraw(60000, 50000, "current", True) == 10000


def test_withdraw_at_daily_limit_savings():
    """Verify withdrawal at exactly the savings daily limit."""
    assert withdraw(30000, 25000, "savings", True) == 5000


def test_withdraw_at_daily_limit_current():
    """Verify withdrawal at exactly the current daily limit."""
    assert withdraw(60000, 50000, "current", True) == 10000


# ============================================================================
# Tests for pin_check()
# ============================================================================

def test_pin_check_already_blocked():
    """Verify card is blocked when attempts >= 3."""
    assert pin_check(1234, 5678, 3) == "card blocked"
    assert pin_check(1234, 1234, 4) == "card blocked"


def test_pin_check_correct_pin():
    """Verify correct pin returns 'ok'."""
    assert pin_check(1234, 1234, 0) == "ok"
    assert pin_check(9999, 9999, 2) == "ok"


def test_pin_check_wrong_pin_third_attempt():
    """Verify wrong pin on the 3rd attempt (index 2) blocks the card."""
    assert pin_check(1234, 5678, 2) == "card blocked"


def test_pin_check_wrong_pin_retry():
    """Verify wrong pin with remaining attempts returns 'retry'."""
    assert pin_check(1234, 5678, 0) == "retry"
    assert pin_check(1234, 5678, 1) == "retry"


# ============================================================================
# Tests for note_breakup()
# ============================================================================

def test_note_breakup_invalid_amount():
    """Verify non-multiples of 100 raise a ValueError."""
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(150)


def test_note_breakup_only_500s():
    """Verify breakup when amount is exact multiple of 500."""
    assert note_breakup(1000) == (2, 0, 0)
    assert note_breakup(2500) == (5, 0, 0)


def test_note_breakup_with_200s():
    """Verify breakup when remainder >= 200 after 500s."""
    # 1200: 500s = 2, remainder = 200 -> 200s = 1, 100s = 0
    assert note_breakup(1200) == (2, 1, 0)
    # 1400: 500s = 2, remainder = 400 -> 200s = 2, 100s = 0
    assert note_breakup(1400) == (2, 2, 0)


def test_note_breakup_with_100s():
    """Verify breakup when remainder < 200 after 500s (only 100s)."""
    # 600: 500s = 1, remainder = 100 -> 200s = 0, 100s = 1
    assert note_breakup(600) == (1, 0, 1)


def test_note_breakup_with_all_notes():
    """Verify breakup uses 500s, 200s, and 100s together."""
    # 1300: 500s = 2, remainder = 300 -> 200s = 1, remaining = 100, 100s = 1
    assert note_breakup(1300) == (2, 1, 1)


def test_note_breakup_minimum():
    """Verify breakup of smallest valid amount."""
    assert note_breakup(100) == (0, 0, 1)


def test_note_breakup_200():
    """Verify breakup of 200."""
    assert note_breakup(200) == (0, 1, 0)


def test_note_breakup_500():
    """Verify breakup of exactly 500."""
    assert note_breakup(500) == (1, 0, 0)

