"""Core package - exports database and configuration"""
from app.core.database import connect_to_mongo, close_mongo_connection, get_database, db

__all__ = [
    "connect_to_mongo",
    "close_mongo_connection",
    "get_database",
    "db",
]

