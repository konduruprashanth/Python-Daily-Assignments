from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.auth import create_access_token, verify_password
from app.database import Base, engine, get_db
from app.dependencies import get_current_user, require_roles
from app.schemas import UserRole


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RBAC Employee Management API",
    description="Employee management with JWT authentication and role-based authorization",
    version="1.0.0",
)


# ---------------- AUTHENTICATION APIs ----------------

@app.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: schemas.UserRegister,
    db: Session = Depends(get_db),
):
    if crud.get_user_by_email(db, str(user.email)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    try:
        return crud.create_user(db, user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        ) from None


@app.post("/login", response_model=schemas.TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, form_data.username)

    if user is None or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.get("/users/me", response_model=schemas.UserResponse)
def get_my_user(
    current_user: models.User = Depends(get_current_user),
):
    return current_user


# ---------------- ADMIN ROLE MANAGEMENT ----------------

@app.patch(
    "/users/{user_id}/role",
    response_model=schemas.UserResponse,
)
def change_user_role(
    user_id: int,
    role_data: schemas.RoleUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    user = crud.update_user_role(
        db,
        user_id,
        role_data.role,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


# ---------------- EMPLOYEE APIs ----------------

@app.post(
    "/employees",
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    linked_user = crud.get_user_by_id(db, employee.user_id)

    if linked_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Linked user not found",
        )

    if crud.get_employee_by_user_id(db, employee.user_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already has an employee record",
        )

    try:
        return crud.create_employee(db, employee)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee email already exists or employee data conflicts",
        ) from None


@app.get(
    "/employees/me",
    response_model=schemas.EmployeeResponse,
)
def get_my_employee_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    employee = crud.get_employee_by_user_id(db, current_user.id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found",
        )

    return employee


@app.patch(
    "/employees/me/phone",
    response_model=schemas.EmployeeResponse,
)
def update_my_phone(
    phone_data: schemas.PhoneUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    employee = crud.get_employee_by_user_id(db, current_user.id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found",
        )

    return crud.update_employee_phone(
        db,
        employee.id,
        phone_data.phone_number,
    )


@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def list_employees(
    department: str | None = None,
    designation: str | None = None,
    min_salary: float | None = Query(default=None, ge=0),
    max_salary: float | None = Query(default=None, ge=0),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if (
        min_salary is not None
        and max_salary is not None
        and min_salary > max_salary
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="min_salary cannot exceed max_salary",
        )

    if current_user.role == UserRole.EMPLOYEE.value:
        employee = crud.get_employee_by_user_id(db, current_user.id)
        return [employee] if employee else []

    return crud.get_employees(
        db,
        department=department,
        designation=designation,
        min_salary=min_salary,
        max_salary=max_salary,
    )


@app.get(
    "/employees/{employee_id}",
    response_model=schemas.EmployeeResponse,
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    employee = crud.get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    if (
        current_user.role == UserRole.EMPLOYEE.value
        and employee.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own employee details",
        )

    return employee


@app.put(
    "/employees/{employee_id}",
    response_model=schemas.EmployeeResponse,
)
def update_employee(
    employee_id: int,
    employee_data: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    manager: models.User = Depends(
        require_roles(UserRole.ADMIN, UserRole.MANAGER)
    ),
):
    employee = crud.get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    try:
        updated_employee = crud.update_employee(
            db,
            employee_id,
            employee_data,
        )
        return updated_employee
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee email already exists",
        ) from None


@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = crud.delete_employee(db, employee_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)