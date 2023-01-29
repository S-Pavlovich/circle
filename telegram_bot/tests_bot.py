import config
import telebot
from telebot import types
import time
from DWH.views import user_search, add_new_user, add_birthdate, timezone_check, get_timezone, add_timezone_db, notice_check, user_set_time
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from notifiers import get_notifier

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    message = f'Привет, {m.from_user.first_name}, сейчас проверю есть ли у меня информация по твоим дням'
    bot.send_message(m.chat.id, message)
    if user_search(m.from_user.id) == 'Old user':
        bot.send_message(m.chat.id, 'Все отлично, можно продолжать вести статистику')
    else:
        add_new_user(m.from_user.username, m.from_user.id, m.from_user.first_name, m.from_user.last_name)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да, давай")
        btn2 = types.KeyboardButton("Нет, не сейчас")
        markup.add(btn1, btn2)
        bot.send_message(m.chat.id, 'Как насчет небольшого знакомства для того чтобы узнать друг друга получше?',
                         reply_markup=markup)


@bot.message_handler(commands=["info"])
def info(m, res=False):
    bot.send_message(m.chat.id, m)


@bot.message_handler(commands=["time"])
def time(m, res=False):
    if notice_check(m.from_user.id) == 'Время уведомлений не установлено':
        mesg = bot.send_message(m.chat.id, 'Напиши время в формате "xx.xx" для оповещения в конце дня')
        bot.register_next_step_handler(mesg, add_notice_time)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Оставить текущее время")
        btn2 = types.KeyboardButton("Изменить время уведомлений")
        markup.add(btn1, btn2)
        bot.send_message(m.chat.id, f'Текущее время уведомлений - {notice_check(m.from_user.id)}', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def func(m, res=False):
    if m.text == "Да, давай":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("Указать дату")
        btn4 = types.KeyboardButton("Пропустить шаг")
        markup.add(btn3, btn4)
        bot.send_message(m.chat.id, 'Укажи свою дату рождения', reply_markup=markup)
    elif m.text == "Нет, не сейчас":
        mesg_tz = bot.send_message(m.chat.id, 'Напиши свой город, для определения часового пояса')
        bot.register_next_step_handler(mesg_tz, add_timezone)
    elif m.text == "Пропустить шаг":
        mesg_tz = bot.send_message(m.chat.id, 'Напиши свой город, для определения часового пояса')
        bot.register_next_step_handler(mesg_tz, add_timezone)
    elif m.text == "Указать дату":
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(m.chat.id, f"Select {LSTEP[step]}",
                         reply_markup=calendar)
        mesg = bot.send_message(m.chat.id, 'Напиши свой город, для определения часового пояса')
        bot.register_next_step_handler(mesg, add_timezone)
        # вылезает если выбрать сначала город потом дату
    elif m.text == "Изменить время уведомлений":
        mesg = bot.send_message(m.chat.id, 'Напиши время в формате "xx.xx" для оповещения в конце дня')
        bot.register_next_step_handler(mesg, add_notice_time)


def add_timezone(m, res=False):
    if timezone_check(m.from_user.id) == 'Часовой пояс не установлен':
        user_timezone = str(get_timezone(m.text))
        user_timezone_split = str(get_timezone(m.text)).split()
        if user_timezone == 'Нет такого города':
            error_city = bot.send_message(m.chat.id, 'Не удалось найти такой город. Попробуйте написать его название '
                                                     'латиницей или указать более крупный город поблизости.')
            bot.register_next_step_handler(error_city, add_timezone)
        else:
            bot.send_message(m.chat.id,
                             f"Часовой пояс установлен в {user_timezone_split[0]} ({user_timezone_split[1]}s от GMT).")
            add_timezone_db(m.from_user.id, get_timezone(m.text)[0], get_timezone(m.text)[1])
            # переход на time


def add_notice_time(m, res=False):
    user_set_time(m.from_user.id, m.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Оставить текущее время")
    btn2 = types.KeyboardButton("Изменить время уведомлений")
    markup.add(btn1, btn2)
    bot.send_message(m.chat.id, f'Время уведомлений установлено на {user_set_time(m.from_user.id, m.text)}',
                     reply_markup=markup)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)
        add_birthdate(c.from_user.id, result)


bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
    bot.infinity_polling()
