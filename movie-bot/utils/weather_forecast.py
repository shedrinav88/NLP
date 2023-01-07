import config
import logging
from aiohttp import ClientSession, TCPConnector
from datetime import datetime

logger = logging.getLogger(__name__)


async def get_weather_forecast(city_name: str) -> str:
    try:
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as sess:
            resp = await sess.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={config.weather_token}")
            res_weather = await resp.json()
            temp_min = int(res_weather['main']['temp_min'] - 273)  # перевод из градусов Кельвина в Цельсия
            temp_max = int(res_weather['main']['temp_max'] - 273)
            wind_speed = res_weather['wind']['speed']
            print('5')
            # вспомогательная функция для вывода даты
            date = datetime.now().date()

            def get_month(date):
                months_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                               'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
                return months_list[date.month - 1]  # т.к. индексация с нуля

            logger.info(f'Got weather forcast for "{city_name}"')
            return f'Погода сегодня, {date.strftime(f"%d {get_month(date)} %Y г.")}, в г. {city_name.title()}: \
            \nМинимальная t: {temp_min}°C, максимальная t: {temp_max}°C, скорость ветра: {wind_speed} м/с'
    except Exception as err:
        logger.error(f"Can't get weather forecast. {err}")
        return "Упс, не получилось узнать погоду"
