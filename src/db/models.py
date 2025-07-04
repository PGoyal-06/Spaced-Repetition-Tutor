from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime
from db.session import Base

class Document(Base):
    __tablename__ = "documents"
    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chunks     = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"
    id          = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    text        = Column(Text, nullable=False)
    embedding   = Column(Vector(1536), nullable=False)

    document    = relationship("Document", back_populates="chunks")

class Flashcard(Base):
    __tablename__ = "flashcards"
    id          = Column(Integer, primary_key=True, index=True)
    question    = Column(Text, nullable=False)
    answer      = Column(Text, nullable=False)
    source      = Column(String, nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)

    document    = relationship("Document", back_populates="flashcards")
    reviews     = relationship("Review", back_populates="flashcard", cascade="all, delete-orphan")

class Review(Base):
    __tablename__  = "reviews"
    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, nullable=False)
    flashcard_id   = Column(Integer, ForeignKey("flashcards.id", ondelete="CASCADE"), nullable=False)
    quality        = Column(Integer, nullable=False)
    ease_factor    = Column(Float,   nullable=False)
    interval_days  = Column(Integer, nullable=False)
    next_due       = Column(DateTime(timezone=True), nullable=False)
    timestamp      = Column(DateTime(timezone=True), server_default=func.now())

    flashcard      = relationship("Flashcard", back_populates="reviews")