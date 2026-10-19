from fastapi import FastAPI
from app.db.db import CallDB
from app.router.auth_route import auth_route
from app.router.otp_route import otp_route
from app.service.startup_service import lifespan
app = FastAPI(
    title="Chap chat BE",
    version= "1.0.0",
    lifespan=lifespan
)

CallDB()
app.include_router(auth_route)
app.include_router(otp_route)

@app.get("/")
async def root():
    print("-----------Port is running on 8000-------------------")
    return{
        "message":"Backend is running"
    }