from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
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
    priority: str = Field(default="medium", pattern="^(high|medium|low)$", description="Todo priority: high, medium, or low")
    deadline: date = Field(..., description="Deadline date (must be today or later)")
    labels: List[str] = Field(default_factory=list, description="Labels: Work, Personal, Urgent")
    username: str = Field(..., min_length=4, max_length=32, description="Username (4-32 characters)")
    
    @field_validator('deadline')
    @classmethod
    def validate_deadline(cls, v):
        if v < date.today():
            raise ValueError('Deadline must be today or later')
        return v
    
    @field_validator('labels')
    @classmethod
    def validate_labels(cls, v):
        valid_labels = {'Work', 'Personal', 'Urgent'}
        for label in v:
            if label not in valid_labels:
                raise ValueError(f'Invalid label: {label}. Must be one of: Work, Personal, Urgent')
        return v


class TodoCreate(TodoBase):
    """Model for creating a new todo"""


class TodoUpdate(BaseModel):
    """Model for updating an existing todo"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(None, pattern="^(high|medium|low)$")
    deadline: Optional[date] = None
    labels: Optional[List[str]] = None
    username: Optional[str] = Field(None, min_length=4, max_length=32)
    
    @field_validator('deadline')
    @classmethod
    def validate_deadline(cls, v):
        if v is not None and v < date.today():
            raise ValueError('Deadline must be today or later')
        return v
    
    @field_validator('labels')
    @classmethod
    def validate_labels(cls, v):
        if v is not None:
            valid_labels = {'Work', 'Personal', 'Urgent'}
            for label in v:
                if label not in valid_labels:
                    raise ValueError(f'Invalid label: {label}. Must be one of: Work, Personal, Urgent')
        return v


class TodoInDB(TodoBase):
    """Model for todo as stored in database"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, date: lambda v: v.isoformat()}


class TodoResponse(BaseModel):
    """Model for todo API responses"""
    id: str = Field(..., description="Todo ID")
    title: str
    description: Optional[str] = None
    completed: bool
    priority: str
    deadline: date
    labels: List[str]
    username: str

    class Config:
        json_encoders = {ObjectId: str, date: lambda v: v.isoformat()}
