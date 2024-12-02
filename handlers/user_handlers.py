from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from database.core_database import beginning, get_page, add_page, get_bookmarks, add_bookmarks, edit_bookmarks, create_table_and_insert_data, get_book_path, create_table_of_books

from filters import IsDelBookmarkCallbackData, IsDigitCallbackData

from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard

from services.functions import book, prepare_book

from lexicon import LEXICON


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id

    await create_table_and_insert_data(tg_id=user_id)
    await create_table_of_books()

    await message.answer(LEXICON[message.text])


@router.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer(LEXICON[message.text])

@router.message(Command('beginning'))
async def beggining_cmd(message: Message):
    user_id = message.from_user.id
    path = await get_book_path(tg_id=user_id)
    print(path)
    prepare_book(path)
    page = await get_page(tg_id=user_id)
    await beginning(tg_id=user_id)

    await message.answer(
        text=book[page],
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{page}/{len(book)}',
            'forward'
        )
    )

@router.message(Command('continue'))
async def continue_cmd(message: Message):
    user_id = message.from_user.id
    page = await get_page(tg_id=user_id)


    try:
       text = await get_page(tg_id=user_id)
    except KeyError:
        await message.answer(LEXICON['continue_without_reading'])

    await message.answer(
        text=book[page],
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{page}/{len(book)}',
            'forward'
        )
    )

@router.message(Command('bookmarks'))
async def bookmarks_cmd(message: Message):
    user_id = message.from_user.id
    bookmarks = ''.join(await get_bookmarks(tg_id=user_id))
    if bookmarks:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(bookmarks)
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'forward')
async def forward_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    page = await get_page(tg_id=user_id)

    if page < len(book):
        await add_page(tg_id=user_id, count=1)
        text = book[page]
        page = await get_page(tg_id=user_id)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{page}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()

@router.callback_query(F.data == 'backward')
async def backward_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    page = await get_page(tg_id=user_id)

    if page > 1:
        await add_page(tg_id=user_id, count=-1)
        text = book[page]
        page = await get_page(tg_id=user_id)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{page}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()

@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def page_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    page = await get_page(tg_id=user_id)

    await add_bookmarks(tg_id=user_id, page=page)
    await callback.answer('Страница добавлена в закладки!')

@router.callback_query(IsDigitCallbackData())
async def bookmark_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    page = await get_page(tg_id=user_id)

    text = book[int(callback.data)]
    await add_page(tg_id=user_id, count=int(callback.data)-page)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
             f'{page}/{len(book)}',
            'forward'
        )
    )

@router.callback_query(F.data == 'edit_bookmarks')
async def edit_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    bookmarks = ''.join(await get_bookmarks(tg_id=user_id))

    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(bookmarks))

@router.callback_query(F.data == 'cancel')
async def cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])

@router.callback_query(IsDelBookmarkCallbackData())
async def del_bookmark_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    await edit_bookmarks(tg_id=user_id, callback=callback.data)
    bookmarks = ''.join(await get_bookmarks(tg_id=user_id))

    if bookmarks:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(bookmarks)
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])


















