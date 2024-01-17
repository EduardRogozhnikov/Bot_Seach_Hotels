import sqlite3
from loguru import logger
from TG_API.config_data import config


def read_query(user: int) -> list:
    """
        Принимает id пользователя, делает запрос к базе данных, получает в ответ
        результаты запросов данного пользователя.
        : param user : int
        : return : list
    """
    logger.info(f'Читаем таблицу query. User_id: {user}')
    connect = sqlite3.connect("SB_bot.bd")
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT `id`, `date_time`, `input_city`, `dest_id` FROM query WHERE `user_id` = ?",
                       (user,))
        records = cursor.fetchall()
        connect.close()
        return records
    except sqlite3.OperationalError:
        logger.info(f"В базе данных пока нет таблицы с запросами. User_id: {user}")
        return []


def get_history_response(message) -> dict:
    """
       Принимает id-запроса, обращается к базе данных и выдает данные которые нашел бот для
       пользователя по его запросам.
       : param query : str
       : return : dict
    """
    logger.info(f'Читаем таблицу response. User_id: {message.chat.id}')
    connect = sqlite3.connect("SB_bot.bd")
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT * FROM response WHERE `query_id` = ?", (message.text,))
        records = cursor.fetchall()
        history = {}
        for item in records:
            id_hotel = item[2]
            history[item[2]] = {'description': item[3], 'url': item[4]}
            cursor.execute("SELECT * FROM images WHERE `id_hotel` = ?", (id_hotel, ))
            images = cursor.fetchall()
            links = []
            for link in images:
                links.append(link[2])
            history[item[2]]['images'] = links
        connect.close()
        return history
    except sqlite3.OperationalError:
        logger.info(f"В базе данных пока нет таблицы с запросами. User_id: {message.chat.id}")
        return {}
