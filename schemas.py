from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Pydantic User model
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: bytes  # Use bytes for the binary password

class User(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        # This allows SQLAlchemy objects to be automatically converted to Pydantic models
        from_attributes = True


# Pydantic OAuthClient model
class OAuthClientBase(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str
    user_id: int  # Use an integer for the user ID


class OAuthClient(OAuthClientBase):
    id: int
    user: User  # Relationship back to User

    class Config:
        # orm_mode = True
        from_attributes = True

# Pydantic OAuthToken model
class OAuthTokenBase(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None  # Refresh token is optional
    expires_in: datetime
    client_id: int
    user_id: int


class OAuthToken(OAuthTokenBase):
    id: int
    client: OAuthClient  # Relationship back to OAuthClient
    user: User  # Relationship back to User

    class Config:
        # orm_mode = True
        from_attributes = True
