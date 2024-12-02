from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

admin = 7511084146
class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()

class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == admin

