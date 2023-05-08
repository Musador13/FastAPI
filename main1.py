from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

from fastapi import FastAPI

# строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# создаем движок SqlAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# создаем модель, объекты которой будут храниться в бд
Base = declarative_base()
class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer, )

# создаем таблицы
Base.metadata.create_all(bind=engine)

# создаем сессию подключения к бд
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

# создаем объект Person для добавления в бд
tom = Person(name="Tom", age=38)
db.add(tom)  # добавляем в бд
db.commit()  # сохраняем изменения
db.refresh(tom)  # обновляем состояние объекта
print(tom.id)   # можно получить установленный id

bob = Person(name="Bob", age=42)
sam = Person(name="Sam", age=25)
db.add(bob)
db.add(sam)
db.commit()

alice = Person(name="Alice", age=33)
kate = Person(name="Kate", age=28)
db.add_all([alice, kate])
db.commit()

# приложение, которое ничего не делает
app = FastAPI()
