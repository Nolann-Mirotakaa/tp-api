from flask import Blueprint, jsonify, request

from src.data import students as student_data
from src.data.students import FIELDS, is_valid_email

students_bp = Blueprint("students", __name__)
REQUIRED_FIELDS = ("firstName", "lastName", "email", "grade", "field")


def validate_student(data, current_id=None, require_all=True):
    if not isinstance(data, dict):
        return "JSON object required", 400
    if require_all and any(key not in data for key in REQUIRED_FIELDS):
        return "missing fields", 400
    for key in ("firstName", "lastName"):
        if key in data and (not isinstance(data[key], str) or len(data[key].strip()) < 2):
            return "name too short", 400
    if "email" in data:
        if not is_valid_email(data["email"]):
            return "invalid email", 400
        if any(
            student["email"].casefold() == data["email"].casefold()
            and student["id"] != current_id
            for student in student_data.students
        ):
            return "email exists", 409
    if "grade" in data:
        grade = data["grade"]
        if isinstance(grade, bool) or not isinstance(grade, (int, float)) or not 0 <= grade <= 20:
            return "invalid grade", 400
    if "field" in data and data["field"] not in FIELDS:
        return "invalid field", 400
    return None


def parse_id(value):
    return int(value) if value.isdigit() else None


@students_bp.route("/students", methods=["GET"])
def get_students():
    result = list(student_data.students)
    sort = request.args.get("sort")
    order = request.args.get("order", "asc")
    if order not in ("asc", "desc"):
        return jsonify({"error": "invalid order"}), 400
    if sort:
        if sort not in ("id", "firstName", "lastName", "email", "grade", "field"):
            return jsonify({"error": "invalid sort field"}), 400
        result.sort(key=lambda student: student[sort], reverse=order == "desc")
    if "page" in request.args or "limit" in request.args:
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)
        if page is None or limit is None or page < 1 or limit < 1:
            return jsonify({"error": "page and limit must be positive integers"}), 400
        start = (page - 1) * limit
        result = result[start:start + limit]
    return jsonify(result), 200


@students_bp.route("/students/stats", methods=["GET"])
def stats():
    total = len(student_data.students)
    average = round(sum(s["grade"] for s in student_data.students) / total, 2) if total else 0
    by_field = {field: sum(s["field"] == field for s in student_data.students) for field in FIELDS}
    best = max(student_data.students, key=lambda s: s["grade"], default=None)
    return jsonify({
        "totalStudents": total,
        "averageGrade": average,
        "studentsByField": by_field,
        "bestStudent": best,
    }), 200


@students_bp.route("/students/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "missing query"}), 400
    query = query.casefold()
    result = [
        s for s in student_data.students
        if query in s["firstName"].casefold() or query in s["lastName"].casefold()
    ]
    return jsonify(result), 200


@students_bp.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    parsed_id = parse_id(student_id)
    if parsed_id is None:
        return jsonify({"error": "invalid id"}), 400
    student = next((s for s in student_data.students if s["id"] == parsed_id), None)
    if student is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(student), 200


@students_bp.route("/students", methods=["POST"])
def create_student():
    data = request.get_json(silent=True)
    error = validate_student(data)
    if error:
        return jsonify({"error": error[0]}), error[1]
    new_id = max((s["id"] for s in student_data.students), default=0) + 1
    student = {"id": new_id, **data}
    student_data.students.append(student)
    return jsonify(student), 201


@students_bp.route("/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    parsed_id = parse_id(student_id)
    if parsed_id is None:
        return jsonify({"error": "invalid id"}), 400
    student = next((s for s in student_data.students if s["id"] == parsed_id), None)
    if student is None:
        return jsonify({"error": "not found"}), 404
    data = request.get_json(silent=True)
    error = validate_student(data, current_id=parsed_id)
    if error:
        return jsonify({"error": error[0]}), error[1]
    updated = {**student, **data}
    error = validate_student(updated, current_id=parsed_id)
    if error:
        return jsonify({"error": error[0]}), error[1]
    student.update(data)
    return jsonify(student), 200


@students_bp.route("/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    parsed_id = parse_id(student_id)
    if parsed_id is None:
        return jsonify({"error": "invalid id"}), 400
    student = next((s for s in student_data.students if s["id"] == parsed_id), None)
    if student is None:
        return jsonify({"error": "not found"}), 404
    student_data.students.remove(student)
    return jsonify({"message": "deleted"}), 200
