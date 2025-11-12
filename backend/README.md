# Backend Setup Guide

This is the FastAPI backend for the Fidgi project.

## Prerequisites

-   Python 3.8 or higher
-   pip or another Python package manager

## Getting Started

### 1. Create a `.env` File

Create a `.env` file in the `backend/` directory with the necessary environment variables. You'll need to define:

```env
# Database Configuration
DATABASE_URL=sqlite:///../test.db

# Clerk Configuration (Public Key for JWT verification)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_aGlwLWJ1ZmZhbG8tMTcuY2xlcmsuYWNjb3VudHMuZGV2JA

# Clerk PEM Public Key (for JWT token verification)
CLERK_PEM_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5cqstKMtxiBXzkZxymq5\n0Keiy4mDd6smRTmRKdlfday2jfIVfOkrfthiEbOiJYQJF16FcfDT1bQTruGHvQSV\nEyhgbBK8jg8pSxvlpAagjI03+cSXpoFMdSJAcYZPp8hkv0BxtRPYd0+j9NhLG8SD\n45Jif64LIUyoFy079qkSMKedxIRVtJXE96dgnbHGFLYuOblE80x81IJJp5V/qoeH\nJjyz5Z79VXoqqgzrrWgVmzWc0nv9n1+jlyaXzpE+vHgxecq5GoavkuQ52H/meIcT\n1MuQTjZ0aF+UHh8MbECQWYvG6pPz4TabpwzG8j6qJXVIavRPk0SediILXgyXPsVV\n0wIDAQAB\n-----END PUBLIC KEY-----"
```

**Note:** Do not commit `.env` to version control. It's already in `.gitignore`.

### 2. Run the Backend

Simply run the startup script:

```bash
./run.sh
```

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

## Testing Protected Endpoints with Clerk Authentication

Protected endpoints require a valid Clerk session token. Here's how to test them using Swagger UI:

### Step 1: Start the Frontend

In a separate terminal, start the Next.js frontend:

```bash
cd /path/to/Fidgi
pnpm dev
```

The frontend will run on http://localhost:3000.

### Step 2: Sign In / Sign Up with Clerk

1. Open http://localhost:3000 in your browser
2. Click **Sign Up** or **Sign In** to create/login with a test account
3. Once authenticated, the Clerk user will appear in your Clerk dashboard

### Step 3: Get a Clerk Session Token

1. Keep the frontend open (logged in)
2. Open **DevTools** → **Console**
3. Paste and run this command:

```javascript
await window.Clerk.session.getToken();
```

4. Copy the token value (without quotes) that appears in the console

### Step 4: Authorize Swagger UI with the Token

1. Open http://localhost:8080/docs (Swagger UI)
2. Look for the **Authorize** button (top right)
3. Click **Authorize**
4. In the dialog that appears, paste your token in the **Value** field
5. Click **Authorize** to set the Authorization header for all requests

### Step 5: Test a Protected Endpoint

1. In Swagger UI, find a protected endpoint (e.g., `/me/profile`)
2. Click **Try it out**
3. Click **Execute**
4. You should receive a 200 response with user data (or a 401 if the token is invalid)

### Troubleshooting Token Issues

-   **401 Unauthorized**: Token may be expired or invalid. Get a new token from the frontend console.
-   **Missing Authorization header**: Make sure you clicked **Authorize** and the token was set in Swagger UI.
-   **CORS errors**: The backend allows `*` origins in development mode, so cross-origin requests should work. If issues persist, check the backend logs.

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
