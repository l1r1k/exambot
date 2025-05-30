from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, ForeignKey, Numeric

from typing import Annotated
from datetime import date, datetime

from schemas import MoviesDTO, SessionsDTO, TicketsDTO

intpk = Annotated[int, mapped_column(primary_key=True)]

str_100 = Annotated[str, mapped_column(String(100))]
str_50 = Annotated[str, mapped_column(String(50))]

class Base(DeclarativeBase):
    pass

class MoviesOrm(Base):
    __tablename__ = 'movies'

    id_movie: Mapped[intpk]
    title: Mapped[str_100]
    release_year: Mapped[int]

    def to_pydantic(self):
        return MoviesDTO.model_validate(self)

class SessionsOrm(Base):
    __tablename__ = 'sessions'

    id_session: Mapped[intpk]
    movie_id: Mapped[int] = mapped_column(ForeignKey('movies.id_movie'))
    session_datetime: Mapped[datetime]
    hall_number: Mapped[int]

    def to_pydantic(self):
        return SessionsDTO.model_validate(self)

class TicketsOrm(Base):
    __tablename__ = 'tickets'

    id_ticket: Mapped[intpk]
    session_id: Mapped[int] = mapped_column(ForeignKey('sessions.id_session'))
    price: Mapped[float] = mapped_column(Numeric(6,2))
    sale_datetime: Mapped[datetime]

    def to_pydantic(self):
        return TicketsDTO.model_validate(self)
