from typing import Optional
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

#create book objects 
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    #constructor
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date 


'''book request object that we can use to validate the book request'''
class BookRequest(BaseModel):
     id: Optional[int] = Field( description= 'ID is not needed on create', default=None)  #makes the book id optional
     title: str = Field(min_length=3)
     author: str = Field(min_length=1)
     description: str = Field(min_length=1, max_length=100)
     rating: int = Field(gt=0, lt=6)
     published_date: int = Field (gt=1999, lt=2031)
     

    # create a descriptive request within the swagger documentation
     model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwAlba",
                "description": "A new description of the book",
                "rating": 5,
                "published_book":2020
            }
        }
     }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithalba', 'A very nice book', 5, 2012),
    Book(2, 'Python Fundamentals', 'john_doe', 'Beginner-friendly guide to Python programming', 4, 2012),
    Book(3, 'Deep Learning Mastery', 'jane_smith', 'Comprehensive book on deep learning concepts and practices', 5,2022),
    Book(4, 'Web Development Essentials', 'devguru', 'Covers HTML, CSS, and JavaScript basics', 3, 2002),
    Book(5, 'Data Structures & Algorithms', 'algo_master', 'Step-by-step approach with coding examples', 4, 2011),
    Book(6, 'FastAPI in Action', 'api_builder', 'Learn how to build APIs with FastAPI', 5, 2011),
    Book(7, 'SQL Made Easy', 'db_expert', 'Simple explanations of SQL queries and database design', 4, 2001),
    Book(8, 'Machine Learning with Python', 'ml_coder', 'Hands-on projects and examples for ML beginners', 5, 2000),
    Book(9, 'Cloud Computing Basics', 'cloudy_mind', 'Introduction to cloud services and architectures', 3, 2005),
    Book(10, 'Clean Code Practices', 'senior_dev', 'Best practices for writing clean and maintainable code', 5, 2011)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def return_all_books():
    return BOOKS

#find a book based on book id 
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    #raise a HTTPExecption if the book is not found
    raise HTTPException(status_code=404, detail='Item not found')

#filter from book ratings 
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

#filter from rating and id 
@app.get("/books/filter/{book_id}", status_code=status.HTTP_200_OK)
async def filter_book(book_id: int, book_rating : int):
    return_filtered_books = []
    for book in BOOKS:
        if book.rating == book_rating and  book.id == book_id:
            return_filtered_books.append(book)


#get publishing date of a book 
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def filter_by_publishing_date(publishing_date: int):
    return_publishing_date = []
    for book in BOOKS:
        if book.published_date == publishing_date:
            return_publishing_date.append(book)
    return return_publishing_date


'''add a new book'''
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

#normal python function checks the id for each book
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    #if len(BOOKS) >0 :
    #    book.id = BOOKS[-1].id + 1
    #else:
    #    book.id = 1
    return book 

#update an object - piece of data 
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=104, detail='Item not found')

#delete a book 
@app.delete("/books/{book_id}",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=104, detail='Item not found')           
            
