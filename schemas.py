from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel

class ShopNewOrderDTO(BaseModel):
    id: int
    order_date:datetime
    product_names: list[str]
    quantities: list[int]
    total_cost: float
    customer_name: str
    customer_email: str
    delivery_address: str
    user_id: str

class ShopNewVisitDTO(BaseModel):
    id: int
    user_id: str
    group: str
    visit_date: date
    device: str
    page_views: int
    time_spent: int
    total_amount: int
    session_id: str

class ShopOldOrderDTO(BaseModel):
    id: int
    order_date:datetime
    product_names: list[str]
    quantities: list[int]
    total_cost: float
    customer_name: str
    customer_email: str
    delivery_address: str
    user_id: str

class ShopOldVisitDTO(BaseModel):
    id: int
    user_id: str
    group: str
    visit_date: date
    device: str
    page_views: int
    time_spent: int
    total_amount: int
    session_id: str

class MoviesDTO(BaseModel):
    id_movie: int
    title: str
    release_year: int

class SessionsDTO(BaseModel):
    id_session: int
    movie_id: int
    session_datetime: datetime
    hall_number: int

class TicketsDTO(BaseModel):
    id_ticket: int
    session_id: int
    price: float
    sale_datetime: datetime

class AuthorsDTO(BaseModel):
    id_author: int
    firstname_author: str
    secondname_author: str
    middlename_author: str

class BooksDTO(BaseModel):
    id_book: int
    title: str
    author_id: int
    publication_year: int

class ReadersDTO(BaseModel):
    id_reader: int
    firstname_reader: str
    secondname_reader: str
    middlename_reader: str
    registration_at: date

class BookLoansDTO(BaseModel):
    id_loan: int
    reader_id: int
    book_id: int
    loan_date: Optional[date]
    return_date: Optional[date]

class ClientsDTO(BaseModel):
    id_client: int
    firstname_client: str
    secondname_client: str
    middlename_client: str

class DischesDTO(BaseModel):
    id_dish: int
    name: str
    price: float

class WaitersDTO(BaseModel):
    id_waiter: int
    firstname_waiter: str
    secondname_waiter: str
    middlename_waiter: str

class OrdersDTO(BaseModel):
    id_order: int
    client_id: int
    waiter_id: int
    order_datetime: datetime

class OrderItemsDTO(BaseModel):
    id_order_item: int
    order_id: int
    dish_id: int
    quantity: int

class StudentsDTO(BaseModel):
    id_student: int
    firstname_student: str
    secondname_student: str
    middlename_student: str
    group_name: str

class CoursesDTO(BaseModel):
    id_course: int
    name_course: str
    semester: int

class AttendanceDTO(BaseModel):
    id_attendance: int
    student_id: int
    course_id: int
    date_attendance: date
    is_present: bool

class GradesDTO(BaseModel):
    id_grade: int
    student_id: int
    course_id: int
    value_grade: int