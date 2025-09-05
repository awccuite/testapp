from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict, Any, Annotated

"""
This file defines the Pydantic/Python schemas for API requests/responses.
"""

class ID(BaseModel): # Class wrapper for integer ID's
    id: int = Field(..., description="Primary Key ID")

# Pydantic schemas for API validation and serialization
class UserCreate(BaseModel):
    username: str = Field(..., max_length=26)
    email: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    profile_picture: Optional[str] = None

class UserRead(BaseModel):
    id: int = Field(..., description="Primary Key ID")
    username: str = Field(..., max_length=26)
    email: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    last_login: Optional[datetime] = None
    is_active: bool = True
    created_at: datetime
    profile_picture: Optional[str] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """Class for updating user data (all fields are optional)"""
    id: int = Field(..., description="Primary Key ID") # ID of user to update
    username: Optional[str] = Field(None, min_length=3, max_length=26)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    profile_picture: Optional[str] = Field(None, min_length=3, max_length=255)

    # Pydantic model configurations for read from DB
    class Config:
        from_attributes = True

class UserDelete(BaseModel):
    id: int = Field(..., description="Primary Key ID")
    message: str = Field(..., max_length=255)

# Post schema's
class PostCreate(BaseModel):
    """
    Schema for creating a new post. Requires content, title and user_id.
    """
    user_id: int = Field(..., description="ID of the user creating the post")
    title: str = Field(..., max_length=100)
    content: str = Field(..., max_length=500)

    class Config:
        from_attributes = True

class PostRead(BaseModel):
    id: int = Field(..., description="Primary Key ID")
    user_id: int = Field(..., description="ID of the user who created the post")
    content: str = Field(..., max_length=500)
    title: str = Field(..., max_length=100)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    id: int = Field(..., description="Primary Key ID") # Post to update
    title: Optional[str] = Field(None, max_length=100) # Optional title to update
    content: Optional[str] = Field(None, max_length=500) # Optional content to update

class PostDelete(BaseModel):
    id: int = Field(..., description="Primary Key ID")

class LeadRead(BaseModel):
    id: int = Field(..., description="Primary Key ID")
    lead_name: str = Field(None, max_length=100)
    email: str = Field(None, max_length=100)
    source: str = Field(None)
    interest_level: str = Field(None)
    status: str = Field(None)
    salesperson: str = Field(None)

    # Pydantic model configurations for read from DB
    class Config:
        from_attributes = True
