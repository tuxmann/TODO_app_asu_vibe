"""
FastAPI dependencies for authentication and authorization
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import logging

from auth import decode_access_token
from user_models import User
from user_crud import user_crud

logger = logging.getLogger(__name__)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        User document
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode token
    username = decode_access_token(token)
    if username is None:
        logger.warning("Invalid token: could not decode")
        raise credentials_exception
    
    # Get user from database
    user = await user_crud.get_user_by_username(username)
    if user is None:
        logger.warning("User not found: %s", username)
        raise credentials_exception
    
    # Check if user is active
    if not user.is_active:
        logger.warning("Inactive user attempted access: %s", username)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user is active.
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        Active user document
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user is a superuser.
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        Superuser document
        
    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        logger.warning("Non-superuser attempted admin access: %s", current_user.username)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[User]:
    """
    Dependency to optionally get current user (doesn't raise exception if not authenticated).
    
    Args:
        token: Optional JWT token
        
    Returns:
        User document or None
    """
    if token is None:
        return None
    
    try:
        username = decode_access_token(token)
        if username is None:
            return None
        
        user = await user_crud.get_user_by_username(username)
        return user
    except Exception:
        return None
