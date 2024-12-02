import asyncio

import aiosqlite

path = 'database/database.db'

async def create_table_of_books():
    async with aiosqlite.connect(path) as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                callback TEXT NOT NULL
            )
        ''')
        await conn.commit()

async def add_book(name: str, callback: str):
    async with aiosqlite.connect(path) as conn:
        await conn.execute('INSERT INTO Books (name, callback) VALUES (?, ?)', (name, callback))
        await conn.commit()

async def get_name_book(callback: str):
    async with aiosqlite.connect(path) as conn:
        name = await conn.execute('SELECT name FROM Books WHERE callback = ?', (callback,))
        return await name.fetchone()

async def get_names_book():
    async with aiosqlite.connect(path) as conn:
        names = await (await conn.execute('SELECT name FROM Books')).fetchall()
        res = [''.join(name) for name in names]
        return res

async def get_callback_book(name: str):
    async with aiosqlite.connect(path) as conn:
        callback = await conn.execute('SELECT callback FROM Books WHERE name = ?', (name,))
        return await callback.fetchone()

async def get_callbacks_book():
    async with aiosqlite.connect(path) as conn:
        callbacks = await (await conn.execute('SELECT callback FROM Books')).fetchall()
        res = [''.join(callback) for callback in callbacks]
        return res

async def create_table_and_insert_data(tg_id: int):
    # Подключаемся к базе данных
    async with aiosqlite.connect(path) as conn:
        # Создаем таблицу если она не существует
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                page INTEGER NOT NULL,
                bookmarks TEXT,
                book_path TEXT NOT NULL
            )
        ''')

        # Вставляем данные в таблицу
        user_dict_template = {
            'page': '1',
            'bookmarks': set(),  # Преобразуем set в строку для хранения в БД
            'book_path': 'D:/pyProjects/book_bot/books/'
        }

        # Преобразуем set в строку для хранения в БД
        bookmarks_str = ','.join(map(str, user_dict_template['bookmarks']))

        await conn.execute("INSERT INTO Users (tg_id, page, bookmarks, book_path) VALUES (?, ?, ?, ?)",
                           (tg_id, user_dict_template['page'], bookmarks_str, user_dict_template['book_path']))


        # Сохраняем изменения
        await conn.commit()
async def beginning(tg_id: int):
    async with aiosqlite.connect(path) as conn:
        await conn.execute('UPDATE Users SET page = 1 WHERE tg_id = ?', (tg_id,))
        await conn.commit()


async def set_book(tg_id: int, book_path: str):
    async with aiosqlite.connect(path) as conn:
        await conn.execute('UPDATE Users SET book_path = ? WHERE tg_id = ?', (book_path, tg_id,))
        await conn.commit()

async def get_book_path(tg_id: int):
    async with aiosqlite.connect(path) as conn:
        bp = await conn.execute('SELECT book_path FROM Users WHERE tg_id = ?', (tg_id,))
        return ''.join((await bp.fetchone()))

async def get_page(tg_id: int):
    async with aiosqlite.connect(path) as conn:
        p = await conn.execute('SELECT page FROM Users WHERE tg_id = ?', (tg_id,))
        return (await p.fetchone())[0]

async def add_page(tg_id: int, count: int):
    async with aiosqlite.connect(path) as conn:
        await conn.execute('UPDATE Users SET page = page + ? WHERE tg_id = ?', (count, tg_id,))
        await conn.commit()

async def get_bookmarks(tg_id: int):
    async with aiosqlite.connect(path) as conn:
        bookmarks_set = set()
        bookmarks = (await (await conn.execute('SELECT bookmarks FROM Users WHERE tg_id = ?', (tg_id,))).fetchone())[0]
        for bookmark in sorted(bookmarks.split(' ')):
            bookmarks_set.add(bookmark)
        return sorted(bookmarks_set)

async def add_bookmarks(tg_id: int, page):
    async with aiosqlite.connect(path) as conn:
        bookmarks = await get_bookmarks(tg_id=tg_id)
        bookmarks.append(page)
        bookmarks_str = ' '.join(map(str, bookmarks)).strip()

        await conn.execute('UPDATE Users SET bookmarks = ? WHERE tg_id = ?', (bookmarks_str, tg_id,))
        await conn.commit()

async def edit_bookmarks(tg_id: int, callback: str):
    async with aiosqlite.connect(path) as conn:
        bookmarks = await get_bookmarks(tg_id=tg_id)
        bookmarks.remove(callback[:-3])
        bookmarks_str = ' '.join(bookmarks)

        await conn.execute('UPDATE Users SET bookmarks = ? WHERE tg_id = ?', (bookmarks_str, tg_id,))
        await conn.commit()