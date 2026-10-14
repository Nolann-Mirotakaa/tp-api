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


# GET : lecture (5 tests)
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


# POST : cr?ation (4 tests)
def test_post_valid_student_returns_201_and_generated_id():
    response = client().post("/students", json=valid_student())
    assert response.status_code == 201
    assert response.get_json()["id"] == 6


def test_post_missing_required_field_returns_400():
    assert client().post("/students", json={"firstName": "David"}).status_code == 400


def test_post_invalid_grade_returns_400():
    assert client().post("/students", json=valid_student(grade=25)).status_code == 400


def test_post_duplicate_email_returns_409():
    assert client().post(
        "/students", json=valid_student(email="alice@test.com")
    ).status_code == 409


# PUT : modification (2 tests)
def test_put_valid_student_returns_200_and_updated_data():
    response = client().put(
        "/students/1", json=valid_student(email="alice.updated@test.com")
    )
    assert response.status_code == 200
    assert response.get_json()["firstName"] == "David"


def test_put_unknown_id_returns_404():
    assert client().put("/students/999", json=valid_student()).status_code == 404


# DELETE : suppression (2 tests)
def test_delete_valid_id_returns_200():
    assert client().delete("/students/1").status_code == 200


def test_delete_unknown_id_returns_404():
    assert client().delete("/students/999").status_code == 404


# Stats et recherche (2 tests)
def test_stats_returns_required_statistics():
    response = client().get("/students/stats")
    body = response.get_json()
    assert response.status_code == 200
    assert {"totalStudents", "averageGrade", "studentsByField", "bestStudent"} <= body.keys()


def test_search_returns_matching_students():
    response = client().get("/students/search?q=ALI")
    assert response.status_code == 200
    assert len(response.get_json()) == 1
