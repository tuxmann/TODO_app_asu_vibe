# Setup Instructions

## Quick Start

### 1. Create Virtual Environment
```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
project_db_url=mongodb://localhost:27017
project_db_name=todo_app_db
API_HOST=0.0.0.0
API_PORT=8000
```

### 5. Make Sure MongoDB is Running
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Start MongoDB if not running
sudo systemctl start mongod

# Or use Docker
docker run -d -p 27017:27017 --name mongodb mongo
```

### 6. Test the Setup
```bash
python test_beanie_setup.py
```

Expected output:
```
🚀 Testing Beanie ODM setup...
✅ Imports successful
📡 Connecting to MongoDB...
✅ Connected to MongoDB successfully
📝 Testing todo creation...
✅ Todo created successfully with ID: ...
📖 Testing todo retrieval...
✅ Todo retrieved successfully: Test Todo Item
📋 Testing todo listing...
✅ Retrieved X todos
✏️  Testing todo update...
✅ Todo updated successfully
🗑️  Testing todo deletion...
✅ Todo deleted successfully
🔌 Closing database connection...
✅ Connection closed
🎉 All tests passed! Beanie ODM is working correctly!
```

### 7. Run the Application
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

### 8. Access the API
- API Root: http://localhost:8000/
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Troubleshooting

### Issue: `datetime.date` object is not iterable

**Solution:** This has been fixed by adding BSON encoders in the `Todo` Document model:

```python
class Settings:
    bson_encoders = {
        date: lambda v: datetime.combine(v, datetime.min.time()),
        datetime: lambda v: v
    }
```

This converts Python `date` objects to MongoDB-compatible `datetime` objects.

### Issue: Cannot import 'beanie'

**Solution:** Make sure you've installed the requirements in your virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Connection refused to MongoDB

**Solution:** Make sure MongoDB is running:
```bash
sudo systemctl start mongod
```

Or check your MongoDB connection string in `.env`.

### Issue: Module not found errors

**Solution:** Always activate the virtual environment before running Python scripts:
```bash
source venv/bin/activate
```

## Development Workflow

1. Always activate the virtual environment first:
   ```bash
   source venv/bin/activate
   ```

2. Run the application in development mode:
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

3. Test your changes:
   ```bash
   python test_beanie_setup.py
   ```

4. Deactivate when done:
   ```bash
   deactivate
   ```

## Project Structure

```
TODO_app_asu_vibe/
├── main.py              # FastAPI application entry point
├── models.py            # Beanie Document models & Pydantic schemas
├── database.py          # Database connection & Beanie initialization
├── crud.py              # CRUD operations using Beanie ODM
├── routes.py            # API endpoints
├── requirements.txt     # Python dependencies
├── test_beanie_setup.py # Test script
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore rules
├── venv/               # Virtual environment (created by you)
├── BEANIE_GUIDE.md     # Comprehensive Beanie ODM guide
├── MIGRATION_SUMMARY.md # Migration details
└── SETUP_INSTRUCTIONS.md # This file
```

## API Endpoints

### Todo Operations

- `POST /api/v1/todos/` - Create a new todo
- `GET /api/v1/todos/` - List all todos (with filtering)
- `GET /api/v1/todos/{id}` - Get a specific todo
- `PUT /api/v1/todos/{id}` - Update a todo
- `DELETE /api/v1/todos/{id}` - Delete a todo
- `PATCH /api/v1/todos/{id}/complete` - Mark todo as complete
- `PATCH /api/v1/todos/{id}/incomplete` - Mark todo as incomplete

### Search & Filter

- `GET /api/v1/todos/search?q=query` - Search todos
- `GET /api/v1/todos/count` - Count todos
- `GET /api/v1/todos/user/{username}` - Get user's todos

### Health & Info

- `GET /` - API information
- `GET /health` - Health check

## Example API Calls

### Create a Todo
```bash
curl -X POST "http://localhost:8000/api/v1/todos/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Beanie ODM",
    "description": "Master MongoDB ODM for Python",
    "priority": "high",
    "deadline": "2024-12-31",
    "labels": ["Work"],
    "username": "developer"
  }'
```

### Get All Todos
```bash
curl "http://localhost:8000/api/v1/todos/"
```

### Search Todos
```bash
curl "http://localhost:8000/api/v1/todos/search?q=learn"
```

### Update a Todo
```bash
curl -X PUT "http://localhost:8000/api/v1/todos/{todo_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

## Next Steps

1. ✅ Setup complete - all tests passing
2. 📚 Read `BEANIE_GUIDE.md` for advanced features
3. 🚀 Start building your application
4. 📝 Check the interactive API docs at `/docs`

## Resources

- [Beanie Documentation](https://beanie-odm.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)

