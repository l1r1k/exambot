from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, ForeignKey

from typing import Annotated
from datetime import date

from schemas import ReadersDTO, AuthorsDTO, BooksDTO, BookLoansDTO

intpk = Annotated[int, mapped_column(primary_key=True)]

str_100 = Annotated[str, mapped_column(String(100))]
str_50 = Annotated[str, mapped_column(String(50))]

class Base(DeclarativeBase):
    pass

class AuthorsOrm(Base):
    __tablename__ = 'authors'

    id_author: Mapped[intpk]
    firstname_author: Mapped[str_100]
    secondname_author: Mapped[str_100]
    middlename_author: Mapped[str_100]

    def to_pydantic(self):
        return AuthorsDTO.model_validate(self)

class BooksOrm(Base):
    __tablename__ = 'books'

    id_book: Mapped[intpk]
    title: Mapped[str_100]
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id_author'))
    publication_year: Mapped[int]

    def to_pydantic(self):
        return BooksDTO.model_validate(self)

class ReadersOrm(Base):
    __tablename__ = 'readers'

    id_reader: Mapped[intpk]
    firstname_reader: Mapped[str_100]
    secondname_reader: Mapped[str_100]
    middlename_reader: Mapped[str_100]
    registration_at: Mapped[date]

    def to_pydantic(self):
        return ReadersDTO.model_validate(self)

class BookLoansOrm(Base):
    __tablename__ = 'bookloans'

    id_loan: Mapped[intpk]
    reader_id: Mapped[int] = mapped_column(ForeignKey('readers.id_reader'))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id_book'))
    loan_date: Mapped[date | None]
    return_date: Mapped[date | None]

    def to_pydantic(self):
        return BookLoansDTO.model_validate(self)