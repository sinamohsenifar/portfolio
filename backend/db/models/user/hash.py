from enum import auto
from warnings import deprecated
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes="bcrypt", deprecated = "auto")


class Hash():
    def bcrypt(password: str):
        return pwd_ctx.hash(password)
    
    def verify_pass(plain_password , hashed_password):
        return pwd_ctx.verify(plain_password, hashed_password) 