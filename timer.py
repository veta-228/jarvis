import telebot
import time
import datetime
import pymysql


token = '5336433139:AAEWtMsLq86KMuIveVrLzWvzy3aGEQ7K_ZM'
bot = telebot.TeleBot(token)


def dailyArray():
    con = pymysql.connect(host='localhost', user='root', password='', database='bot', charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
    with con:
        cur = con.cursor()
        now = datetime.datetime.now()
        date = now.strftime("%d.%m.%Y")
        cur.execute(f"SELECT * FROM `timetable` WHERE date = '{date}';")
        rows = cur.fetchall()
        return rows


rows = dailyArray()

while True:
    time.sleep(1)
    now = datetime.datetime.now()
    if now.strftime("%S") == "00" or now.strftime("%S") == "30":
        rows = dailyArray()
    for row in rows:
        if now.strftime("%d.%m.%Y") == row["date"] and now.strftime("%H:%M:%S") == row["time"]:
            bot.send_message(row["userid"], text=row["message"])
