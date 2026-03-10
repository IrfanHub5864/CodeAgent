"""Manage students and statistics for simple demonstrations."""

from __future__ import annotations

from typing import Dict, List, Optional


class StudentManager:
    """Holds students and provides summary helpers."""

    def __init__(self) -> None:
        self.students: List[Dict[str, object]] = []

    def add_student(self, name: str, age: int, marks: float) -> None:
        """Add a student record; marks must be numeric."""

        if not isinstance(marks, (int, float)):
            raise ValueError("marks must be a number")

        student = {"name": name, "age": age, "marks": float(marks)}
        self.students.append(student)

    def calculate_average(self) -> float:
        """Return the average marks, or 0.0 when no students exist."""

        if not self.students:
            return 0.0

        total = sum(float(s["marks"]) for s in self.students)
        return total / len(self.students)

    def get_top_student(self) -> Optional[Dict[str, object]]:
        """Return the student with the highest marks, or None if empty."""

        if not self.students:
            return None

        return max(self.students, key=lambda s: float(s["marks"]))

    def print_students(self) -> None:
        """Print every student record, correcting the marks key."""

        if not self.students:
            print("No students to display.")
            return

        for s in self.students:
            print("Name:", s["name"])
            print("Age:", s["age"])
            print("Marks:", s["marks"])
            print("----------------")


def load_students() -> StudentManager:
    """Create a manager and seed it with sample data."""

    manager = StudentManager()
    manager.add_student("Alice", 20, 85)
    manager.add_student("Bob", 21, 92.2)
    manager.add_student("Charlie", 19, 78)
    return manager


def main() -> None:
    """Demonstrate features so you can run the module directly."""

    manager = load_students()

    print("All Students:")
    manager.print_students()
    print()

    average = manager.calculate_average()
    print(f"Average marks: {average:.2f}")

    top_student = manager.get_top_student()
    if top_student:
        print("Top student:", top_student["name"], top_student["marks"])
    else:
        print("Top student: none")


if __name__ == "__main__":
    main()
