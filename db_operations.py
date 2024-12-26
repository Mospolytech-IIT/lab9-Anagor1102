"""модуль различных операций с бд"""
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


def add_users():
    """добавление пользователей"""
    try:
        users = [
            User(username="user1", email="user1@example.com", password="password1"),
            User(username="user2", email="user2@example.com", password="password2"),
        ]
        session.add_all(users)
        session.commit()
        print("Пользователи добавлены.")
    finally:
        session.close()


def add_posts():
    """добавление постов"""
    try:
        posts = [
            Post(title="First Post", content="This is the first post", user_id=1),
            Post(title="Second Post", content="This is the second post", user_id=1),
            Post(title="Another Post", content="This is another post", user_id=2),
        ]
        session.add_all(posts)
        session.commit()
        print("Посты добавлены.")
    finally:
        session.close()


def get_all_users():
    """получение всех пользователей"""
    try:
        users = session.query(User).all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
    finally:
        session.close()


def get_all_posts():
    """получение всех постов"""
    try:
        posts = session.query(Post).all()
        for post in posts:
            print(f"ID: {post.id}, Title: {post.title}," 
                  f"Content: {post.content}, User ID: {post.user_id}")
    finally:
        session.close()


def get_user_posts(user_id):
    """получение постов пользователя"""
    try:
        posts = session.query(Post).filter_by(user_id=user_id).all()
        for post in posts:
            print(f"Title: {post.title}, Content: {post.content}")
    finally:
        session.close()


def update_user_email(user_id, new_email):
    """редактирование почты пользовтеля"""
    try:
        user = session.query(User).get(user_id)
        if user:
            user.email = new_email
            session.commit()
    finally:
        session.close()


def update_post_content(post_id, new_content):
    """редактирование поста"""
    try:
        post = session.query(Post).get(post_id)
        if post:
            post.content = new_content
            session.commit()
    finally:
        session.close()


def delete_post(post_id):
    """удаление поста"""
    try:
        post = session.query(Post).get(post_id)
        if post:
            session.delete(post)
            session.commit()
    finally:
        session.close()


def delete_user_and_posts(user_id):
    """удаление пользователя и его постов"""
    try:
        user = session.query(User).get(user_id)
        if user:
            session.query(Post).filter_by(user_id=user_id).delete()
            session.delete(user)
            session.commit()
    finally:
        session.close()
