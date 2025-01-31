# # from sqlmodel import SQLModel, Field
# # from typing import Optional

# # class User(SQLModel, table=True):
# #     id: Optional[int] = Field(default=None, primary_key=True)
# #     name: str
# #     email: str

# from sqlmodel import SQLModel, Field, Relationship
# from typing import Optional, List
# from datetime import datetime

# class User(SQLModel, table=True):
#     __tablename__ = 'users'

#     user_id: Optional[int] = Field(default=None, primary_key=True)
#     username: str = Field(sa_column_kwargs={"unique": True, "nullable": False}, max_length=50)
#     email: str = Field(sa_column_kwargs={"unique": True, "nullable": False}, max_length=100)
#     password: bytes = Field(nullable=False)  # LargeBinary equivalent in SQLModel
#     # created_at: datetime = Field(default_factory=datetime.utcnow)
#     # updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
#     created_at: datetime = Field(default_factory=datetime.now)
#     updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

#     # Relationships
#     clients: List["OAuthClient"] = Relationship(back_populates="user")
#     # tokens: List["OAuthToken"] = Relationship(back_populates="user")

#     def to_dict(self):
#         return {
#             'user_id': self.user_id,
#             'username': self.username,
#             'email': self.email,
#             'created_at': self.created_at.isoformat(),
#             'updated_at': self.updated_at.isoformat()
#         }

#     def to_json(self):
#         from collections import OrderedDict
#         return OrderedDict([
#             ('user_id', self.user_id),
#             ('username', self.username),
#             ('email', self.email),
#             ('created_at', self.created_at.isoformat()),
#             ('updated_at', self.updated_at.isoformat())
#         ])


# class OAuthClient(SQLModel, table=True):
#     __tablename__ = 'clients'

#     id: Optional[int] = Field(default=None, primary_key=True)
#     client_id: str = Field(nullable=False, unique=True, max_length=80)
#     client_secret: str = Field(nullable=False, max_length=200)
#     redirect_uri: str = Field(nullable=False, max_length=200)
#     user_id: Optional[int] = Field(foreign_key="users.user_id", nullable=False)

#     # Relationship to User
#     user: Optional[User] = Relationship(back_populates="clients")
#     # token: Optional[OAuthToken] = Relationship(back_populates='client')
#     # tokens: List["OAuthToken"] = Relationship(back_populates="user")

# class OAuthToken(SQLModel, table=True):
#     __tablename__ = 'tokens'

#     id: Optional[int] = Field(default=None, primary_key=True)
#     access_token: str = Field(nullable=False, unique=True, max_length=255)
#     refresh_token: Optional[str] = Field(default=None, max_length=255)
#     expires_in: datetime = Field(nullable=False)
#     client_id: Optional[int] = Field(foreign_key="clients.id", nullable=False)
#     user_id: Optional[int] = Field(foreign_key="users.user_id", nullable=False)

#     # Relationships
#     client: Optional[OAuthClient] = Relationship(back_populates="tokens")
#     user: Optional[User] = Relationship(back_populates="tokens")


from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from collections import OrderedDict

class User(SQLModel, table=True):
    __tablename__ = 'users'

    # user_id: int = Field(default=None, primary_key=True, autoincrement=True)
    user_id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, nullable=False)
    email: str = Field(max_length=100, unique=True, nullable=False)
    password: bytes = Field(nullable=False)  # Use bytes for the binary password
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    # Define a one-to-many relationship with OAuthClient
    clients: List["OAuthClient"] = Relationship(back_populates="user")  # Reference to OAuthClient
    # One-to-many relationship with OAuthToken
    tokens: List["OAuthToken"] = Relationship(back_populates="user")  # Relationship to OAuthToken

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def to_json(self):
        return OrderedDict([
            ('user_id', self.user_id),
            ('username', self.username),
            ('email', self.email),
            ('created_at', self.created_at.isoformat()),  # Convert to string for JSON serialization
            ('updated_at', self.updated_at.isoformat())
        ])

class OAuthClient(SQLModel, table=True):
    __tablename__ = "clients"

    id: int = Field(default=None, primary_key=True)
    client_id: str = Field(max_length=80, unique=True, nullable=False)
    client_secret: str = Field(max_length=200, nullable=False)
    redirect_uri: str = Field(max_length=200, nullable=False)
    user_id: int = Field(foreign_key="users.user_id", nullable=False)

    user: User = Relationship(back_populates="clients")  # Back reference to User
    tokens: List["OAuthToken"] = Relationship(back_populates="client")  # Relationship to OAuthToken

class OAuthToken(SQLModel, table=True):
    __tablename__ = "tokens"

    id: int = Field(default=None, primary_key=True)
    access_token: str = Field(max_length=255, unique=True, nullable=False)
    refresh_token: Optional[str] = Field(default=None, max_length=255)
    expires_in: datetime = Field(nullable=False)
    client_id: int = Field(foreign_key="clients.id", nullable=False)
    user_id: int = Field(foreign_key="users.user_id", nullable=False)

    client: OAuthClient = Relationship(back_populates="tokens")  # Back reference to OAuthClient
    user: User = Relationship(back_populates="tokens")  # Back reference to User
