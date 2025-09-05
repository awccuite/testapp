"""
This file defines the database models that Alembic will use for migrations.
These define our database schema.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()
# Class definitions live here

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(26), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    profile_picture = Column(String(255), nullable=True)  # New field to test migration checks

    # Can also add a relationship to the Post model
    # posts = relationship("Post", back_populates="user"), to update user posts from the user side

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key to users table
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', user_id={self.user_id})>"

class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True)  # Supplied by csv
    lead_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    source = Column(String(100), nullable=True) 
    interest_level = Column(String(100), nullable=True)
    status = Column(String(100), nullable=True)
    salesperson = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Lead(id={self.id}, lead_name='{self.lead_name}', source='{self.source}')>"

# Export all models for Alembic
__all__ = ['Base', 'User', 'Post', 'Lead']
