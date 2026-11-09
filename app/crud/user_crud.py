
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserUpdate, UserRoleUpdate
from app.models import User

import bcrypt

def create_user(db: Session, user: UserCreate):

    statement = select(User).where((User.email == user.email) | (User.username == user.username))
    existing_user = db.execute(statement).scalar_one_or_none()

    if existing_user:
        return None # later we will change None to EmailNotExist
    
    password_bytes = user.password.encode("utf-8") # convert string to bytes cuz bcrypt only read bytes
    salt = bcrypt.gensalt() # randamn char since 2 or more user dont have the same hash pass

    hashed_password = bcrypt.hashpw(password_bytes, salt) # combine hash password with salt(random char)
    hashed_password = hashed_password.decode("utf-8") # convert bytes to string cuz our sqlalchemy model is in str
    
    user_db = User(
        username = user.username,
        email = user.email,
        password = hashed_password 
    )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db

def get_user(db: Session, id: int):
    statement = select(User).where(User.id == id)
    user = db.execute(statement).scalar_one_or_none()
    return user 


def get_users(db: Session):

    statement = select(User)
    
    result = db.execute(statement).scalars().all()

    return result


def update_user(db: Session, id: int, user: UserUpdate):

    statement = select(User).where(User.id == id)
    user_db = db.execute(statement).scalar_one_or_none()

    if user_db is None:
        return None
    
    duplicate_statement = select(User).where(((User.email == user.email) | (User.username == user.username)) &(User.id != id))

    existing_user = db.execute(duplicate_statement).scalars().first()

    if existing_user is not None:
        return None
    
    user_db.username = user.username
    user_db.email = user.email

    db.commit()
    db.refresh(user_db)

    return user_db


def delete_user(db: Session, id: int):
    statement = select(User).where(User.id == id)
    deleted_user = db.execute(statement).scalar_one_or_none()

    if deleted_user is None:
        return None
    
    db.delete(deleted_user)
    db.commit()
    
    return deleted_user



def login_user(db: Session, email: str, password: str):

    statement = select(User).where(User.email == email)

    user = db.execute(statement).scalar_one_or_none()

    if user is None:
        return None

    try:
        password_match = bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))
        
    except ValueError:
        return None

    if not password_match:
        return None

    return user

    
def update_user_role(db: Session, user_id: int, user: UserRoleUpdate):

    # find the user
    existing_user = db.get(User, user_id)

    if existing_user is None:
        return None
    
    # changes the user role user -> {role: "admin or user"}
    existing_user.role = user.role

    db.commit()
    db.refresh(existing_user)
    return existing_user



