from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


class Address(BaseModel):
    street: str
    city: str
    zipcode: str = Field(..., min_length=5, max_length=6)


class User(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    age: Optional[int] = Field(None, ge=18)
    is_active: bool = True
    skills: List[str] = []
    address: Address
