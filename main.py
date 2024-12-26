"""модуль подключения к бд и создания таблиц"""
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:anagor@localhost/postgres"

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class User(Base):
    """модель данных пользователей"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship("Post", back_populates="user")


class Post(Base):
    """модель данных постов"""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
