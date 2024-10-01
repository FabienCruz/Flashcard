# avec SQLAlchemy
# reçoit la base (SQLite) du module principal (flaskcard)
# from sqlalchemy import Column, Integer, String, ForeignKey, Table
# from sqlalchemy.ext.declarative import declarative_base
# reprendre https://docs.sqlalchemy.org/en/20/orm/quickstart.html
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = create_engine("sqlite+pysqlite:///flashcards.db")

class Database:
    pass