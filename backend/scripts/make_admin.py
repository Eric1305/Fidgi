import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database.models import SessionLocal
from app.database import models

db = SessionLocal()

ADMIN_CLERK_IDS = [
    "user_35a8kjDGrcHJXYuBeQ3LYmmZEzn", # Zane
    "user_35R7k2p0k30xaZNAaD9lOz6buuu", # Thomas
    "user_35PXEJSeeR4IzaPCblNECgJcktD", # Steve
]

for clerk_id in ADMIN_CLERK_IDS:
    user = db.query(models.User).filter(models.User.clerk_user_id == clerk_id).first()
    if user:
        user.is_admin = 1
        print(f"✓ Set {user.name or user.email or clerk_id} as admin")
    else:
        print(f"✗ User with clerk_id {clerk_id} not found")

db.commit()
db.close()

print(f"\nAdmin setup complete!")
