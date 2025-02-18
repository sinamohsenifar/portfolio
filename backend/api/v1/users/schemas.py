from pydantic import BaseModel

class User_Schema(BaseModel):
    username: str
    email: str
    password: str