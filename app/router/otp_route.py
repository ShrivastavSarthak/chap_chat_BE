from fastapi import APIRouter, Depends
from  app.schema.otp_schema import OTPBase, OTPMatch
from app.controller.otp_controller import createOTP
from app.controller.otp_controller import verifyOTP
from sqlalchemy.orm import Session
from app.db.db import CallDB

otp_route = APIRouter(
    prefix="/otp",
    tags=['auth']
)

@otp_route.post("/create")
async def create_otp(data: OTPBase, db:Session = Depends(CallDB)):
    return await createOTP(data, db=db)

@otp_route.post('/verify')
async def verify_otp(data:OTPMatch, db:Session = Depends(CallDB)):
    return await verifyOTP(data,db)