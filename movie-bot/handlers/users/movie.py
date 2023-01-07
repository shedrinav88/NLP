import logging
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loader import dp
from states.main import MainStates

from utils.kinopoisk_search import KinopoiskType, search_kinopoisk
from utils.data_cleaner import clean_inp, is_num
from .start import movie_phrases
from .start import actor_phrases

logger = logging.getLogger(__name__)


@dp.message_handler(lambda message: (any(e in clean_inp(message.text).split(" ") for e in movie_phrases)), state="*")
async def movie(message: Message):
    logger.info(f'User @{message.chat.username} requested a movie')
    await MainStates.askedForMovie.set()
    await message.bot.send_message(message.chat.id, "Напиши частично или полностью название фильма, я поищу")


# Find a movie by name
@dp.message_handler(state=MainStates.askedForMovie)
async def process_movie(message: Message, state: FSMContext):
    logger.info(f'User @{message.chat.username} is searching for "{message.text}"')
    await MainStates.askedForMovie.set()
    movies = (await search_kinopoisk(KinopoiskType.search_film, message.text.lower()))["docs"]
    async with state.proxy() as data:
        data['movies'] = movies
    logger.info(f'Got {len(movies)} results from kinopoisk')
    msg = "Ничего не найдено"
    if len(movies) == 1:
        msg = f"Название: {movies[0]['name']}\nОписание: {movies[0]['description']}"
        await message.bot.send_photo(message.chat.id, movies[0]["poster"]["url"])
    elif len(movies) > 1:
        msg = f"Вот {len(movies)} самых популярных фильмов по вашему запросу\n\n"
        for i, el in enumerate(movies):
            msg += f'{i + 1} {el["name"]}\n'
        msg += "\nЧтобы получить подробную информацию о фильме, отправьте его номер"
    await MainStates.foundMovies.set()
    await message.bot.send_message(message.chat.id, msg)


# Show movie details
@dp.message_handler(lambda message: (is_num(message.text)), state=MainStates.foundMovies)
async def process_movie_details(message: Message, state: FSMContext):
    logger.info(f'User @{message.chat.username} asked for details for movie #{message.text}')
    num = int(message.text) - 1
    if num < 0 or num > 10:
        await message.bot.send_message(message.chat.id, "Введите номер от 1 до 10")
        return
    async with state.proxy() as data:
        movies = data['movies']
        msg = f'{movies[num]["description"]}\n\n' \
              f'Рейтинг Кинопоиска: {movies[num]["rating"]["kp"] if movies[num]["rating"]["kp"] > 0 else "нет информации"}\n' \
              f'Рейтинг IMDB: {movies[num]["rating"]["imdb"] if movies[num]["rating"]["imdb"] else "нет информации"}'
        # await MainStates.shownMovieDetails.set()
        await MainStates.initial.set()
        await message.bot.send_photo(message.chat.id, movies[num]["poster"]["url"])
        await message.bot.send_message(message.chat.id, msg)

@dp.message_handler(lambda message: (any(e in message.text.lower().split(" ") for e in actor_phrases)), state="*")
async def actor(message: Message):
    logger.info(f'User @{message.chat.username} requested to find an actor')
    await MainStates.askedForActor.set()
    await message.bot.send_message(message.chat.id, "Напиши имя актёра/актрисы, я поищу")


# Find actors by name
@dp.message_handler(state=MainStates.askedForActor)
async def process_actor(message: Message, state: FSMContext):
    logger.info(f'User @{message.chat.username} is searching for actor "{message.text}"')
    actors = (await search_kinopoisk(KinopoiskType.search_actors, message.text.lower()))["docs"]
    async with state.proxy() as data:
        data['actors'] = actors
    logger.info(f'Got {len(actors)} results from kinopoisk')
    msg = "Ничего не найдено"
    if len(actors) > 0:
        msg = ""
    for i, el in enumerate(actors):
        msg += f'{i + 1} {el["name"]}\n'
    msg += "\nЧтобы получить подробную информацию об актёре/актрисе, отправьте его номер"
    await MainStates.foundActors.set()
    await message.bot.send_message(message.chat.id, msg)

# Show actor details
@dp.message_handler(lambda message: (is_num(message.text)), state=MainStates.foundActors)
async def process_actor_details(message: Message, state: FSMContext):
    logger.info(f'User @{message.chat.username} asked for details for actor #{message.text}')
    num = int(message.text) - 1
    if num < 0 or num > 10:
        await message.bot.send_message(message.chat.id, "Введите номер от 1 до 10")
        return
    async with state.proxy() as data:
        actors = data['actors']
        r = await search_kinopoisk(KinopoiskType.get_actor, actors[int(message.text.lower()) - 1]["id"])

        msg = f'{r["name"]} ({r["enName"]})\nПол: {r["sex"]}\n' \
              f'Профессии: {", ".join([x["value"] for x in r["profession"]])}\n' \
              f'Место рождения: {", ".join([x["value"] for x in r["birthPlace"]])} '

        await MainStates.initial.set()
        if r["photo"]:
            await message.bot.send_photo(message.chat.id, r["photo"])
        await message.bot.send_message(message.chat.id, msg)
