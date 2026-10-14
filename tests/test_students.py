from src.app import app
from src.data import students as student_data


def setup_function():
    student_data.reset_data()


def client():
    return app.test_client()


def valid_student(**overrides):
    data = {
        "firstName": "David", "lastName": "Test", "email": "david@test.com",
        "grade": 14, "field": "informatique",
    }
    data.update(overrides)
    return data


def test_get_students_returns_200_and_array():
    response = client().get("/students")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_students_returns_all_initial_students():
    assert len(client().get("/students").get_json()) == 5


def test_get_student_by_valid_id_returns_matching_student():
    response = client().get("/students/1")
    assert response.status_code == 200
    assert response.get_json()["firstName"] == "Alice"


def test_get_student_unknown_id_returns_404():
    assert client().get("/students/999").status_code == 404


def test_get_student_invalid_id_returns_400():
    assert client().get("/students/abc").status_code == 400
