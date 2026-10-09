from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import hash_password


# ---------------- USER OPERATIONS ----------------

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(
        models.User.id == user_id
    ).first()


def create_user(db: Session, user: schemas.UserRegister):
    db_user = models.User(
        full_name=user.full_name,
        email=str(user.email),
        hashed_password=hash_password(user.password),
        role=schemas.UserRole.EMPLOYEE.value,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user_role(
    db: Session,
    user_id: int,
    role: schemas.UserRole,
):
    db_user = get_user_by_id(db, user_id)

    if db_user is None:
        return None

    db_user.role = role.value

    db.commit()
    db.refresh(db_user)

    return db_user


# ---------------- EMPLOYEE OPERATIONS ----------------

def get_employee_by_id(db: Session, employee_id: int):
    return db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()


def get_employee_by_user_id(db: Session, user_id: int):
    return db.query(models.Employee).filter(
        models.Employee.user_id == user_id
    ).first()


def get_employees(
    db: Session,
    department: str = None,
    designation: str = None,
    min_salary: float = None,
    max_salary: float = None,
):
    query = db.query(models.Employee)

    if department:
        query = query.filter(
            models.Employee.department.ilike(f"%{department}%")
        )

    if designation:
        query = query.filter(
            models.Employee.designation.ilike(f"%{designation}%")
        )

    if min_salary is not None:
        query = query.filter(
            models.Employee.salary >= min_salary
        )

    if max_salary is not None:
        query = query.filter(
            models.Employee.salary <= max_salary
        )

    return query.all()


def create_employee(
    db: Session,
    employee: schemas.EmployeeCreate,
):
    db_employee = models.Employee(
        user_id=employee.user_id,
        employee_name=employee.employee_name,
        email=str(employee.email),
        phone_number=employee.phone_number,
        department=employee.department,
        designation=employee.designation,
        salary=employee.salary,
        joining_date=employee.joining_date,
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: schemas.EmployeeUpdate,
):
    db_employee = get_employee_by_id(db, employee_id)

    if db_employee is None:
        return None

    db_employee.employee_name = employee_data.employee_name
    db_employee.email = str(employee_data.email)
    db_employee.phone_number = employee_data.phone_number
    db_employee.department = employee_data.department
    db_employee.designation = employee_data.designation
    db_employee.salary = employee_data.salary
    db_employee.joining_date = employee_data.joining_date

    db.commit()
    db.refresh(db_employee)

    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee_by_id(db, employee_id)

    if db_employee is None:
        return False

    db.delete(db_employee)
    db.commit()

    return True


def update_employee_phone(
    db: Session,
    employee_id: int,
    phone_number: str,
):
    db_employee = get_employee_by_id(db, employee_id)

    if db_employee is None:
        return None

    db_employee.phone_number = phone_number

    db.commit()
    db.refresh(db_employee)

    return db_employee