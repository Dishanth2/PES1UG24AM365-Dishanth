# Lab 5: Static Code Analysis — Reflection Report

**Student SRN:** PES1UG24AM365  
**Assigned repository:** `https://github.com/SETAPESU26/L5_04_fitness_booking`  
**File analyzed:** `gym_system.py`

## Question 1: How does static analysis impact code security?

Static analysis checks source code without running the program and can highlight risky patterns early. In this fitness booking program, the most important security concern was the use of `os.system()` to delete old export files. Building a shell command from a string can be dangerous because special characters may change what the shell executes. I replaced it with Python's `pathlib` file operations and checked that the prefix is a simple filename prefix. Bandit can help detect common risky patterns, but the findings still need to be reviewed in context.

## Question 2: How does static analysis improve code quality and maintainability?

Pylint and Flake8 help identify naming, formatting, and programming-practice problems. The original program used a mutable default list in `book_class`, a camelCase function name (`addMembers`), an unclosed-by-context-manager file operation, and a broad exception handler. I changed the list default to `None`, renamed the function to `add_members`, used a `with` statement with UTF-8 encoding, and caught only the expected `ValueError`. These changes make the code easier to understand and reduce hidden bugs.

I also fixed a booking boundary bug: the original condition allowed an extra member because it checked whether the roster length was greater than the capacity. It now rejects bookings when the roster has reached capacity.

## Question 3: What are the limitations of static code analysis tools?

Static analysis tools cannot understand every business requirement or guarantee that a program behaves correctly in all situations. For example, a tool may not know whether the gym's capacity values or guest-booking rules are appropriate. Tools can also report false positives or miss problems that only appear when the program runs with particular input or state. For this reason, static analysis should be combined with manual review and runtime tests. The booking capacity boundary should be tested with a full class, and invalid class names, negative capacities, cancellations, and export behavior should also be checked.

## Question 4: How can static analysis be integrated into the software development life cycle?

Static analysis can be run by developers before committing changes and automatically in a continuous integration pipeline for every pull request. Pylint can check code quality, Flake8 can check style, and Bandit can identify common security risks. A team can configure the pipeline to fail when important checks fail, so issues are corrected before merging. The reports should be reviewed regularly, and automated checks should be supported by tests and human code review.

## Verification note

The corrected source code was prepared for this submission. The analysis tools were not available in the file-preparation environment, and package installation could not reach the package index. Therefore, no final Pylint score or clean Bandit/Flake8 result is claimed here. Run the three commands in the repository and record their actual output before submitting.
