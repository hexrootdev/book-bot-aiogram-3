from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database.core_database import get_book_path, set_book
from keyboards.authors import create_list_authors
from services.functions import prepare_book, book
from keyboards.authors import books

from lexicon import LEXICON

router = Router()



@router.message(Command('authors'))
async def choice_book(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=await create_list_authors(arg=books))

@router.callback_query(F.data)
async def get_chosen_book(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer(LEXICON['succesfully_choice'])

    cursor = await get_book_path(tg_id=user_id)
    path = ''.join(cursor)
    path = path[:path.rfind('/')+1]
    path += str(callback.data) + '.txt'
    prepare_book(path)
    await set_book(tg_id=user_id, book_path=path)

    await callback.answer()
