# Beanie ODM Implementation Guide

## Overview

This Todo API application now uses **Beanie ODM** (Object-Document Mapper) for MongoDB operations. Beanie provides an elegant way to work with MongoDB documents as Python objects with full Pydantic integration.

## What Changed?

### 1. **Dependencies** (`requirements.txt`)
- Replaced `motor==3.3.2` with `beanie==1.23.6`
- Beanie includes Motor as a dependency, so we still have async MongoDB support

### 2. **Models** (`models.py`)

#### Beanie Document Model
```python
class Todo(Document):
    """Beanie Document model for MongoDB collection"""
    title: str
    description: Optional[str]
    completed: bool = False
    priority: str = "medium"
    deadline: date
    labels: List[str]
    username: str
    created_at: datetime
    updated_at: datetime
    
    class Settings:
        name = "todos"  # MongoDB collection name
        indexes = ["deadline", "completed", "priority", "username"]
```

**Key Features:**
- Inherits from `Document` (Beanie's base class)
- Automatic `_id` field handling
- Type validation via Pydantic
- Built-in index management

#### Pydantic Schemas
- `TodoCreate`: Schema for creating new todos
- `TodoUpdate`: Schema for partial updates
- `TodoResponse`: Schema for API responses

### 3. **Database Connection** (`database.py`)

```python
from beanie import init_beanie
from models import Todo

# Initialize Beanie
await init_beanie(
    database=database,
    document_models=[Todo]
)
```

**Key Changes:**
- Uses `init_beanie()` to initialize ODM
- Registers document models
- Automatic index creation

### 4. **CRUD Operations** (`crud.py`)

#### Create
```python
todo = Todo(**todo_data.model_dump())
await todo.insert()
```

#### Read
```python
# By ID
todo = await Todo.get(todo_id)

# Query with filters
todos = await Todo.find(Todo.completed == True).to_list()

# With pagination and sorting
todos = await Todo.find().sort(+Todo.deadline).skip(0).limit(100).to_list()
```

#### Update
```python
todo = await Todo.get(todo_id)
todo.title = "Updated title"
await todo.save()
```

#### Delete
```python
todo = await Todo.get(todo_id)
await todo.delete()
```

### 5. **Routes** (`routes.py`)

All routes now use the Beanie-powered CRUD operations:

- `POST /api/v1/todos/` - Create todo
- `GET /api/v1/todos/` - List todos (with filters)
- `GET /api/v1/todos/{todo_id}` - Get single todo
- `PUT /api/v1/todos/{todo_id}` - Update todo
- `DELETE /api/v1/todos/{todo_id}` - Delete todo
- `GET /api/v1/todos/search` - Search todos
- `GET /api/v1/todos/count` - Count todos
- `PATCH /api/v1/todos/{todo_id}/complete` - Mark complete
- `PATCH /api/v1/todos/{todo_id}/incomplete` - Mark incomplete
- `GET /api/v1/todos/user/{username}` - Get user's todos

## Benefits of Beanie ODM

### 1. **Type Safety**
- Full Pydantic integration
- Type hints throughout
- Validation at the model level

### 2. **Cleaner Code**
```python
# Before (Motor):
collection = await get_collection("todos")
result = await collection.insert_one(todo_dict)

# After (Beanie):
todo = Todo(**todo_data)
await todo.insert()
```

### 3. **Query Builder**
```python
# Intuitive query syntax
todos = await Todo.find(
    Todo.completed == False,
    Todo.priority == "high"
).sort(+Todo.deadline).to_list()
```

### 4. **Automatic Index Management**
Indexes defined in the model are automatically created.

### 5. **Built-in Serialization**
Automatic conversion between MongoDB documents and Pydantic models.

## Installation

```bash
pip install -r requirements.txt
```

## Testing

Run the test script to verify setup:

```bash
python test_beanie_setup.py
```

## Running the Application

```bash
# Development mode
python main.py

# Or using uvicorn directly
uvicorn main:app --reload
```

## API Documentation

Once running, access the interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Advanced Beanie Features

### Aggregation Pipelines
```python
from beanie import PydanticObjectId

results = await Todo.aggregate([
    {"$match": {"completed": False}},
    {"$group": {"_id": "$priority", "count": {"$sum": 1}}}
]).to_list()
```

### Text Search
```python
from beanie.operators import Text

todos = await Todo.find(Text("important")).to_list()
```

### Regex Search
```python
from beanie.operators import RegEx

todos = await Todo.find(
    RegEx(Todo.title, "project.*", options="i")
).to_list()
```

### Complex Queries
```python
from beanie.operators import And, Or, In

todos = await Todo.find(
    Or(
        Todo.priority == "high",
        And(
            Todo.priority == "medium",
            Todo.deadline < date.today() + timedelta(days=7)
        )
    )
).to_list()
```

## Environment Variables

Create a `.env` file:

```env
project_db_url=mongodb://localhost:27017
project_db_name=todo_app_db
API_HOST=0.0.0.0
API_PORT=8000
```

## Example Usage

### Create a Todo
```bash
curl -X POST "http://localhost:8000/api/v1/todos/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete documentation",
    "description": "Write comprehensive API docs",
    "priority": "high",
    "deadline": "2024-12-31",
    "labels": ["Work", "Urgent"],
    "username": "john_doe"
  }'
```

### Get All Todos
```bash
curl "http://localhost:8000/api/v1/todos/?limit=10&completed=false"
```

### Update a Todo
```bash
curl -X PUT "http://localhost:8000/api/v1/todos/{todo_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

## Resources

- [Beanie Documentation](https://beanie-odm.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)

