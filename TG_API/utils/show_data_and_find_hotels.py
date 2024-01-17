import database.add_bd
from TG_API.botTG import bot
from telebot.types import Message, Dict, InputMediaPhoto
from loguru import logger
from TG_API.states.user_states import UserInputState
from site_API.core import HotelCore


def request_and_output(message: Message, data: Dict) -> None:
    logger.info(
        f"Сбор данных. User_id: {message.chat.id}"
    )  # здесь начинается классический блок по сбору инф-ции
    data_arrival = (f"{str(data['checkInDate']['year'])}-{str(data['checkInDate']['month'])}-"
                    f"{str(data['checkInDate']['day'])}")
    data_departure = (f"{str(data['checkOutDate']['year'])}-{str(data['checkOutDate']['month'])}-"
                      f"{str(data['checkOutDate']['day'])}")

    logger.info(f"Делается запрос с данными. User_id: {message.chat.id}")
    response = HotelCore.hotels()
    response = response(
        data["dest_id"],
        data_arrival,
        data_departure,
        data['price_min'],
        data['price_max'],
        int(data['quantity_hotels'])
    )

    database.add_bd.add_query(data)

    if response == "Error":
        logger.info(f"Ошибка ввода данных. User_id: {message.chat.id}")

    elif response == "empty":
        logger.info(f"По запросу пользователя нет отелей. User_id: {message.chat.id}")
        bot.send_message(message.chat.id, 'По вашему запросу ничего не найдено')

    else:
        logger.info(f"Успешно. Вывод данных в чат. User_id: {message.chat.id}")

        for answer in response:

            medias = []
            id_hotel = response[answer]["id_hotel"]
            description = response[answer]["description"]
            url = response[answer]["url"]
            photo_list = response[answer]["photo"]

            data_to_db = {
                id_hotel: {
                    'description': description, 'url': url, 'photo_list': photo_list, 'date_time': data['date_time'],
                    'user_id': message.chat.id
                }
            }
            database.add_bd.add_response(data_to_db)

            caption = (f"ID отеля: {id_hotel}\nОписание отеля: {description}"
                       f"\nСсылка на отель: {url}")

            for number, url in enumerate(photo_list):
                if number == 0:
                    medias.append(InputMediaPhoto(media=url, caption=caption))
                else:
                    medias.append(InputMediaPhoto(media=url))

            bot.send_media_group(message.chat.id, medias)
