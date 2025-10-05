from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from beanie import Document
from passlib.context import CryptContext


# Password hashing context using bcrypt
# Note: Bcrypt has a 72-byte limit for passwords, handled automatically
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Document):
    """Beanie Document model for User collection"""
    username: str = Field(..., min_length=4, max_length=32, description="Unique username")
    password_hash: str = Field(..., description="Hashed password")
    email: Optional[str] = Field(None, description="User email address")
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")
    is_active: bool = Field(default=True, description="Account active status")
    is_superuser: bool = Field(default=False, description="Superuser status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """Validate username format"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain text password using bcrypt.
        
        Args:
            password: Plain text password to hash
            
        Returns:
            Hashed password string
        """
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str) -> bool:
        """
        Verify a plain text password against the stored hash.
        
        Args:
            plain_password: Plain text password to verify
            
        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, self.password_hash)
    
    def set_password(self, password: str) -> None:
        """
        Set a new password for the user (hashes it automatically).
        
        Args:
            password: Plain text password to set
        """
        self.password_hash = self.hash_password(password)
        self.updated_at = datetime.utcnow()
    
    class Settings:
        name = "users"  # Collection name in MongoDB
        indexes = [
            "username",  # Unique index for username
            "email",     # Index for email lookups
            "is_active", # Index for filtering active users
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password_hash": "$2b$12$...",  # This would be a real bcrypt hash
                "email": "john@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False
            }
        }


class UserCreate(BaseModel):
    """Pydantic schema for creating a new user"""
    username: str = Field(..., min_length=4, max_length=32, description="Unique username")
    password: str = Field(..., min_length=8, max_length=100, description="Plain text password (will be hashed)")
    email: Optional[str] = Field(None, description="User email address")
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """Validate username format"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "SecurePass123",
                "email": "john@example.com",
                "full_name": "John Doe"
            }
        }


class UserUpdate(BaseModel):
    """Pydantic schema for updating a user"""
    email: Optional[str] = Field(None, description="User email address")
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="New password")
    is_active: Optional[bool] = Field(None, description="Account active status")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength"""
        if v is not None:
            if len(v) < 8:
                raise ValueError('Password must be at least 8 characters long')
            if not any(c.isupper() for c in v):
                raise ValueError('Password must contain at least one uppercase letter')
            if not any(c.islower() for c in v):
                raise ValueError('Password must contain at least one lowercase letter')
            if not any(c.isdigit() for c in v):
                raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    """Pydantic schema for user login"""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "SecurePass123"
            }
        }


class UserResponse(BaseModel):
    """Pydantic schema for user API responses (excludes password_hash)"""
    id: str = Field(..., description="User ID")
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserInDB(UserResponse):
    """User model with password hash (for internal use only)"""
    password_hash: str = Field(..., description="Hashed password")


class Token(BaseModel):
    """OAuth2 token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data stored in JWT token"""
    username: Optional[str] = None

