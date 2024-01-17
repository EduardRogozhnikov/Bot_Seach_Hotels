from TG_API.botTG import bot
from telebot.types import Message
from loguru import logger
from TG_API.states.user_states import UserInputState
from TG_API.keyboards.calendar_telebot import Calendar
from site_API.utils.seach_hotels import SiteApiInterface
from TG_API.utils.show_data_and_find_hotels import request_and_output


@bot.message_handler(state=UserInputState.input_city)
def input_sity(message: Message) -> None:
    """
    Здесь обрабатывается информация о городе, который ввел пользователь. При успешном запросе достаем и записываем
    id города.

    :param message: Message
    :return: None
    """

    with bot.retrieve_data(message.chat.id) as data:
        data['input_city'] = message.text
        logger.info('Пользователь ввел город: ' + message.text + f' User_id: {message.chat.id}')
        logger.info(f"Делаем запрос, проверяем на ошибку. User_id: {message.chat.id}")
        response = SiteApiInterface.seach_city_requests()
        response = response(message.text)
        dest_id = response
        if dest_id == "Error" or len(dest_id["data"]) == 0:
            logger.info(f"Ошибка ввода. User_id: {message.chat.id}")
            bot.send_message(message.chat.id, "Ошибка ввода, повторите ввод!")

        else:
            dest_id = dest_id["data"][0]["dest_id"]

            logger.info(f"Проверка прошла успешно. ID-города: {dest_id}, User_id: {message.chat.id}")
            data['dest_id'] = dest_id

            my_calendar(message, 'заезда')


@bot.message_handler(state=UserInputState.quantity_hotels)
def quantity_hotels(message: Message) -> None:
    """
    Здесь сохраняем информацию количества отелей, нужное пользователю, а также
    проверяем, чтобы количество было в диапазоне от 1 до 20.

    :param message: Message
    :return: None
    """

    if message.text.isdigit():
        if 0 < int(message.text) <= 20:
            logger.info('Ввод и запись количества отелей: ' + message.text + f' User_id: {message.chat.id}')
            with bot.retrieve_data(message.chat.id) as data:
                data['quantity_hotels'] = message.text

                if data["command"] == "/highprice" or data["command"] == "/custom":
                    bot.set_state(message.chat.id, UserInputState.priceMin)
                    bot.send_message(message.chat.id, 'Введите минимальную стоимость отеля (в USD)')

                else:
                    bot.set_state(message.chat.id, UserInputState.priceMax)
                    bot.send_message(message.chat.id, 'Введите максимальную стоимость отеля (в USD)')
        else:
            bot.send_message(message.chat.id, 'Ошибка! Это должно быть число в диапазоне от 1 до 25! Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputState.priceMin)
def priceMin(message: Message) -> None:
    """
    Здесь сохраняем информацию о минимальной стоимости отеля и проверяем, чтобы это было число.

    :param message: Message
    :return: None
    """

    if message.text.isdigit():
        logger.info('Ввод и запись минимальной стоимости отеля: ' + message.text + f' User_id: {message.chat.id}')
        with bot.retrieve_data(message.chat.id) as data:
            data['price_min'] = message.text

            if data['command'] == "/custom":
                bot.set_state(message.chat.id, UserInputState.priceMax)
                bot.send_message(message.chat.id, 'Введите максимальную стоимость отеля (в USD)')

            else:
                request_and_output(message, data)
                bot.set_state(message.chat.id, None)
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputState.priceMax)
def priceMax(message: Message) -> None:
    """
    Здесь сохраняем информацию о максимальной стоимости отеля и проверяем, чтобы это было число.

    :param message: Message
    :return: None
    """

    if message.text.isdigit():
        logger.info('Ввод и запись максимальной стоимости отеля: ' + message.text + f' User_id: {message.chat.id}')
        with bot.retrieve_data(message.chat.id) as data:
            data['price_max'] = message.text
            request_and_output(message, data)
            bot.set_state(message.chat.id, None)

    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state="*", commands=['cancel'])
def any_state(message: Message):
    """
    Cancel state
    """
    logger.info(f"Выход из state. User_id: {message.chat.id}")
    bot.send_message(message.chat.id, f"<b><i>Отмена команды. Введите команду</i></b> \U0001F423", parse_mode="HTML")
    bot.delete_state(message.from_user.id, message.chat.id)


bot_calendar = Calendar()


def my_calendar(message: Message, word: str) -> None:
    """
    Запуск инлайн-клавиатуры (календаря) для выбора дат заезда и выезда
    : param message : Message
    : param word : str слово (заезда или выезда)
    : return : None
    """
    logger.info(f'Вызов календаря {word}. User_id: {message.chat.id}')
    bot.send_message(message.chat.id, f'Выберите дату: {word}',
                     reply_markup=bot_calendar.create_calendar(), )


