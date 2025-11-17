#!/bin/bash

# === Fidgi Backend Setup & Run Script ===

# Check if virtual environment exists; create if it doesn't
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Installing default dependencies..."
    pip install fastapi uvicorn psycopg2-binary sqlalchemy python-dotenv
    echo "Freezing installed packages to requirements.txt..."
    pip freeze > requirements.txt
fi

# Run FastAPI server
echo "Starting FastAPI server on http://localhost:8000 ..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload