from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from . import models, schemas

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(
    db: Session,
    role: schemas.Role | None = None,
    name: str | None = None,
):
    query = db.query(models.User)
    if role:
        query = query.filter(models.User.role == role.value)
    if name:
        query = query.filter(
            models.User.full_name.ilike(f"%{name}%")
        )
    return query.all()

def create_user(
    db: Session,
    user: schemas.UserCreate,
):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password,
        role=user.role.value,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(
    db: Session,
    user_id: int,
    user: schemas.UserUpdate,
):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db_user.full_name = user.full_name
    db_user.email = user.email
    db_user.phone_number = user.phone_number
    db_user.role = user.role.value
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(
    db: Session,
    user_id: int,
):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

def change_password(
    db: Session,
    user_id: int,
    password_data: schemas.PasswordChange,
):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    if not verify_password(
        password_data.current_password,
        db_user.password,
    ):
        return False
    db_user.password = hash_password(
        password_data.new_password
    )
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_login(
    db: Session,
    email: str,
    password: str,
):
    db_user = get_user_by_email(db, email)
    if not db_user:
        return None
    if not verify_password(
        password,
        db_user.password,
    ):
        return None
    return db_user