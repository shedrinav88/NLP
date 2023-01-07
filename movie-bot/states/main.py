from aiogram.dispatcher.filters.state import StatesGroup, State


class MainStates(StatesGroup):
    initial = State()
    askedForMovie = State()
    foundMovies = State()
    shownMovieDetails = State()
    askedForActor = State()
    foundActors = State()
    askedForWeather = State()
