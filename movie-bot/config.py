import os
from environs import Env

env = Env()
env.read_env()

telegram_token = env.str("telegram_token")
weather_token = env.str("weather_token")
kinopoisk_token = env.str("kinopoisk_token")
dialogflow_project_id = env.str("dialogflow_project_id")
dialogflow_lang_code = env.str("dialogflow_lang_code")
dialogflow_session_id = env.str("dialogflow_session_id")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'tg-bot-qofj-209f87d5a832.json'
