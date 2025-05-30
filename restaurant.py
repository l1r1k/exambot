from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, ForeignKey, Numeric

from typing import Annotated
from datetime import datetime

from schemas import ClientsDTO, WaitersDTO, DischesDTO, OrdersDTO, OrderItemsDTO

intpk = Annotated[int, mapped_column(primary_key=True)]

str_100 = Annotated[str, mapped_column(String(100))]
str_50 = Annotated[str, mapped_column(String(50))]

class Base(DeclarativeBase):
    pass

class ClientsOrm(Base):
    __tablename__ = 'clients'

    id_client: Mapped[intpk]
    firstname_client: Mapped[str_100]
    secondname_client: Mapped[str_100]
    middlename_client: Mapped[str_100]

    def to_pydantic(self):
        return ClientsDTO.model_validate(self)

class DischesOrm(Base):
    __tablename__ = 'dishes'

    id_dish: Mapped[intpk]
    name: Mapped[str_100]
    price: Mapped[float] = mapped_column(Numeric(6,2))

    def to_pydantic(self):
        return DischesDTO.model_validate(self)

class WaitersOrm(Base):
    __tablename__ = 'waiters'

    id_waiter: Mapped[intpk]
    firstname_waiter: Mapped[str_100]
    secondname_waiter: Mapped[str_100]
    middlename_waiter: Mapped[str_100]

    def to_pydantic(self):
        return WaitersDTO.model_validate(self)

class OrdersOrm(Base):
    __tablename__ = 'orders'

    id_order: Mapped[intpk]
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id_client'))
    waiter_id: Mapped[int] = mapped_column(ForeignKey('waiters.id_waiter'))
    order_datetime: Mapped[datetime]

    def to_pydantic(self):
        return OrdersDTO.model_validate(self)

class OrderItemsOrm(Base):
    __tablename__ = 'orderitems'

    id_order_item: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id_order'))
    dish_id: Mapped[int] = mapped_column(ForeignKey('dishes.id_dish'))
    quantity: Mapped[int]

    def to_pydantic(self):
        return OrderItemsDTO.model_validate(self)