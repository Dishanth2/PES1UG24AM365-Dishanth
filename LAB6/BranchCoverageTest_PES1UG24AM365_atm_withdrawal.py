"""
Branch Coverage Test Suite for atm_withdrawal.py
Software Engineering Lab 6: Code and Branch Coverage
Student: Dishanth (PES1UG24AM365)

This test suite targets 100% Branch Coverage by exercising:
1. Every decision outcome (True and False) for each conditional statement.
2. Compound condition sub-decisions (MC/DC & condition coverage).
3. Boundary value analysis on daily limits, fee thresholds, PIN attempts,
   and note denomination breakup.
4. Exception paths and error states.
"""

import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ============================================================================
# 1. withdraw() - Decision & Branch Coverage
# ============================================================================

class TestWithdrawBranches:
    """Branch and decision coverage for withdraw()."""

    # --- Decision: account_type not in DAILY_LIMIT ---
    def test_unknown_account_branch_true(self):
        """Branch TRUE: unknown account type raises ValueError."""
        with pytest.raises(ValueError, match="unknown account"):
            withdraw(10000, 1000, "credit", True)

    def test_unknown_account_branch_false(self):
        """Branch FALSE: valid 'savings' account proceeds past check."""
        result = withdraw(5000, 1000, "savings", True)
        assert result == 4000

    def test_unknown_account_branch_false_current(self):
        """Branch FALSE: valid 'current' account proceeds past check."""
        result = withdraw(60000, 1000, "current", True)
        assert result == 59000

    # --- Compound Decision: amount <= 0 or amount % 100 != 0 ---
    # Condition 1: amount <= 0 (T/F), Condition 2: amount % 100 != 0 (T/F)

    def test_amount_zero_branch_cond1_true(self):
        """Condition 1 TRUE (amount == 0): raises ValueError."""
        with pytest.raises(ValueError, match="invalid amount"):
            withdraw(10000, 0, "savings", True)

    def test_amount_negative_branch_cond1_true(self):
        """Condition 1 TRUE (amount < 0): raises ValueError."""
        with pytest.raises(ValueError, match="invalid amount"):
            withdraw(10000, -100, "savings", True)

    def test_amount_not_multiple_100_branch_cond2_true(self):
        """Condition 2 TRUE (amount % 100 != 0, amount > 0): raises ValueError."""
        with pytest.raises(ValueError, match="invalid amount"):
            withdraw(10000, 150, "savings", True)

    def test_amount_valid_branch_both_false(self):
        """Both FALSE (amount > 0 and amount % 100 == 0): proceeds."""
        assert withdraw(5000, 100, "savings", True) == 4900

    # --- Decision: amount > DAILY_LIMIT[account_type] ---
    def test_over_daily_limit_savings_branch_true(self):
        """Branch TRUE: savings amount 26000 > 25000 limit."""
        assert withdraw(50000, 26000, "savings", True) == "limit exceeded"

    def test_over_daily_limit_current_branch_true(self):
        """Branch TRUE: current amount 51000 > 50000 limit."""
        assert withdraw(100000, 51000, "current", True) == "limit exceeded"

    def test_at_daily_limit_savings_branch_false(self):
        """Branch FALSE (boundary): savings amount 25000 == 25000 limit."""
        assert withdraw(30000, 25000, "savings", True) == 5000

    def test_at_daily_limit_current_branch_false(self):
        """Branch FALSE (boundary): current amount 50000 == 50000 limit."""
        assert withdraw(60000, 50000, "current", True) == 10000

    def test_below_daily_limit_branch_false(self):
        """Branch FALSE: amount well below limit."""
        assert withdraw(10000, 1000, "savings", True) == 9000

    # --- Decision: not own_bank ---
    def test_own_bank_branch_false(self):
        """Branch FALSE (not own_bank is False): own_bank=True -> no fee."""
        assert withdraw(5000, 1000, "savings", True) == 4000

    def test_other_bank_branch_true(self):
        """Branch TRUE (not own_bank is True): own_bank=False -> fee applied."""
        # fee = 20; 5000 - 1000 - 20 = 3980
        assert withdraw(5000, 1000, "savings", False) == 3980

    # --- Decision: amount > 10000 (nested inside not own_bank) ---
    def test_other_bank_small_amount_branch_false(self):
        """Branch FALSE: other bank, amount <= 10000 -> fee = 20 only."""
        # fee = 20; 20000 - 10000 - 20 = 9980
        assert withdraw(20000, 10000, "savings", False) == 9980

    def test_other_bank_amount_at_boundary_10000_branch_false(self):
        """Branch FALSE (boundary): amount == 10000 exactly -> fee = 20."""
        assert withdraw(15000, 10000, "savings", False) == 4980

    def test_other_bank_large_amount_branch_true(self):
        """Branch TRUE: other bank, amount > 10000 -> fee = 20 + 10 = 30."""
        # fee = 30; 30000 - 15000 - 30 = 14970
        assert withdraw(30000, 15000, "savings", False) == 14970

    def test_other_bank_amount_at_boundary_10100_branch_true(self):
        """Branch TRUE (boundary): amount == 10100 -> fee = 30."""
        # fee = 30; 15000 - 10100 - 30 = 4870
        assert withdraw(15000, 10100, "savings", False) == 4870

    # --- Decision: amount + fee > balance ---
    def test_insufficient_funds_own_bank_branch_true(self):
        """Branch TRUE: own bank, amount > balance -> insufficient funds."""
        assert withdraw(500, 1000, "savings", True) == "insufficient funds"

    def test_insufficient_funds_other_bank_branch_true(self):
        """Branch TRUE: other bank, amount + fee > balance."""
        # amount=1000, fee=20, total=1020 > balance=1000
        assert withdraw(1000, 1000, "savings", False) == "insufficient funds"

    def test_insufficient_funds_other_bank_large_branch_true(self):
        """Branch TRUE: other bank, large amount + fee > balance."""
        # amount=15000, fee=30, total=15030 > balance=15000
        assert withdraw(15000, 15000, "savings", False) == "insufficient funds"

    def test_sufficient_funds_branch_false(self):
        """Branch FALSE: amount + fee <= balance -> returns new balance."""
        assert withdraw(10000, 5000, "savings", True) == 5000

    def test_exact_balance_branch_false(self):
        """Branch FALSE (boundary): amount + fee == balance exactly."""
        # own bank, no fee -> 1000 - 1000 = 0
        assert withdraw(1000, 1000, "savings", True) == 0

    def test_exact_balance_with_fee_branch_false(self):
        """Branch FALSE (boundary): amount + fee == balance with other bank fee."""
        # other bank, amount=1000, fee=20 -> total=1020 == balance
        assert withdraw(1020, 1000, "savings", False) == 0


