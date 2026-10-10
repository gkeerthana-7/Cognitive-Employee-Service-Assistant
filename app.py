from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Cognitive Employee Service Assistant",
    description="An API to manage employee leave services",
    version="1.0.0"
)

# Sample employee data
employees = {
    "E101": {
        "name": "Ravi",
        "leave_balance": 8
    },
    "E102": {
        "name": "Priya",
        "leave_balance": 5
    }
}

# Store leave requests temporarily
leave_requests = {}
next_request_id = 1


class LeaveRequest(BaseModel):
    employee_id: str
    days: int


@app.get("/")
def home():
    return {
        "message": "Welcome to the Employee Service Assistant!"
    }


@app.get("/employees/{employee_id}/leave-balance")
def get_leave_balance(employee_id: str):
    employee = employees.get(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "employee_id": employee_id,
        "name": employee["name"],
        "leave_balance": employee["leave_balance"]
    }


@app.post("/leave-requests")
def create_leave_request(request: LeaveRequest):
    global next_request_id

    if request.days <= 0:
        raise HTTPException(
            status_code=400,
            detail="Days must be greater than zero"
        )
    employee = employees.get(request.employee_id)
    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if request.days <= 0:
        raise HTTPException(
            status_code=400,
            detail="Leave days must be greater than zero"
        )

    if request.days > employee["leave_balance"]:
        raise HTTPException(
            status_code=400,
            detail="Insufficient leave balance"
        )

    request_id = next_request_id

    leave_requests[request_id] = {
        "request_id": request_id,
        "employee_id": request.employee_id,
        "days": request.days,
        "status": "Pending"
    }

    next_request_id += 1

    return {
        **leave_requests[request_id],
        "remaining_leave_balance": employee["leave_balance"]
    }


@app.get("/leave-requests/{request_id}")
def get_leave_request_status(request_id: int):
    request = leave_requests.get(request_id)

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    return request
@app.put("/leave-requests/{request_id}/approve")
def approve_leave_request(request_id: int):
    leave_request = leave_requests.get(request_id)

    if leave_request is None:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    if leave_request["status"] != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Leave request has already been processed"
        )
    employee = employees[leave_request["employee_id"]]

    if leave_request["days"] > employee["leave_balance"]:
        raise HTTPException(
            status_code=400,
            detail="Insufficient leave balance"
        )

    employee["leave_balance"] -= leave_request["days"]
    leave_request["status"] = "Approved"

    return {
        "message": "Leave request approved successfully",
        "request": leave_request
    }


@app.put("/leave-requests/{request_id}/reject")
def reject_leave_request(request_id: int):
    leave_request = leave_requests.get(request_id)

    if leave_request is None:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    if leave_request["status"] != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Leave request has already been processed"
        )

    leave_request["status"] = "Rejected"

    return {
        "message": "Leave request rejected successfully",
        "request": leave_request
    }