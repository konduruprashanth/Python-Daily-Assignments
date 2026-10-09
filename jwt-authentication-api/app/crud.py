from sqlalchemy.orm import Session

from app import models
from app.auth import hash_password
from app.schemas import TaskCreate, TaskUpdate, UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_task(
    db: Session,
    task: TaskCreate,
    user_id: int
):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        assigned_to=user_id,
        due_date=task.due_date
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_tasks(
    db: Session,
    user_id: int,
    status: str = None,
    priority: str = None
):
    query = db.query(models.Task).filter(
        models.Task.assigned_to == user_id
    )

    if status:
        query = query.filter(
            models.Task.status == status
        )

    if priority:
        query = query.filter(
            models.Task.priority == priority
        )

    return query.all()


def get_task(
    db: Session,
    task_id: int,
    user_id: int
):
    return db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.assigned_to == user_id
    ).first()


def update_task(
    db: Session,
    db_task,
    task: TaskUpdate
):
    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status
    db_task.priority = task.priority
    db_task.due_date = task.due_date

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, db_task):
    db.delete(db_task)
    db.commit()


def complete_task(db: Session, db_task):
    db_task.status = "Completed"

    db.commit()
    db.refresh(db_task)

    return db_task