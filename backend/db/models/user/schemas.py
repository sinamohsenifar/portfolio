from pydantic import BaseModel

class User_Schema(BaseModel):
    id: int
    username: str
    email: str
    password: str
    
    class Config:
        orm_mode = True