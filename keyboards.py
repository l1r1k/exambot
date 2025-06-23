from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from .app import DBS_ERD

dbs_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=db_name) for db_name in DBS_ERD.keys()]
], resize_keyboard=True, input_field_placeholder='Выберите БД', one_time_keyboard=False)