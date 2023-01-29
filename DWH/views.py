import os
import re
import time

from IPython.utils.tz import utcnow
from django.utils.timezone import now

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "circle.settings")

import django

django.setup()

from DWH.models import User
import geopy
from tzwhere import tzwhere
import datetime
import pytz
from datetime import time


# Create your views here.


def user_search(x):
    for i in User.objects.all():
        if int(i) == x:
            return 'Old user'


def index_user_search(x):
    for i in User.objects.all():
        if int(i) == x:
            return i.id


def add_new_user(nickname, tg_id, first_name, last_name):
    User(nickname=nickname, telegram_id=tg_id, first_name=first_name, last_name=last_name).save()
    # Не писать данные в бд
    # pass


def add_birthdate(x, birthdate):
    # User(telegram_id=tg_id, date_of_birth=birthdate).save()
    index_user = index_user_search(x) - 44
    # костыль изза бд
    b = User.objects.all()[index_user]
    b.date_of_birth = f'{birthdate}'
    b.save()
    return 'Birthdate added!'


def add_timezone_db(x, city, timezone):
    # User(telegram_id=tg_id, date_of_birth=birthdate).save()
    index_user = index_user_search(x) - 44
    # костыль изза бд
    b = User.objects.all()[index_user]
    b.timezone = timezone
    b.city = city
    b.save()
    return 'Timezone added!'


def get_timezone(city):
    geo = geopy.geocoders.Nominatim(user_agent="SuperMon_Bot")
    location = geo.geocode(city)  # преобразуе
    if location is None:
        return "Нет такого города"
    else:
        tzw = tzwhere.tzwhere()
        timezone_str = tzw.tzNameAt(location.latitude, location.longitude)  # получаем название часового пояса
        tz = pytz.timezone(timezone_str)
        tz_info = datetime.datetime.now(tz=tz).strftime("%z")  # получаем смещение часового пояса
        tz_info = tz_info[0:3] + ":" + tz_info[3:]  # приводим к формату ±ЧЧ:ММ
        # здесь должно быть сохранение выбранной строки в БД
        return timezone_str, tz_info


def timezone_check(x):
    index_user = index_user_search(x) - 44
    # костыль изза бд
    b = User.objects.all()[index_user]
    if b.timezone is not None:
        return b.timezone
    else:
        return 'Часовой пояс не установлен'


def notice_check(x):
    index_user = index_user_search(x) - 44
    # костыль изза бд
    b = User.objects.all()[index_user]
    if b.time_to_notificate is not None:
        return b.time_to_notificate
    else:
        return 'Время уведомлений не установлено'


# время в utc

# локальное время

# часовой пояе


# приводим к формату ±ЧЧ:ММ


# задаю вручную время уведомлений для каждого пользователя
# функцию для записи времени
# mesg = bot.send_message(m.chat.id, 'Напиши время в формате 'xx.xx' для отправки уведомлений')
# bot.register_next_step_handler(mesg_tz, user_set_time)


def user_set_time(tg_id, text):
    match = re.search(r'\D', text).group()
    user_time = datetime.time(int(text.split(match)[0]), int(text.split(match)[1]))
    user_full_time = datetime.datetime.strptime(str(user_time), "%H:%M:%S")
    user_note_time = user_full_time.strftime('%H:%M')
    index_user = index_user_search(tg_id) - 44
    b = User.objects.all()[index_user]
    b.time_to_notificate = user_note_time
    b.save()
    # узнать сколько время в его часовом поясе и в это время и выполнять напомининие
    return user_note_time

#  функцию на уведомление



# вывести во вью сообщения с уточнением и возможностью изменить




