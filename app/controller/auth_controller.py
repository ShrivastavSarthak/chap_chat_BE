from app.schema.user_schema import UserLogin
from app.model.user_modal import User, Guest
from sqlalchemy.orm import Session
from app.service.JWT_service import create_access_token
from fastapi import HTTPException, status
from datetime import timedelta
import uuid
async def authUser(userData:UserLogin, db:Session):
    existing_user = db.query(User).filter(User.email == userData.email).first()
    if existing_user:
        return {
            "message":"user fetched successfully",
            "status_code":200,
            "data":existing_user
        }
    new_user =User(email = userData.email, name = userData.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
            "message":"user created successfully",
            "status_code":200,
            "data":new_user
        }

async def guestLogin(db: Session):
    try:
        raw_guest_id = uuid.uuid4()
        guest_id_str = str(raw_guest_id)
        guest_name = "Guest"

        guest_user = Guest(id=raw_guest_id)
        db.add(guest_user)
        db.commit()
        db.refresh(guest_user)

        access_token = create_access_token(
            data={
                "sub": guest_id_str,
                "name": guest_name,
                "role": guest_user.role,
            },
            expire_time=timedelta(minutes=5),
        )

        return {
            "message": "Guest login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 300,
            "user": {
                "id": guest_id_str,
                "name": guest_name,
                "role": guest_user.role,
            },
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create guest session: {str(e)}",
        )