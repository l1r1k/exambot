from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

DBS_ERD = {
    'universitydb': 'universitydb_erd.png',
    'cinemadb': 'cinemadb_erd.png',
    'librarydb': 'librarydb_erd.png',
    'restaurantdb': 'restaurantdb_erd.png',
    'albumshopdb': 'albumshopdb_erd.png',
}

dbs_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=db_name)] for db_name in DBS_ERD.keys()
], resize_keyboard=True, input_field_placeholder='Выберите БД', one_time_keyboard=False)
