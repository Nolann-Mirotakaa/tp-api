import re
from copy import deepcopy

FIELDS = ["informatique", "math?matiques", "physique", "chimie"]

students_initial = [
    {"id": 1, "firstName": "Alice", "lastName": "Martin", "email": "alice@test.com",
     "grade": 15, "field": "informatique"},
    {"id": 2, "firstName": "Bob", "lastName": "Durand", "email": "bob@test.com", "grade": 12, "field": "physique"},
    {"id": 3, "firstName": "Charlie", "lastName": "Bernard",
     "email": "charlie@test.com", "grade": 18, "field": "math?matiques"},
    {"id": 4, "firstName": "Diane", "lastName": "Petit", "email": "diane@test.com", "grade": 9, "field": "chimie"},
    {"id": 5, "firstName": "Eric", "lastName": "Leroy", "email": "eric@test.com", "grade": 14, "field": "informatique"},
]

students = deepcopy(students_initial)


def reset_data():
    global students
    students = deepcopy(students_initial)


def is_valid_email(email):
    return isinstance(email, str) and re.fullmatch(
        r"[^\s@]+@[^\s@]+\.[^\s@]+", email
    ) is not None
