"""
Fuzz Testing Suite for processor.py using Hypothesis
Software Engineering Lab 7: Fuzz Testing and Input Validation Bug Fixes
Student: Dishanth (PES1UG24AM365)
"""

from hypothesis import given, settings, strategies as st
from processor import notes_needed, mask_card, average_withdrawal


# Strategy for arbitrary unexpected inputs: strings, None, numbers, bytes
arbitrary_unexpected_input = (
    st.text()
    | st.none()
    | st.integers()
    | st.floats()
    | st.binary()
)


def is_valid_integer(value):
    """Helper to check if a string can be parsed as an integer after stripping."""
    try:
        int(value.strip())
        return True
    except (ValueError, AttributeError):
        return False


# ============================================================================
# 1. notes_needed() Fuzz & Property Tests
# ============================================================================

@settings(max_examples=100)
@given(arbitrary_unexpected_input)
def test_notes_needed_no_crash(s):
    """Fuzz test notes_needed() with unexpected inputs: must not crash."""
    result = notes_needed(s)
    if result is not None:
        assert isinstance(result, int)
        assert result >= 0


@settings(max_examples=100)
@given(
    st.one_of(
        # Empty string
        st.just(""),
        # Whitespace-only string
        st.just("   "),
        # Non-numeric alphabetic strings
        st.text(alphabet=st.characters(categories=["L", "P"], exclude_characters=[","]), min_size=1),
        # Negative numbers formatted as string
        st.integers(max_value=-1).map(lambda x: str(x)),
        # Invalid punctuation or decimals
        st.sampled_from(["2,500.50", "abc", "$1000", "100-", "++200", ",,"]),
    )
)
def test_notes_needed_malformed_inputs(amount):
    """Verify that malformed or invalid amount inputs safely return None."""
    assert notes_needed(amount) is None


@settings(max_examples=100)
@given(
    amount=st.integers(min_value=0, max_value=10_000_000),
    use_commas=st.booleans()
)
def test_notes_needed_valid_properties(amount, use_commas):
    """Verify that valid integer withdrawal amounts correctly calculate notes of 100 needed."""
    formatted = f"{amount:,}" if use_commas else str(amount)
    result = notes_needed(formatted)
    assert result is not None
    assert result == amount // 100
    assert isinstance(result, int)
    assert result >= 0


# ============================================================================
# 2. mask_card() Fuzz & Property Tests
# ============================================================================

@settings(max_examples=100)
@given(arbitrary_unexpected_input)
def test_mask_card_no_crash(s):
    """Fuzz test mask_card() with unexpected inputs: must not crash."""
    result = mask_card(s)
    if result is not None:
        assert isinstance(result, str)
        assert result.startswith("XXXX XXXX XXXX ")
        assert len(result) == 19


@settings(max_examples=100)
@given(
    st.one_of(
        # Empty string
        st.just(""),
        # Whitespace-only
        st.just("    "),
        # Fewer than 4 groups
        st.sampled_from(["1234", "1234 5678", "1234 5678 9012"]),
        # More than 4 groups
        st.sampled_from(["1234 5678 9012 3456 7890", "1 2 3 4 5"]),
        # Groups with wrong length (not 4 digits per group)
        st.sampled_from(["12 34 56 78", "123 456 789 012", "12345 5678 9012 3456", "1234 5678 9012 345"]),
        # Non-digit groups
        st.sampled_from(["abcd efgh ijkl mnop", "1234 5678 9012 abcd", "1234 5678 abcd 3456"]),
    )
)
def test_mask_card_malformed_inputs(card):
    """Verify that malformed or invalid card numbers safely return None."""
    assert mask_card(card) is None


@settings(max_examples=100)
@given(
    g1=st.integers(min_value=0, max_value=9999).map(lambda x: f"{x:04d}"),
    g2=st.integers(min_value=0, max_value=9999).map(lambda x: f"{x:04d}"),
    g3=st.integers(min_value=0, max_value=9999).map(lambda x: f"{x:04d}"),
    g4=st.integers(min_value=0, max_value=9999).map(lambda x: f"{x:04d}"),
)
def test_mask_card_valid_properties(g1, g2, g3, g4):
    """Verify that valid 16-digit space-separated card numbers produce properly masked output."""
    card_str = f"{g1} {g2} {g3} {g4}"
    result = mask_card(card_str)
    assert result is not None
    assert result == f"XXXX XXXX XXXX {g4}"
    assert len(result) == 19


# ============================================================================
# 3. average_withdrawal() Fuzz & Property Tests
# ============================================================================

@settings(max_examples=100)
@given(arbitrary_unexpected_input)
def test_average_withdrawal_no_crash(s):
    """Fuzz test average_withdrawal() with unexpected inputs: must not crash."""
    result = average_withdrawal(s)
    if result is not None:
        assert isinstance(result, int)
        assert result >= 0


@settings(max_examples=100)
@given(
    st.one_of(
        # Empty string
        st.just(""),
        # Whitespace-only string
        st.just("   "),
        # Empty CSV elements (e.g. leading, trailing, or double commas)
        st.sampled_from([",", ",,", "500,,1000", "500,1000,", ",500,1000"]),
        # Non-integer tokens
        st.sampled_from(["500,abc,1000", "hello", "500,1000.5,2000", "foo,bar"]),
        # Negative withdrawal amounts
        st.sampled_from(["500,-1000,2000", "-500", "-100,-200,-300"]),
    )
)
def test_average_withdrawal_malformed_inputs(text):
    """Verify that malformed CSV inputs safely return None."""
    assert average_withdrawal(text) is None


@settings(max_examples=100)
@given(
    amounts=st.lists(st.integers(min_value=0, max_value=1_000_000), min_size=1, max_size=50)
)
def test_average_withdrawal_valid_properties(amounts):
    """Verify that valid CSV integer inputs compute the correct integer average."""
    amounts_csv = ",".join(str(a) for a in amounts)
    result = average_withdrawal(amounts_csv)
    assert result is not None
    assert result == sum(amounts) // len(amounts)
    assert isinstance(result, int)
