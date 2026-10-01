from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import engine, Base, get_db
from . import models, schemas, crud


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


# ---------------- BOOK APIs ----------------

@app.post("/books", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book(db, book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="ISBN already exists"
        )


@app.get("/books", response_model=list[schemas.BookResponse])
def get_books(
    category: str | None = None,
    author: str | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_books(db, category, author)


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    try:
        updated_book = crud.update_book(db, book_id, book)

        if updated_book is None:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        return updated_book

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="ISBN already exists"
        )


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.delete_book(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )


# ---------------- MEMBER APIs ----------------

@app.post("/members", response_model=schemas.MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(
    member: schemas.MemberCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_member(db, member)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Member email already exists"
        )


@app.get("/members", response_model=list[schemas.MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return crud.get_members(db)


@app.get("/members/{member_id}", response_model=schemas.MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = crud.get_member(db, member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member


@app.put("/members/{member_id}", response_model=schemas.MemberResponse)
def update_member(
    member_id: int,
    member: schemas.MemberCreate,
    db: Session = Depends(get_db)
):
    try:
        updated_member = crud.update_member(
            db,
            member_id,
            member
        )

        if updated_member is None:
            raise HTTPException(
                status_code=404,
                detail="Member not found"
            )

        return updated_member

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Member email already exists"
        )


@app.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = crud.delete_member(db, member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )


# ---------------- BORROW BOOK ----------------

@app.post("/members/{member_id}/books/{book_id}/borrow")
def borrow_book(
    member_id: int,
    book_id: int,
    db: Session = Depends(get_db)
):
    result, error = crud.borrow_book(
        db,
        member_id,
        book_id
    )

    if error:
        if error == "Member or book not found":
            raise HTTPException(
                status_code=404,
                detail=error
            )

        raise HTTPException(
            status_code=400,
            detail=error
        )

    return {
        "message": "Book borrowed successfully",
        "member_id": member_id,
        "book_id": book_id
    }


# ---------------- RETURN BOOK ----------------

@app.post("/members/{member_id}/books/{book_id}/return")
def return_book(
    member_id: int,
    book_id: int,
    db: Session = Depends(get_db)
):
    result, error = crud.return_book(
        db,
        member_id,
        book_id
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return {
        "message": "Book returned successfully",
        "member_id": member_id,
        "book_id": book_id
    }