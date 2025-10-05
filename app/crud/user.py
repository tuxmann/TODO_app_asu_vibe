from typing import Optional, List
from datetime import datetime
import logging

from app.models.user import User, UserCreate, UserUpdate, UserResponse

logger = logging.getLogger(__name__)


class UserCRUD:
    """CRUD operations for User items using Beanie ODM"""
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Create a new user with hashed password.
        
        Args:
            user_data: UserCreate schema with plain text password
            
        Returns:
            UserResponse with created user data (without password)
            
        Raises:
            ValueError: If username already exists
        """
        try:
            # Check if username already exists
            existing_user = await User.find_one(User.username == user_data.username)
            if existing_user:
                raise ValueError(f"Username '{user_data.username}' already exists")
            
            # Check if email already exists (if provided)
            if user_data.email:
                existing_email = await User.find_one(User.email == user_data.email)
                if existing_email:
                    raise ValueError(f"Email '{user_data.email}' already exists")
            
            # Create user with hashed password
            user = User(
                username=user_data.username,
                password_hash=User.hash_password(user_data.password),
                email=user_data.email,
                full_name=user_data.full_name
            )
            
            # Insert into database
            await user.insert()
            
            logger.info("User created successfully: %s", user.username)
            return self._to_response(user)
            
        except ValueError:
            raise
        except Exception as e:
            logger.error("Error creating user: %s", e)
            raise
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get a user by ID"""
        try:
            user = await User.get(user_id)
            
            if user:
                return self._to_response(user)
            return None
            
        except Exception as e:
            logger.error("Error getting user by ID %s: %s", user_id, e)
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by username (returns full User document with password_hash).
        Used for authentication purposes.
        
        Args:
            username: Username to search for
            
        Returns:
            User document or None
        """
        try:
            user = await User.find_one(User.username == username)
            return user
            
        except Exception as e:
            logger.error("Error getting user by username %s: %s", username, e)
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get a user by email"""
        try:
            user = await User.find_one(User.email == email)
            
            if user:
                return self._to_response(user)
            return None
            
        except Exception as e:
            logger.error("Error getting user by email %s: %s", email, e)
            return None
    
    async def get_all_users(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[UserResponse]:
        """Get all users with optional filtering"""
        try:
            query = User.find()
            
            if is_active is not None:
                query = query.find(User.is_active == is_active)
            
            users = await query.sort("created_at").skip(skip).limit(limit).to_list()
            
            return [self._to_response(user) for user in users]
            
        except Exception as e:
            logger.error("Error getting users: %s", e)
            raise
    
    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[UserResponse]:
        """Update a user"""
        try:
            user = await User.get(user_id)
            
            if not user:
                return None
            
            # Get update data (exclude unset fields)
            update_data = user_update.model_dump(exclude_unset=True)
            
            if not update_data:
                return self._to_response(user)
            
            # Handle password update separately
            if 'password' in update_data:
                password = update_data.pop('password')
                user.set_password(password)
                logger.info("Password updated for user: %s", user.username)
            
            # Update timestamp
            update_data['updated_at'] = datetime.utcnow()
            
            # Apply other updates
            for field, value in update_data.items():
                setattr(user, field, value)
            
            # Save to database
            await user.save()
            
            logger.info("User updated successfully: %s", user.username)
            return self._to_response(user)
            
        except Exception as e:
            logger.error("Error updating user %s: %s", user_id, e)
            raise
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            user = await User.get(user_id)
            
            if not user:
                return False
            
            username = user.username
            await user.delete()
            
            logger.info("User deleted successfully: %s", username)
            return True
            
        except Exception as e:
            logger.error("Error deleting user %s: %s", user_id, e)
            raise
    
    async def deactivate_user(self, user_id: str) -> Optional[UserResponse]:
        """Deactivate a user (soft delete)"""
        try:
            user = await User.get(user_id)
            
            if not user:
                return None
            
            user.is_active = False
            user.updated_at = datetime.utcnow()
            await user.save()
            
            logger.info("User deactivated: %s", user.username)
            return self._to_response(user)
            
        except Exception as e:
            logger.error("Error deactivating user %s: %s", user_id, e)
            raise
    
    async def activate_user(self, user_id: str) -> Optional[UserResponse]:
        """Activate a user"""
        try:
            user = await User.get(user_id)
            
            if not user:
                return None
            
            user.is_active = True
            user.updated_at = datetime.utcnow()
            await user.save()
            
            logger.info("User activated: %s", user.username)
            return self._to_response(user)
            
        except Exception as e:
            logger.error("Error activating user %s: %s", user_id, e)
            raise
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            User document if authentication successful, None otherwise
        """
        try:
            user = await self.get_user_by_username(username)
            
            if not user:
                logger.warning("Authentication failed: user not found - %s", username)
                return None
            
            if not user.is_active:
                logger.warning("Authentication failed: user inactive - %s", username)
                return None
            
            if not user.verify_password(password):
                logger.warning("Authentication failed: invalid password - %s", username)
                return None
            
            logger.info("User authenticated successfully: %s", username)
            return user
            
        except Exception as e:
            logger.error("Error authenticating user %s: %s", username, e)
            return None
    
    async def get_users_count(self, is_active: Optional[bool] = None) -> int:
        """Get total count of users"""
        try:
            query = User.find()
            
            if is_active is not None:
                query = query.find(User.is_active == is_active)
            
            return await query.count()
            
        except Exception as e:
            logger.error("Error getting users count: %s", e)
            raise
    
    def _to_response(self, user: User) -> UserResponse:
        """Convert User document to UserResponse (excludes password_hash)"""
        return UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at
        )


# Create global instance
user_crud = UserCRUD()

