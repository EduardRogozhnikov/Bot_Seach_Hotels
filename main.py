from TG_API.botTG import bot
import TG_API.handlers
from telebot.custom_filters import StateFilter
from TG_API.set_bot_command import set_default_commands

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling(none_stop=True, interval=0)


