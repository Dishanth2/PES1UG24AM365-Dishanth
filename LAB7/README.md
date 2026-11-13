# SE Lab 7: Fuzz Testing and Input Validation Bug Fixes

## Student Details
- **Name:** Dishanth
- **SRN:** PES1UG24AM365
- **Course:** Software Engineering Lab (UE24CS252AA)
- **Topic:** Fuzz Testing and Input Validation Bug Fixes (ATM Withdrawal)

---

## 1. Experiment Overview & Objectives

Traditional example-based unit tests typically only validate anticipated, well-formed inputs. In production environments, applications frequently encounter malformed, unexpected, or adversarial inputs. This experiment applies **property-based fuzz testing** using the **Hypothesis** framework to identify crash vulnerabilities and harden the Python ATM withdrawal application (`atm_withdrawal.py` / `processor.py`).

Key objectives:
1. **Automated Defect Discovery:** Use Hypothesis strategies to generate unexpected input types (arbitrary Unicode, None, numbers, bytes, and malformed strings).
2. **Root-Cause Analysis:** Utilize Hypothesis automatic test-case shrinking to identify minimal reproducible counterexamples.
3. **Application Hardening:** Fix input validation defects using explicit defensive validation without broad exception suppression.
4. **Verification:** Confirm that malformed inputs are handled safely (returning `None`) while normal valid-input behavior remains 100% intact.

---

## 2. Tools & Environment

- **Python Version:** 3.13.14
- **Test Framework:** `pytest` (v9.1.0)
- **Fuzz Testing Framework:** `hypothesis` (v6.170.15)
- **Operating System:** Windows 11

---

## 3. Application Architecture

The module `atm_withdrawal.py` (also available as `processor.py`) provides three core functions:

1. `notes_needed(amount)`:
   - **Valid Format:** String representing a non-negative integer amount, optionally containing commas (e.g., `'2,500'` or `'2500'`).
   - **Output:** Number of 100 currency notes needed: `amount // 100` where `amount >= 0`.
2. `mask_card(card_number)`:
   - **Valid Format:** 16-digit card number in 4 space-separated groups of 4 digits (e.g., `'1234 5678 9012 3456'`).
   - **Output:** Masked card string: `'XXXX XXXX XXXX ' + last_group`.
3. `average_withdrawal(amounts_csv)`:
   - **Valid Format:** Comma-separated non-negative integer withdrawal amounts (e.g., `'500,1000,2000'`).
   - **Output:** Integer floor average: `sum(amounts) // len(amounts)`.

---

## 4. Discovered Bugs & Minimal Counterexamples (Before Fix)

Running the Hypothesis fuzz suite against the original application exposed **6 critical failures** across all functions:

| Function | Minimal Counterexamples | Observed Exceptions / Behavior | Root Cause |
|:---|:---|:---|:---|
| `notes_needed` | `s = ''`<br/>`s = None`<br/>`s = b''`<br/>`amount = '-1'`<br/>`amount = 'abc'` | `ValueError: invalid literal for int()`<br/>`AttributeError: 'NoneType' has no replace`<br/>`TypeError: bytes-like required`<br/>Calculated negative note count (`-1`)<br/>`ValueError: invalid literal` | Unchecked `.replace(',', '')` without type validation. No validation for empty strings, non-numeric characters, or negative withdrawal amounts. |
| `mask_card` | `s = ''`<br/>`s = None`<br/>`s = b''`<br/>`card = '1234'`<br/>`card = '12 34 56 78'` | `IndexError: list index out of range`<br/>`AttributeError: 'NoneType' has no split`<br/>`TypeError: bytes-like required`<br/>`IndexError: list index out of range`<br/>Accepted invalid card format | Directly accessed `groups[3]` without validating list length. Did not validate 4-group structure, 4-digit token length, or non-digit characters. |
| `average_withdrawal` | `s = ''`<br/>`s = None`<br/>`s = b''`<br/>`text = ','`<br/>`text = '500,-1000,2000'` | `ValueError: invalid literal for int()`<br/>`AttributeError: 'NoneType' has no split`<br/>`TypeError: bytes-like required`<br/>`ValueError: invalid literal`<br/>Accepted negative withdrawal (`500`) | Unchecked `.split(',')` iteration converting empty or malformed tokens with `int()`. No validation for empty elements, non-numeric strings, or negative withdrawal amounts. |

