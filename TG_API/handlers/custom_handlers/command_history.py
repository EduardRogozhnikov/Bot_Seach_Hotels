from TG_API.botTG import bot
from telebot.types import Message, InputMediaPhoto
from loguru import logger
import database
from TG_API.states.user_states import UserInputState


@bot.message_handler(commands=['history'])
def get_list_history(message: Message) -> None:
    """
        Обработчик команд, срабатывает на команду /history
        Обращается к базе данных и выдает в чат запросы пользователя
        по отелям.
        : param message : Message
        : return : None
    """
    logger.info(f'Выбрана команда history! User_id: {message.chat.id}')
    queries = database.read_bd.read_query(message.chat.id)
    if queries:
        logger.info(f'Получены записи из таблицы query:\n {queries}. User_id: {message.chat.id}')
        for item in queries:
            bot.send_message(message.chat.id, f"({item[0]}). Дата и время: {item[1]}. Вы вводили город: {item[2]}")
        bot.set_state(message.chat.id, UserInputState.select_number)
        bot.send_message(message.from_user.id, "Введите номер интересующего вас варианта: ")
    else:
        bot.send_message(message.chat.id, 'В базе данных пока нет записей')


@bot.message_handler(state=UserInputState.select_number)
def input_number(message: Message) -> None:
    """
        Ввод пользователем номера запроса, которые есть в списке. Если пользователь введет
        неправильный номер или это будет "не цифры", то бот попросит повторить ввод.
        Запрос к базе данных нужных нам записей. Выдача в чат результата.
        : param message : Message
        : return : None
    """
    if message.text.isdigit():
        queries = database.read_bd.read_query(message.chat.id)
        number_query = []
        for item in queries:
            number_query.append(item[0])

        if int(message.text) in number_query:
            logger.info(f"Посылаем запрос к базе данных. User_id: {message.chat.id}")
            history_dict = database.read_bd.get_history_response(message)
            with bot.retrieve_data(message.chat.id) as data:
                data.clear()
            if history_dict:
                logger.info(f'Выдаем результаты выборки из базы данных. User_id: {message.chat.id}')
                for hotel in history_dict.items():
                    medias = []
                    caption = f"ID отеля: {hotel[0]}]\nОписание отеля: {hotel[1]['description']}" \
                              f"\nСсылка на отель: {hotel[1]['url']}"
                    urls = hotel[1]['images']
                    for number, url in enumerate(urls):
                        if number == 0:
                            medias.append(InputMediaPhoto(media=url, caption=caption))
                        else:
                            medias.append(InputMediaPhoto(media=url))
                    bot.send_media_group(message.chat.id, medias)
            else:
                bot.send_message(message.chat.id, "Почему-то ответ пуст! Попробуйте другие операции.")
                logger.info(f'Почему-то ответ пуст! User_id: {message.chat.id}')
        else:
            bot.send_message(message.chat.id, 'Ошибка! Вы ввели число, которого нет в списке! Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')
    bot.set_state(message.chat.id, None)
