import subprocess
import schedule
import time
import datetime
import sqlite3
from pushbullet import Pushbullet


def run_script():
    subprocess.run(["scrapy", "crawl", "aukro"])
    now_time = datetime.datetime.now()
    date_format = "%Y-%m-%d %H:%M:%S"
    cursor.execute("SELECT id, dead_line, total_price, max_bid FROM items")
    date = cursor.fetchall()
    for d in date:
        final_date = datetime.datetime.strptime(d[1], date_format)
        diff_time = final_date - now_time
        if diff_time.days == 0:
            hour = diff_time.seconds / 3600
            if hour < 4 and d[3] / d[2] * 100 < 10:
                push_notification(d[0])


def push_notification(idn):
    with open("key.txt") as k:
        ac_token = k.readlines(1)[0]
    cursor.execute("""SELECT link, dead_line, total_price, max_bid, top_item_price, top_item_quantity,
     top_item_description, top_item_img FROM items WHERE id=?""", (idn,))
    r = cursor.fetchall()
    r = r[0]

    pb = Pushbullet(ac_token)
    pb.push_note("Nenech si ujít", f"{r[0]}\nKončí v: {r[1]}\nCelková hodnota: {r[2]}Kč\n Nejvyší příhoz: {r[3]}Kč\n"
                                          f"Nejdražší předmět: {r[4]}Kč\nMnožství: {r[5]}\nks Popis: {r[6]}\n"
                                          f"Obrázek: {r[7]}")


connection = sqlite3.connect("../db.db")
cursor = connection.cursor()

schedule.every().day.at("18:00").do(run_script)

while True:
    schedule.run_pending()
    time.sleep(10)