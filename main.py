import telebot
import datetime
from telebot import types
import pymysql

token = '53'
bot = telebot.TeleBot(token)


def timeIn(time, utc):
    if utc[0] == '+':
        utc = utc.replace("+", "")
        time = time.split(":")
        hours = int(time[0])
        hours = hours - int(utc)

        if hours < 0 : hours += 24
    else:
        utc = utc.replace("-", "")
        time = time.split(":")
        hours = int(time[0])
        hours = hours + int(utc)

        if hours > 24 : hours -= 24
    hours = str(hours)
    if len(hours) == 1:
        hours = "0" + hours
    out = str(hours) + ":" + time[1]
    return out


def timeOut(time, utc):
    if utc[0] == '+':
        utc = utc.replace("+", "")
        time = time.split(":")
        hours = int(time[0])
        hours = hours + int(utc)

        if hours > 24 : hours -= 24
    else:
        utc = utc.replace("-", "")
        time = time.split(":")
        hours = int(time[0])
        hours = hours - int(utc)

        if hours < 0 : hours += 24
    hours = str(hours)
    if len(hours) == 1:
        hours = "0" + hours
    out = str(hours) + ":" + time[1]
    return out


def dateIn(time, utc, date):
    day = datetime.datetime.strptime(date, "%d.%m.%Y")
    if utc[0] == '+':
        utc = utc.replace("+", "")
        time = time.split(":")
        hours = int(time[0])
        hours = hours - int(utc)

        if hours < 0 :
            day = day - datetime.timedelta(days=1)
    else:
        utc = utc.replace("-", "")
        time = time.split(":")
        hours = int(time[0])
        hours = hours + int(utc)

        if hours > 24 :
            day = day + datetime.timedelta(days=1)
    return day


def dateOut(time, utc, date):
    day = datetime.datetime.strptime(date, "%d.%m.%Y")
    if utc[0] == '+':
        utc = utc.replace("+", "")
        time = time.split(":")
        hours = int(time[0])
        hours = hours + int(utc)

        if hours > 24 :
            day = day + datetime.timedelta(days=1)
    else:
        utc = utc.replace("-", "")
        time = time.split(":")
        hours = int(time[0])
        hours = hours - int(utc)
        min = int(time[1])
        if hours < 0 :
            day = day - datetime.timedelta(days=1)
    return day


def getStatus(userid):
    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM `statustable` WHERE userid = '{userid}';")
        rows = cur.fetchall()
    if rows:
        return rows[0]["status"]
    else:
        return 0


def editStatus(userid, status):
    if not getStatus(userid):
        con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        with con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO `statustable` (`id`, `userid`, `status`) VALUES (NULL, '{userid}',"
                        f" '{status}');")
            con.commit()

    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    with con:
        cur = con.cursor()
        cur.execute(f"UPDATE `statustable` SET `status` = '{status}' WHERE `userid` = {userid};")
        con.commit()


def getUTC(userid):
    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM `utctable` WHERE userid = '{userid}';")
        rows = cur.fetchall()
    if rows:
        return rows[0]["utc"]
    else:
        return 0


def addUTC(userid, utc):
    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    if utc >= 0:
        utc = "+" + str(utc)
    with con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO `utctable` (`id`, `userid`, `utc`) VALUES (NULL, '{userid}',"
                    f" '{utc}');")
        con.commit()


def delUTC(userid):
    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    with con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM `utctable` WHERE `utctable`.`userid` = '{userid}';")
        con.commit()


def addNote(userid, date, time, message):
    utc = getUTC(userid)
    time = timeIn(time, utc)
    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


    with con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO `timetable` (`id`, `userid`, `date`, `time`, `message`) VALUES (NULL, '{userid}', "
                    f"'{date}', '{time + ':00'}', '{message}');")
        con.commit()


def getNotes(userid, date):
    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM `timetable` WHERE date = '{date}' and userid = '{userid}' ORDER BY "
                    f"`timetable`.`time` ASC;")
        rows = cur.fetchall()
    return rows


def delNote(userid, noteid):
    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    with con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM `timetable` WHERE `timetable`.`id` = {noteid} and `timetable`.`userid` = '{userid}';")
        con.commit()


def getMoney(userid):
    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM `money` WHERE userid = '{userid}';")
        rows = cur.fetchall()
    return rows


