from fastapi import FastAPI
import models
from database.db_manager import engine
from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)  
app.include_router(todos.router)
