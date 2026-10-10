import pytest
from fastapi.testclient import TestClient
import app as app_module
from app import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_data():
    app_module.employees = {
        "E101": {"name": "Ravi", "leave_balance": 8},
        "E102": {"name": "Priya", "leave_balance": 5}
    }
    app_module.leave_requests = {}
    app_module.next_request_id = 1


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Employee Service Assistant!"
    }


def test_get_valid_employee_leave_balance():
    response = client.get("/employees/E101/leave-balance")

    assert response.status_code == 200
    assert response.json()["employee_id"] == "E101"


def test_invalid_employee():
    response = client.get("/employees/E999/leave-balance")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_leave_request_insufficient_balance():
    response = client.post(
        "/leave-requests",
        json={"employee_id": "E101", "days": 100}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient leave balance"


def test_leave_request_pending_does_not_deduct_balance():
    response = client.post(
        "/leave-requests",
        json={"employee_id": "E101", "days": 3}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Pending"

    balance = client.get("/employees/E101/leave-balance")

    assert balance.json()["leave_balance"] == 8


def test_approve_leave_request_deducts_balance():
    created = client.post(
        "/leave-requests",
        json={"employee_id": "E101", "days": 3}
    )

    request_id = created.json()["request_id"]

    response = client.put(
        f"/leave-requests/{request_id}/approve"
    )

    assert response.status_code == 200
    assert response.json()["request"]["status"] == "Approved"

    balance = client.get("/employees/E101/leave-balance")

    assert balance.json()["leave_balance"] == 5


def test_reject_leave_request_keeps_balance():
    created = client.post(
        "/leave-requests",
        json={"employee_id": "E102", "days": 2}
    )

    request_id = created.json()["request_id"]

    response = client.put(
        f"/leave-requests/{request_id}/reject"
    )

    assert response.status_code == 200
    assert response.json()["request"]["status"] == "Rejected"

    balance = client.get("/employees/E102/leave-balance")

    assert balance.json()["leave_balance"] == 5


def test_leave_request_zero_days():
    response = client.post(
        "/leave-requests",
        json={"employee_id": "E101", "days": 0}
    )

    assert response.status_code == 400