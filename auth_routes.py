"""
Authentication routes for user registration and login
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import logging

from user_models import UserCreate, UserResponse, UserLogin, Token
from user_crud import user_crud
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import get_current_user, get_current_active_user
from user_models import User

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user.
    
    - **username**: Unique username (4-32 characters, alphanumeric with _ and -)
    - **password**: Strong password (min 8 chars, must have uppercase, lowercase, digit)
    - **email**: Optional email address
    - **full_name**: Optional full name
    
    Returns the created user (without password hash).
    """
    try:
        # Create user (password will be hashed automatically)
        new_user = await user_crud.create_user(user_data)
        
        logger.info("New user registered: %s", new_user.username)
        
        return new_user
        
    except ValueError as e:
        # Username or email already exists
        logger.warning("Registration failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Error during registration: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login with username and password to get an access token.
    
    Uses OAuth2 password flow (form data):
    - **username**: Your username
    - **password**: Your password
    
    Returns a JWT access token that expires in 30 minutes (configurable).
    
    Use the token in subsequent requests:
    ```
    Authorization: Bearer <token>
    ```
    """
    # Authenticate user
    user = await user_crud.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        logger.warning("Failed login attempt for username: %s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    logger.info("User logged in: %s", user.username)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login/json", response_model=Token)
async def login_json(credentials: UserLogin):
    """
    Alternative login endpoint that accepts JSON instead of form data.
    
    - **username**: Your username
    - **password**: Your password
    
    Returns a JWT access token.
    """
    # Authenticate user
    user = await user_crud.authenticate_user(credentials.username, credentials.password)
    
    if not user:
        logger.warning("Failed login attempt for username: %s", credentials.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    logger.info("User logged in (JSON): %s", user.username)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user's information.
    
    Requires authentication (Bearer token in Authorization header).
    
    Returns the current user's profile.
    """
    from user_crud import user_crud
    return user_crud._to_response(current_user)


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_active_user)):
    """
    Refresh access token.
    
    Requires valid authentication token.
    Returns a new access token with extended expiration.
    """
    # Create new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username},
        expires_delta=access_token_expires
    )
    
    logger.info("Token refreshed for user: %s", current_user.username)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout endpoint (for completeness).
    
    Note: JWT tokens are stateless, so actual logout happens client-side
    by discarding the token. This endpoint just confirms the token is valid.
    
    For true logout, implement token blacklisting or use short-lived tokens.
    """
    logger.info("User logged out: %s", current_user.username)
    
    return {
        "message": "Successfully logged out",
        "detail": "Please discard your access token"
    }


@router.get("/test-auth")
async def test_authentication(current_user: User = Depends(get_current_active_user)):
    """
    Test endpoint to verify authentication is working.
    
    Requires authentication.
    Returns a success message with username.
    """
    return {
        "message": "Authentication successful!",
        "username": current_user.username,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser
    }
