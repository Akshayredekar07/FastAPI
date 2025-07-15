
from fastapi import FastAPI, Path, Query, HTTPException
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel
import re 
import json


app = FastAPI(title="Bookstore Application API")

JSON_FILE = "books.json"

ISBN_PATTERN = r"^978-\d{10}-\d$"


# pydantic model for input and response 
class Book(BaseModel):
    id:int
    isbn:str 
    title:str
    author:str 
    programming_language:Optional[str]
    publisher:str 
    price:float
    publication_year:int 

#pydantic model for new book
class BookCreate(BaseModel):
    isbn: str
    title: str
    author: str
    programming_language: Optional[str]
    publisher: str
    price: float
    publication_year: int



class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


# Enum for sort field
class SortField(str, Enum):
    price = "price"
    publication_year = "publication_year"


def load_books():
    try:
        with open('books.json', 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Corrupted JSON file")


# Save books to JSON file
def save_books(books):
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(books, f, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save data: {str(e)}")


@app.get("/books/isbn/{isbn}", response_model=Book)
async def get_book_by_isbn(isbn: str = Path(..., description="ISBN of the book e.g (978-0112345678)", regex=ISBN_PATTERN)):

    """
    Retrieve a book by its ISBN.
    """
    books = load_books()
    for book in books:
        if book['isbn'] == isbn:
            return book
        else:
            raise HTTPException(status_code=404, detail="Book not found")



# Get the book by the book id

@app.get("/book/id/{book_id}", response_model=Book)
async def get_book_by_id(book_id :int = Path(..., ge=1, description="ID of book(positive integer)")):
    """
    Return book by its id
    """
    books = load_books()
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", response_model=List[Book])
async def get_books(
    skip:int = Query(0, ge=0, description="No of books ot skip pagination"),
    limit:int = Query(10, ge=1, le=100, description="Maximum number of books to return"),
    search: Optional[str] = Query(None, min_length=3, max_length=50, description="Search by title or author"),
    programming_languages: List[str] = Query([], description="Filter by one or more programming languages"),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    sort_field: SortField = Query(..., description="Field to sort by (price or publication_year)"),
    sort_order: SortOrder = Query(..., description="Sort order (asc or desc)")
):
    books = load_books()
    filtered_books = books

        # Apply search filter (title or author)
    if search:
        search = search.lower()
        filtered_books = [
            book for book in filtered_books
            if search in book["title"].lower() or search in book["author"].lower()
        ]

    # Apply programming language filter
    if programming_languages:
        filtered_books = [
            book for book in filtered_books
            if book["programming_language"] in programming_languages
        ]

    # Apply publisher filter
    if publisher:
        filtered_books = [
            book for book in filtered_books
            if book["publisher"].lower() == publisher.lower()
        ]

    # Apply price range filter
    if min_price is not None:
        filtered_books = [book for book in filtered_books if book["price"] >= min_price]
    if max_price is not None:
        filtered_books = [book for book in filtered_books if book["price"] <= max_price]

    # Sort by specified field
    filtered_books = sorted(
        filtered_books,
        key=lambda x: x[sort_field],
        reverse=(sort_order == SortOrder.desc)
    )

    # Apply pagination
    return filtered_books[skip:skip + limit]


@app.post("/books/", response_model=Book)
async def add_book(book: BookCreate):
    """
    Add a new book to the inventory.
    """
    books = load_books()

    # Validate ISBN format
    if not re.match(ISBN_PATTERN, book.isbn):
        raise HTTPException(status_code=422, detail="Invalid ISBN format")

    # Check for duplicate ISBN
    if any(b["isbn"] == book.isbn for b in books):
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    # Generate new ID
    new_id = max(b["id"] for b in books) + 1 if books else 1

    # Create new book
    new_book = {
        "id": new_id,
        **book.dict()
    }

    # Add to books and save to JSON
    books.append(new_book)
    save_books(books)
    return new_book