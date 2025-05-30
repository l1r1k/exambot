from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, ForeignKey

from typing import Annotated
from datetime import date

intpk = Annotated[int, mapped_column(primary_key=True)]

str_100 = Annotated[str, mapped_column(String(100))]
str_50 = Annotated[str, mapped_column(String(50))]

class Base(DeclarativeBase):
    pass

class StudentsOrm(Base):
    __tablename__ = 'students'

    id_student: Mapped[intpk]
    firstname_student: Mapped[str_100]
    secondname_student: Mapped[str_100]
    middlename_student: Mapped[str_100]
    group_name: Mapped[str_50]

class CoursesOrm(Base):
    __tablename__ = 'courses'

    id_course: Mapped[intpk]
    name_course: Mapped[str_100]
    semester: Mapped[int]

class AttendanceOrm(Base):
    __tablename__ = 'attendance'

    id_attendance: Mapped[intpk]
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id_student'))
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id_course'))
    date_attendance: Mapped[date]
    is_present: Mapped[bool]

class GradesOrm(Base):
    __tablename__ = 'grades'

    id_grade: Mapped[intpk]
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id_student'))
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id_course'))
    value_grade: Mapped[int]