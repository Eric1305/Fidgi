from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from ..database.models import get_db, discountCode
from ..utils import authenticate_and_get_user_details

router = APIRouter(prefix="/discount", tags=["Discounts"])

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