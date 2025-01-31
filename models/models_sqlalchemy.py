from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# from sqlalchemy import *
from datetime import datetime
from collections import OrderedDict

# from .database import Base
# from db_sqlalchemy import Base
from helpers.db_sqlalchemy import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False) 
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Define a one-to-many relationship with OAuthClient
    clients = relationship('OAuthClient', back_populates='user')  # Reference to OAuthClient

    # Method to convert User object to a dictionary
    # def to_dict(self):
    #     return {
    #         'user_id': self.user_id,
    #         'username': self.username,
    #         'email': self.email,
    #         'created_at': self.created_at.isoformat(),  # Convert to string for JSON serialization
    #         'updated_at': self.updated_at.isoformat()
    #     }
    def to_dict(self):
        return OrderedDict([
            ('user_id', self.user_id),
            ('username', self.username),
            ('email', self.email),
            ('created_at', self.created_at.isoformat()),  # Convert to string for JSON serialization
            ('updated_at', self.updated_at.isoformat())
        ])
    
    # Method to convert User object to a dictionary, preserving order
    def to_json(self):
        return OrderedDict([
            ('user_id', self.user_id),
            ('username', self.username),
            ('email', self.email),
            ('created_at', self.created_at.isoformat()),  # Convert to string for JSON serialization
            ('updated_at', self.updated_at.isoformat())
        ])

class OAuthClient(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    client_id = Column(String(80), unique=True, nullable=False)
    client_secret = Column(String(200), nullable=False)
    redirect_uri = Column(String(200), nullable=False)
    # user_id = Column(Integer, ForeignKey('users.user_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    
    # user = relationship('User')
    user = relationship('User', back_populates='clients')  # Back reference to User
    tokens = relationship('OAuthToken', back_populates='client')  # One-to-many with OAuthToken

class OAuthToken(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    access_token = Column(String(255), unique=True, nullable=False)
    refresh_token = Column(String(255), nullable=True)
    expires_in = Column(DateTime, nullable=False)
    
    # client_id = Column(String(80), ForeignKey('clients.client_id'))
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    # user_id = Column(Integer, ForeignKey('users.user_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    
    # client = relationship('OAuthClient')
    client = relationship('OAuthClient', back_populates='tokens')  # Back reference to OAuthClient
    user = relationship('User')
    # user = relationship('User', back_populates='clients')  # Back reference to User


# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import datetime

# from helpers.db_sqlalchemy import Base

# Pydantic User model
# class UserBase(BaseModel):
    # username: str
    # email: str

# class UserCreate(UserBase):
#     password: bytes  # Use bytes for the binary password

# class User(UserBase):
#     user_id: int
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         # orm_mode = True  # Allow ORM mode for compatibility with SQLAlchemy models
#         from_attributes = True

# class User(BaseModel):
# # class User(Base):
#     user_id: int
#     username: str
#     email: str
#     password: bytes
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         # orm_mode = True  # Allow ORM mode for compatibility with SQLAlchemy models
#         from_attributes = True


# # Pydantic OAuthClient model
# class OAuthClientBase(BaseModel):
#     client_id: str
#     client_secret: str
#     redirect_uri: str
#     user_id: int  # Use an integer for the user ID

# class OAuthClient(OAuthClientBase):
#     id: int
#     user: User  # Relationship back to User

#     class Config:
#         # orm_mode = True
#         from_attributes = True

# # Pydantic OAuthToken model
# class OAuthTokenBase(BaseModel):
#     access_token: str
#     refresh_token: Optional[str] = None  # Refresh token is optional
#     expires_in: datetime
#     client_id: int
#     user_id: int

# class OAuthToken(OAuthTokenBase):
#     id: int
#     client: OAuthClient  # Relationship back to OAuthClient
#     user: User  # Relationship back to User

#     class Config:
#         # orm_mode = True
#         from_attributes = True
