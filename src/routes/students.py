from flask import Blueprint, jsonify, request

from src.data import students as student_data

students_bp = Blueprint("students", __name__)


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

def parse_id(value):
    return int(value) if value.isdigit() else None

@students_bp.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    parsed_id = parse_id(student_id)
    if parsed_id is None:
        return jsonify({"error": "invalid id"}), 400
    student = next((s for s in student_data.students if s["id"] == parsed_id), None)
    if student is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(student), 200
