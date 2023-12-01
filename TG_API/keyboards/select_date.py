from TG_API.botTG import bot
from loguru import logger
import datetime
from TG_API.states.user_states import UserInputState
from TG_API.keyboards.calendar_telebot import CallbackData, Calendar, check_month_day
from TG_API.handlers.custom_handlers import default_call_func
from telebot.types import CallbackQuery


calendar = Calendar()
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def input_date(call: CallbackQuery) -> None:
    """
    Пользователь нажал какую то кнопку на календаре. Если это кнопка какого-то определенного
    дня, то сравниваем эту дату с сегодняшним днём. Дата заезда должна быть либо сегодня, либо
    любой последующий день. А дата выезда не может быть меньше, либо равна, дате заезда.
    : param call : CallbackQuery нажатие на кнопку получения даты в календаре.
    """
    name, action, year, month, day = call.data.split(calendar_callback.sep)
    calendar.calendar_query_handler(
        bot=bot,
        call=call,
        name=name,
        action=action,
        year=year,
        month=month,
        day=day
    )

    if action == 'DAY':
        logger.info(f'Выбрана какая-то дата, нужно ее проверить. User_id: {call.message.chat.id}')
        month = check_month_day(month)
        day = check_month_day(day)
        select_date = year + month + day

        now_year, now_month, now_day = datetime.datetime.now().strftime('%Y.%m.%d').split('.')
        now = now_year + now_month + now_day

        bot.set_state(call.message.chat.id, UserInputState.input_date)
        with bot.retrieve_data(call.message.chat.id) as data:
            if 'checkInDate' in data:
                checkin = int(data['checkInDate']['year'] + data['checkInDate']['month'] + data['checkInDate']['day'])
                if int(select_date) > checkin:
                    logger.info(f'Ввод и сохранение даты выезда. User_id: {call.message.chat.id}')
                    data['checkOutDate'] = {'day': day, 'month': month, 'year': year}
                    # далее две переменные-заглушки, чтобы не было ошибки при получении словаря с отелями
                    data['landmark_in'] = 0
                    data['landmark_out'] = 0

                    bot.send_message(call.message.chat.id, f'Дата заезда: {data["checkInDate"]["day"]}.'
                                                           f'{data["checkInDate"]["month"]}.'
                                                           f'{data["checkInDate"]["year"]}\n'
                                                           f'Дата выезда: {data["checkOutDate"]["day"]}.'
                                                           f'{data["checkOutDate"]["month"]}.'
                                                           f'{data["checkOutDate"]["year"]}'
                                     )
                    bot.set_state(call.message.chat.id, UserInputState.quantity_hotels)
                    bot.send_message(call.message.chat.id, 'Сколько нужно вывести карточек отелей (от 1 до 20)?')

                else:
                    bot.send_message(call.message.chat.id, 'Дата выезда должна быть больше даты заезда! '
                                                           'Повторите выбор даты!')
                    default_call_func.my_calendar(call.message, 'выезда')
            else:
                logger.info(f'Ввод и сохранение даты заезда. User_id: {call.message.chat.id}')
                data['checkInDate'] = {'day': day, 'month': month, 'year': year}
                default_call_func.my_calendar(call.message, 'выезда')

