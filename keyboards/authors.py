from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.functions import _to_dict
from database.core_database import get_names_book, get_callbacks_book, get_name_book, get_callback_book

books = ['Рэй Бредбери "Марсианские хроники']
callbacks = ['marsian']



async def create_list_authors(arg: list[str]) -> InlineKeyboardMarkup:
    names, callbacks = await get_names_book(), await get_callbacks_book()
    data = _to_dict(arg1=names, arg2=callbacks)
    authors_kb = InlineKeyboardBuilder()

    for name, callback in data.items():
        authors_kb.row(
            InlineKeyboardButton(text=name, callback_data=callback)
        )
    return authors_kb.as_markup()






