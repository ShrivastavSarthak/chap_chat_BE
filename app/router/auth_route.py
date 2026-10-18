from fastapi import APIRouter, Depends
from  app.schema.user_schema import UserLogin
from app.controller.auth_controller import authUser
from sqlalchemy.orm import Session
from app.db.db import CallDB
auth_route = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@auth_route.post("/user")
async def auth(data: UserLogin, db:Session = Depends(CallDB)):
    return await authUser(data, db=db)