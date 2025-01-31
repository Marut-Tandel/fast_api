# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# DATABASE_URL = "postgresql+asyncpg://username:password@localhost:5432/dbname"

# # Creating the async engine
# engine = create_async_engine(DATABASE_URL, echo=True)

# # Creating a session for interaction with the database
# async_session = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )

# Base = declarative_base()

# # Dependency to get a session for each request
# async def get_db():
#     async with async_session() as session:
#         yield session


from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# import config
from config import settings

# Database Setup
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
# SQLALCHEMY_TRACK_MODIFICATIONS = settings.SQLALCHEMY_TRACK_MODIFICATIONS
# SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_uri
# SQLALCHEMY_TRACK_MODIFICATIONS = settings.sqlalchemy_track_modifications

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# # engine = create_engine(SQLALCHEMY_DATABASE_URL, SQLALCHEMY_TRACK_MODIFICATIONS, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create SQLAlchemy engine for PostgreSQL (No 'check_same_thread')
engine = create_engine(settings.sqlalchemy_database_uri)
# engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# Create all tables based on the model definitions
Base.metadata.create_all(engine)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()