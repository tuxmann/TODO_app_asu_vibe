# User Model with Password Hashing - Complete Guide

## Overview

The User model is a **Beanie Document** that provides secure user authentication with password hashing using **bcrypt**. It includes methods for password hashing, verification, and complete CRUD operations.

## Features

✅ **Secure Password Hashing** - Uses bcrypt with 12 rounds  
✅ **Password Verification** - Built-in method to verify passwords  
✅ **User Authentication** - Complete authentication flow  
✅ **Active/Inactive Status** - Soft delete support  
✅ **Superuser Support** - Role-based access control foundation  
✅ **Automatic Timestamps** - Created and updated timestamps  
✅ **MongoDB Indexes** - Optimized for fast lookups  

## User Model (`user_models.py`)

### Beanie Document Model

```python
from beanie import Document
from passlib.context import CryptContext

class User(Document):
    """Beanie Document model for User collection"""
    username: str              # Unique username (4-32 chars)
    password_hash: str         # Bcrypt hashed password
    email: Optional[str]       # User email (optional)
    full_name: Optional[str]   # Full name (optional)
    is_active: bool           # Account active status
    is_superuser: bool        # Superuser flag
    created_at: datetime      # Creation timestamp
    updated_at: datetime      # Last update timestamp
```

### Key Methods

#### 1. Hash Password (Static Method)
```python
hashed = User.hash_password("MySecurePassword123")
```
- Uses bcrypt with 12 rounds
- Returns hashed password string
- Static method - can be called without instance

#### 2. Verify Password (Instance Method)
```python
user = await User.find_one(User.username == "john_doe")
is_valid = user.verify_password("MySecurePassword123")
```
- Verifies plain text password against stored hash
- Returns `True` if password matches, `False` otherwise
- Uses constant-time comparison for security

#### 3. Set Password (Instance Method)
```python
user = await User.find_one(User.username == "john_doe")
user.set_password("NewPassword456")
await user.save()
```
- Sets a new password (automatically hashes it)
- Updates the `updated_at` timestamp
- Requires calling `save()` to persist to database

## Pydantic Schemas

### UserCreate
Used when creating a new user (accepts plain text password):
```python
{
    "username": "john_doe",
    "password": "SecurePass123",
    "email": "john@example.com",
    "full_name": "John Doe"
}
```

**Validation Rules:**
- Username: 4-32 characters, alphanumeric with underscores/hyphens
- Password: Minimum 8 characters, must contain:
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
- Email: Optional, valid email format
- Full Name: Optional, max 100 characters

### UserUpdate
Used for updating user information:
```python
{
    "email": "newemail@example.com",
    "full_name": "John Updated Doe",
    "password": "NewPassword789",  # Optional - only if changing
    "is_active": true
}
```

### UserLogin
Used for authentication:
```python
{
    "username": "john_doe",
    "password": "SecurePass123"
}
```

### UserResponse
Returned by API (excludes password_hash):
```python
{
    "id": "507f1f77bcf86cd799439011",
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
}
```

## CRUD Operations (`user_crud.py`)

### Create User
```python
from user_models import UserCreate
from user_crud import user_crud

user_data = UserCreate(
    username="john_doe",
    password="SecurePass123",
    email="john@example.com",
    full_name="John Doe"
)

user = await user_crud.create_user(user_data)
```

**Features:**
- Automatically hashes password
- Checks for duplicate username
- Checks for duplicate email
- Returns `UserResponse` (without password hash)

### Authenticate User
```python
user = await user_crud.authenticate_user("john_doe", "SecurePass123")

if user:
    print("Authentication successful!")
else:
    print("Authentication failed!")
```

**Checks:**
- User exists
- User is active
- Password is correct

### Get User by Username
```python
user = await user_crud.get_user_by_username("john_doe")
# Returns User document (with password_hash) for authentication
```

### Get User by ID
```python
user = await user_crud.get_user_by_id("507f1f77bcf86cd799439011")
# Returns UserResponse (without password_hash)
```

### Update User
```python
from user_models import UserUpdate

update_data = UserUpdate(
    email="newemail@example.com",
    password="NewPassword789"  # Optional
)

updated_user = await user_crud.update_user(user_id, update_data)
```

**Features:**
- Only updates provided fields
- Automatically hashes new password if provided
- Updates `updated_at` timestamp

### Delete User
```python
deleted = await user_crud.delete_user(user_id)
# Returns True if deleted, False if not found
```

### Deactivate User (Soft Delete)
```python
user = await user_crud.deactivate_user(user_id)
# Sets is_active = False
```

### Activate User
```python
user = await user_crud.activate_user(user_id)
# Sets is_active = True
```

### List Users
```python
users = await user_crud.get_all_users(
    skip=0,
    limit=10,
    is_active=True  # Optional filter
)
```

### Count Users
```python
total = await user_crud.get_users_count()
active = await user_crud.get_users_count(is_active=True)
```

## Password Security

