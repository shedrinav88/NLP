import logging
from aiogram.types import Message
from loader import dp
from states.main import MainStates
from utils.data_cleaner import clean_inp
from utils.weather_forecast import get_weather_forecast
from .start import weather_phrases

logger = logging.getLogger(__name__)


@dp.message_handler(lambda message: (any(e in clean_inp(message.text).split(" ") for e in weather_phrases)), state="*")
async def weather(message: Message):
    logger.info(f'User @{message.chat.username} requested a weather forecast')
    await MainStates.askedForWeather.set()
    await message.bot.send_message(message.chat.id, "В каком городе?")


@dp.message_handler(state=MainStates.askedForWeather)
async def get_weather(message: Message):
    logger.info(f'User @{message.chat.username} requested a weather forecast in city "{message.text}"')
    await MainStates.initial.set()
    res = await get_weather_forecast(clean_inp(message.text))
    await message.bot.send_message(message.chat.id, res)