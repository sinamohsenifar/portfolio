from pydantic import BaseModel


class Mysql(BaseModel):
    uri: str
    user: str
    password: str