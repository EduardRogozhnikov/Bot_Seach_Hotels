from telebot.handler_backends import State, StatesGroup


class UserInputState(StatesGroup):
    command = State()  # команда, которую выбрал пользователь
    input_city = State()  # город, который ввел пользователь
    quantity_hotels = State()  # количество отелей, нужное пользователю
    input_date = State()  # ввод даты (заезда, выезда)
    priceMin = State()  # минимальная стоимость отеля
    priceMax = State()  # максимальная стоимость отеля
    select_number = State()  # выбор истории поиска
    validation_and_out_data = State()  # проверка данных и вывод их в чат
