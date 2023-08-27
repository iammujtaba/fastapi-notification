from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote as urlquote
from fasnof.base_domain import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./fasnof.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(cls=Base)
