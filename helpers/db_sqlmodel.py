from sqlmodel import SQLModel, create_engine, Session

# import config
from config import settings

# DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/dbname"
# DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
DATABASE_URL = settings.sqlalchemy_database_uri

engine = create_engine(DATABASE_URL)

# Dependency to get a session for each request
def get_session():
    with Session(engine) as session:
        yield session

# To create the database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
