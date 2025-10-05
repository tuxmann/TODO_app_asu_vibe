from typing import List, Optional
from datetime import datetime
import logging
import re
from beanie.operators import RegEx, Text, Or

from models import Todo, TodoCreate, TodoUpdate, TodoResponse

logger = logging.getLogger(__name__)


class TodoCRUD:
    """CRUD operations for Todo items using Beanie ODM"""
    
    async def create_todo(self, todo_data: TodoCreate) -> TodoResponse:
        """Create a new todo item"""
        try:
            # Create Todo document from Pydantic schema
            # Convert TodoCreate to dict and create Todo document
            todo_dict = todo_data.model_dump()
            todo = Todo(**todo_dict)
            
            # Insert into database using Beanie
            await todo.insert()
            
            # Return response
            return self._to_response(todo)
            
        except Exception as e:
            logger.error("Error creating todo: %s", e)
            raise
    
    async def get_todo_by_id(self, todo_id: str) -> Optional[TodoResponse]:
        """Get a todo item by ID"""
        try:
            # Use Beanie's get method
            todo = await Todo.get(todo_id)
            
            if todo:
                return self._to_response(todo)
            return None
            
        except Exception as e:
            logger.error(f"Error getting todo by ID {todo_id}: {e}")
            return None
    
    async def get_all_todos(
        self, 
        skip: int = 0, 
        limit: int = 100,
        completed: Optional[bool] = None,
        priority: Optional[str] = None
    ) -> List[TodoResponse]:
        """Get all todo items with optional filtering"""
        try:
            # Build query using Beanie
            query = Todo.find()
            
            # Apply filters
            if completed is not None:
                query = query.find(Todo.completed == completed)
            if priority:
                query = query.find(Todo.priority == priority)
            
            # Execute query with pagination and sorting
            todos = await query.sort(+Todo.deadline).skip(skip).limit(limit).to_list()
            
            return [self._to_response(todo) for todo in todos]
            
        except Exception as e:
            logger.error(f"Error getting todos: {e}")
            raise
    
    async def update_todo(self, todo_id: str, todo_update: TodoUpdate) -> Optional[TodoResponse]:
        """Update a todo item"""
        try:
            # Get the todo
            todo = await Todo.get(todo_id)
            
            if not todo:
                return None
            
            # Update fields (only non-None values)
            update_data = todo_update.model_dump(exclude_unset=True)
            
            if not update_data:
                # No fields to update
                return self._to_response(todo)
            
            # Update timestamp
            update_data['updated_at'] = datetime.utcnow()
            
            # Apply updates to the document
            for field, value in update_data.items():
                setattr(todo, field, value)
            
            # Save to database
            await todo.save()
            
            return self._to_response(todo)
            
        except Exception as e:
            logger.error(f"Error updating todo {todo_id}: {e}")
            raise
    
    async def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item"""
        try:
            todo = await Todo.get(todo_id)
            
            if not todo:
                return False
            
            # Delete using Beanie
            await todo.delete()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting todo {todo_id}: {e}")
            raise
    
    async def search_todos(self, query: str, skip: int = 0, limit: int = 100) -> List[TodoResponse]:
        """Search todos by title and description"""
        try:
            # Handle wildcard search
            if '*' in query:
                # Convert wildcard to regex pattern
                escaped_query = re.escape(query).replace(r'\*', '.*')
                
                # Search using regex in title or description
                todos = await Todo.find(
                    Or(
                        RegEx(Todo.title, escaped_query, options='i'),
                        RegEx(Todo.description, escaped_query, options='i')
                    )
                ).sort(+Todo.deadline).skip(skip).limit(limit).to_list()
            else:
                # Use text search
                todos = await Todo.find(
                    Text(query)
                ).sort(+Todo.deadline).skip(skip).limit(limit).to_list()
            
            return [self._to_response(todo) for todo in todos]
            
        except Exception as e:
            logger.error(f"Error searching todos with query '{query}': {e}")
            raise
    
    async def get_todos_count(self, completed: Optional[bool] = None) -> int:
        """Get total count of todos"""
        try:
            query = Todo.find()
            
            if completed is not None:
                query = query.find(Todo.completed == completed)
            
            return await query.count()
            
        except Exception as e:
            logger.error(f"Error getting todos count: {e}")
            raise
    
    def _to_response(self, todo: Todo) -> TodoResponse:
        """Convert Todo document to TodoResponse"""
        from datetime import datetime, date as dt_date
        
        # Convert deadline back to date if it's datetime
        deadline = todo.deadline
        if isinstance(deadline, datetime):
            deadline = deadline.date()
        elif not isinstance(deadline, dt_date):
            deadline = dt_date.fromisoformat(str(deadline))
        
        return TodoResponse(
            id=str(todo.id),
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            priority=todo.priority,
            deadline=deadline,
            labels=todo.labels,
            username=todo.username,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )


# Create global instance
todo_crud = TodoCRUD()
