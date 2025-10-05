"""
Example usage of the User model with password hashing

This demonstrates how to use the User model in your application.
"""
import asyncio


async def example_usage():
    """Example: Complete user management workflow"""
    
    # Import required modules
    from database import connect_to_mongo, close_mongo_connection
    from user_models import User, UserCreate, UserUpdate
    from user_crud import user_crud
    
    print("=" * 60)
    print("User Model Example Usage")
    print("=" * 60)
    
    # Connect to database
    await connect_to_mongo()
    
    try:
        # 1. CREATE USER
        print("\n1️⃣  Creating a new user...")
        user_data = UserCreate(
            username="demo_user",
            password="DemoPass123",
            email="demo@example.com",
            full_name="Demo User"
        )
        
        try:
            new_user = await user_crud.create_user(user_data)
            print(f"   ✅ User created: {new_user.username}")
            print(f"   📧 Email: {new_user.email}")
            print(f"   🆔 ID: {new_user.id}")
        except ValueError as e:
            print(f"   ℹ️  User exists: {e}")
            # Get existing user
            user_doc = await user_crud.get_user_by_username("demo_user")
            new_user = user_crud._to_response(user_doc)
        
        # 2. AUTHENTICATE USER
        print("\n2️⃣  Authenticating user...")
        auth_user = await user_crud.authenticate_user("demo_user", "DemoPass123")
        
        if auth_user:
            print("   ✅ Authentication successful!")
            print(f"   👤 Welcome, {auth_user.username}!")
        else:
            print("   ❌ Authentication failed!")
        
        # 3. TEST WRONG PASSWORD
        print("\n3️⃣  Testing wrong password...")
        wrong_auth = await user_crud.authenticate_user("demo_user", "WrongPassword")
        
        if not wrong_auth:
            print("   ✅ Wrong password correctly rejected")
        
        # 4. UPDATE USER INFO
        print("\n4️⃣  Updating user information...")
        update_data = UserUpdate(
            full_name="Demo User Updated",
            email="demo.updated@example.com"
        )
        
        updated = await user_crud.update_user(new_user.id, update_data)
        if updated:
            print(f"   ✅ User updated")
            print(f"   📝 New name: {updated.full_name}")
            print(f"   📧 New email: {updated.email}")
        
        # 5. CHANGE PASSWORD
        print("\n5️⃣  Changing password...")
        password_update = UserUpdate(password="NewDemoPass456")
        await user_crud.update_user(new_user.id, password_update)
        print("   ✅ Password changed")
        
        # Verify new password works
        auth_new = await user_crud.authenticate_user("demo_user", "NewDemoPass456")
        if auth_new:
            print("   ✅ New password verified")
        
        # 6. LIST ALL USERS
        print("\n6️⃣  Listing all users...")
        all_users = await user_crud.get_all_users(limit=5)
        print(f"   📋 Total users: {len(all_users)}")
        for user in all_users:
            status = "🟢" if user.is_active else "🔴"
            print(f"   {status} {user.username} - {user.email or 'No email'}")
        
        # 7. DEACTIVATE USER
        print("\n7️⃣  Deactivating user...")
        deactivated = await user_crud.deactivate_user(new_user.id)
        if deactivated and not deactivated.is_active:
            print("   ✅ User deactivated")
        
        # Test that deactivated user cannot authenticate
        auth_inactive = await user_crud.authenticate_user("demo_user", "NewDemoPass456")
        if not auth_inactive:
            print("   ✅ Inactive user cannot authenticate")
        
        # 8. REACTIVATE USER
        print("\n8️⃣  Reactivating user...")
        reactivated = await user_crud.activate_user(new_user.id)
        if reactivated and reactivated.is_active:
            print("   ✅ User reactivated")
        
        # 9. USER STATISTICS
        print("\n9️⃣  User statistics...")
        total = await user_crud.get_users_count()
        active = await user_crud.get_users_count(is_active=True)
        print(f"   📊 Total users: {total}")
        print(f"   🟢 Active users: {active}")
        print(f"   🔴 Inactive users: {total - active}")
        
        # 10. CLEANUP (Optional)
        print("\n🔟 Cleanup...")
        print("   ℹ️  Keeping demo user for future tests")
        # Uncomment to delete:
        # await user_crud.delete_user(new_user.id)
        # print("   ✅ Demo user deleted")
        
        print("\n" + "=" * 60)
        print("✅ Example completed successfully!")
        print("=" * 60)
        
    finally:
        # Always close connection
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(example_usage())

