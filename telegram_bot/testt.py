print(time(16, 30))
b = User.objects.all()[25]
print(b.timezone)
print(utcnow())
date = datetime.datetime.today()
print(date.strftime('%H:%M'))
print(now())
geo = geopy.geocoders.Nominatim(user_agent="SuperMon_Bot")
location = geo.geocode('Tbilisi')  # преобразуе
tzw = tzwhere.tzwhere()
timezone_str = tzw.tzNameAt(location.latitude, location.longitude)  # получаем название часового пояса
tz = pytz.timezone(timezone_str)
tz_info = datetime.datetime.now(tz=tz).strftime("%z")  # получаем смещение часового пояса
tz_info = tz_info[0:3] + ":" + tz_info[3:]
tz_hours = tz_info[0:3]
print(get_timezone('Tbilisi')[1])
print(00000000000)
b = User.objects.all()[25]
bb = b.timezone
print(bb)
tzz = datetime.timezone(offset=-datetime.timedelta(hours=3))
print(tzz)
print(date.time())
print(datetime.datetime.now(tz=tz))





a = user_set_time('22.57')[1]
date = datetime.datetime.now(pytz.timezone('Asia/Tbilisi'))
print(date.strftime('%H:%M'))
if date.strftime('%H:%M') == a:
    print('успех')
else:
    print('no')