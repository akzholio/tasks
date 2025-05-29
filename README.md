
# Async Task Management API

A lightweight and modular FastAPI-based backend for task management with asynchronous SQLAlchemy, background processing, and PostgreSQL support.

## 🌐 Features

- FastAPI-based RESTful API
- Async SQLAlchemy support (PostgreSQL backend)
- Background task processing using `asyncio`
- Alembic migrations
- Full CRUD operations with task filtering & pagination
- Type hints, validation, and structured project layout
- Unit tests with `pytest` and `httpx`

---

## 📋 API Endpoints

| Method | Endpoint                    | Description                             |
|--------|-----------------------------|-----------------------------------------|
| POST   | `/tasks`                   | Create a new task                        |
| GET    | `/tasks`                   | List tasks (filtering + pagination)     |
| GET    | `/tasks/{task_id}`        | Get task details                         |
| PUT    | `/tasks/{task_id}`        | Update task (status, etc.)              |
| DELETE | `/tasks/{task_id}`        | Delete a task                            |
| POST   | `/tasks/{task_id}/process`| Trigger background processing            |
| GET    | `/healthcheck`            | Healthcheck endpoint                     |

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/yourname/async-task-api.git
cd async-task-api
```

### 2. Set up Python environment with Poetry
```bash
poetry install
```

### 3. Create and configure environment file
```bash
cp .env.example .env
# Update the DATABASE_URL in .env to point to your PostgreSQL instance
```

### 4. Start PostgreSQL with Docker (optional)
```bash
make docker-up
```

### 5. Run Alembic migrations
```bash
make upgrade
```

### 6. Start the application
```bash
make run
# OR for auto-reloading in development
make dev
```

### 7. Run tests
```bash
make test
```

---

## 🎨 Example Task Object
```json
{
  "title": "Clean up workspace",
  "description": "Remove unused files",
  "status": "pending",
  "priority": 2
}
```

---

## 🔧 Developer Workflow

- `make test` - run unit tests
- `make fmt` - auto-format code
- `make lint` - run linter
- `make migrate` - generate Alembic migration
- `make resetdb` - drop + recreate DB schema

---

## 📅 Future Improvements

- User authentication (OAuth2)
- Real-time status updates via WebSockets
- Email notifications

---

## 🛡 Monitoring (conceptual only)

- Use tools like **Prometheus** and **Grafana** for metrics
- Log aggregation with **ELK** or **Loki**
- Healthchecks, response time tracking
