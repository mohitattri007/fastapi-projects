from fastapi import FastAPI
from app.models import User
from app.validators import PasswordPayload
from app.schemas import UserCreate, UserResponse

app = FastAPI(title="Pydantic Validation Playground")

fake_db = []


@app.get("/users", response_model=list[UserResponse])
def list_users():
    return fake_db

@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    new_user = {
        "id": len(fake_db) + 1,
        "username": user.username,
        "email": user.email
    }
    fake_db.append(new_user)
    return new_user


@app.post("/validate-password")
def validate_password(payload: PasswordPayload):
    return {"message": "Password is valid"}
