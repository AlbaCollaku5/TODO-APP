from typing_extensions import Annotated
from fastapi import FastAPI, Depends, HTTPException, Path 
from sqlalchemy import Column, Integer, String, create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session

#FastAPI instance
app = FastAPI()

#Database connection
DATABASE_URL = "sqlite:///./data/books.db"
engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

#Database model
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(String, index=True)
    rating = Column(Integer, index=True)
   
#create tables
Base.metadata.create_all(bind=engine)

#Dependency to get the DB session
def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_dependency = Annotated[Session, Depends(get_db)]


#Pydentic  for request data 
class BookRequest(BaseModel):
    title: str = Field(min_length=2)
    author: str = Field(min_length=2)
    category: str = Field(min_length=2)
    description: str = Field(min_length=10)
    rating: int = Field(ge=1, le=5)

#Pydentic  for response data 
class BookResponse(BaseModel):
    id: int
    title: str = Field(min_length=2)
    author: str = Field(min_length=2)
    category: str = Field(min_length=2)
    description: str = Field(min_length=10)
    rating: int = Field(ge=1, le=5)

#API endpoint to create a new book
@app.post("/books/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest, db: db_dependency):
    book_model = Book(**book_request.model_dump()) #unpack the data
    db.add(book_model)
    db.commit()
    db.refresh(book_model)  # Refresh to get the generated ID
    return book_model

#API endpoint to get all books
@app.get("/")
async def read_all(db: db_dependency):
     return db.query(Book).all()

#API endpoint read an item by ID 
@app.get("/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def read_book(db: db_dependency, book_id: int = Path(gt=0)):
   book_model = db.query(Book).filter(Book.id == book_id).first()
   if book_model is not None:  #if there is data in the model
       return book_model
   raise HTTPException(status_code=404, detail="Book not found")
