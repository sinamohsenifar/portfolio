from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base
import bcrypt
from fastapi import HTTPException , status

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Use a string-based reference for the relationship to avoid circular imports
    users = relationship("User", back_populates="user")



# Function to create the table
def create_role_table(engine):
    Role.metadata.create_all(bind=engine)



def get_role(role_id,db):
    role = db.query(Role).filter(Role.id==role_id).first()
    if role:
        return role
    else:
        return {"status": "role not found"}


def get_roles(db):
    roles = db.query(Role).all()
    return roles

def create_role(role,db):
    check_name = db.query(Role).filter(Role.name == role.name).first()
    if check_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="duplicate role name")
    else:
        new_role = Role(name=role.name)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role


def update_role(role_id,role,db):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    check_name = db.query(Role).filter(Role.name == role.name).first()
    if check_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="duplicate name")
    else:
        # Update the comment
        for key, value in role.model_dump(exclude_unset=True).items():
            setattr(db_role, key, value)
        db.commit()
        db.refresh(db_role)
        return db_role


def delete_role(role_id,db):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role:
        db.delete(db_role)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Role not found")