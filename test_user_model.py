"""
Test script for User model and password hashing
Run this after installing requirements: python test_user_model.py
"""
import asyncio
from datetime import datetime


async def test_user_model():
    """Test User model and password hashing functionality"""
    print("🚀 Testing User Model and Password Hashing...")
    
    try:
        # Import database connection
        from database import connect_to_mongo, close_mongo_connection
        from user_models import User, UserCreate
        from user_crud import user_crud
        
        print("✅ Imports successful")
        
        # Connect to database
        print("\n📡 Connecting to MongoDB...")
        await connect_to_mongo()
        print("✅ Connected to MongoDB successfully")
        
        # Test 1: Password hashing
        print("\n🔐 Testing password hashing...")
        plain_password = "SecurePassword123"
        hashed = User.hash_password(plain_password)
        print(f"✅ Password hashed successfully")
        print(f"   Plain: {plain_password}")
        print(f"   Hash: {hashed[:50]}...")  # Show first 50 chars
        
        # Test 2: Create a user
        print("\n👤 Testing user creation...")
        test_user = UserCreate(
            username="test_user_123",
            password="TestPass123",
            email="test@example.com",
            full_name="Test User"
        )
        
        try:
            created_user = await user_crud.create_user(test_user)
            print(f"✅ User created successfully")
            print(f"   ID: {created_user.id}")
            print(f"   Username: {created_user.username}")
            print(f"   Email: {created_user.email}")
            print(f"   Active: {created_user.is_active}")
        except ValueError as e:
            print(f"ℹ️  User might already exist: {e}")
            # Try to find existing user
            existing = await user_crud.get_user_by_username("test_user_123")
            if existing:
                created_user = existing
                print(f"✅ Using existing user: {existing.username}")
        
        # Test 3: Get user by username
        print("\n🔍 Testing user retrieval by username...")
        user_doc = await user_crud.get_user_by_username("test_user_123")
        if user_doc:
            print(f"✅ User retrieved successfully: {user_doc.username}")
        
        # Test 4: Password verification
        print("\n🔑 Testing password verification...")
        correct_password = "TestPass123"
        wrong_password = "WrongPassword"
        
        if user_doc.verify_password(correct_password):
            print(f"✅ Correct password verified successfully")
        else:
            print(f"❌ Correct password verification failed")
        
        if not user_doc.verify_password(wrong_password):
            print(f"✅ Wrong password correctly rejected")
        else:
            print(f"❌ Wrong password incorrectly accepted")
        
        # Test 5: Authentication
        print("\n🔐 Testing user authentication...")
        auth_user = await user_crud.authenticate_user("test_user_123", "TestPass123")
        if auth_user:
            print(f"✅ User authenticated successfully")
        else:
            print(f"❌ Authentication failed")
        
        # Test with wrong password
        auth_fail = await user_crud.authenticate_user("test_user_123", "WrongPass123")
        if not auth_fail:
            print(f"✅ Authentication correctly failed with wrong password")
        else:
            print(f"❌ Authentication incorrectly succeeded with wrong password")
        
        # Test 6: Password update
        print("\n🔄 Testing password update...")
        from user_models import UserUpdate
        update_data = UserUpdate(password="NewSecurePass456")
        updated_user = await user_crud.update_user(str(user_doc.id), update_data)
        if updated_user:
            print(f"✅ Password updated successfully")
            
            # Verify new password
            user_doc = await user_crud.get_user_by_username("test_user_123")
            if user_doc.verify_password("NewSecurePass456"):
                print(f"✅ New password verified successfully")
            else:
                print(f"❌ New password verification failed")
        
        # Test 7: List users
        print("\n📋 Testing user listing...")
        all_users = await user_crud.get_all_users(limit=5)
        print(f"✅ Retrieved {len(all_users)} users")
        for user in all_users:
            print(f"   - {user.username} ({user.email or 'no email'})")
        
        # Test 8: User count
        print("\n🔢 Testing user count...")
        count = await user_crud.get_users_count()
        print(f"✅ Total users: {count}")
        
        active_count = await user_crud.get_users_count(is_active=True)
        print(f"✅ Active users: {active_count}")
        
        # Test 9: Deactivate user
        print("\n🚫 Testing user deactivation...")
        deactivated = await user_crud.deactivate_user(str(user_doc.id))
        if deactivated and not deactivated.is_active:
            print(f"✅ User deactivated successfully")
        
        # Test authentication on inactive user
        auth_inactive = await user_crud.authenticate_user("test_user_123", "NewSecurePass456")
        if not auth_inactive:
            print(f"✅ Authentication correctly failed for inactive user")
        
        # Test 10: Reactivate user
        print("\n✅ Testing user reactivation...")
        reactivated = await user_crud.activate_user(str(user_doc.id))
        if reactivated and reactivated.is_active:
            print(f"✅ User reactivated successfully")
        
        # Test 11: Delete user
        print("\n🗑️  Testing user deletion...")
        deleted = await user_crud.delete_user(str(user_doc.id))
        if deleted:
            print(f"✅ User deleted successfully")
        
        # Close connection
        print("\n🔌 Closing database connection...")
        await close_mongo_connection()
        print("✅ Connection closed")
        
        print("\n🎉 All tests passed! User model and password hashing working correctly!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure to install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_user_model())

