"""
Simple test script to verify Beanie ODM setup
Run this after installing requirements: python test_beanie_setup.py
"""
import asyncio
from datetime import date, timedelta


async def test_beanie_setup():
    """Test basic Beanie operations"""
    print("🚀 Testing Beanie ODM setup...")
    
    try:
        # Import database connection
        from database import connect_to_mongo, close_mongo_connection
        from models import Todo
        from crud import todo_crud
        
        print("✅ Imports successful")
        
        # Connect to database
        print("\n📡 Connecting to MongoDB...")
        await connect_to_mongo()
        print("✅ Connected to MongoDB successfully")
        
        # Test creating a todo
        print("\n📝 Testing todo creation...")
        from models import TodoCreate
        
        test_todo = TodoCreate(
            title="Test Todo Item",
            description="This is a test todo created by the setup script",
            completed=False,
            priority="high",
            deadline=date.today() + timedelta(days=7),
            labels=["Work", "Urgent"],
            username="test_user"
        )
        
        created_todo = await todo_crud.create_todo(test_todo)
        print(f"✅ Todo created successfully with ID: {created_todo.id}")
        
        # Test reading the todo
        print("\n📖 Testing todo retrieval...")
        retrieved_todo = await todo_crud.get_todo_by_id(created_todo.id)
        if retrieved_todo:
            print(f"✅ Todo retrieved successfully: {retrieved_todo.title}")
        
        # Test listing todos
        print("\n📋 Testing todo listing...")
        all_todos = await todo_crud.get_all_todos(limit=5)
        print(f"✅ Retrieved {len(all_todos)} todos")
        
        # Test updating the todo
        print("\n✏️  Testing todo update...")
        from models import TodoUpdate
        update_data = TodoUpdate(completed=True)
        updated_todo = await todo_crud.update_todo(created_todo.id, update_data)
        if updated_todo and updated_todo.completed:
            print("✅ Todo updated successfully")
        
        # Test deleting the todo
        print("\n🗑️  Testing todo deletion...")
        deleted = await todo_crud.delete_todo(created_todo.id)
        if deleted:
            print("✅ Todo deleted successfully")
        
        # Close connection
        print("\n🔌 Closing database connection...")
        await close_mongo_connection()
        print("✅ Connection closed")
        
        print("\n🎉 All tests passed! Beanie ODM is working correctly!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure to install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_beanie_setup())

