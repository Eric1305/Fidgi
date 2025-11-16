# Fidgi

Fidgi is a full-stack web application using Next.js for the frontend and FastAPI for the backend with Clerk authentication.

---

## Frontend + Backend Setup Guide

This guide walks you through connecting our Next.js frontend with the FastAPI backend using Clerk authentication. Each team member will set up their own development environment with individual ngrok tunnels.

### Prerequisites

- Node.js and pnpm installed
- Python 3.x installed
- Clerk account access
- ngrok installed (see Step 3)

---

### Step 1: Clone the Repository

```bash
git clone <repo-url>
cd Fidgi
```

---

### Step 2: Frontend Environment Setup

Create a `.env.local` file in the **root directory** (same level as `package.json`):

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_aGlwLWJ1ZmZhbG8tMTcuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY=[check Discord for shared key]
```

⚠️ **Important:** The `.env.local` file goes in your project root directory, NOT in the backend folder.

---

### Step 3: Backend Environment Setup

Create a `.env` file in the **`backend/`** directory (same level as `run.sh`):

```env
CLERK_SECRET_KEY=[check Discord for shared key]
CLERK_WEBHOOK_SECRET=[you'll generate your own in Step 6]
JWT_KEY="-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5cqstKMtxiBXzkZxymq5
0Keiy4mDd6smRTmRKdlfday2jfIVfOkrfthiEbOiJYQJF16FcfDT1bQTruGHvQSV
EyhgbBK8jg8pSxvlpAagjI03+cSXpoFMdSJAcYZPp8hkv0BxtRPYd0+j9NhLG8SD
45Jif64LIUyoFy079qkSMKedxIRVtJXE96dgnbHGFLYuOblE80x81IJJp5V/qoeH
Jjyz5Z79VXoqqgzrrWgVmzWc0nv9n1+jlyaXzpE+vHgxecq5GoavkuQ52H/meIcT
1MuQTjZ0aF+UHh8MbECQWYvG6pPz4TabpwzG8j6qJXVIavRPk0SediILXgyXPsVV
0wIDAQAB
-----END PUBLIC KEY-----"
DATABASE_URL=sqlite:///./database.db
```

📁 **Location:** This file goes in the `backend/` directory.

---

### Step 4: Install Dependencies

**Frontend:**

```bash
pnpm install
```

**Backend:**

The backend dependencies will be installed automatically when you run `./run.sh` in Step 7.

---

### Step 5: Install ngrok

Visit [https://dashboard.ngrok.com/get-started/setup](https://dashboard.ngrok.com/get-started/setup) and follow the instructions for your OS.

After installation, authenticate ngrok with your token:

```bash
ngrok config add-authtoken YOUR_NGROK_TOKEN
```

---

### Step 6: Start ngrok Tunnel

In a **new terminal window**, run:

```bash
ngrok http 8000
```

**You'll see output like this:**

```
Forwarding https://abc123.ngrok.io -> http://localhost:8000
```

> ⚠️ **Copy your unique ngrok URL** - you'll need it for the next step!
>
> 📝 **Note:** This URL changes every time you restart ngrok (unless you have a paid plan). Keep this terminal window open while developing.

---

### Step 7: Configure Clerk Webhook

1. Go to [Clerk Dashboard](https://dashboard.clerk.com), then click on **Webhooks**
2. Click **"Add Endpoint"**
3. For **Endpoint URL**, enter: `https://YOUR-NGROK-URL.ngrok.io/clerk`
   - Example: `https://abc123.ngrok.io/clerk`
   - ⚠️ Don't forget the `/clerk` at the end!
4. In the **Description** field, add your name (e.g., "Steve's Dev Webhook")
5. Under **Subscribe to events**, check the box for `user.created`
6. Click **"Create"**
7. Copy the **webhook secret** (it starts with `whsec_...`)
8. Add it to your `backend/.env` file:
   ```env
   CLERK_WEBHOOK_SECRET=whsec_your_secret_here
   ```

---

### Step 8: Start the Application

**Terminal 1 - Start Backend:**

```bash
cd backend
./run.sh
```

The backend will run on `http://localhost:3000`.

**Terminal 2 - Start Frontend:**

```bash
pnpm dev
```

The frontend will run on `http://localhost:3000`.

---

### Step 9: Test the Connection

1. Open browser: [http://localhost:3000](http://localhost:3000)
2. Sign up with a new account
3. Visit test page: [http://localhost:3000/test](http://localhost:3000/test)

If everything is working, you should see:

- Clerk user info
- Database profile (synced via webhook)
- List of all users

---

## Project Structure

```
Fidgi/
├── app/           # Next.js app directory
├── components/    # React components
├── backend/       # FastAPI backend
├── .env.local     # Frontend Clerk keys (not committed)
├── package.json   # Frontend dependencies
└── README.md
```

---

## Notes

- **Keep your Clerk keys private.** Never commit `.env.local` or `backend/.env` to git.
- If you accidentally committed secrets, remove them from git history immediately.
- Your ngrok URL changes each time you restart it (unless you have a paid plan).
- Each team member needs their own ngrok tunnel and Clerk webhook endpoint.

---

## Troubleshooting

**Backend won't start:**

- Check that `backend/.env` exists and has all required keys
- Make sure Python 3.x is installed: `python3 --version`

**Frontend can't connect to backend:**

- Verify backend is running on port 8000
- Check CORS settings in `backend/app/main.py`

**Webhook not working:**

- Verify ngrok is running and forwarding to port 8000
- Check Clerk webhook endpoint URL ends with `/clerk`
- Make sure `CLERK_WEBHOOK_SECRET` matches the one in Clerk dashboard

**Users not appearing in database:**

- Check ngrok terminal for incoming webhook requests
- Verify `user.created` event is enabled in Clerk webhook settings
- Check backend logs for errors
