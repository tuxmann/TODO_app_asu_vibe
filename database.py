import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def get_database():
    """Get database instance"""
    return db.database


async def connect_to_mongo():
    """Create database connection"""
    try:
        # Get configuration from environment variables
        db_url = os.getenv("project_db_url", "mongodb://localhost:27017")
        db_name = os.getenv("project_db_name", "todo_app_db")
        
        logger.info(f"Connecting to MongoDB at {db_url}")
        
        # Create client with timeout settings
        db.client = AsyncIOMotorClient(
            db_url,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=10000,  # 10 second connection timeout
            socketTimeoutMS=10000,   # 10 second socket timeout
        )
        
        # Test the connection
        await db.client.admin.command('ping')
        
        # Get database (will be created if it doesn't exist)
        db.database = db.client[db_name]
        
        # Create indexes for better performance
        await create_indexes()
        
        logger.info(f"Successfully connected to MongoDB database: {db_name}")
        
    except ServerSelectionTimeoutError:
        logger.error("Failed to connect to MongoDB: Server selection timeout")
        raise
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("Disconnected from MongoDB")


async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Create index on created_at field for sorting
        await db.database.todos.create_index("created_at")
        
        # Create text index for searching in title and description
        await db.database.todos.create_index([
            ("title", "text"),
            ("description", "text")
        ])
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.warning(f"Failed to create indexes: {e}")


async def get_collection(collection_name: str):
    """Get a collection from the database"""
    return db.database[collection_name]
