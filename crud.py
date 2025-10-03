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
            # Convert date to string for MongoDB storage
            if 'deadline' in todo_dict:
                todo_dict['deadline'] = todo_dict['deadline'].isoformat()
            
            # Insert into database
            result = await collection.insert_one(todo_dict)
            
            # Retrieve the created todo
            created_todo = await collection.find_one({"_id": result.inserted_id})
            
            return self._format_todo_response(created_todo)
            
        except Exception as e:
            logger.error("Error creating todo: %s", e)
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
            logger.error("Error getting todo by ID %s: %s", todo_id, e)
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
            
            # Execute query with pagination (sort by deadline)
            cursor = collection.find(filter_query).sort("deadline", 1).skip(skip).limit(limit)
            todos = await cursor.to_list(length=limit)
            
            return [self._format_todo_response(todo) for todo in todos]
            
        except Exception as e:
            logger.error("Error getting todos: %s", e)
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
            
            # Convert date to string for MongoDB storage
            if 'deadline' in update_data:
                update_data['deadline'] = update_data['deadline'].isoformat()
            
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
            logger.error("Error updating todo %s: %s", todo_id, e)
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
            logger.error("Error deleting todo %s: %s", todo_id, e)
            raise
    
    async def search_todos(self, query: str, skip: int = 0, limit: int = 100) -> List[TodoResponse]:
        """Search todos by title and description with wildcard support"""
        try:
            collection = await get_collection(self.collection_name)
            
            # Convert wildcard pattern to regex
            if '*' in query:
                # Escape special regex characters except *
                import re
                escaped_query = re.escape(query).replace(r'\*', '.*')
                # Create regex pattern (case insensitive, matches anywhere in text)
                regex_pattern = escaped_query
                
                # Use regex search on title and description
                cursor = collection.find({
                    "$or": [
                        {"title": {"$regex": regex_pattern, "$options": "i"}},
                        {"description": {"$regex": regex_pattern, "$options": "i"}}
                    ]
                }).sort("deadline", 1).skip(skip).limit(limit)
            else:
                # Use text search for non-wildcard queries
                cursor = collection.find(
                    {"$text": {"$search": query}}
                ).sort("deadline", 1).skip(skip).limit(limit)
            
            todos = await cursor.to_list(length=limit)
            return [self._format_todo_response(todo) for todo in todos]
            
        except Exception as e:
            logger.error("Error searching todos with query '%s': %s", query, e)
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
            logger.error("Error getting todos count: %s", e)
            raise
    
    def _format_todo_response(self, todo_doc: dict) -> TodoResponse:
        """Convert database document to TodoResponse model"""
        from datetime import date as dt_date
        
        # Convert deadline string back to date object
        deadline_str = todo_doc.get("deadline")
        if isinstance(deadline_str, str):
            deadline = dt_date.fromisoformat(deadline_str)
        else:
            deadline = deadline_str
        
        return TodoResponse(
            id=str(todo_doc["_id"]),
            title=todo_doc["title"],
            description=todo_doc.get("description"),
            completed=todo_doc["completed"],
            priority=todo_doc.get("priority", "medium"),
            deadline=deadline,
            labels=todo_doc.get("labels", []),
            username=todo_doc["username"]
        )


# Create global instance
todo_crud = TodoCRUD()
