from fastapi import APIRouter

from app.api.v1.endpoints import todos

# Create the main API v1 router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(todos.router)

# Future routers can be added here:
# api_router.include_router(users.router)
# api_router.include_router(auth.router)

