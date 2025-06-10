from datetime import datetime, date
from typing import Optional

from sqlalchemy import Integer, String, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, ForeignKey, relationship
from sqlalchemy.sql.sqltypes import DateTime, Date


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    contacts: Mapped[list["Contact"]] = relationship(
        "Contact",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, login={self.login})"


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    additional_info: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="contacts")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Contact(id={self.id}, name={self.name}, last_name={self.last_name}, email={self.email})"
