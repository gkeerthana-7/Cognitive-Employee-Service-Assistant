# Cognitive Employee Service Assistant

## Project Overview
A Python-based employee leave management service built using FastAPI. It provides REST API endpoints to check employee leave balances, submit leave requests, and approve or reject requests.

## Technologies Used
- Python
- FastAPI
- REST APIs
- JSON
- Pytest
- Swagger UI

## Features
- Check employee leave balance
- Submit employee leave requests
- Approve leave requests and update leave balances
- Reject leave requests without deducting leave balance
- Validate leave request inputs
- Handle invalid employee IDs and requests

## Sample Employees
- E101 – Ravi
- E102 – Priya

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/employees/{employee_id}/leave-balance` | Check leave balance |
| POST | `/leave-requests` | Create a leave request |
| PUT | `/leave-requests/{request_id}/approve` | Approve a leave request |
| PUT | `/leave-requests/{request_id}/reject` | Reject a leave request |

## Run the Project

Install dependencies:

```bash
pip install fastapi uvicorn pytest
