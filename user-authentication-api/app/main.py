from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Authentication API")


@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = crud.get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    return crud.create_user(db, user)


@app.post("/login")
def login_user(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    user = crud.verify_login(
        db,
        login_data.email,
        login_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {
        "message": "Login successful",
        "user_id": user.id,
        "full_name": user.full_name,
        "role": user.role,
    }


@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(
    role: schemas.Role | None = Query(default=None),
    name: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud.get_users(db, role, name)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    existing_email = crud.get_user_by_email(db, user_data.email)

    if existing_email and existing_email.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    return crud.update_user(db, user_id, user_data)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = crud.delete_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return None


@app.put("/users/{user_id}/password", response_model=schemas.UserResponse)
def change_user_password(
    user_id: int,
    password_data: schemas.PasswordChange,
    db: Session = Depends(get_db),
):
    result = crud.change_password(
        db,
        user_id,
        password_data,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if result is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect",
        )

    return result