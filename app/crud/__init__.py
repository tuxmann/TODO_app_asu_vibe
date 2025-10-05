"""CRUD package - exports all CRUD operations"""
from app.crud.todo import todo_crud, TodoCRUD
from app.crud.user import user_crud, UserCRUD

__all__ = [
    "todo_crud",
    "TodoCRUD",
    "user_crud",
    "UserCRUD",
]

