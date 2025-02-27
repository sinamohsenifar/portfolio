from sqlalchemy import Column, Integer, String 
from sqlalchemy.orm import relationship
from db.database import Base 
from fastapi import HTTPException , status 
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Many-to-many relationship with User (string-based reference)
    users = relationship("User", secondary="user_role_association", back_populates="roles")

async def get_role(role_id: int, db: AsyncSession):
    result = await db.execute(select(Role).filter(Role.id == role_id))
    role = result.scalar_one_or_none()
    if role:
        return role
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

async def get_roles(db: AsyncSession):
    result = await db.execute(select(Role))
    roles = result.scalars().all()
    return roles

async def create_role(role, db: AsyncSession):
    result = await db.execute(select(Role).filter(Role.name == role.name))
    existing_role = result.scalar_one_or_none()
    if existing_role:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role name already exists")

    new_role = Role(name=role.name)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return new_role

async def update_role(role_id: int, role, db: AsyncSession):
    result = await db.execute(select(Role).filter(Role.id == role_id))
    db_role = result.scalar_one_or_none()
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    result = await db.execute(select(Role).filter(Role.name == role.name))
    existing_role = result.scalar_one_or_none()
    if existing_role and existing_role.id != role_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role name already exists")

    db_role.name = role.name
    await db.commit()
    await db.refresh(db_role)
    return db_role

async def delete_role(role_id: int, db: AsyncSession):
    result = await db.execute(select(Role).filter(Role.id == role_id))
    db_role = result.scalar_one_or_none()
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    await db.delete(db_role)
    await db.commit()
    return {"status": "Role deleted"}

async def create_default_roles(db: AsyncSession):
    default_roles = [
        {"name": "admin"},
        {"name": "user"}
    ]

    for role_data in default_roles:
        # Check if the role already exists
        result = await db.execute(select(Role).where(Role.name == role_data["name"]))
        existing_role = result.scalar_one_or_none()
        if not existing_role:
            # Create the role if it doesn't exist
            new_role = Role(**role_data)
            db.add(new_role)
            await db.commit()
            await db.refresh(new_role)
            
            