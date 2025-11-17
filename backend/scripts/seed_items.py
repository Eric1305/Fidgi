import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import models
from app.database.models import SessionLocal, discountCode
from app.database.db import create_item

db = SessionLocal()

items = [
    {
        "name": "Infinity Cube",
        "price": 24.99,
        "image": "/img/metallic-infinity-cube-fidget-toy.jpg",
        "category": "Cubes",
        "description": "Premium aluminum infinity cube with smooth rotation",
        "quantity": 50
    },
    {
        "name": "Magnetic Spinner",
        "price": 19.99,
        "image": "/img/colorful-magnetic-fidget-spinner.jpg",
        "category": "Spinners",
        "description": "High-speed magnetic bearing spinner",
        "quantity": 0
    },
    {
        "name": "Sensory Ring Set",
        "price": 14.99,
        "image": "/img/colorful-fidget-rings-set.jpg",
        "category": "Rings",
        "description": "Silicone textured rings for tactile stimulation",
        "quantity": 4
    },
    {
        "name": "Fidget Pad Pro",
        "price": 29.99,
        "image": "/img/multi-function-fidget-pad-with-buttons.jpg",
        "category": "Pads",
        "description": "Multi-function pad with buttons, switches, and sliders",
        "quantity": 3
    },
    {
        "name": "Mesh Marble",
        "price": 16.99,
        "image": "/img/mesh-and-marble-fidget-toy.jpg",
        "category": "Marbles",
        "description": "Stainless steel mesh with satisfying marble movement",
        "quantity": 60
    },
    {
        "name": "Chain Links",
        "price": 12.99,
        "image": "/img/colorful-chain-link-fidget-toy.jpg",
        "category": "Chains",
        "description": "Interlocking chain links with smooth motion",
        "quantity": 80
    },
    {
        "name": "Pop Bubble Keychain",
        "price": 9.99,
        "image": "/img/pop-bubble-fidget-keychain.jpg",
        "category": "Keychains",
        "description": "Portable pop bubble sensory keychain",
        "quantity": 150
    },
    {
        "name": "Roller Chain",
        "price": 21.99,
        "image": "/img/metal-roller-chain-fidget-toy.jpg",
        "category": "Chains",
        "description": "Silent roller chain with premium finish",
        "quantity": 45
    },
]

for item_data in items:
    existing = db.query(models.Item).filter(models.Item.name == item_data["name"]).first()
    if not existing:
        create_item(db, **item_data)
    
codes = [
    {"code": "THOMAS10", "discount_percentage": 10},
    {"code": "ERIC20", "discount_percentage": 20},
    {"code": "FREEMONEY25", "discount_percentage": 25},
]

for code_data in codes:
    existing = db.query(discountCode).filter(discountCode.code == code_data["code"]).first()
    if not existing:
        discount = discountCode(**code_data)
        db.add(discount)

db.commit()
db.refresh(discount)
print("Seeded %d items and %d discount codes successfully!" % (len(items), len(codes)))
db.close()