# ============================================================================
# 2. pin_check() - Decision & Boundary Coverage
# ============================================================================

class TestPinCheckBranches:
    """Branch and boundary coverage for pin_check()."""

    # --- Decision: attempts >= 3 ---
    def test_attempts_at_boundary_3_branch_true(self):
        """Branch TRUE (boundary): attempts == 3 -> card blocked."""
        assert pin_check(1234, 5678, 3) == "card blocked"

    def test_attempts_above_3_branch_true(self):
        """Branch TRUE: attempts > 3 -> card blocked regardless of pin."""
        assert pin_check(1234, 1234, 5) == "card blocked"

    def test_attempts_below_3_branch_false(self):
        """Branch FALSE: attempts < 3 -> proceeds to pin check."""
        assert pin_check(1234, 1234, 0) == "ok"

    # --- Decision: entered == actual ---
    def test_correct_pin_branch_true_attempt_0(self):
        """Branch TRUE: correct pin on attempt 0 -> ok."""
        assert pin_check(1111, 1111, 0) == "ok"

    def test_correct_pin_branch_true_attempt_1(self):
        """Branch TRUE: correct pin on attempt 1 -> ok."""
        assert pin_check(5555, 5555, 1) == "ok"

    def test_correct_pin_branch_true_attempt_2(self):
        """Branch TRUE: correct pin on attempt 2 -> ok."""
        assert pin_check(9999, 9999, 2) == "ok"

    def test_wrong_pin_branch_false(self):
        """Branch FALSE: wrong pin -> proceeds to attempt check."""
        assert pin_check(1234, 5678, 0) == "retry"

    # --- Decision: attempts == 2 ---
    def test_wrong_pin_attempt_2_branch_true(self):
        """Branch TRUE: wrong pin on attempt 2 -> card blocked (3rd wrong try)."""
        assert pin_check(1234, 5678, 2) == "card blocked"

    def test_wrong_pin_attempt_0_branch_false(self):
        """Branch FALSE: wrong pin on attempt 0 -> retry."""
        assert pin_check(1234, 5678, 0) == "retry"

    def test_wrong_pin_attempt_1_branch_false(self):
        """Branch FALSE: wrong pin on attempt 1 -> retry."""
        assert pin_check(1234, 5678, 1) == "retry"


