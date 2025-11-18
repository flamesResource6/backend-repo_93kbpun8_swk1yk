"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (you can keep these for reference)

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Gift search schema for peek-like experience
class Gift(BaseModel):
    """
    Gifts collection schema
    Collection name: "gift"
    """
    gift: str = Field(..., description="Gift type or name (e.g., flowers, toy, gadget)")
    background: str = Field(..., description="Background style identifier")
    pattern: str = Field(..., description="Pattern identifier")
    number: Optional[str] = Field(None, description="Number or code associated with item")

    title: Optional[str] = Field(None, description="Display title")
    description: Optional[str] = Field(None, description="Short description")
    image_url: Optional[str] = Field(None, description="Preview image URL")
    price: Optional[float] = Field(None, ge=0, description="Price if applicable")
    tags: Optional[List[str]] = Field(default=None, description="Search tags")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
