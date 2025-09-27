from database.db_manager import Base 
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

#what kind of db table we will create in the future// the actual records in the table 
class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to Users table (if needed)