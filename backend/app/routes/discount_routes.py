from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database.models import get_db, discountCode
from ..utils import authenticate_and_get_user_details

router = APIRouter(prefix="/discount", tags=["Discounts"])

class DiscountCodeCreate(BaseModel):
    code: str
    discount_percentage: int

# Get all discount codes
@router.get("/")
def get_all_discounts(
    request: Request,
    db: Session = Depends(get_db)
):
    authenticate_and_get_user_details(request)
    discounts = db.query(discountCode).all()
    return discounts

# Get single discount code by code string
@router.get("/{code}")
def get_discount_code(
    code: str,
    request: Request,
    db: Session = Depends(get_db)
):
    authenticate_and_get_user_details(request)
    
    discount = db.query(discountCode).filter(
        discountCode.code == code.upper()
    ).first()
    
    if not discount:
        raise HTTPException(status_code=404, detail="Invalid discount code")
    
    return {
        "code": discount.code,
        "discount_percentage": discount.discount_percentage,
    }

# Create new discount code
@router.post("/")
def create_discount_code(
    discount_data: DiscountCodeCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    authenticate_and_get_user_details(request)
    
    existing = db.query(discountCode).filter(
        discountCode.code == discount_data.code.upper()
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Discount code already exists")
    
    discount = discountCode(
        code=discount_data.code.upper(),
        discount_percentage=discount_data.discount_percentage
    )
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount

# Delete discount code by ID
@router.delete("/{discount_id}")
def delete_discount_code(
    discount_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    authenticate_and_get_user_details(request)
    
    discount = db.query(discountCode).filter(discountCode.id == discount_id).first()
    if not discount:
        raise HTTPException(status_code=404, detail="Discount code not found")
    
    db.delete(discount)
    db.commit()
    return {"message": "Discount code deleted successfully"}