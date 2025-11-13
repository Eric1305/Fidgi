from fastapi import APIRouter, Request, HTTPException, Depends
from ..database.db import create_user
from ..database.models import get_db
from svix.webhooks import Webhook
import os
import json

router = APIRouter()

@router.post("/clerk")
async def handle_clerk_webhook(request: Request, db=Depends(get_db)):
    webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")

    if not webhook_secret:
        raise HTTPException(status_code=500, detail="CLERK_WEBHOOK_SECRET not set")

    body = await request.body()
    payload = body.decode("utf-8")
    headers = dict(request.headers)

    try:
        wh = Webhook(webhook_secret)
        wh.verify(payload, headers)

        data = json.loads(payload)

        if data.get("type") != "user.created":
            return {"status": "ignored"}

        user_data = data.get("data", {})
        clerk_user_id = user_data.get("id")
        name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
        email = user_data.get("email_addresses", [{}])[0].get("email_address")

        create_user(db, clerk_user_id, name=name, email=email)

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))