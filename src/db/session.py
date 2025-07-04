import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Ensure DATABASE_URL is set
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Declarative Base import for models
# Models should define Base = declarative_base() or import this Base
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# Utility: initialize database schema

def init_db():
    # Import all modules that define models so they get registered
    import db.models  # ensure this module imports Base subclasses
    Base.metadata.create_all(bind=engine)