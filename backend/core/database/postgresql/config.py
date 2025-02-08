from pydantic import BaseModel

class Postgres(BaseModel):
    uri: str
    user: str
    password: str

