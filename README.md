# Cognitive Employee Service Assistant

## Project Overview

A Python-based employee leave management service built using FastAPI. It provides REST API endpoints to check employee leave balances, submit leave requests, and approve or reject requests.

## Technologies Used

- Python
- REST APIs
- JSON
- Pytest
- FastAPI
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

### 1. Install Dependencies

```bash
pip install fastapi uvicorn pytest
```

### 2. Start the Application

```bash
python -m uvicorn app:app --reload
```

### 3. Open Swagger UI

Open the following URL in your browser:

http://127.0.0.1:8000/docs

Use Swagger UI to explore and test the API endpoints.

## Run Tests

Run the following command in the terminal:

```bash
python -m pytest -v
```

The project includes automated tests for the employee leave management APIs.

## Future Enhancements

- Integrate a conversational assistant using IBM watsonx Assistant
- Explore workflow automation using IBM watsonx Orchestrate
- Add database support for persistent storage
- Implement employee authentication
