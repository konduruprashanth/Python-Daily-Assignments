from sqlalchemy.orm import Session

from . import models, schemas


# ---------------- BOOKS ----------------

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, category=None, author=None):
    query = db.query(models.Book)

    if category:
        query = query.filter(models.Book.category == category)

    if author:
        query = query.filter(models.Book.author == author)

    return query.all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db_book = get_book(db, book_id)

    if db_book is None:
        return None

    for key, value in book.model_dump().items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)

    if db_book is None:
        return None

    db.delete(db_book)
    db.commit()

    return db_book


# ---------------- MEMBERS ----------------

def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_members(db: Session):
    return db.query(models.Member).all()


def get_member(db: Session, member_id: int):
    return (
        db.query(models.Member)
        .filter(models.Member.id == member_id)
        .first()
    )


def update_member(
    db: Session,
    member_id: int,
    member: schemas.MemberCreate
):
    db_member = get_member(db, member_id)

    if db_member is None:
        return None

    for key, value in member.model_dump().items():
        setattr(db_member, key, value)

    db.commit()
    db.refresh(db_member)

    return db_member


def delete_member(db: Session, member_id: int):
    db_member = get_member(db, member_id)

    if db_member is None:
        return None

    db.delete(db_member)
    db.commit()

    return db_member


# ---------------- BORROW / RETURN ----------------

def borrow_book(db: Session, member_id: int, book_id: int):
    member = get_member(db, member_id)
    book = get_book(db, book_id)

    if member is None or book is None:
        return None, "Member or book not found"

    if book.available_quantity <= 0:
        return None, "Book is not available"

    existing = (
        db.query(models.BorrowedBook)
        .filter(
            models.BorrowedBook.member_id == member_id,
            models.BorrowedBook.book_id == book_id
        )
        .first()
    )

    if existing:
        return None, "Book already borrowed by this member"

    borrowed_book = models.BorrowedBook(
        member_id=member_id,
        book_id=book_id
    )

    book.available_quantity -= 1

    db.add(borrowed_book)
    db.commit()

    return borrowed_book, None


def return_book(db: Session, member_id: int, book_id: int):
    borrowed_book = (
        db.query(models.BorrowedBook)
        .filter(
            models.BorrowedBook.member_id == member_id,
            models.BorrowedBook.book_id == book_id
        )
        .first()
    )

    if borrowed_book is None:
        return None, "This book was not borrowed by this member"

    book = get_book(db, book_id)

    if book is not None:
        book.available_quantity += 1

    db.delete(borrowed_book)
    db.commit()

    return borrowed_book, None