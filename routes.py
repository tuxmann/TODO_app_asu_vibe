from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
import logging

from models import TodoCreate, TodoUpdate, TodoResponse
from crud import todo_crud

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/todos", tags=["todos"])


@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate):
    """Create a new todo item"""
    try:
        return await todo_crud.create_todo(todo)
    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[TodoResponse])
async def get_todos(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, pattern="^(high|medium|low)$", description="Filter by priority")
):
    """Get all todo items with optional filtering and pagination"""
    try:
        return await todo_crud.get_all_todos(
            skip=skip, 
            limit=limit, 
            completed=completed, 
            priority=priority
        )
    except Exception as e:
        logger.error(f"Error getting todos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/search", response_model=List[TodoResponse])
async def search_todos(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return")
):
    """Search todo items by title and description"""
    try:
        return await todo_crud.search_todos(query=q, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error searching todos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/count")
async def get_todos_count(
    completed: Optional[bool] = Query(None, description="Filter by completion status")
):
    """Get total count of todo items"""
    try:
        count = await todo_crud.get_todos_count(completed=completed)
        return {"count": count}
    except Exception as e:
        logger.error(f"Error getting todos count: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str = Path(..., description="Todo item ID")
):
    """Get a specific todo item by ID"""
    try:
        todo = await todo_crud.get_todo_by_id(todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_update: TodoUpdate,
    todo_id: str = Path(..., description="Todo item ID")
):
    """Update a specific todo item"""
    try:
        todo = await todo_crud.update_todo(todo_id, todo_update)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: str = Path(..., description="Todo item ID")
):
    """Delete a specific todo item"""
    try:
        deleted = await todo_crud.delete_todo(todo_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Todo not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Convenience endpoints for common operations
@router.patch("/{todo_id}/complete", response_model=TodoResponse)
async def mark_todo_complete(
    todo_id: str = Path(..., description="Todo item ID")
):
    """Mark a todo item as completed"""
    return await update_todo(TodoUpdate(completed=True), todo_id)


@router.patch("/{todo_id}/incomplete", response_model=TodoResponse)
async def mark_todo_incomplete(
    todo_id: str = Path(..., description="Todo item ID")
):
    """Mark a todo item as incomplete"""
    return await update_todo(TodoUpdate(completed=False), todo_id)
