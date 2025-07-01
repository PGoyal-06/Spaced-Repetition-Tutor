from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id         = Column(Integer, primary_key=True)
    title      = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    chunks     = relationship("Chunk", back_populates="document")
    flashcards = relationship("Flashcard", back_populates="document")

class Chunk(Base):
    __tablename__ = "chunks"
    id          = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    text        = Column(Text, nullable=False)
    embedding   = Column(Vector(1536), nullable=False)
    document    = relationship("Document", back_populates="chunks")

class Flashcard(Base):
    __tablename__ = "flashcards"
    id          = Column(Integer, primary_key=True)
    question    = Column(Text, nullable=False)
    answer      = Column(Text, nullable=False)
    source      = Column(String, nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    document    = relationship("Document", back_populates="flashcards")
    reviews     = relationship("Review", back_populates="flashcard")

class Review(Base):
    __tablename__  = "reviews"
    id             = Column(Integer, primary_key=True)
    user_id        = Column(Integer, nullable=False)
    flashcard_id   = Column(Integer, ForeignKey("flashcards.id"), nullable=False)
    quality        = Column(Integer, nullable=False)
    ease_factor    = Column(Float,   nullable=False)
    interval_days  = Column(Integer, nullable=False)
    next_due       = Column(DateTime, nullable=False)
    timestamp      = Column(DateTime, default=datetime.utcnow)

    flashcard = relationship("Flashcard", back_populates="reviews")
