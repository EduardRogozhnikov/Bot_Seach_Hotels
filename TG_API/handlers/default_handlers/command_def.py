from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from loguru import logger
import database.add_bd
from TG_API.botTG import bot
from TG_API.config_data.config import DEFAULT_COMMANDS


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="/help"))

    bot.reply_to(message, f"<b><i>Привет, {message.from_user.full_name}!</i></b> \U0000270C\n"
                          f"Этот бот может подобрать вам отель в любом городе мира (ну почти любом\U0001F440).\n"
                          f"Для того, чтобы бот работал корректно введите одну из доступных команд. "
                          f"Для более подробной информации по командам введите команду /help",
                 parse_mode="HTML",
                 reply_markup=markup)
    database.add_bd.add_user(message)


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))

