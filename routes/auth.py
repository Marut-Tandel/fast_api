# from fastapi import FastAPI, APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy.orm import Session
# # from ..helpers.db_sqlalchemy import get_db, Base, engine
# # from ..models.models_sqlalchemy import User
# from helpers.db_sqlalchemy import get_db, Base, engine
# # from models.models_sqlalchemy import User, UserCreate
# # from models.models_sqlalchemy import UserCreate
# # from models.models_sqlalchemy import User
# from models.models_sqlalchemy import User as SQLAlchemyUser  # Your SQLAlchemy model
# from schemas import User, UserCreate  # Your Pydantic response model

# from typing import List, Optional
# import bcrypt

# router = APIRouter()
# # auth = APIRouter()

# # http://127.0.0.1:8000/auth/check
# @router.get("/check")
# async def auth_check():
#     return {
#         "status": 200,
#         "success": True
#     }

# # # Create the database
# # # @auth.on_event("startup")
# # @router.on_event("startup")
# # async def startup():
# #     async with engine.begin() as conn:
# #         await conn.run_sync(Base.metadata.create_all)

# #############################
# # SQLAlchemy

# # # Create a new user
# # @router.post("/sqlalchemy/users/")
# # async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
# #     user = User(name=name, email=email)
# #     db.add(user)
# #     await db.commit()
# #     return user

# # # Get all users
# # @router.get("/sqlalchemy/users/")
# # async def get_users(db: AsyncSession = Depends(get_db)):
# #     result = await db.execute(select(User))
# #     users = result.scalars().all()
# #     return users

# # Endpoint to create a user
# # @router.post("/sqlalchemy/users/", response_model=User)
# # async def create_user(user: UserCreate, db: Session = Depends(get_db)):
# #     db_user = User(username=user.username, email=user.email, password=user.password)
# #     db.add(db_user)
# #     db.commit()
# #     db.refresh(db_user)
# #     return db_user

# # @router.post("/sqlalchemy/users/", response_model=User)
# # async def create_user(user: UserCreate, db: Session = Depends(get_db)):
# #     # db_user = User(username=user.username, email=user.email, password=user.password)
# #     db_user = User(username=user.username, email=user.email, password=user.password)
# #     db.add(db_user)
# #     db.commit()
# #     db.refresh(db_user)
# #     return db_user

# # Create a new user
# @router.post("/sqlalchemy/users/", response_model=User)
# async def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.username == user.username).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
    
#     # new_user = SQLAlchemyUser(
#     #     username=user.username,
#     #     email=user.email,
#     #     password=user.password,  # Ensure password is hashed in a real application
#     # )
#     hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
#     new_user = SQLAlchemyUser(
#         username=user.username,
#         email=user.email,
#         password=hashed_password,  # Store hashed password
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# # Get all users
# # @router.get("/sqlalchemy/users", response_model=List[User])
# # @router.get("/sqlalchemy/users", response_model=List[Dict])
# @router.get("/sqlalchemy/users")
# async def get_all_user(db: Session = Depends(get_db)):
#     # users = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.user_id == user_id).all()
#     users = db.query(SQLAlchemyUser).all()
#     if not users:
#         raise HTTPException(status_code=404, detail="User not found")
#     # return users
#     # return [User.from_orm(user) for user in users]
#     # return [User.from_orm(user) for user in users]
#     # return [OrderedDict([
#     #     ("user_id", user.user_id),
#     #     ("username", user.username),
#     #     ("email", user.email),
#     #     ("created_at", user.created_at.isoformat()),
#     #     ("updated_at", user.updated_at.isoformat()),
#     # ]) for user in users]
#     return [user.to_dict() for user in users]

# # Get user by user_id
# # @router.get("/sqlalchemy/users/{user_id}", response_model=User)
# @router.get("/sqlalchemy/users/{user_id}")
# async def get_user(user_id: int, db: Session = Depends(get_db)):
#     # user = db.query(User).filter(User.user_id == user_id).first()
#     # user = db.query(User).filter(User.user_id == user_id)
#     user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.user_id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user.to_json()


# # Update a user
# @router.put("/sqlalchemy/users/{user_id}", response_model=User)
# async def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
#     user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.user_id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Update user attributes
#     user.username = user_data.username
#     user.email = user_data.email
#     # user.password = user_data.password  # Ensure to hash the password
#     # user.password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())

#     db.commit()
#     db.refresh(user)
#     return user.to_dict()


# # Delete a user
# @router.delete("/sqlalchemy/users/{user_id}")
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.user_id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     db.delete(user)
#     db.commit()
#     return {"detail": "User deleted successfully"}


from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
# from ..helpers.db_sqlmodel import get_session
from helpers.db_sqlmodel import get_session
# from models.models_sqlmodel import User
from schemas import User  # Pydantic model
# from sqlalchemy.future import select

from models.models_sqlmodel import User as SQLModelUser  # Your SQLModel user model
from schemas import User  # Your Pydantic user schema
# from helpers.db_sqlalchemy import get_db  # Your database session dependency

from helpers.redis_cache_user import UserCacheService, get_user_by_id

router = APIRouter()

##########################
# SQLModel

# # Create a new user
# @router.post("/sqlmodel/users/")
# def create_user(user: User, session: Session = Depends(get_session)):
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user

# # Get all users
# @router.get("/sqlmodel/users/")
# def get_users(session: Session = Depends(get_session)):
#     users = session.exec(select(User)).all()
#     return users

# Create a new user
@router.post("/sqlmodel/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    db_user = SQLModelUser.from_orm(user)  # Convert Pydantic model to SQLModel
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user  # Return the created user

# Get all users
# @router.get("/sqlmodel/users/", response_model=list[User])
@router.get("/sqlmodel/users/")
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(SQLModelUser)).all()  # Get all users
    # return users  # Return the list of users

     # If no users found, raise an HTTPException
    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    # Convert each SQLModel user instance to Pydantic User model before returning
    return [user.to_json() for user in users]

# @router.get("/sqlmodel/users")
# async def get_users(session: Session = Depends(get_session)):
#     users = db.query(User).all()
#     return [user.to_dict() for user in users]  # Ensure you have a method to serialize each user

# @router.get("/sqlmodel/users/{user_id}")
# async def get_user(user_id: int, session: Session = Depends(get_session)):
#     user = db.query(User).filter(User.user_id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user  # FastAPI handles the serialization for you

async def find_user(user_id, session):
    # users = session.exec(select(SQLModelUser)).all()
    user = session.exec(select(SQLModelUser)).filter(SQLModelUser.user_id == user_id).first()
    if user is None:
        # []
        return None
    # return [user.to_json() for user in users]
    return user.to_json()

@router.get("/redis/users/{user_id}")
async def get_users(user_id: int, session: Session = Depends(get_session)):
    # users = session.exec(select(SQLModelUser)).all()
    # if not users:
    #     raise HTTPException(status_code=404, detail="No users found")
    # return [user.to_json() for user in users]
    user = await get_user_by_id(session, user_id)
    if not user:
        return {"error": "User not found"}
        # user = await find_user(user_id=user_id, session=session)
        # if user is None:
        #     # raise HTTPException(status_code=404, detail="No users found")
        #     return {"error": "User not found"}
        
        # UserCacheService.set_user_to_cache(user=user)
        # return user.to_dict()
        
    return user
