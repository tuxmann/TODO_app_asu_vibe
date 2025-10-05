import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def connect_to_mongo():
    """Initialize database connection and Beanie ODM"""
    try:
        # Get configuration from environment variables
        db_url = os.getenv("project_db_url", "mongodb://localhost:27017")
        db_name = os.getenv("project_db_name", "todo_app_db")
        
        logger.info(f"Connecting to MongoDB at {db_url}")
        
        # Create Motor client
        db.client = AsyncIOMotorClient(
            db_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
        )
        
        # Test the connection
        await db.client.admin.command('ping')
        logger.info("Successfully pinged MongoDB")
        
        # Get database
        database = db.client[db_name]
        
        # Import document models
        from app.models.todo import Todo
        from app.models.user import User
        
        # Initialize Beanie with all document models
        await init_beanie(
            database=database,
            document_models=[Todo, User]
        )
        
        logger.info(f"Beanie ODM initialized with database: {db_name}")
        logger.info("Application startup completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("MongoDB connection closed")


async def get_database():
    """Get the database instance"""
    if db.client:
        db_name = os.getenv("project_db_name", "todo_app_db")
        return db.client[db_name]
    raise Exception("Database not initialized")

