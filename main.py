from fastapi import FastAPI
from fastapi import Depends
from functools import lru_cache
from typing_extensions import Annotated
from contextlib import asynccontextmanager

from config import *
# from config import Settings
# from config import settings
from helpers.db_sqlalchemy import get_db, Base, engine
# from helpers.db_sqlalchemy import get_db, engine
from helpers.db_sqlmodel import create_db_and_tables
# from .routes.auth import router as auth_router
from routes.auth import router as auth_router


# app = FastAPI()

# # Create the database
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# Lifespan handler (asynchronous context manager)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform startup actions, like connecting to a database
    print("App is starting up")
    Base.metadata.create_all(bind=engine)  # Create the tables in the database
    yield
    # Perform cleanup actions, like closing database connections
    print("App is shutting down")

# # Create the database on startup
# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup logic
#     create_db_and_tables()
#     yield
#     # Shutdown logic (if needed)
#     # For example, closing DB connections
#     print("App is shutting down.")

app = FastAPI(lifespan=lifespan)

# Include the auth router
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@lru_cache
def get_settings():
    return Settings()


@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@app.get("/info")
# async def info():
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name or "",
        "admin_email": settings.admin_email or "",
        "items_per_user": settings.items_per_user or "",
    }



# ASGI - ASGI server
# uvicorn main:app --reload


# run Gunicorn with Uvicorn workers to leverage the strengths of both, allowing you to benefit from Gunicorn's process management and Uvicorn's asynchronous capabilities.

### Python Servers: Uvicorn and Gunicorn

# Type: ASGI server
# Uvicorn is a lightning-fast ASGI server implementation, built on top of httptools and uvloop, designed specifically for handling asynchronous applications.
# - Ideal for running asynchronous web applications like FastAPI
# - Very high performance due to its asynchronous nature.
# - Handles many simultaneous connections effectively.
# Supports HTTP/2 and WebSocket, Easy to use and configure, Lightweight and minimalistic.

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Type: WSGI/ASGI server
# Gunicorn is a Python WSGI HTTP server for UNIX that can serve WSGI applications.
# it can also be used as an ASGI server when combined with a worker class like uvicorn.workers.UvicornWorker.
# - Suitable for production deployments with better concurrency and load handling.
# - Can be used with synchronous applications (WSGI) and asynchronous applications (ASGI) via Uvicorn workers.
# - Handles multiple worker processes, improving the ability to handle requests under load.
# - Better suited for CPU-bound workloads.
# Allows you to configure multiple workers, enabling load balancing.
# Can run in various environments (e.g., multi-core servers).

# gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# -w 4 specifies the number of worker processes to handle requests.
# -k uvicorn.workers.UvicornWorker specifies using Uvicorn's worker class to handle ASGI applications.