### Bcrypt Configuration
- **Algorithm**: bcrypt
- **Rounds**: 12 (configurable)
- **Salt**: Automatically generated per password
- **Hash Length**: 60 characters

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- Maximum 100 characters (API limit)

### Security Best Practices
✅ Passwords are never stored in plain text  
✅ Passwords are hashed using bcrypt (industry standard)  
✅ Each password has a unique salt  
✅ Password verification uses constant-time comparison  
✅ Password hashes are never returned in API responses  

## Example Usage

### Complete User Registration Flow
```python
from user_models import UserCreate
from user_crud import user_crud

# 1. Create user
try:
    user_data = UserCreate(
        username="alice_wonder",
        password="AliceInWonderland123",
        email="alice@example.com",
        full_name="Alice Wonderland"
    )
    
    new_user = await user_crud.create_user(user_data)
    print(f"User created: {new_user.username}")
    
except ValueError as e:
    print(f"Error: {e}")  # Username or email already exists
```

### Complete Authentication Flow
```python
# 2. Authenticate user
username = "alice_wonder"
password = "AliceInWonderland123"

user = await user_crud.authenticate_user(username, password)

if user:
    print(f"Welcome, {user.username}!")
else:
    print("Invalid credentials")
```

### Password Change Flow
```python
# 3. Change password
from user_models import UserUpdate

update_data = UserUpdate(password="NewSecurePass456")
updated_user = await user_crud.update_user(str(user.id), update_data)

if updated_user:
    print("Password changed successfully")
```

## Testing

Run the test script to verify everything works:

```bash
python test_user_model.py
```

Expected output:
```
🚀 Testing User Model and Password Hashing...
✅ Imports successful
📡 Connecting to MongoDB...
✅ Connected to MongoDB successfully
🔐 Testing password hashing...
✅ Password hashed successfully
👤 Testing user creation...
✅ User created successfully
🔑 Testing password verification...
✅ Correct password verified successfully
✅ Wrong password correctly rejected
🔐 Testing user authentication...
✅ User authenticated successfully
🎉 All tests passed!
```

## MongoDB Collection Structure

```javascript
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "username": "john_doe",
  "password_hash": "$2b$12$...",  // Bcrypt hash
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": ISODate("2024-01-01T12:00:00Z"),
  "updated_at": ISODate("2024-01-01T12:00:00Z")
}
```

### Indexes
- `username` - For fast user lookups
- `email` - For email-based queries
- `is_active` - For filtering active users

## Integration with Database

The User model is automatically registered with Beanie during application startup in `database.py`:

```python
from user_models import User

await init_beanie(
    database=database,
    document_models=[Todo, User]  # User model registered
)
```

## Common Patterns

### Check if User Exists
```python
existing = await User.find_one(User.username == "john_doe")
if existing:
    print("User already exists")
```

### Find Active Users Only
```python
active_users = await User.find(User.is_active == True).to_list()
```

### Find Superusers
```python
admins = await User.find(User.is_superuser == True).to_list()
```

### Search by Email Domain
```python
from beanie.operators import RegEx

gmail_users = await User.find(
    RegEx(User.email, r".*@gmail\.com$", options="i")
).to_list()
```

## API Integration Example

Here's how you might use the User model in FastAPI routes:

```python
from fastapi import APIRouter, HTTPException, status
from user_models import UserCreate, UserLogin, UserResponse
from user_crud import user_crud

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    try:
        return await user_crud.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(credentials: UserLogin):
    user = await user_crud.authenticate_user(
        credentials.username,
        credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    # Generate JWT token here
    return {"access_token": "...", "token_type": "bearer"}
```

## Troubleshooting

### Issue: Password validation fails
**Solution**: Ensure password meets all requirements:
- At least 8 characters
- Contains uppercase, lowercase, and digit

### Issue: bcrypt compatibility error
**Solution**: Use bcrypt version 4.0.1:
```bash
pip install bcrypt==4.0.1
```

### Issue: User not found after creation
**Solution**: Make sure you're using the correct database and that Beanie is initialized properly.

## Security Considerations

⚠️ **Never log or display password hashes**  
⚠️ **Always use HTTPS in production**  
⚠️ **Implement rate limiting on authentication endpoints**  
⚠️ **Consider adding 2FA for enhanced security**  
⚠️ **Implement password reset functionality**  
⚠️ **Set password expiry policies if needed**  

## Next Steps

1. ✅ User model created and tested
2. 📝 Create authentication routes (login, register)
3. 🔐 Implement JWT token generation
4. 🛡️ Add authentication middleware
5. 🎭 Implement role-based access control
6. 📧 Add email verification
7. 🔄 Add password reset functionality

## Resources

- [Passlib Documentation](https://passlib.readthedocs.io/)
- [Bcrypt Wikipedia](https://en.wikipedia.org/wiki/Bcrypt)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Beanie Authentication Example](https://beanie-odm.dev/tutorial/authentication/)

