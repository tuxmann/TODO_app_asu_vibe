from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
from beanie import Document
from pydantic import ConfigDict


class TodoBase(BaseModel):
    """Base Todo model with shared fields"""
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


class Todo(Document):
    """Beanie Document model for MongoDB collection"""
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")
    deadline: date = Field(...)
    labels: List[str] = Field(default_factory=list)
    username: str = Field(..., min_length=4, max_length=32)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        if v not in ['high', 'medium', 'low']:
            raise ValueError('Priority must be high, medium, or low')
        return v
    
    @field_validator('deadline')
    @classmethod
    def validate_deadline(cls, v):
        if isinstance(v, str):
            v = date.fromisoformat(v)
        if v < date.today():
            raise ValueError('Deadline must be today or later')
        return v
    
    @field_validator('labels')
    @classmethod
    def validate_labels(cls, v):
        if not v:
            return v
        valid_labels = {'Work', 'Personal', 'Urgent'}
        for label in v:
            if label not in valid_labels:
                raise ValueError(f'Invalid label: {label}. Must be one of: Work, Personal, Urgent')
        return v
    
    class Settings:
        name = "todos"  # Collection name in MongoDB
        indexes = [
            "deadline",  # Index for sorting by deadline
            "completed",  # Index for filtering by completion status
            "priority",  # Index for filtering by priority
            "username",  # Index for filtering by username
        ]
        # Configure BSON encoders for date/datetime
        bson_encoders = {
            date: lambda v: datetime.combine(v, datetime.min.time()),
            datetime: lambda v: v
        }
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive docs for the API",
                "completed": False,
                "priority": "high",
                "deadline": "2024-12-31",
                "labels": ["Work", "Urgent"],
                "username": "john_doe"
            }
        }


class TodoCreate(TodoBase):
    """Pydantic schema for creating a new todo"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive docs for the API",
                "completed": False,
                "priority": "high",
                "deadline": "2024-12-31",
                "labels": ["Work", "Urgent"],
                "username": "john_doe"
            }
        }


class TodoUpdate(BaseModel):
    """Pydantic schema for updating an existing todo"""
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


class TodoResponse(BaseModel):
    """Pydantic schema for API responses"""
    id: str = Field(..., description="Todo ID")
    title: str
    description: Optional[str] = None
    completed: bool
    priority: str
    deadline: date
    labels: List[str]
    username: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Pydantic v2 way (replaces orm_mode)
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }
