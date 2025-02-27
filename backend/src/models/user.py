from sqlalchemy import Column, Integer, String , ForeignKey, Table
from sqlalchemy.orm import relationship
from db.database import Base
import bcrypt
from fastapi import status ,HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserEmailUpdate
from sqlalchemy.orm import joinedload

# Association table for many-to-many relationship between users and roles
user_role_association = Table(
    "user_role_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Many-to-many relationship with Role (string-based reference)
    roles = relationship("Role", secondary="user_role_association", back_populates="users")

    # Relationships with other tables
    articles = relationship("Article", back_populates="author")
    comments = relationship("Comment", back_populates="user")

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), self.hashed_password.encode("utf-8"))


async def get_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

async def get_users(db: AsyncSession):
    result = await db.execute(select(User).options(joinedload(User.roles)))
    users = result.scalars().unique().all()
    return users

async def create_user(user, db: AsyncSession):
    # Check for duplicate username or email
    result = await db.execute(select(User).filter((User.username == user.username) | (User.email == user.email)))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")

    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=User.hash_password(user.password),
    )
    result = await db.execute(select(Role).filter(Role.name == "user"))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    user.roles.append(role)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(user_id: int, user, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check for duplicate username or email
    result = await db.execute(select(User).filter((User.username == user.username) | (User.email == user.email)))
    existing_user = result.scalar_one_or_none()
    if existing_user and existing_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")

    # Update user fields
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await db.delete(db_user)
    await db.commit()
    return {"status": "User deleted"}


async def update_email(user_id: int, user: UserEmailUpdate, db: AsyncSession):
    user_result = db.execute(select(User).filter(User.id == user_id))
    db_user = user_result.scalar_one_or_none()
    email_result = db.execute(select(User).filter(User.email == user.email,User.id != user_id))
    db_email_user = email_result.scalar_one_or_none()  
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    elif db_email_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate Email")
    db_user.email = user.email
    await db.commit()
    await db.refresh(db_user)
    return db_user

def get_user_by_username(username,db: AsyncSession):
    user_result = db.execute(select(User).filter(User.username == username))
    db_user = user_result.scalar_one_or_none()
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    

async def create_admin_users(db: AsyncSession):
    admins = [
        {"username": "admin","email":"sinamohsenifar@gmail.com","hashed_password": "123qweasd"},
        {"username": "mary","email":"sinoohe77@gmail.com","hashed_password": "123qweasd"},
    ]

    for admin_data in admins:
        # Check if the role already exists
        result = await db.execute(select(User).where(User.username == admin_data["username"]))
        existing_role = result.scalar_one_or_none()
        if not existing_role:
            # Create the admin user if it doesn't exist
            new_admin = User(**admin_data)
            new_admin.hashed_password = User.hash_password(new_admin.hashed_password)
            
            # asign user role
            role = await get_role(2,db)
            new_admin.roles.append(role)
            
            # asign admin role
            role = await get_role(1,db)
            new_admin.roles.append(role)
            
            db.add(new_admin)
            await db.commit()
            await db.refresh(new_admin)