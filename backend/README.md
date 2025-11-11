# Backend Setup Guide

This is the FastAPI backend for the Fidgi project.

## Prerequisites

-   Python 3.8 or higher
-   pip or another Python package manager

## Getting Started

### 1. Create a `.env` File

Create a `.env` file in the `backend/` directory with the necessary environment variables. You'll need to define:

````env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/fidgi_db

**Note:** Do not commit `.env` to version control. It's already in `.gitignore`.

### 2. Run the Backend

Simply run the startup script:

```bash
./run.sh
````

This script will:

1. Create a virtual environment (if it doesn't exist)
2. Activate the virtual environment
3. Install dependencies from `requirements.txt`
4. Start the FastAPI server on `http://localhost:8080`

The server will automatically reload when you make changes to the code.

## Stopping the Server

Press `CTRL+C` in the terminal to stop the server.

## API Documentation

Once the server is running, you can access:

-   **Swagger UI**: http://localhost:8080/docs
-   **ReDoc**: http://localhost:8080/redoc

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── routes/           # API endpoint definitions
│   ├── utils/            # Utility functions (auth, etc.)
│   ├── models/           # Database models
│   └── schemas/          # Pydantic request/response schemas
├── requirements.txt      # Python dependencies
├── run.sh               # Startup script
├── .env                 # Environment variables (not in repo)
└── venv/                # Virtual environment
```

## Troubleshooting

### Module Not Found Errors

If you see `ModuleNotFoundError`, make sure:

1. Your `.env` file exists
2. You've run `./run.sh` to install all dependencies
3. The virtual environment is activated

### Port Already in Use

If port 8080 is already in use, you can change it in `run.sh`:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Development

To add new dependencies:

1. Install the package: `pip install package_name`
2. Add it to `requirements.txt`
3. Commit the updated `requirements.txt`
