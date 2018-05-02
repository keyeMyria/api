from telepot import Bot
from .models import User
from django.conf import settings
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
# ReplyKeyboardMarkup
# from functools import wraps


def no_debug(func):
    def func_wrapper(msg):
        if settings.DEBUG:
            print('Telegram notifications are disabled in DEBUG mode.')
        else:
            func(msg)
    # def tags_decorator(func):
    #     @wraps(func)
    #     def func_wrapper(name):
    #         return "<{0}>{1}</{0}>".format(tag_name, func(name))

    return func_wrapper
    # return tags_decorator


@no_debug
def superusers(msg):
    users = User.objects.filter(
        is_superuser=True,
        telegram_chat_id__isnull=False,
    )
    bot = Bot(settings.TELEGRAM_TOKEN)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Опубликовать', callback_data='publish'),
            InlineKeyboardButton(text='Пропустить', callback_data='skip'),
            InlineKeyboardButton(text='Спам', callback_data='spam'),
        ],
    ])

    # bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

    for user in users:
        bot.sendMessage(
            user.telegram_chat_id,
            msg,
            reply_markup=keyboard,
        )
