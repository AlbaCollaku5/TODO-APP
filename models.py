from database.db_manager import Base 
from sqlalchemy import Column, Integer, String, Boolean


#what kind of db table we will create in the future// the actual records in the table 
class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)