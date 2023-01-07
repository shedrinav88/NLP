import logging
from aiogram import Dispatcher
from aiogram.types import AllowedUpdates
from aiogram.utils import executor
from utils.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


async def startup(dp: Dispatcher):
    await set_default_commands(dp)

if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, on_startup=startup, allowed_updates=AllowedUpdates.all())
