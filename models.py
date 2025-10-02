from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic models"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")
        return field_schema


class TodoBase(BaseModel):
    """Base Todo model"""
    title: str = Field(..., min_length=1, max_length=100, description="Todo title")
    description: Optional[str] = Field(None, max_length=500, description="Todo description")
    completed: bool = Field(default=False, description="Todo completion status")
    priority: Optional[str] = Field(default="medium", pattern="^(low|medium|high)$", description="Todo priority")


class TodoCreate(TodoBase):
    """Model for creating a new todo"""


class TodoUpdate(BaseModel):
    """Model for updating an existing todo"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")


class TodoInDB(TodoBase):
    """Model for todo as stored in database"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class TodoResponse(BaseModel):
    """Model for todo API responses"""
    id: str = Field(..., description="Todo ID")
    title: str
    description: Optional[str] = None
    completed: bool
    priority: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {ObjectId: str}
