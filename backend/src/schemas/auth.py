from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    username: str
    password: str
    
    class Config:
        orm_mode = True
   
     
class UserLogoutSchema(BaseModel):
    username: str
    
    class Config:
        orm_mode = True
        
class UserCheckSchema(BaseModel):
    username: str
    password: str
    email: str
    
    class Config:
        orm_mode = True