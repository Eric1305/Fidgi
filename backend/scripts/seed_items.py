import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

sys.path.append(str(Path(__file__).parent.parent))

from app.database import models
from app.database.models import SessionLocal, discountCode, User, Order, OrderItem
from app.database.db import create_item, create_user

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

real_users = [
    {"clerk_user_id": "user_35a8kjDGrcHJXYuBeQ3LYmmZEzn", "name": "Zane Lakhani", "email": "zanelakhani123@gmail.com"},
    {"clerk_user_id": "user_35R7k2p0k30xaZNAaD9lOz6buuu", "name": "Thomas Bracco", "email": "thomasabr010305@gmail.com"},
    {"clerk_user_id": "user_35PXEJSeeR4IzaPCblNECgJcktD", "name": "Abraham Steve Colin", "email": "astevetheprogramminglover@gmail.com"},
]

created_users = []
for user_data in real_users:
    existing = db.query(User).filter(User.clerk_user_id == user_data["clerk_user_id"]).first()
    if not existing:
        user = create_user(db, **user_data)
        created_users.append(user)
    else:
        created_users.append(existing)

all_items = db.query(models.Item).all()

orders_data = [
    {
        "user": created_users[0],
        "items": [
            {"item": all_items[0], "quantity": 2},
            {"item": all_items[4], "quantity": 1},
        ],
        "discount_code": "THOMAS10",
        "status": "completed",
        "days_ago": 2
    },
    {
        "user": created_users[1],
        "items": [
            {"item": all_items[6], "quantity": 5},
        ],
        "discount_code": None,
        "status": "completed",
        "days_ago": 5
    },
    {
        "user": created_users[2],
        "items": [
            {"item": all_items[3], "quantity": 1},
            {"item": all_items[2], "quantity": 2},
            {"item": all_items[7], "quantity": 1},
        ],
        "discount_code": "FREEMONEY25",
        "status": "completed",
        "days_ago": 7
    },
    {
        "user": created_users[0],
        "items": [
            {"item": all_items[1], "quantity": 3},
        ],
        "discount_code": None,
        "status": "pending",
        "days_ago": 0
    },
    {
        "user": created_users[1],
        "items": [
            {"item": all_items[5], "quantity": 4},
            {"item": all_items[6], "quantity": 3},
        ],
        "discount_code": "ERIC20",
        "status": "completed",
        "days_ago": 10
    },
    {
        "user": created_users[2],
        "items": [
            {"item": all_items[0], "quantity": 1},
        ],
        "discount_code": None,
        "status": "cancelled",
        "days_ago": 3
    },
    {
        "user": created_users[0],
        "items": [
            {"item": all_items[4], "quantity": 2},
            {"item": all_items[7], "quantity": 2},
            {"item": all_items[2], "quantity": 1},
        ],
        "discount_code": None,
        "status": "completed",
        "days_ago": 15
    },
    {
        "user": created_users[1],
        "items": [
            {"item": all_items[3], "quantity": 2},
            {"item": all_items[5], "quantity": 2},
        ],
        "discount_code": "THOMAS10",
        "status": "pending",
        "days_ago": 1
    },
    {
        "user": created_users[2],
        "items": [
            {"item": all_items[6], "quantity": 10},
        ],
        "discount_code": "FREEMONEY25",
        "status": "completed",
        "days_ago": 20
    },
    {
        "user": created_users[0],
        "items": [
            {"item": all_items[1], "quantity": 1},
            {"item": all_items[0], "quantity": 1},
        ],
        "discount_code": None,
        "status": "completed",
        "days_ago": 12
    },
]

orders_created = 0
for order_data in orders_data:
    subtotal = sum(item["item"].price * item["quantity"] for item in order_data["items"])
    
    discount_amount = 0.0
    if order_data["discount_code"]:
        discount_obj = db.query(discountCode).filter(
            discountCode.code == order_data["discount_code"]
        ).first()
        if discount_obj:
            discount_amount = subtotal * (discount_obj.discount_percentage / 100)
    
    after_discount = subtotal - discount_amount
    tax = after_discount * 0.0825  # 8.25% tax
    total = after_discount + tax
    
    order_date = datetime.now() - timedelta(days=order_data["days_ago"])
    
    order = Order(
        user_id=order_data["user"].id,
        subtotal=round(subtotal, 2),
        discount=round(discount_amount, 2),
        tax=round(tax, 2),
        total=round(total, 2),
        discount_code=order_data["discount_code"],
        stripe_payment_id=f"pi_{random.randint(100000000000000, 999999999999999)}",
        status=order_data["status"],
        created_at=order_date
    )
    db.add(order)
    db.flush()
    
    for item_info in order_data["items"]:
        order_item = OrderItem(
            order_id=order.id,
            item_id=item_info["item"].id,
            name=item_info["item"].name,
            price=item_info["item"].price,
            quantity=item_info["quantity"]
        )
        db.add(order_item)
    
    orders_created += 1

db.commit()
print(f" Seeded {len(items)} items, {len(codes)} discount codes, {len(real_users)} users, and {orders_created} orders successfully!")
db.close()