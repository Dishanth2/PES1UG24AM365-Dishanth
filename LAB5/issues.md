# Static Code Analysis Issue Inventory — Fitness Club Class Booking Ledger

**Student SRN:** PES1UG24AM365  
**Target file:** `gym_system.py`  
**Assigned repository:** `https://github.com/SETAPESU26/L5_04_fitness_booking`

> Line numbers below refer to the original starter script. Re-run the tools locally to capture the exact report line numbers and messages for your environment.

## Issue summary

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Shell command injection risk | Security | 23 | `os.system("rm -f " + prefix + "*.json")` builds a shell command from a string. | Replaced shell execution with `pathlib.Path.glob()` and `unlink()`, and validate the prefix. |
| Mutable default argument | Bug | 8 | `attendance_log=[]` reuses the same list between calls. | Default to `None` and initialize a new list inside the function. |
| Incorrect capacity boundary | Logic bug | 11 | `len(rosters[class_name]) > capacity` allows one extra booking. | Reject a booking when the current count is `>=` capacity. |
| Broad exception handler | Reliability | 17–18 | Bare `except` hides every exception and makes failures hard to diagnose. | Catch only `ValueError` when a member is not present. |
| File handle not managed / encoding omitted | Reliability | 21–22 | `open()` is not used with a context manager and no encoding is specified. | Use `with open(..., encoding="utf-8")`. |
| Invalid class accepted | Logic bug | 10, 31 | Unknown class names can create rosters with no configured capacity. | Validate class names before booking and when setting capacity. |
| Negative capacity accepted | Input validation | 32 | A negative seat count is stored and produces confusing results. | Require a non-negative integer capacity. |
| Invalid guest count | Input validation | 35, 41 | The input is converted directly to `int`; negative values and invalid text are not handled cleanly. | Validate non-negative counts; `main()` still expects a valid integer input. |
| Non-PEP 8 function name | Style | 25 | `addMembers` uses camelCase. | Renamed to `add_members`. |
| Script runs on import | Maintainability | 45 | Calling `main()` unconditionally starts interactive input when imported. | Add the `if __name__ == "__main__":` guard. |

## Verification checklist

Run these commands from the repository directory and save the output after fixes:

```bash
pylint gym_system.py > pylint_report.txt
bandit -r gym_system.py > bandit_report.txt
flake8 gym_system.py > flake8_report.txt
```

Review the reports and update this file with any additional findings and exact final results. Do not claim a clean scan unless the local tool output confirms it.
