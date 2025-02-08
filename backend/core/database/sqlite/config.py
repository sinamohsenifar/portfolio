from pydantic import BaseModel

class Sqlite(BaseModel):
    uri: str
    user: str
    password: str
    autocommit: bool
    autoflush: bool