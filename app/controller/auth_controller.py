from app.schema.user_schema import UserLogin
from app.model.user_modal import User
from sqlalchemy.orm import Session
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