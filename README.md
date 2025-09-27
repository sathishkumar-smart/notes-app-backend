# Keep Notes

This is the **FastAPI backend** for the Keep Notes App.

It provides REST APIs for creating, updating, deleting, and fetching notes. This backend is designed to work with a MySQL database and can be easily run locally or via Docker.

---

## Features

* FastAPI (Python 3.12)
* MySQL database
* Docker-ready for production
* CRUD APIs for Notes
* Supports connection to the frontend app via environment variables

---

## Requirements

* Python 3.12+
* pip
* MySQL 8+
* Docker & Docker Compose (optional but recommended)

---

## .env Configuration

Create a `.env` file in the root directory with the following content:

```env
# Database connection
DATABASE_URL=mysql+pymysql://notesuser:notespass@db:3306/notesapp

# FastAPI secret key
SECRET_KEY=your-secret-key

# Frontend URL (used for CORS)
FRONTEND_URL=http://localhost:3000
```

> **Important:** Add `.env` to `.gitignore` to avoid pushing sensitive credentials.

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running Locally

1. Make sure MySQL is running locally and the database `notesapp` exists.
2. Set your `.env` variables.
3. Run the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Docker Setup (Recommended)

### 1. Build and run using Docker Compose

```bash
docker-compose build
docker-compose up
```

### 2. Access

* FastAPI backend: [http://localhost:8000](http://localhost:8000)
* MySQL: `localhost:3306` (username/password from `.env`)

---

## Frontend Integration

Update the `.env` file in your **frontend** with:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

> This ensures the frontend app can call the backend APIs.

---

## Notes

* Use `requirements.txt` to freeze dependencies:

```bash
pip freeze > requirements.txt
```

* All sensitive information (like database credentials) should always remain in `.env`.
* Docker Compose automatically sets the MySQL host to the service name `db`.

---

## License

MIT License
