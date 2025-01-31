import json
from sqlmodel import Session, select
from datetime import datetime
from typing import Optional

from helpers.redis_cache import redis_client, CACHE_EXPIRATION
from models.models_sqlmodel import User

class UserCacheService:
    @staticmethod
    async def get_user_from_cache(user_id: int) -> Optional[User]:
        """Fetch user from Redis cache."""
        user_data = redis_client.get(f"user:{user_id}")
        if user_data:
            return User(**json.loads(user_data))
        return None

    @staticmethod
    async def set_user_to_cache(user: User) -> None:
        """Store user in Redis cache with an expiration time."""
        redis_client.setex(
            f"user:{user.user_id}",
            CACHE_EXPIRATION,
            json.dumps(user.to_dict())
        )

    @staticmethod
    async def delete_user_from_cache(user_id: int) -> None:
        """Remove user from Redis cache."""
        redis_client.delete(f"user:{user_id}")

# In your repository/controller

async def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    # Check if user exists in Redis cache first
    user = await UserCacheService.get_user_from_cache(user_id)
    if user:
        return user

    # user = session.exec(select(SQLModelUser)).filter(SQLModelUser.user_id == user_id).first()
    # If not, fetch from the database
    # statement = select(User).where(User.user_id == user_id)
    statement = select(User).filter(User.user_id == user_id)
    user = session.exec(statement).first()

    if user:
        # Store user in Redis cache
        await UserCacheService.set_user_to_cache(user)

    return user

async def update_user(session: Session, user: User) -> None:
    """Update user and refresh cache."""
    session.add(user)
    session.commit()
    session.refresh(user)

    # Update cache with new data
    await UserCacheService.set_user_to_cache(user)

async def delete_user(session: Session, user_id: int) -> None:
    """Delete user from DB and cache."""
    statement = select(User).where(User.user_id == user_id)
    user = session.exec(statement).first()
    
    if user:
        session.delete(user)
        session.commit()

        # Remove user from Redis cache
        await UserCacheService.delete_user_from_cache(user_id)
