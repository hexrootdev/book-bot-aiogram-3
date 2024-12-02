import os

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.core_database import get_book_path, set_book, add_book
from keyboards.authors import create_list_authors
from services.functions import prepare_book, book
from keyboards.admin_kbs import create_admin_panel
from filters import IsAdmin
from fsm import adminFSM

from lexicon import LEXICON

router = Router()



@router.message(Command('admin'), IsAdmin())
async def admin_panel(message: Message):
    await message.answer(LEXICON['admin_panel'], reply_markup=create_admin_panel())


@router.message(F.text == '➕Добавить книгу', IsAdmin())
async def adding_book_name(message: Message, state: FSMContext):
    await message.answer(LEXICON['enter_name'])
    await state.set_state(adminFSM.name)


@router.message(adminFSM.name)
async def adding_book_file(message: Message, state: FSMContext):
    name, callback = str(message.text).split('_')

    await state.update_data(name=name)
    await state.update_data(callback=callback)

    await message.answer(LEXICON['send_book_file'])
    await state.set_state(adminFSM.file)


@router.message(adminFSM.file)
async def adding_book(message: Message, state: FSMContext):
    data = await state.get_data()
    name, callback = data['name'], data['callback']
    bot = message.bot

    # Убедитесь, что папка существует
    books_directory = r'D:/pyProjects/book_bot/books/'
    os.makedirs(books_directory, exist_ok=True)

    await message.answer(f'<b>✅Перехватил.\nИмя книги - <em>{name}</em>, callback - <em>{callback}</em></b>')

    try:
        txt = await bot.get_file(message.document.file_id)
        print(txt)

        # Скачиваем файл
        await bot.download_file(txt.file_path, destination=os.path.join(books_directory, callback+'.txt'))
        await message.answer("✅ Файл успешно загружен.")
        await add_book(name=name, callback=callback)

    except Exception as e:
        await message.answer("❌ Ошибка при загрузке файла.")
        print(f"Ошибка: {e}")

    await state.clear()