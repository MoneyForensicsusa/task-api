# Task Manager API

A REST API for managing tasks with status tracking built with FastAPI and PostgreSQL.

## Tech Stack
- FastAPI
- PostgreSQL
- psycopg2
- pytest

## Setup

1. Clone the repo
2. Create virtual environment:
   python -m venv .venv
   .venv\Scripts\Activate.ps1

3. Install dependencies:
   pip install -r requirements.txt

4. Create .env file:
   DB_HOST=localhost
   DB_NAME=task_db
   DB_USER=postgres
   DB_PASSWORD=yourpassword

5. Create the database and table in pgAdmin:
   CREATE TABLE tasks (
       id SERIAL PRIMARY KEY,
       title TEXT NOT NULL,
       description TEXT,
       status TEXT DEFAULT 'pending'
           CHECK (status IN ('pending', 'in_progress', 'done')),
       priority INTEGER DEFAULT 3
           CHECK (priority BETWEEN 1 AND 5),
       due_date TIMESTAMP,
       created_at TIMESTAMP DEFAULT NOW()
   );

6. Run the server:
   python -m uvicorn main:app --reload

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks/stats | Get task statistics by status |
| GET | /tasks/overdue | Get all overdue tasks |
| GET | /tasks/priority/{level} | Get tasks by priority level |
| POST | /tasks | Create a new task |
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get a specific task |
| PATCH | /tasks/{id}/status | Update task status only |
| DELETE | /tasks/{id} | Delete a task |
| PATCH | /tasks/bulk-status | Bulk update task statuses |

## Task Status Flow
pending → in_progress → done

## Example Requests

### Create a Task
POST /tasks
{
    "title": "Review proposal",
    "description": "Review the ALINEDS DIR proposal",
    "priority": 1,
    "due_date": "2026-08-01T00:00:00"
}

Response:
{
    "id": 1,
    "title": "Review proposal",
    "status": "pending",
    "priority": 1
}

### Update Task Status
PATCH /tasks/1/status
{
    "status": "in_progress"
}

Response:
{
    "message": "Task 1 has been updated to in_progress",
    "id": 1,
    "status": "in_progress"
}

## Running Tests
python -m pytest