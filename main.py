from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

books_db: list[Book] = []
next_id = 1

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

@app.get("/")
def read_root():
    return {"message": "Library API is running!"}

@app.get("/books")
def get_books():
    return books_db

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books")
def create_book(book: BookCreate):
    global next_id
    new_book = Book(id=next_id, title=book.title, author=book.author, year=book.year)
    books_db.append(new_book)
    next_id += 1
    return new_book

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: BookCreate):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db[index] = Book(id=book_id, title=updated_book.title, author=updated_book.author, year=updated_book.year)
            return books_db[index]
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            deleted_book = books_db.pop(index)
            return {"message": "Book deleted", "book": deleted_book}
    raise HTTPException(status_code=404, detail="Book not found")
