# SE Lab 6: Code and Branch Coverage Analysis

## Student Details
- **Name:** Dishanth
- **SRN:** PES1UG24AM365
- **Course:** Software Engineering Lab (UE24CS252AA)
- **Topic:** Code Coverage and Branch Coverage Analysis

---

## 1. Experiment Overview & Objectives

Software testing coverage metrics quantify how thoroughly a test suite exercises application source code. This experiment focuses on white-box testing strategies applied to an ATM withdrawal system:
1. **Code Coverage (Statement Coverage):** Ensures that every executable line and statement in the application module is executed at least once during testing.
2. **Branch Coverage (Decision Coverage):** Ensures that every boolean decision outcome evaluates to both `True` and `False`, exercising all control flow paths, compound condition branches, and boundary conditions.

---

## 2. Application Architecture

The application module under test is `atm_withdrawal.py`, containing three core business logic functions:

### 2.1. `withdraw(balance, amount, account_type, own_bank)`
Processes ATM cash withdrawals with daily limits and cross-bank fees:
- Daily limits: `{"savings": 25000, "current": 50000}`.
- Cross-bank fee: ₹20 base fee when `own_bank=False`; additional ₹10 surcharge when `amount > 10000`.
- Returns `"limit exceeded"` if `amount > DAILY_LIMIT[account_type]`.
- Returns `"insufficient funds"` if `amount + fee > balance`.
- Returns the updated balance on success.
- Input validation: Raises `ValueError("unknown account")` for invalid account types, and `ValueError("invalid amount")` if `amount <= 0` or `amount % 100 != 0`.

### 2.2. `pin_check(entered, actual, attempts)`
Validates ATM PIN entry with attempt tracking:
- Returns `"card blocked"` if `attempts >= 3` (card already locked).
- Returns `"ok"` if `entered == actual` (correct PIN).
- Returns `"card blocked"` if `attempts == 2` and PIN is wrong (3rd failed attempt).
- Returns `"retry"` otherwise (wrong PIN, attempts remaining).

### 2.3. `note_breakup(amount)`
Calculates denomination breakup for dispensing cash:
- Uses ₹500, ₹200, and ₹100 notes.
- Raises `ValueError("invalid amount")` if `amount % 100 != 0`.
- Returns a tuple `(notes_500, notes_200, notes_100)`.

---

## 3. Difference Between Code Coverage and Branch Coverage

| Aspect | Code Coverage (Statement Coverage) | Branch Coverage (Decision Coverage) |
|:---|:---|:---|
| **Definition** | Measures the percentage of executable statements executed by the test suite. | Measures the percentage of decision branch outcomes (True/False) traversed. |
| **Granularity** | Line / statement level. | Control flow branch / decision level. |
| **Decision Logic** | An `if` statement without an `else` achieves 100% statement coverage if executed when `True`, ignoring the `False` branch. | Requires tests for both `True` (branch taken) and `False` (branch skipped). |
| **Rigor** | Basic baseline; leaves edge conditions and alternate paths untested. | Stronger metric; subsumes statement coverage and validates boundary logic. |

---

## 4. Tools & Environment

- **Python Version:** 3.13.14
- **Test Framework:** `pytest` (v9.1.0)
- **Coverage Tool:** `coverage.py` (v7.17.3)
- **Operating System:** Windows 11

---

## 5. Test Suites and Execution Instructions

### 5.1. Code Coverage Test Suite (`CodeCoverageTest_PES1UG24AM365_atm_withdrawal.py`)

Exercises every executable statement across all three functions, handling normal paths, boundary returns, and exceptions.

**Execution Commands:**
```bash
coverage erase
coverage run --source=atm_withdrawal -m pytest -v CodeCoverageTest_PES1UG24AM365_atm_withdrawal.py
coverage report -m
```

*(Note: The code coverage run measured statement coverage using `--source=atm_withdrawal` without `--branch`.)*

**Verified Results:**
- **Test cases:** 25
- **Statements:** 34
- **Missed statements:** 0
- **Statement coverage:** **100%**

---

### 5.2. Branch Coverage Test Suite (`BranchCoverageTest_PES1UG24AM365_atm_withdrawal.py`)

Tests both `True` and `False` outcomes of every conditional decision, compound boolean sub-expressions, boundary values, and exception triggers:
- Valid and invalid account types (`"savings"`, `"current"`, unknown types).
- Amount validation (zero, negative, non-multiples of 100).
- Daily limit enforcement for both savings and current accounts.
- Own-bank vs. other-bank fee calculation (₹20 base fee, ₹10 surcharge for amounts > ₹10,000).
- Insufficient funds with and without fees.
- PIN check: correct vs. wrong, attempt boundaries (0, 1, 2, 3, >3).
- Card blocking on 3rd wrong attempt and pre-blocked states.
- Note denomination breakup: all remainder patterns (0, 100, 200, 300, 400 after ₹500 notes).
- Boundary values at exact daily limits, fee thresholds, and balance boundaries.

**Execution Commands:**
```bash
coverage erase
coverage run --branch --source=atm_withdrawal -m pytest -v BranchCoverageTest_PES1UG24AM365_atm_withdrawal.py
coverage report -m
```

**Verified Results:**
- **Test cases:** 63
- **Statements:** 34
- **Missed statements:** 0
- **Branches:** 22
- **Partial branches:** 0
- **Coverage:** **100%**

---

## 6. Coverage Summary Comparison

| Test Suite | Total Tests | Statements Covered | Missed Stmts | Statement Coverage | Branches Covered | Partial Branches | Branch Coverage |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Code Coverage Suite** | 25 | 34 / 34 | 0 | **100%** | N/A* | N/A* | N/A* |
| **Branch Coverage Suite** | 63 | 34 / 34 | 0 | **100%** | 22 / 22 | 0 | **100%** |

*\*Note: The code coverage suite was executed with `--source=atm_withdrawal` (without `--branch`) to measure statement coverage specifically.*

---

## 7. Deliverable File Structure

```text
Lab 6/
│
├── atm_withdrawal.py
├── test_atm_withdrawal.py
├── CodeCoverageTest_PES1UG24AM365_atm_withdrawal.py
├── BranchCoverageTest_PES1UG24AM365_atm_withdrawal.py
├── README.md
│
└── screenshots/
    ├── CodeCoverage.jpeg
    └── BranchCoverage.jpeg
```

---

## 8. Verification Screenshots

- **Code Coverage Screenshot:** [`screenshots/CodeCoverage.jpeg`](screenshots/CodeCoverage.jpeg)
  Demonstrates all 25 test cases passing and 100% statement coverage.
  
  ![Code Coverage](screenshots/CodeCoverage.jpeg)

- **Branch Coverage Screenshot:** [`screenshots/BranchCoverage.jpeg`](screenshots/BranchCoverage.jpeg)
  Demonstrates all 63 test cases passing, 22/22 branches covered, and 100% branch coverage.
  
  ![Branch Coverage](screenshots/BranchCoverage.jpeg)
