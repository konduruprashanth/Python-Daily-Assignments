from .database import get_connection
from .schemas import StudentCreate


def create_student(student: StudentCreate):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO students
        (id, name, email, phone, age, course, address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student.id,
            student.name,
            student.email,
            student.phone,
            student.age,
            student.course,
            student.address,
        ),
    )

    connection.commit()
    connection.close()


def get_students(course=None, min_age=None, max_age=None):
    connection = get_connection()

    query = "SELECT * FROM students WHERE 1=1"
    values = []

    if course:
        query += " AND course = ?"
        values.append(course)

    if min_age is not None:
        query += " AND age >= ?"
        values.append(min_age)

    if max_age is not None:
        query += " AND age <= ?"
        values.append(max_age)

    students = connection.execute(query, values).fetchall()

    connection.close()

    return [dict(student) for student in students]


def get_student(student_id):
    connection = get_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,),
    ).fetchone()

    connection.close()

    return dict(student) if student else None


def update_student(student_id, student: StudentCreate):
    connection = get_connection()

    connection.execute(
        """
        UPDATE students
        SET name = ?, email = ?, phone = ?, age = ?, course = ?, address = ?
        WHERE id = ?
        """,
        (
            student.name,
            student.email,
            student.phone,
            student.age,
            student.course,
            student.address,
            student_id,
        ),
    )

    connection.commit()
    connection.close()


def delete_student(student_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,),
    )

    connection.commit()
    connection.close()