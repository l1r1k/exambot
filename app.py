# Other
import asyncio
import os
import logging
import sys

from enum import Enum
import pandas as pd

# Aiogram
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

# Env
from dotenv import load_dotenv

# SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import text

# Models
from albumshop import ShopNewOrderOrm, ShopNewVisitOrm, ShopOldOrderOrm, ShopOldVisitOrm
from cinema import MoviesOrm, SessionsOrm, TicketsOrm
from library import ReadersOrm, AuthorsOrm, BooksOrm, BookLoansOrm
from restaurant import ClientsOrm, WaitersOrm, DischesOrm, OrdersOrm, OrderItemsOrm
from university import StudentsOrm, AttendanceOrm, GradesOrm, CoursesOrm

load_dotenv()

# constants

TG_API = os.getenv('TG_API')

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

DBS_ERD = {
    'universitydb': 'universitydb_erd.png',
    'cinemadb': 'cinemadb_erd.png',
    'librarydb': 'librarydb_erd.png',
    'restaurantdb': 'restaurantdb_erd.png',
    'albumshopdb': 'albumshopdb_erd.png',
}

CONNECTION_STRING = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/'

DBS_TABLE_DESCRIPTION = {
    'universitydb': 'Таблица students - Студенты;\nТаблица courses - Предмет, по которому проводятся пары;\nТаблица attencdance - Присутствие на паре;\nТаблица grades - Оценка студента по предмету',
    'cinemadb': 'Таблица movies - Фильмы;\nТаблица sessions - сессии фильма, на которую могут прийти зрители;\nТаблица tickets - Таблица проданных билетов на киносессию',
    'librarydb': 'Таблица authors - Автор книг;\nТаблица readers - читатели;\nТаблица books - Книги;\nТаблица bookloans - Записи взятия книги читателем',
    'restaurantdb': 'Таблица clients - Клиенты ресторана;\nТаблица waiters - Официанты;\nТаблица dishes - Блюда, которые продаются;\nТаблица orders - Заказы;\nТаблица orderitems - Состав заказов',
    'albumshopdb': 'Таблица shop_new_order - Заказы нового магазина;\nТаблица shop_new_visit - Визиты посетителей в новом магазине;\nТаблица shop_old_order - Заказы старого магазина;\nТаблица shop_old_visit - Визиты посетителей в старом магазине',
}

DBS = list(DBS_TABLE_DESCRIPTION.keys())

class DbTables(Enum):
    albumshopdb=[ShopNewOrderOrm.__tablename__, ShopNewVisitOrm.__tablename__, ShopOldOrderOrm.__tablename__, ShopOldVisitOrm.__tablename__]
    cinemadb=[MoviesOrm.__tablename__, SessionsOrm.__tablename__, TicketsOrm.__tablename__]
    librarydb=[ReadersOrm.__tablename__,AuthorsOrm.__tablename__,BooksOrm.__tablename__,BookLoansOrm.__tablename__]
    restaurantdb=[ClientsOrm.__tablename__,WaitersOrm.__tablename__,DischesOrm.__tablename__,OrdersOrm.__tablename__,OrderItemsOrm.__tablename__]
    universitydb=[StudentsOrm.__tablename__,CoursesOrm.__tablename__,AttendanceOrm.__tablename__,GradesOrm.__tablename__]

#------------------------------------------

# Async functions for work with DB

async def save_table_to_csv_file(table_name, db_name, async_engine: AsyncEngine):
    async with async_engine.connect() as conn:
        result = await conn.execute(text(f'SELECT * FROM {table_name}'))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        await asyncio.to_thread(
            df.to_csv,
            f'{db_name}/{table_name}.csv',
            index=False,
            encoding='utf-8'
        )

    
async def create_csv_files(db_name):
    tables = []
    async_engine = create_async_engine(CONNECTION_STRING+db_name)

    match(db_name):
        case 'albumshopdb':
            tables = DbTables.albumshopdb.value
        case 'cinemadb':
            tables = DbTables.cinemadb.value
        case 'librarydb':
            tables = DbTables.librarydb.value
        case 'restaurantdb':
            tables = DbTables.restaurantdb.value
        case 'universitydb':
            tables = DbTables.universitydb.value

    tasks_on_select_query = [asyncio.create_task(save_table_to_csv_file(table_name, db_name, async_engine)) for table_name in tables]
    await asyncio.wait(tasks_on_select_query)

async def get_fsinput_csv(db_name):
    if not os.path.isdir(db_name):
        os.makedirs(db_name)
        task = asyncio.create_task(create_csv_files(db_name))
        await asyncio.wait_for(task, timeout=60)

    tables_csv_path = os.listdir(db_name)

    for idx, table in enumerate(tables_csv_path):
        tables_csv_path[idx] = f'{db_name}/{table}'

    tables_csv = [FSInputFile(csv_file) for csv_file in tables_csv_path]

    return tables_csv


# End Async functions

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'Привет, {message.from_user.full_name}.\n\nЧтобы получить ERD-модель или Датасеты (csv) таблиц из БД - {html.bold('напиши название БД из билета или введи номер БД из списка ниже')}.\n\nНапоминаю список наименования БД:\n\n{'\n'.join([f'{idx+1}) {name_db}' for idx, name_db in enumerate(DBS_ERD.keys())])}')

@dp.message()
async def echo_handler(message: Message) -> None:
    user_text = message.text

    user_text = user_text.strip()

    user_text_to_int = int(user_text) if user_text[0].isnumeric() else None

    if user_text_to_int and user_text_to_int >= 1 and user_text_to_int <= 5:
        choosed_db = DBS[user_text_to_int - 1]

        photo = FSInputFile(DBS_ERD[choosed_db])

        await message.answer_photo(photo, caption=f'ERD-модель для БД {choosed_db}')
        await message.answer(DBS_TABLE_DESCRIPTION[choosed_db])

        tables_csv = await get_fsinput_csv(choosed_db)

        for table in tables_csv:
            await message.answer_document(table)

        return None
    
    if user_text in DBS:
        photo = FSInputFile(DBS_ERD[user_text])

        await message.answer_photo(photo, caption=f'ERD-модель для БД {user_text}')
        await message.answer(DBS_TABLE_DESCRIPTION[user_text])

        tables_csv = await get_fsinput_csv(user_text)

        for table in tables_csv:
            await message.answer_document(table)

        return None
    
    await message.answer(f'Такой БД нет!\n\nНапоминаю список наименования БД:\n\n{'\n'.join([f'{idx+1}) {name_db}' for idx, name_db in enumerate(DBS_ERD.keys())])}\nМожете ввести как имя БД так и номер из списка')
    

async def main():
    bot = Bot(token=TG_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