---

## 5. Summary of Fixes Applied (Application Hardening)

A consistent invalid-input contract was implemented: **all functions safely return `None` when given invalid, malformed, or out-of-range input**. Broad `except Exception: return None` was avoided in favor of explicit defensive validation:

1. **`notes_needed(amount)`**:
   - Validates `isinstance(amount, str)` and rejects empty or whitespace-only strings.
   - Strips commas and ensures remaining string is non-empty.
   - Safely parses integer amount inside a targeted `try/except ValueError` block.
   - Enforces non-negative values (`val >= 0`).
   - Computes integer floor division `val // 100`.
2. **`mask_card(card_number)`**:
   - Validates `isinstance(card_number, str)` and rejects empty or whitespace-only strings.
   - Splits by whitespace and enforces exactly 4 groups (`len(groups) == 4`).
   - Verifies each group consists of exactly 4 digits (`len(g) == 4 and g.isdigit()`).
   - Returns normalized `'XXXX XXXX XXXX ' + groups[3]`.
3. **`average_withdrawal(amounts_csv)`**:
   - Validates `isinstance(amounts_csv, str)` and rejects empty or whitespace-only strings.
   - Splits by comma and verifies all tokens are non-empty (rejecting double, leading, or trailing commas).
   - Validates every token as integer with targeted `ValueError` handling.
   - Enforces non-negative withdrawal amounts (`val >= 0`).
   - Ensures non-empty list before integer floor division `sum(values) // len(values)`.

---

## 6. Execution Commands & Test Results

### 6.1. Running the Application Interactively
```bash
python atm_withdrawal.py
```
**Sample Inputs and Results:**
- Withdrawal amount: `2,500` $\rightarrow$ `25` notes of 100
- Card number: `1234 5678 9012 3456` $\rightarrow$ `XXXX XXXX XXXX 3456`
- Withdrawal CSV: `500,1000,2000` $\rightarrow$ `1166`

### 6.2. Running Hypothesis Fuzz Tests
```bash
python -m pytest -v test_atm_withdrawal.py
```

### 6.3. Summary of Test Results
- **Total Test Functions:** 9
- **Total Inputs Evaluated:** 900+ automatically generated test cases
- **Pre-Fix Result:** 6 Failed, 3 Passed
- **Post-Fix Result:** **9 Passed, 0 Failed (100% Success Rate)**

---

## 7. Deliverable Structure

```text
Lab 7/
│
├── atm_withdrawal.py                  # Hardened application code
├── processor.py                       # Alias application code
├── test_atm_withdrawal.py             # Hypothesis property-based fuzz tests
├── test_processor.py                  # Hypothesis property-based fuzz tests
├── README.md                          # Experiment documentation
├── LAB7_FuzzTesting_PES1UG24AM365.pdf # Complete formatted PDF report
├── Lab7_FuzzTesting_Report.pdf        # Standard named PDF report
│
└── screenshots/
    ├── 01_original_application.jpeg       # Original application run with valid inputs
    ├── 02_fuzz_failures_before_fix.jpeg   # Hypothesis failures on original code
    ├── 03_fixed_application.jpeg          # Hardened application run with valid inputs
    ├── 04_fuzz_tests_after_fix.jpeg       # All 9 Hypothesis tests passing after fixes
    ├── original_application.png           # Alternate screenshot name
    ├── failing_tests.png                  # Alternate screenshot name
    ├── fixed_application.png              # Alternate screenshot name
    └── passing_tests.png                  # Alternate screenshot name
```
