from fastapi import APIRouter, HTTPException, Query, Path, status
from typing import List, Optional
import logging

from models import TodoCreate, TodoUpdate, TodoResponse
from crud import todo_crud

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/todos", tags=["todos"])


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    """
    Create a new todo item.
    
    - **title**: Todo title (1-100 characters)
    - **description**: Optional description (max 500 characters)
    - **completed**: Completion status (default: False)
    - **priority**: Priority level - high, medium, or low (default: medium)
    - **deadline**: Deadline date (must be today or later)
    - **labels**: List of labels (Work, Personal, Urgent)
    - **username**: Username (4-32 characters)
    """
    try:
        return await todo_crud.create_todo(todo)
    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create todo item"
        )


@router.get("/", response_model=List[TodoResponse])
async def get_todos(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, pattern="^(high|medium|low)$", description="Filter by priority")
):
    """
    Get all todo items with optional filtering and pagination.
    
    - **skip**: Number of items to skip (for pagination)
    - **limit**: Maximum number of items to return (1-1000)
    - **completed**: Filter by completion status (true/false)
    - **priority**: Filter by priority (high/medium/low)
    """
    try:
        return await todo_crud.get_all_todos(
            skip=skip, 
            limit=limit, 
            completed=completed, 
            priority=priority
        )
    except Exception as e:
        logger.error(f"Error getting todos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todo items"
        )


@router.get("/search", response_model=List[TodoResponse])
async def search_todos(
    q: str = Query(..., min_length=1, description="Search query (supports wildcards with *)"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return")
):
    """
    Search todo items by title and description.
    
    Supports wildcard searches using asterisk (*).
    Example: "project*" will match "project", "projects", etc.
    
    - **q**: Search query string
    - **skip**: Number of items to skip
    - **limit**: Maximum number of items to return
    """
    try:
        return await todo_crud.search_todos(query=q, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error searching todos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search todo items"
        )


@router.get("/count", response_model=dict)
async def get_todos_count(
    completed: Optional[bool] = Query(None, description="Filter by completion status")
):
    """
    Get total count of todo items.
    
    - **completed**: Optional filter by completion status
    """
    try:
        count = await todo_crud.get_todos_count(completed=completed)
        return {"count": count}
    except Exception as e:
        logger.error(f"Error getting todos count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get todo count"
        )


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str = Path(..., description="Todo item ID")
):
    """
    Get a specific todo item by ID.
    
    - **todo_id**: The unique identifier of the todo item
    """
    try:
        todo = await todo_crud.get_todo_by_id(todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id '{todo_id}' not found"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting todo {todo_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todo item"
        )


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_update: TodoUpdate,
    todo_id: str = Path(..., description="Todo item ID")
):
    """
    Update a specific todo item.
    
    Only provided fields will be updated. All fields are optional.
    
    - **todo_id**: The unique identifier of the todo item
    """
    try:
        todo = await todo_crud.update_todo(todo_id, todo_update)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id '{todo_id}' not found"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating todo {todo_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update todo item"
        )


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: str = Path(..., description="Todo item ID")
):
    """
    Delete a specific todo item.
    
    - **todo_id**: The unique identifier of the todo item
    """
    try:
        deleted = await todo_crud.delete_todo(todo_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id '{todo_id}' not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting todo {todo_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete todo item"
        )


# Convenience endpoints for common operations
@router.patch("/{todo_id}/complete", response_model=TodoResponse)
async def mark_todo_complete(
    todo_id: str = Path(..., description="Todo item ID")
):
    """
    Mark a todo item as completed.
    
    - **todo_id**: The unique identifier of the todo item
    """
    return await update_todo(TodoUpdate(completed=True), todo_id)


@router.patch("/{todo_id}/incomplete", response_model=TodoResponse)
async def mark_todo_incomplete(
    todo_id: str = Path(..., description="Todo item ID")
):
    """
    Mark a todo item as incomplete.
    
    - **todo_id**: The unique identifier of the todo item
    """
    return await update_todo(TodoUpdate(completed=False), todo_id)


@router.get("/user/{username}", response_model=List[TodoResponse])
async def get_todos_by_username(
    username: str = Path(..., min_length=4, max_length=32, description="Username"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status")
):
    """
    Get all todos for a specific user.
    
    - **username**: The username to filter by
    - **skip**: Number of items to skip
    - **limit**: Maximum number of items to return
    - **completed**: Optional filter by completion status
    """
    try:
        from models import Todo
        
        query = Todo.find(Todo.username == username)
        
        if completed is not None:
            query = query.find(Todo.completed == completed)
        
        todos = await query.sort(+Todo.deadline).skip(skip).limit(limit).to_list()
        
        return [todo_crud._to_response(todo) for todo in todos]
        
    except Exception as e:
        logger.error(f"Error getting todos for user {username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user's todo items"
        )
