#!/usr/bin/env python3
"""
Startup script for the Todo List API
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("📝 Please create a .env file with the following content:")
        print("""
# MongoDB Configuration
project_db_url=mongodb://localhost:27017
project_db_name=todo_app_db

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
        """)
        return False
    print("✅ .env file found")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_mongodb():
    """Check if MongoDB is accessible"""
    try:
        import pymongo
        from dotenv import load_dotenv
        
        load_dotenv()
        db_url = os.getenv("project_db_url", "mongodb://localhost:27017")
        
        client = pymongo.MongoClient(db_url, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        client.close()
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("💡 Make sure MongoDB is running:")
        print("   - Docker: docker run -d -p 27017:27017 --name mongodb mongo:latest")
        print("   - System service: sudo systemctl start mongod")
        return False

def start_application():
    """Start the FastAPI application"""
    print("🚀 Starting Todo List API...")
    try:
        import uvicorn
        from dotenv import load_dotenv
        
        load_dotenv()
        host = os.getenv("API_HOST", "0.0.0.0")
        port = int(os.getenv("API_PORT", "8000"))
        
        print(f"🌐 API will be available at: http://{host}:{port}")
        print(f"📚 API Documentation: http://{host}:{port}/docs")
        print("🛑 Press Ctrl+C to stop the server")
        
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main startup function"""
    print("🎯 Todo List API Startup")
    print("=" * 30)
    
    # Check Python version
    check_python_version()
    
    # Check .env file
    if not check_env_file():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check MongoDB connection
    if not check_mongodb():
        print("⚠️  MongoDB connection failed, but starting anyway...")
        print("   The API will fail until MongoDB is available")
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()
