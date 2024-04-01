from sqlalchemy import Text, Integer, Double, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "hhuser"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(Text, unique=True)
    age: Mapped[int] = mapped_column(Integer)

    def __init__(self, email, age):
        pass

class Hobby(Base):
    __tablename__ = "hobby"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    aproved: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[DateTime] = mapped_column(DateTime)

    def __init__(self, name):
        self.name = name
        self.aproved = False
        self.created_at = datetime.now()