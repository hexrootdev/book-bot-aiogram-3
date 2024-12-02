import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import other_handlers, choice_author, user_handlers, admin
from keyboards.main_menu import set_main_menu

from config_reader import config

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('Starting bot...')
    bot = Bot(token=config.bot_token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    await set_main_menu(bot)
    dp.include_routers(user_handlers.router, choice_author.router, admin.router, other_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
