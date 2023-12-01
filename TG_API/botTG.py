from settings import SiteSettings
from telebot import TeleBot
from telebot.storage import StateMemoryStorage


site = SiteSettings()
token = site.token_bot.get_secret_value()
storage = StateMemoryStorage()


bot = TeleBot(token, state_storage=storage)

