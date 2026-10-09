from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.auth import (
    create_access_token,
    get_current_user,
    verify_password,
)
from app.database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(title="JWT Authentication API")


# -------------------- Authentication APIs --------------------


@app.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = crud.get_user_by_email(
        db,
        user.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    return crud.create_user(db, user)


@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OAuth2 uses the username field for the user's email.
    user = crud.get_user_by_email(
        db,
        form_data.username,
    )

    if not user or not verify_password(
        form_data.password,
        user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.get(
    "/users/me",
    response_model=schemas.UserResponse,
)
def get_me(
    current_user: models.User = Depends(get_current_user),
):
    return current_user


# -------------------- Task APIs --------------------


@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: schemas.TaskCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_task(
        db,
        task,
        current_user.id,
    )


@app.get(
    "/tasks",
    response_model=list[schemas.TaskResponse],
)
def get_tasks(
    status_filter: str | None = Query(
        default=None,
        alias="status",
    ),
    priority: str | None = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.get_tasks(
        db,
        current_user.id,
        status_filter,
        priority,
    )


@app.get(
    "/my-tasks",
    response_model=list[schemas.TaskResponse],
)
def get_my_tasks(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.get_tasks(
        db,
        current_user.id,
    )


@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
)
def get_task(
    task_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = crud.get_task(
        db,
        task_id,
        current_user.id,
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_task = crud.get_task(
        db,
        task_id,
        current_user.id,
    )

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    crud.update_task(
        db,
        db_task,
        task,
    )

    return db_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_task = crud.get_task(
        db,
        task_id,
        current_user.id,
    )

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    crud.delete_task(
        db,
        db_task,
    )


@app.patch(
    "/tasks/{task_id}/complete",
    response_model=schemas.TaskResponse,
)
def complete_task(
    task_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_task = crud.get_task(
        db,
        task_id,
        current_user.id,
    )

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return crud.complete_task(
        db,
        db_task,
    )