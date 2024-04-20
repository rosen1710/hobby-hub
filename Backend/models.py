from sqlalchemy import Text, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
import bcrypt

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "hhuser"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(Text, unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    fullname: Mapped[str] = mapped_column(Text)
    age: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    messages: Mapped[List["Message"]] = relationship(back_populates="user")

    def __init__(self, email, password, fullname, age, description):
        self.email = email
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.fullname = fullname
        self.age = age
        self.description = description


class Hobby(Base):
    __tablename__ = "hobby"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True)
    approved: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[DateTime] = mapped_column(DateTime)

    def __init__(self, name):
        self.name = name
        self.approved = False
        self.created_at = datetime.now()

class Hobby_User(Base):
    __tablename__ = "hobby_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("hhuser.id"))
    hobby_id: Mapped[int] = mapped_column(ForeignKey("hobby.id"))

    def __init__ (self, user_id, hobby_id):
        self.user_id = user_id
        self.hobby_id =  hobby_id

class Channel(Base):
    __tablename__ = "channel"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    hobby_id: Mapped[int] = mapped_column(ForeignKey("hobby.id"))
    approved: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[DateTime] = mapped_column(DateTime)

    def __init__(self, name, hobby_id):
        self.name = name
        self.hobby_id = hobby_id
        self.approved = False
        self.created_at = datetime.now()

class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("hhuser.id"))
    user: Mapped["User"] = relationship(back_populates="messages")
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"))
    created_at: Mapped[DateTime] = mapped_column(DateTime)

    def __init__(self, text, user_id, channel_id):
        self.text = text
        self.user_id = user_id
        self.channel_id = channel_id
        self.created_at = datetime.now()