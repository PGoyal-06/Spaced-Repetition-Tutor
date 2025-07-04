import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

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

# Declarative Base for models
Base = declarative_base()

def init_db():
    # 1) Ensure pgvector extension is present
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

    # 2) Import all models so they register with Base
    import db.models  # noqa: F401

    # 3) Create all tables
    Base.metadata.create_all(bind=engine)
