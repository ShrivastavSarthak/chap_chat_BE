from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.db import engine, Base
from app.model.user_modal import User  # Must be imported so Base registers the schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: place cleanup logic here if needed