# Todo List API

A RESTful API for managing todo items built with FastAPI and MongoDB.

## Features

- ✅ Full CRUD operations for todo items
- 🔍 Search functionality
- 📊 Filtering by completion status and priority
- 📄 Pagination support
- 🏷️ Priority levels (low, medium, high)
- 📝 Detailed descriptions
- 🕐 Automatic timestamps
- 🔄 Async/await support
- 📚 Auto-generated API documentation

## Quick Start

### Prerequisites

- Python 3.8+
- MongoDB (local or remote)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd TODO_app_asu_vibe
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Configure your `.env` file:
```env
# MongoDB Configuration
project_db_url=mongodb://localhost:27017
project_db_name=todo_app_db

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

5. Start MongoDB (if running locally):
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or using system service
sudo systemctl start mongod
```

6. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Todo Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/todos/` | Create a new todo |
| GET | `/api/v1/todos/` | Get all todos (with filtering) |
| GET | `/api/v1/todos/{id}` | Get a specific todo |
| PUT | `/api/v1/todos/{id}` | Update a todo |
| DELETE | `/api/v1/todos/{id}` | Delete a todo |
| GET | `/api/v1/todos/search` | Search todos |
| GET | `/api/v1/todos/count` | Get todos count |
| PATCH | `/api/v1/todos/{id}/complete` | Mark todo as complete |
| PATCH | `/api/v1/todos/{id}/incomplete` | Mark todo as incomplete |

### Other Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |

## Usage Examples

### Create a Todo

```bash
curl -X POST "http://localhost:8000/api/v1/todos/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Learn FastAPI",
       "description": "Complete the FastAPI tutorial",
       "priority": "high"
     }'
```

### Get All Todos

```bash
curl "http://localhost:8000/api/v1/todos/"
```

### Filter Todos

```bash
# Get only completed todos
curl "http://localhost:8000/api/v1/todos/?completed=true"

# Get high priority todos
curl "http://localhost:8000/api/v1/todos/?priority=high"

# Pagination
curl "http://localhost:8000/api/v1/todos/?skip=0&limit=10"
```

### Search Todos

```bash
curl "http://localhost:8000/api/v1/todos/search?q=FastAPI"
```

### Update a Todo

```bash
curl -X PUT "http://localhost:8000/api/v1/todos/{todo_id}" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Learn FastAPI Advanced",
       "completed": true
     }'
```

### Delete a Todo

```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/{todo_id}"
```

## Data Model

### Todo Item

```json
{
  "id": "string",
  "title": "string (required, 1-100 chars)",
  "description": "string (optional, max 500 chars)",
  "completed": "boolean (default: false)",
  "priority": "string (low|medium|high, default: medium)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Development

### Project Structure

```
TODO_app_asu_vibe/
├── main.py           # FastAPI application entry point
├── models.py         # Pydantic models
├── database.py       # MongoDB connection and configuration
├── crud.py          # CRUD operations
├── routes.py        # API routes
├── requirements.txt # Python dependencies
├── .env.example     # Environment variables template
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

### Running in Development Mode

The application runs with auto-reload enabled by default when started with `python main.py`.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `project_db_url` | MongoDB connection URL | `mongodb://localhost:27017` |
| `project_db_name` | Database name | `todo_app_db` |
| `API_HOST` | API host | `0.0.0.0` |
| `API_PORT` | API port | `8000` |

## Error Handling

The API includes comprehensive error handling:

- **400**: Bad Request (validation errors)
- **404**: Not Found (todo doesn't exist)
- **500**: Internal Server Error
- **503**: Service Unavailable (database connection issues)

## Database

The application uses MongoDB with the following features:

- Automatic database and collection creation
- Indexes for better performance
- Text search capabilities
- Async operations with Motor driver

### Database Indexes

- `created_at`: For sorting by creation date
- Text index on `title` and `description`: For search functionality

## License

This project is created for educational purposes.