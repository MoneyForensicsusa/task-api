from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

import psycopg2, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

#Defining the Task model
class Task(BaseModel):
    title: str
    description: str
    priority: int = Field(ge=1, le=5)

#Defining class for status update
class StatusUpdate(BaseModel):
    status: Literal['pending', 'in_progress', 'done']

#connectiong to db
def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

#async route to post a task
@app.post('/tasks/', status_code=201)
async def post_task(task: Task):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, description, priority) VALUES (%s, %s, %s) RETURNING ID", 
            (task.title, task.description, task.priority))
            new_id = cursor.fetchone()[0]
            conn.commit()
        return {
            "id": new_id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority
        }
    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))



#async route for deleting a task
@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = %s",
            (task_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="task not found")
            conn.commit()
        return {'message': f'Task {task_id} has been deleted'}
    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e)) 

#async route to PATCH status for task
@app.patch('/tasks/{task_id}/status')
async def patch_status(task_id: int, update: StatusUpdate):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status = %s WHERE id = %s RETURNING id, title, description, status, priority",
            (update.status, task_id))
            row = cursor.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail='task not found')
            updated_status = row[3]
            conn.commit()
        return {
            'message': f"Task {task_id} has been updated to {updated_status}",
            'id': task_id,
            'title': row[1],
            'description': row[2],
            'status': updated_status,
            'priority': row[4]
        }
    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))

#async route to GET a task
@app.get('/tasks/{task_id}')
async def get_task(task_id: int):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, description, status, priority FROM tasks WHERE id = %s",
            (task_id,))
            row = cursor.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail='Task not found')
        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "priority": row[4]
        }
    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))


