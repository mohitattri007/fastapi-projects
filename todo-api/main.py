from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

todos = []

@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo added!", "todo": todo}

@app.get("/todos")
def list_todos():
    return todos

@app.put("/todos/{todo_id}")
def mark_complete(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = True
            return {"message": "Todo marked complete", "todo": todo}
    return {"error": "Todo not found"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return {"message": "Todo deleted"}
    return {"error": "Todo not found"}
