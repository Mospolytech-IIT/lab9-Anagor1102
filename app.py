"""базовые операции с бд в веб-приложении"""
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

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


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """главная страница"""
    users = session.query(User).all()
    posts = session.query(Post).all()
    return templates.TemplateResponse("index.html", 
    {"request": request, "users": users, "posts": posts})


@app.post("/users/create")
async def create_user(
    username: str = Form(...), email: str = Form(...), password: str = Form(...)
):
    """создание поьзователя"""
    new_user = User(username=username, email=email, password=password)
    session.add(new_user)
    session.commit()
    return RedirectResponse(url="/", status_code=303)


@app.get("/users/delete/{user_id}")
async def delete_user(user_id: int):
    """удаление пользвоателя и его постов"""
    user = session.query(User).get(user_id)
    if user:
        session.query(Post).filter(Post.user_id == user_id).delete()
        session.delete(user)
        session.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/posts/create")
async def create_post(
    title: str = Form(...), content: str = Form(...), user_id: int = Form(...)
):
    """создание поста"""
    new_post = Post(title=title, content=content, user_id=user_id)
    session.add(new_post)
    session.commit()
    return RedirectResponse(url="/", status_code=303)


@app.get("/posts/delete/{post_id}")
async def delete_post(post_id: int):
    """удаление поста"""
    post = session.query(Post).get(post_id)
    if post:
        session.delete(post)
        session.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/posts/edit/{post_id}")
async def edit_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
):
    """редактирование поста"""
    post = session.query(Post).get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    post.title = title
    post.content = content
    session.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/users/edit/{user_id}")
async def edit_user(
    user_id: int,
    username: str = Form(...),
    email: str = Form(...)
):
    """редактирование пользователя"""
    user = session.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.username = username
    user.email = email
    session.commit()
    return RedirectResponse(url="/", status_code=303)
