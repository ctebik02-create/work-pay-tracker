import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in .env file.")
sqlalchemy_url = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)


engine = create_engine(sqlalchemy_url)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column("password")
    shifts: Mapped[list["Shift"]] = relationship(back_populates="user")

class Shift(Base):
    __tablename__ = "shifts"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    hours: Mapped[float]
    earned: Mapped[float]
    note: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="shifts")

class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    hour_rate: Mapped[float]
    default_shift_normal_hours: Mapped[int]
    salary_period_start_day: Mapped[int]
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))


