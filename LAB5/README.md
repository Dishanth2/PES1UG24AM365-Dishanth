# Lab 5: Static Code Analysis — Fitness Club Class Booking Ledger

**Your file:** `gym_system.py`

Follow the lab handout for the full instructions.

## About the Program

A booking ledger for gym classes such as Yoga, HIIT and Spin. It books members into classes up to a capacity limit, handles cancellations and exports the rosters to `gym_schedule.json`.

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to Do

### 1. Run It First

Run the program and read the output carefully:

```bash
python gym_system.py
```

It asks one question. Press Enter to use the default, then try a few inputs of your own. Not every problem in this file is something a tool will flag, so pay attention to output that looks wrong.

### 2. Install the Tools

```bash
pip install pylint bandit flake8
```

### 3. Run the Analysis and Save the Reports

```bash
pylint gym_system.py > pylint_report.txt
bandit -r gym_system.py > bandit_report.txt
flake8 gym_system.py > flake8_report.txt
```

### 4. Document the Issues

Document the identified issues in `issues.md` using this table. Include at least four rows, listing high- and medium-severity issues first.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Issue 1 | Security / Bug / Quality | Line number | Describe the identified issue | Explain the fix |
| Issue 2 | Security / Bug / Quality | Line number | Describe the identified issue | Explain the fix |
| Issue 3 | Security / Bug / Quality | Line number | Describe the identified issue | Explain the fix |
| Issue 4 | Security / Bug / Quality | Line number | Describe the identified issue | Explain the fix |

Replace the example rows with actual findings from your source code and analysis reports.

### 5. Fix the Code

Fix at least four of the issues documented in `issues.md`. Rerun all three tools to confirm the issues have been resolved. Repeat until you are satisfied.

The program should still perform its intended functions after the fixes.

### 6. Write the Reflection

Answer the four reflection questions from the lab handout in `reflection.md`.

## Deliverables

1. `gym_system.py` — cleaned code with at least four issues fixed.
2. `issues.md` — completed issue table.
3. `reflection.md` — answers to the reflection questions.

## Target

Aim for a Pylint score above **9.5/10** on the final file. A perfect score of 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.
