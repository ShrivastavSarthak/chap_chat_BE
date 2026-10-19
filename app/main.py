from fastapi import FastAPI
from app.db.db import CallDB
from app.router.auth_route import auth_route
from app.router.otp_route import otp_route
from app.service.startup_service import lifespan
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Chap chat BE",
    version= "1.0.0",
    lifespan=lifespan
)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows listed origins (or ["*"] for public testing)
    allow_credentials=True,           # Allows cookies and authorization headers
    allow_methods=["*"],              # Allows all HTTP methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],              # Allows all headers (e.g., Content-Type, Authorization)
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