from fastapi import APIRouter, Depends, status, HTTPException, Cookie, Response
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from models.user import create_user, get_user, get_users, update_email, update_user, delete_user, get_user_by_username
from schemas.users import UserCreate, UserResponse, UserUpdate, UserEmailUpdate, UserVerifyPassword
from typing import Optional
import csv
from io import StringIO

users_router = APIRouter(prefix="/users", tags=["users"])

# Get a user by ID
@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    user_cookie: Optional[str] = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    print(f"User cookie: {user_cookie}")  # For debugging
    user = await get_user(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Convert roles to a list of role names
    roles = [role.name for role in user.roles]
    
    # Create the response
    response_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "roles": roles
    }
    
    # Set a cookie with the user_id
    response = Response(content=response_data, media_type="application/json")
    response.set_cookie(key="user_cookie", value=str(user_id))
    return response

# Get all users
@users_router.get("/", response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users

# Get all users as CSV
@users_router.get("/csv")
async def get_all_users_csv(db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

    # Create a CSV buffer
    csv_buffer = StringIO()
    fieldnames = ["id", "username", "email", "roles"]
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    
    # Write headers and rows
    csv_writer.writeheader()
    for user in users:
        roles = ", ".join([role.name for role in user.roles])
        csv_writer.writerow({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "roles": roles
        })
    
    # Return the CSV content
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()
    return Response(content=csv_content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=users.csv"})

# Create a new user
@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user(user, db)
    return new_user

# Update a user
@users_router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_user = await update_user(user_id, user, db)
    return updated_user

# Update a user's email
@users_router.patch("/{user_id}/email", response_model=UserResponse)
async def update_user_email(
    user_id: int,
    email_update: UserEmailUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_user = await update_email(user_id, email_update, db)
    return updated_user

# Delete a user
@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db)):
    await delete_user(user_id, db)
    return None

# Verify a user's password
@users_router.post("/verify", response_model=dict)
async def verify_user_password(
    credentials: UserVerifyPassword,
    db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_username(credentials.username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not user.verify_password(credentials.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    return {"detail": "Password is correct"}