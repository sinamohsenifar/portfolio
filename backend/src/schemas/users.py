from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List, Optional
from schemas.roles import RoleResponse
    
# Base schema for User
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="The username of the user")
    email: EmailStr = Field(..., description="The email of the user")

    model_config = ConfigDict(from_attributes=True)

# Schema for creating a user
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="The password of the user")

# Schema for updating a user
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="The username of the user")
    email: Optional[EmailStr] = Field(None, description="The email of the user")
    password: Optional[str] = Field(None, min_length=8, description="The password of the user")

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    roles: List[RoleResponse]

    model_config = ConfigDict(from_attributes=True)

# Schema for updating email
class UserEmailUpdate(BaseModel):
    email: EmailStr = Field(..., description="The new email of the user")

# Schema for verifying password
class UserVerifyPassword(BaseModel):
    username: str = Field(..., description="The username of the user")
    password: str = Field(..., description="The password to verify")