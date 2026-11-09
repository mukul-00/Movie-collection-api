from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserResponse, UserUpdate, Token, UserRoleUpdate
from app.dependencies import get_db, get_current_user, get_current_admin
from app.crud import user_crud
from app.security.jwt import create_access_token
from app.models import User

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    created_user = user_crud.create_user(db, user)

    if created_user is None:
        raise HTTPException(status_code=409, detail="This email or username already exists.")
    
    return created_user


@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return user_crud.get_users(db)


@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.id != id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You are not allowed to view this user.")

    user = user_crud.get_user(db, id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/users/{id}", response_model=UserResponse)
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this user.")

    updated_user = user_crud.update_user(db, id, user)

    if updated_user is None:
        raise HTTPException(status_code=409, detail="Username or email already in use")

    return updated_user


@router.delete("/users/{id}", status_code=204)
def delete_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.id != id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this user.")    

    user = user_crud.delete_user(db, id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return 


@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = user_crud.login_user(db, form_data.username, form_data.password)   # this will contain the email and pass

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    
    token = create_access_token({"sub": str(user.id)}) # ⭐️
    
    return {"access_token": token, "token_type": "bearer"}


@router.get("/admin/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    return user_crud.get_users(db)


@router.put("/admin/users/{id}/role", response_model=UserResponse)
def update_user_role(id: int, user: UserRoleUpdate, db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    
    existing_user = user_crud.update_user_role(db, id, user)

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return existing_user