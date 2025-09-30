from typing import List, Optional
from bson import ObjectId
from datetime import datetime
import logging

from database import get_collection
from models import TodoCreate, TodoUpdate, TodoResponse

logger = logging.getLogger(__name__)


class TodoCRUD:
    """CRUD operations for Todo items"""
    
    def __init__(self):
        self.collection_name = "todos"
    
    async def create_todo(self, todo_data: TodoCreate) -> TodoResponse:
        """Create a new todo item"""
        try:
            collection = await get_collection(self.collection_name)
            
            # Create todo document
            todo_dict = todo_data.dict()
            todo_dict["created_at"] = datetime.utcnow()
            todo_dict["updated_at"] = datetime.utcnow()
            
            # Insert into database
            result = await collection.insert_one(todo_dict)
            
            # Retrieve the created todo
            created_todo = await collection.find_one({"_id": result.inserted_id})
            
            return self._format_todo_response(created_todo)
            
        except Exception as e:
            logger.error(f"Error creating todo: {e}")
            raise
    
    async def get_todo_by_id(self, todo_id: str) -> Optional[TodoResponse]:
        """Get a todo item by ID"""
        try:
            if not ObjectId.is_valid(todo_id):
                return None
                
            collection = await get_collection(self.collection_name)
            todo = await collection.find_one({"_id": ObjectId(todo_id)})
            
            if todo:
                return self._format_todo_response(todo)
            return None
            
        except Exception as e:
            logger.error(f"Error getting todo by ID {todo_id}: {e}")
            raise
    
    async def get_all_todos(
        self, 
        skip: int = 0, 
        limit: int = 100,
        completed: Optional[bool] = None,
        priority: Optional[str] = None
    ) -> List[TodoResponse]:
        """Get all todo items with optional filtering"""
        try:
            collection = await get_collection(self.collection_name)
            
            # Build filter query
            filter_query = {}
            if completed is not None:
                filter_query["completed"] = completed
            if priority:
                filter_query["priority"] = priority
            
            # Execute query with pagination
            cursor = collection.find(filter_query).sort("created_at", -1).skip(skip).limit(limit)
            todos = await cursor.to_list(length=limit)
            
            return [self._format_todo_response(todo) for todo in todos]
            
        except Exception as e:
            logger.error(f"Error getting todos: {e}")
            raise
    
    async def update_todo(self, todo_id: str, todo_update: TodoUpdate) -> Optional[TodoResponse]:
        """Update a todo item"""
        try:
            if not ObjectId.is_valid(todo_id):
                return None
                
            collection = await get_collection(self.collection_name)
            
            # Build update document (only include non-None fields)
            update_data = {k: v for k, v in todo_update.dict().items() if v is not None}
            
            if not update_data:
                # No fields to update, return current todo
                return await self.get_todo_by_id(todo_id)
            
            # Add updated timestamp
            update_data["updated_at"] = datetime.utcnow()
            
            # Update the document
            result = await collection.update_one(
                {"_id": ObjectId(todo_id)},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                return None
            
            # Return updated todo
            return await self.get_todo_by_id(todo_id)
            
        except Exception as e:
            logger.error(f"Error updating todo {todo_id}: {e}")
            raise
    
    async def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item"""
        try:
            if not ObjectId.is_valid(todo_id):
                return False
                
            collection = await get_collection(self.collection_name)
            result = await collection.delete_one({"_id": ObjectId(todo_id)})
            
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting todo {todo_id}: {e}")
            raise
    
    async def search_todos(self, query: str, skip: int = 0, limit: int = 100) -> List[TodoResponse]:
        """Search todos by title and description"""
        try:
            collection = await get_collection(self.collection_name)
            
            # Use text search
            cursor = collection.find(
                {"$text": {"$search": query}}
            ).sort("created_at", -1).skip(skip).limit(limit)
            
            todos = await cursor.to_list(length=limit)
            return [self._format_todo_response(todo) for todo in todos]
            
        except Exception as e:
            logger.error(f"Error searching todos with query '{query}': {e}")
            raise
    
    async def get_todos_count(self, completed: Optional[bool] = None) -> int:
        """Get total count of todos"""
        try:
            collection = await get_collection(self.collection_name)
            
            filter_query = {}
            if completed is not None:
                filter_query["completed"] = completed
            
            return await collection.count_documents(filter_query)
            
        except Exception as e:
            logger.error(f"Error getting todos count: {e}")
            raise
    
    def _format_todo_response(self, todo_doc: dict) -> TodoResponse:
        """Convert database document to TodoResponse model"""
        return TodoResponse(
            id=str(todo_doc["_id"]),
            title=todo_doc["title"],
            description=todo_doc.get("description"),
            completed=todo_doc["completed"],
            priority=todo_doc.get("priority", "medium"),
            created_at=todo_doc["created_at"],
            updated_at=todo_doc["updated_at"]
        )


# Create global instance
todo_crud = TodoCRUD()
