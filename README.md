# Fidgi

Fidgi is a full-stack web application using Next.js for the frontend and FastAPI for the backend.

## Getting Started (Frontend)

### 1. Clone the repository

```bash
git clone <repo-url>
cd Fidgi
```

### 2. Create a `.env.local` file in the root directory

Add your Clerk keys to `.env.local`:

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key_here
CLERK_SECRET_KEY=your_clerk_secret_key_here
```

-   Get these keys from your Clerk dashboard.
-   **Do not commit `.env.local` to git.** It is already in `.gitignore`.

### 3. Install dependencies

```bash
pnpm install
```

### 4. Run the frontend

```bash
pnpm dev
```

The app will be available at `http://localhost:3000`.

## Getting Started (Backend)

See `backend/README.md` for backend setup instructions.

## Project Structure

```
Fidgi/
├── app/           # Next.js app directory
├── components/    # React components
├── backend/       # FastAPI backend
├── .env.local     # Clerk and other secrets (not committed)
├── package.json   # Frontend dependencies
└── ...
```

## Notes

-   Make sure to keep your Clerk keys private.
-   If you accidentally committed `.env.local`, remove it from git history and push again.
-   For backend API authentication, the frontend will send Clerk session tokens to the backend.
