from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database import Base

class Movie(Base):

    __tablename__  = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String, nullable=False)

    director: Mapped[str] = mapped_column(String, nullable=False)

    genre: Mapped[str] = mapped_column(String, nullable=False)

    rating: Mapped[float] = mapped_column(Float, nullable=False)

    release_year: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="movies")


class User(Base):
    
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    password: Mapped[str] = mapped_column(String, nullable=False)

    movies = relationship("Movie", back_populates="user", cascade="all, delete-orphan")

    role: Mapped[str] = mapped_column("roles", String, nullable=False, default="user")


