import config
import logging

from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from loader import dp
from states.main import MainStates
from google.cloud import dialogflow

from utils.data_cleaner import clean_inp

logger = logging.getLogger(__name__)


@dp.message_handler(Command("start"), state="*")
async def start(message: Message):
    logger.info(f'User @{message.chat.username} opened /start')
    msg = """
    👋 Привет!
    Я могу дать информацию о фильмах, актёрах или узнать прогноз погоды. С чего начнём?
    """
    await MainStates.initial.set()
    await message.bot.send_message(message.chat.id, msg)


greetings_phrases = ["привет", "здравствуйте", "добрый день", "доброе утро", "добрый вечер", "здорово", "здоров"]
movie_phrases = ["фильм", "кино", "фильмец", "фильмы", "фильме", "фильму"]
actor_phrases = ["актер", "актёр", "актриса", "актера", "актёра", "актрисой", "актером", "актёром", "актрисой", "актеры"]
weather_phrases = ["погода", "погоды", "погодка", "погоду", "температура", "температуру"]


async def get_answer_dialogflow(message: str):
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(config.dialogflow_project_id, config.dialogflow_session_id)
        text_input = dialogflow.TextInput(text=message, language_code=config.dialogflow_lang_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        res = response.query_result.fulfillment_text
        return res if res else "Перефразируй, пожалуйста, я не понял..."
    except Exception as err:
        logger.error(f"Can't get response from Dialogflow. {err}")
        return "Can't get response from Dialogflow"


@dp.message_handler(lambda message: (message.text.lower() in greetings_phrases and not message.text in movie_phrases),
                    state=MainStates.initial)
async def process_hello(message: Message):
    logger.info(f'User @{message.chat.username} said "{message.text}"')
    msg = "Привет!"
    await message.bot.send_message(message.chat.id, msg)


@dp.message_handler(
    lambda message: (
            not any(
                e in clean_inp(message.text).split(" ") for e in
                movie_phrases + greetings_phrases + actor_phrases + weather_phrases)),
    state=MainStates.initial)
async def process_dialogflow(message: Message):
    logger.info(f'User @{message.chat.username} said "{message.text}"')
    reply = await get_answer_dialogflow(message.text)
    logger.info(f'Bot answered to @{message.chat.username}: "{reply}"')
    await message.bot.send_message(message.chat.id, reply)
