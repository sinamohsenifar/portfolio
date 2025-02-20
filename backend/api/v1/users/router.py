from typing import Optional
from fastapi import APIRouter, Depends , status , HTTPException , Cookie , Form
from db.models.user.crud import create_user, get_user, get_users, update_email , update_user , delete_user
from db.models.user.models import User
from .schemas import UserEmailSchema, UserSchema, UserVerifySchema
from db.database import get_db
from sqlalchemy.orm.session import Session
from fastapi.responses import Response , PlainTextResponse , HTMLResponse , FileResponse , JSONResponse
import csv
from io import StringIO

users_router = APIRouter()

@users_router.get("/{user_id}")
def gets_user(user_id: int,user_cookie : Optional[str] = Cookie(None), db: Session = Depends(get_db), status_code = status.HTTP_200_OK):
    print(user_cookie)
    user = get_user(user_id,db)
    
    # Serialize the User object to a dictionary
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        # Add other fields as needed
    }
    
    # Create a JSONResponse with the serialized user data
    response = JSONResponse(content=user_data)
    # Set a cookie with the user_id
    response.set_cookie(key="user_cookie", value=str(user_id))
    return response

@users_router.post("/all")
def gets_users(db: Session = Depends(get_db), status_code = status.HTTP_200_OK):
    return get_users(db)

@users_router.post("/all/csv")
def gets_users(db: Session = Depends(get_db)):
    users_list = get_users(db)
    if not users_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    csv_buffer = StringIO()
    # Define the CSV column headers (assuming User model has `id`, `username`, and `email`)
    fieldnames = ["id", "username", "email"]
    # Create a CSV writer
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    
    # Write the headers
    csv_writer.writeheader()
    # Write each user as a row in the CSV
    for user in users_list:
        csv_writer.writerow({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })
    # Get the CSV content from the buffer
    csv_content = csv_buffer.getvalue()
    
    # Close the buffer
    csv_buffer.close()
    
    # Return the CSV content as a response with the appropriate media type
    return Response(content=csv_content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=users.csv"})

@users_router.post("/create")
def creates_user(user: UserSchema,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return create_user(user,db)

@users_router.put("/{user_id}/update/user")
def updates_user(user_id: int,user: UserSchema,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return update_user(user_id,user,db)

@users_router.put("/{user_id}/update/email")
def updates_user_email(user_id: int,user: UserEmailSchema,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return update_email(user_id,user,db)



@users_router.delete("/{user_id}")
def deletes_user(user_id: int,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return delete_user(user_id,db)

@users_router.post("/verify")
def verify_password(user: UserVerifySchema,db: Session = Depends(get_db), status_code=status.HTTP_202_ACCEPTED):
    user_found = db.query(User).filter(User.username == user.username).first()
    if user_found:        
        is_valid = user_found.verify_password(user.password)
        if is_valid:
            return {"detail": "correct password"}
        else: 
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="wrong password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")