def calculate(rows):
    summ = 0
    for row in rows:
        row = row["plusminus"]
        if row[0] == '+':
            row = row.replace("+", "")
            summ += int(row)
        else:
            row = row.replace("-", "")
            summ -= int(row)
    return summ


def minusfunc(userid, date, minus, category, isplanned):

    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    if isplanned.lower() == '??':
        planned = 0
    else:
        planned = 1

    minus = '-' + str(minus)

    with con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO `money` (`id`, `userid`, `date`, `plusminus`, `category`, `isplanned`) VALUES"
                    f" (NULL, '{userid}', '{date}', '{minus}', '{category.lower()}', '{planned}');")
        con.commit()


def plusfunc(userid, date, plus):
    con = pymysql.connect(host='projectlove.mysql.pythonanywhere-services.com', user='projectlove', password='ittakestwo28', database='projectlove$bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


    plus = '+' + str(plus)

    with con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO `money` (`id`, `userid`, `date`, `plusminus`) VALUES"
                    f" (NULL, '{userid}', '{date}', '{plus}');")
        con.commit()



def getStat(userid, date):
    rows = getMoney(userid)
    date = date.split(".")
    month = 0
    year = 0
    planned = 0
    notplanned = 0
    arr = [[None, 0]]
    for row in rows:
        split = row["date"].split(".")
        plusminus = row["plusminus"]
        if plusminus[0] == '-':
            plusminus = plusminus.replace("-", "")
            if split[1] == date[1]:
                month += int(plusminus)
                if row["isplanned"] == 1:
                    planned += int(plusminus)
                if row["isplanned"] == 0:
                    notplanned += int(plusminus)
            if split[2] == date[2]:
                year += int(plusminus)
        category = False
        for i in range(len(arr)):
            if arr[i][0] == row["category"]:
                arr[i][1] += int(plusminus)
                category = True
        if not category:
            arr.append([row["category"], int(plusminus)])

    list = "???? ????????????????????:\n"
    for i in range(len(arr)):
        if arr[i][0] is not None:
            list += f"{arr[i][0]}: {arr[i][1]}\n"

    return f"???????? ??????????????\n\n?? ???????? ????????: {year}\n?? ???????? ????????????: {month}\n?????????????????????????????????? ??????????: {notplanned}\n" \
           f"?????????????????????????????? ??????????: {planned}\n\n{list}"


def printNotes(userid):
    utc = getUTC(userid)
    now = datetime.datetime.now()
    date = dateOut(now.strftime("%H:%M"), utc, now.strftime("%d.%m.%Y"))
    out = f'???????????? ???? {date.strftime("%d.%m.%Y")} (??????????????):\n\n'
    date = date - datetime.timedelta(days=1)
    date = date.strftime("%d.%m.%Y")
    rows = getNotes(userid, date)
    for row in rows:
        if utc[0] == '+':
            utc = utc.replace("+", "")
            time = row["time"].split(":")
            hours = int(time[0])
            hours = hours + int(utc)
            utc = "+" + utc
            if hours > 24:
                time = timeOut(row["time"], utc)
                out += f'(id:{row["id"]})  {time[0:5]} | {row["message"]}\n'

    date = dateOut(now.strftime("%H:%M"), utc, now.strftime("%d.%m.%Y"))
    date = date.strftime("%d.%m.%Y")
    rows = getNotes(userid, date)
    for row in rows:
        if utc[0] == '+':
            utc = utc.replace("+", "")
            time = row["time"].split(":")
            hours = int(time[0])
            hours = hours + int(utc)
            utc = "+" + utc
            if hours < 24:
                time = timeOut(row["time"], utc)
                out += f'(id:{row["id"]})  {time[0:5]} | {row["message"]}\n'
        else:
            utc = utc.replace("-", "")
            time = row["time"].split(":")
            hours = int(time[0])
            hours = hours - int(utc)
            utc = "-" + utc
            if hours > 0:
                time = timeOut(row["time"], utc)
                out += f'(id:{row["id"]})  {time[0:5]} | {row["message"]}\n'

    bot.send_message(userid, out)


