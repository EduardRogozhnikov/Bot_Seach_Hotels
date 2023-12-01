from TG_API.botTG import bot
from telebot.types import Message
from loguru import logger
import datetime
from TG_API.states.user_states import UserInputState


@bot.message_handler(commands=['lowprice', 'highprice', 'custom'])
def states_command(message: Message) -> None:
    """
    Обрабатывает команды /lowprice, /highprice, /custom. Здесь начинаются state.
    :param message: Message
    :return: None
    """

    bot.set_state(message.chat.id, UserInputState.command)
    with bot.retrieve_data(message.chat.id) as data:
        data.clear()
        logger.info('Запоминаем выбранную команду: ' + message.text + f" User_id: {message.chat.id}")
        data['command'] = message.text
        data['date_time'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        data['chat_id'] = message.chat.id
        if data['command'] == '/lowprice':
            data['price_min'] = None
        elif data['command'] == '/highprice':
            data['price_max'] = None

    bot.set_state(message.chat.id, UserInputState.input_city)
    bot.send_message(message.from_user.id, "Введите город в котором нужно найти отель: ")

