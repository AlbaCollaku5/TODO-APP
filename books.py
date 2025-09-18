from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'fiction'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'technology'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'philosophy'},
    {'title': 'Title Six', 'author': 'Author Six', 'category': 'art'},
    {'title': 'Title Seven', 'author': 'Author Seven', 'category': 'art'},
    {'title': 'Title Eight', 'author': 'Author Two', 'category': 'art'}
]

@app.get("/books") 
async def read_all_books():
    return BOOKS
  
#get a specific book from the BOOKS list | Path Parameter 
@app.get("/books/{book_title}") 
async def read__book(book_title : str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

#Query Parameters to filter data based on the URL provided (after a ? in the URL)
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book) #append adds the book to the list
    return books_to_return


@app.get("/books/{book_author}/")  #path parameter
async def read_author_category_by_query(book_author: str, category: str):  #query parameter
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
            book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return

#send data through the api endpoint
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

#update data 
@app.put("/books/update_book")
async def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book

#delete book
@app.delete("/books/{delete_book}")
async def delete_book(book_title : str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == delete_book.get('title').casefold():
            BOOKS.pop(i)
        break


#fetch all books from a specific author 
@app.get("/books/byauthor/{author}")
async def fetch_books_specific_author(book_author: str):
    books_fetch = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold():
           books_fetch.append(book)

    return books_fetch