from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Numeric, Text, ARRAY, Integer

from typing import Annotated
from datetime import date, datetime

from schemas import ShopNewOrderDTO, ShopNewVisitDTO, ShopOldOrderDTO, ShopOldVisitDTO

intpk = Annotated[int, mapped_column(primary_key=True)]
str_50 = Annotated[str, mapped_column(String(50))]

class Base(DeclarativeBase):
    pass

class ShopNewOrderOrm(Base):
    __tablename__='shop_new_order'
    
    id: Mapped[intpk]
    order_date:Mapped[datetime]
    product_names: Mapped[list[str]] = mapped_column(ARRAY(String))
    quantities: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    total_cost: Mapped[float] = mapped_column(Numeric(10,2))
    customer_name: Mapped[str] = mapped_column(String(255))
    customer_email: Mapped[str] = mapped_column(String(254))
    delivery_address: Mapped[str] = mapped_column(Text())
    user_id: Mapped[str_50]

    def to_pydantic(self):
        return ShopNewOrderDTO.model_validate(self)

class ShopNewVisitOrm(Base):
    __tablename__ = 'shop_new_visit'

    id: Mapped[intpk]
    user_id: Mapped[str_50]
    group: Mapped[str] = mapped_column(String(1))
    visit_date: Mapped[date]
    device: Mapped[str] = mapped_column(String(20))
    page_views: Mapped[int]
    time_spent: Mapped[int]
    total_amount: Mapped[int]
    session_id: Mapped[str_50]

    def to_pydantic(self):
        return ShopNewVisitDTO.model_validate(self)

class ShopOldOrderOrm(Base):
    __tablename__='shop_old_order'
    
    id: Mapped[intpk]
    order_date:Mapped[datetime]
    product_names: Mapped[list[str]] = mapped_column(ARRAY(String))
    quantities: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    total_cost: Mapped[float] = mapped_column(Numeric(10,2))
    customer_name: Mapped[str] = mapped_column(String(255))
    customer_email: Mapped[str] = mapped_column(String(254))
    delivery_address: Mapped[str] = mapped_column(Text())
    user_id: Mapped[str_50]

    def to_pydantic(self):
        return ShopOldOrderDTO.model_validate(self)

class ShopOldVisitOrm(Base):
    __tablename__ = 'shop_old_visit'

    id: Mapped[intpk]
    user_id: Mapped[str_50]
    group: Mapped[str] = mapped_column(String(1))
    visit_date: Mapped[date]
    device: Mapped[str] = mapped_column(String(20))
    page_views: Mapped[int]
    time_spent: Mapped[int]
    total_amount: Mapped[int]
    session_id: Mapped[str_50]

    def to_pydantic(self):
        return ShopOldVisitDTO.model_validate(self)
