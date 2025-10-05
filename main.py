"""
Main entry point for the Todo List API application.
This is a wrapper that imports from the reorganized app package.
"""
from app.main import app

# For backward compatibility, expose the app at the root level
__all__ = ["app"]

if __name__ == "__main__":
    import os
    import uvicorn
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
