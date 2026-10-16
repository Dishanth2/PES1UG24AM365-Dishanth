"""Fitness club class booking ledger with safe roster management."""

import json
from pathlib import Path

CLASS_CAPACITY = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}


def book_class(member_id, class_name, attendance_log=None):
    """Book a member into a class if it exists and has available seats."""
    if class_name not in CLASS_CAPACITY:
        print("Unknown class:", class_name)
        return False

    if attendance_log is None:
        attendance_log = []

    class_roster = rosters.setdefault(class_name, [])
    if len(class_roster) >= CLASS_CAPACITY[class_name]:
        print("Class full:", class_name)
        return False

    class_roster.append(member_id)
    attendance_log.append(f"{member_id} -> {class_name}")
    return True


def cancel_booking(member_id, class_name):
    """Cancel a member's booking without hiding unrelated exceptions."""
    class_roster = rosters.get(class_name, [])
    try:
        class_roster.remove(member_id)
    except ValueError:
        print("Nothing to cancel")


def set_capacity(class_name, seats):
    """Set a non-negative capacity for a known class."""
    if class_name not in CLASS_CAPACITY:
        raise ValueError(f"Unknown class: {class_name}")
    if isinstance(seats, bool) or not isinstance(seats, int) or seats < 0:
        raise ValueError("seats must be a non-negative integer")
    CLASS_CAPACITY[class_name] = seats


def add_members(class_name, count):
    """Add up to count guest bookings to a class."""
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ValueError("count must be a non-negative integer")
    for guest_number in range(count):
        book_class(f"GUEST-{guest_number}", class_name)


def export_roster(file_name="gym_schedule.json"):
    """Write the current class rosters as UTF-8 JSON."""
    with open(file_name, "w", encoding="utf-8") as file_handle:
        json.dump(rosters, file_handle, indent=2)


def clear_old_exports(prefix="old_"):
    """Delete matching old JSON exports in the current directory safely."""
    if not prefix or not all(char.isalnum() or char in "_-" for char in prefix):
        raise ValueError("prefix may contain only letters, digits, underscores, and hyphens")
    for export_path in Path(".").glob(f"{prefix}*.json"):
        if export_path.is_file():
            export_path.unlink()


def show_rosters():
    """Print the current class rosters."""
    for class_name, members in rosters.items():
        print(class_name, ":", ", ".join(str(member) for member in members))


def main():
    """Run a short interactive demonstration of the booking ledger."""
    book_class("M1", "Yoga")
    book_class("M2", "Yoga")
    book_class("M3", "Yoga")
    book_class("M4", "Yoga")
    book_class("55", "HIIT")
    book_class("M5", "Pilates")
    set_capacity("Spin", 0)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")

    response = input("How many walk-in guests for HIIT? (Enter for 1): ").strip()
    guest_count = int(response) if response else 1
    add_members("HIIT", guest_count)
    clear_old_exports()
    export_roster()
    show_rosters()


if __name__ == "__main__":
    main()
