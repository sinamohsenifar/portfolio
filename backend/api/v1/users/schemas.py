from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    
    class Config:
        orm_mode = True

class UserEmailSchema(BaseModel):
    email: str    
    class Config:
        orm_mode = True



class UserVerifySchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True