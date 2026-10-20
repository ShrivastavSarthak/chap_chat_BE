from app.schema.otp_schema import OTPBase, OTPMatch
from app.service.otp_service import generateOTP
from datetime import datetime, timedelta, timezone
from sqlalchemy.dialects.postgresql import insert
from app.model.email_model import EmailOTP
from app.model.user_modal import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.service.JWT_service import create_access_token
from app.service.email_service import email_service 
from app.utils.email_templates.otp_email_template import get_otp_email_template
from app.schema.email_schema import email_schema

async def createOTP(emailData:OTPBase, db: Session):
    try:
        otp = generateOTP()
        expireAt = datetime.now(timezone.utc) + timedelta(minutes=5)
        
        stmt = insert(EmailOTP).values(
            email = emailData.email,
            otp = otp,
            expire_at = expireAt
        )
        
        stmt = stmt.on_conflict_do_update(
            index_elements=[EmailOTP.email],
            set_ = {
                "otp": stmt.excluded.otp,
                "expire_at": stmt.excluded.expire_at
            }
        )
        
        db.execute(stmt)
        db.commit()
        
        email_template= get_otp_email_template(otp)
        mail = email_schema(
            to=emailData.email,
            title="Verification code",
            description=email_template
        )
        email_service(mail)
        
        return{
            "message":"OTP send successfully",
            "status_code":200,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create OTP, {e}"
        )

async def verifyOTP(otp_data: OTPMatch, db: Session):
    try:
        otp_record = db.query(EmailOTP).filter(EmailOTP.email == otp_data.email).first()
        
        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request or OTP expired"
            )

        now = datetime.now(timezone.utc)
        expire_time = (
            otp_record.expire_at
            if otp_record.expire_at.tzinfo
            else otp_record.expire_at.replace(tzinfo=timezone.utc)
        )
        
        if now > expire_time:
            db.delete(otp_record)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired. Please request a new one."
            )
            
        if otp_record.otp != otp_data.otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP"
            )
        
        user = db.query(User).filter(User.email == otp_data.email).first()
        if not user:
            user = User(email=otp_data.email, isVerifiedEmail=True)
            db.add(user)  # Required so SQLAlchemy tracks the new row
        else:
            user.isVerifiedEmail = True
        
        db.delete(otp_record)
        db.commit()
        db.refresh(user)
        
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email
            }
        )
        
        return {
            "message": "OTP verified successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": str(user.id)
        }

    except HTTPException:
        # Re-raise explicit HTTP exceptions directly so FastAPI handles the status code
        raise

    except Exception as e:
        db.rollback()  # Roll back pending session state on unexpected DB failure
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify OTP: {str(e)}"
        )