def printDate(message):
    utc = getUTC(message.chat.id)
    now = datetime.datetime.now()
    date = dateOut(now.strftime("%H:%M"), utc, message.text)
    out = f'???????????? ???? {date.strftime("%d.%m.%Y")}:\n\n'
    date = date - datetime.timedelta(days=1)
    date = date.strftime("%d.%m.%Y")
    rows = getNotes(message.chat.id, date)
    for row in rows:
        if utc[0] == '+':
            utc = utc.replace("+", "")
            time = row["time"].split(":")
            hours = int(time[0])
            hours = hours + int(utc)
            utc = "+" + utc
            if hours > 24:
                time = timeOut(row["time"], utc)
                out += f'(id:{row["id"]})  {time[0:5]} | {row["message"]}\n'

    date = dateOut(now.strftime("%H:%M"), utc, message.text)
    date = date.strftime("%d.%m.%Y")
    rows = getNotes(message.chat.id, date)
    for row in rows:
        if utc[0] == '+':
            utc = utc.replace("+", "")
            time = row["time"].split(":")
            hours = int(time[0])
            hours = hours + int(utc)
            utc = "+" + utc
            if hours < 24:
                time = timeOut(row["time"], utc)
                out += f'(id:{row["id"]})  {time[0:5]} | {row["message"]}\n'
        else:
            utc = utc.replace("-", "")
            time = row["time"].split(":")
            hours = int(time[0])
            hours = hours - int(utc)
            utc = "-" + utc
            if hours > 0:
                time = timeOut(row["time"], utc)
                out += f'(id:{row["id"]})  {time[0:5]} | {row["message"]}\n'
    bot.send_message(message.chat.id, out)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    plan_but = types.KeyboardButton('????????????????????')
    money_but = types.KeyboardButton('???????????????????? ????????')
    win_but = types.KeyboardButton('????????????')
    markup.add(plan_but, money_but)
    bot.send_message(message.chat.id, f'????????????????????, {message.from_user.first_name}! ?????? ?????? ?????????????????????????',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def eny(message):
    if message.text == '????????????????????':
        if not getUTC(message.chat.id):
            global status
            editStatus(message.chat.id, "UTC")
            bot.send_message(message.chat.id, text="???????????????? ?????????? ?? ?????????? ?????????????? ?????????? ?? ?????????????? ????:????")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            printNotes(message.chat.id)
            day_but = types.KeyboardButton('???????????? ????????')
            add_but = types.KeyboardButton('????????????????')
            del_but = types.KeyboardButton('??????????????')
            edit_but = types.KeyboardButton('???????????????? ?????????????? ????????')
            back_but = types.KeyboardButton('??????????')
            markup.add(day_but, add_but, del_but, edit_but, back_but)
            bot.send_message(message.chat.id, '???????????????? ????????????????', reply_markup=markup)

    elif message.text == '???????????? ????????':
        bot.send_message(message.chat.id, '?????????????? ???????? ?? ?????????????? ????.????.????????')
        editStatus(message.chat.id, 'date')

    elif message.text == '??????????????':
        bot.send_message(message.chat.id, '?????????????? id ????????????')
        editStatus(message.chat.id, 'delete')

    elif message.text == '????????????????':



        bot.send_message(message.chat.id, '?????????????? ???????????? ?? ??????????????\n\n????.????.????????; ????:????; ?????????? ??????????????????\n\n'
                                          '???????????????????? ??????????????')

        editStatus(message.chat.id, 'add')


    elif message.text == '???????????????? ?????????????? ????????':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        plan_but = types.KeyboardButton('????????????????????')
        money_but = types.KeyboardButton('???????????????????? ????????')
        win_but = types.KeyboardButton('????????????')
        markup.add(plan_but, money_but)
        bot.send_message(message.chat.id, text="???????????????? ?????????? ?? ?????????? ?????????????? ?????????? ?? ?????????????? ????:????",
                         reply_markup=markup)
        editStatus(message.chat.id, "UTC")

    elif message.text == '???????????????????? ????????':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        minus_but = types.KeyboardButton('??????????')
        plus_but = types.KeyboardButton('????????????????????')
        hist_but = types.KeyboardButton('????????????????????')
        back_but = types.KeyboardButton('??????????')
        markup.add(minus_but, plus_but, hist_but, back_but)

        rows = getMoney(message.chat.id)
        summ = calculate(rows)
        bot.send_message(message.chat.id, text="??????????????: " + str(summ), reply_markup=markup)


    elif message.text == '??????????':
        bot.send_message(message.chat.id, text="?????????????? ???????????????????? ?????????????????????? ?????????????? ?? ??????????????:\n\n"
                                               "??????????; ?????????????????? ????????; ??/??\n\n?? - ?????????????????????????????????? ??????????\n"
                                               "?? - ?????????????????????????????? ??????????\n???????????????????? ??????????????")
        editStatus(message.chat.id, "minus")

    elif message.text == '????????????????????':
        bot.send_message(message.chat.id, text="?????????????? ?????????? ????????????????????:")
        editStatus(message.chat.id, "plus")

    elif message.text == '????????????????????':
        out = "???????????????????? ????????:\n"
        now = datetime.datetime.now()
        date = now.strftime("%d.%m.%Y")
        try:
            stat = getStat(message.chat.id, date)
            bot.send_message(message.chat.id, text=stat)
        except:
            bot.send_message(message.chat.id, '???????????? ???????? ????????????')


    elif message.text == '??????????':
        start(message)

    else:
        if getStatus(message.chat.id) == 'error':
            bot.send_message(message.chat.id, '???????????????? ????????????')

        elif getStatus(message.chat.id) == 'date':
            try:
                printDate(message)
            except:
                bot.send_message(message.chat.id, '???????????? ??????????')
            editStatus(message.chat.id, 'error')

        elif getStatus(message.chat.id) == 'delete':
            try:
                delNote(message.chat.id, message.text)
                bot.send_message(message.chat.id, '??????????????')
                printNotes(message.chat.id)
            except:
                bot.send_message(message.chat.id, '???????????? ??????????')
            editStatus(message.chat.id, 'error')

        elif getStatus(message.chat.id) == 'add':
            try:
                inf = message.text.split('; ')
                utc = getUTC(message.chat.id)
                date = dateIn(inf[1], utc, inf[0])
                inf[0] = date.strftime("%d.%m.%Y")
                time = datetime.datetime.strptime(inf[1], "%H:%M")
                addNote(message.chat.id, inf[0], inf[1], inf[2])
                bot.send_message(message.chat.id, '??????????????????')
                printNotes(message.chat.id)
                editStatus(message.chat.id, 'error')
            except:
                bot.send_message(message.chat.id, '???????????? ??????????')
            editStatus(message.chat.id, 'error')

        elif getStatus(message.chat.id) == 'UTC':
            try:
                inf = message.text.split(':')
                now = datetime.datetime.now()
                hours = now.strftime("%H")
                delUTC(message.chat.id)
                addUTC(message.chat.id, int(inf[0]) - int(hours))
                bot.send_message(message.chat.id, "?????????????? ???????? ????????????????, ?????????????? ???????????? ?????? ??????")
            except:
                bot.send_message(message.chat.id, '???????????? ??????????')
            editStatus(message.chat.id, 'error')

        elif getStatus(message.chat.id) == 'minus':
            try:
                now = datetime.datetime.now()
                date = now.strftime("%d.%m.%Y")
                inf = message.text.split('; ')
                minusfunc(message.chat.id, date, int(inf[0]), inf[1], inf[2])
                bot.send_message(message.chat.id, '??????????????????')
                rows = getMoney(message.chat.id)
                summ = calculate(rows)
                bot.send_message(message.chat.id, text="??????????????: " + str(summ))
            except:
                bot.send_message(message.chat.id, '???????????? ??????????')
            editStatus(message.chat.id, 'error')

        elif getStatus(message.chat.id) == 'plus':
            try:
                now = datetime.datetime.now()
                date = now.strftime("%d.%m.%Y")
                plusfunc(message.chat.id, date, int(message.text))
                bot.send_message(message.chat.id, '??????????????????')
                rows = getMoney(message.chat.id)
                summ = calculate(rows)
                bot.send_message(message.chat.id, text="??????????????: " + str(summ))
            except:
                bot.send_message(message.chat.id, '???????????? ??????????')

            editStatus(message.chat.id, 'error')

        else:
            bot.send_message(message.chat.id, '?? ?????? ???? ??????????????')



bot.polling(none_stop=True)