# ============================================================================
# 3. note_breakup() - Decision & Branch Coverage
# ============================================================================

class TestNoteBreakupBranches:
    """Branch and boundary coverage for note_breakup()."""

    # --- Decision: amount % 100 != 0 ---
    def test_invalid_amount_branch_true(self):
        """Branch TRUE: amount not divisible by 100 raises ValueError."""
        with pytest.raises(ValueError, match="invalid amount"):
            note_breakup(250)

    def test_invalid_amount_branch_true_odd(self):
        """Branch TRUE: odd amount raises ValueError."""
        with pytest.raises(ValueError, match="invalid amount"):
            note_breakup(99)

    def test_valid_amount_branch_false(self):
        """Branch FALSE: amount divisible by 100 proceeds."""
        result = note_breakup(500)
        assert result == (1, 0, 0)

    # --- Decision: remaining >= 200 ---
    def test_remaining_at_boundary_200_branch_true(self):
        """Branch TRUE (boundary): remainder = 200 -> uses 200-note."""
        # 700: 500s = 1, remainder = 200 -> 200s = 1, 100s = 0
        assert note_breakup(700) == (1, 1, 0)

    def test_remaining_above_200_branch_true(self):
        """Branch TRUE: remainder = 400 -> uses 200-notes."""
        # 900: 500s = 1, remainder = 400 -> 200s = 2, 100s = 0
        assert note_breakup(900) == (1, 2, 0)

    def test_remaining_300_branch_true(self):
        """Branch TRUE: remainder = 300 -> 200s = 1, 100s = 1."""
        # 800: 500s = 1, remainder = 300 -> 200s = 1, 100s = 1
        assert note_breakup(800) == (1, 1, 1)

    def test_remaining_below_200_branch_false(self):
        """Branch FALSE: remainder = 100 -> 200s = 0, uses 100-note."""
        # 600: 500s = 1, remainder = 100 -> 200s = 0, 100s = 1
        assert note_breakup(600) == (1, 0, 1)

    def test_remaining_zero_branch_false(self):
        """Branch FALSE (boundary): remainder = 0 -> no extra notes needed."""
        # 1000: 500s = 2, remainder = 0 -> 200s = 0, 100s = 0
        assert note_breakup(1000) == (2, 0, 0)

    # --- Additional breakup scenarios for complete branch exercise ---
    def test_breakup_minimum_100(self):
        """Minimum amount: 100 -> 500s = 0, remainder = 100 < 200."""
        assert note_breakup(100) == (0, 0, 1)

    def test_breakup_200_only(self):
        """Amount 200: 500s = 0, remainder = 200 >= 200 -> 200s = 1."""
        assert note_breakup(200) == (0, 1, 0)

    def test_breakup_300_mixed(self):
        """Amount 300: 500s = 0, remainder = 300 -> 200s = 1, 100s = 1."""
        assert note_breakup(300) == (0, 1, 1)

    def test_breakup_400(self):
        """Amount 400: 500s = 0, remainder = 400 -> 200s = 2, 100s = 0."""
        assert note_breakup(400) == (0, 2, 0)

    @pytest.mark.parametrize("amount, expected", [
        (500, (1, 0, 0)),
        (1000, (2, 0, 0)),
        (1500, (3, 0, 0)),
        (2000, (4, 0, 0)),
        (2500, (5, 0, 0)),
    ])
    def test_breakup_exact_multiples_of_500(self, amount, expected):
        """Verify amounts that are exact multiples of 500."""
        assert note_breakup(amount) == expected

    @pytest.mark.parametrize("amount, expected", [
        (100, (0, 0, 1)),
        (200, (0, 1, 0)),
        (300, (0, 1, 1)),
        (400, (0, 2, 0)),
        (600, (1, 0, 1)),
        (700, (1, 1, 0)),
        (800, (1, 1, 1)),
        (900, (1, 2, 0)),
        (1100, (2, 0, 1)),
        (1200, (2, 1, 0)),
        (1300, (2, 1, 1)),
        (1400, (2, 2, 0)),
    ])
    def test_breakup_all_remainder_patterns(self, amount, expected):
        """Verify all possible remainder patterns (0, 100, 200, 300, 400)."""
        assert note_breakup(amount) == expected

