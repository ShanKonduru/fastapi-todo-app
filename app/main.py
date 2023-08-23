from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///../db/todo.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Templates setup
templates = Jinja2Templates(directory="templates")

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    todos = SessionLocal().query(Todo).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/")
async def create_todo(task: str = Form(...)):
    db = SessionLocal()
    db.add(Todo(task=task))
    db.commit()
    db.close()
    return {"message": "Todo created successfully"}
