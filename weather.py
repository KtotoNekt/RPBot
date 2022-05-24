from discord_webhook import DiscordWebhook, DiscordEmbed
import random
import time
import sqlite3


db = sqlite3.connect("timezone.db", check_same_thread=False)
cursor = db.cursor()


month_num = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 
    6: "июня", 7: "июля", 8: "августа", 9: 'сентября', 10: 'октября', 11: "ноября", 12: "декабря"
}
weathers = ["Ясная", "Ясная", "Облачная", "Дождливая", "Облачная", "Дождь с грозой", "Ясная"]


def run_change(guild_id, count_bool):
    cursor.execute(f"UPDATE guilds SET run = {count_bool} WHERE guild = {guild_id}")
    db.commit()


def clear(guild_id):
    url = cursor.execute(f"SELECT webhook FROM guilds WHERE guild = {guild_id}").fetchone()[0]

    cursor.execute(f"DELETE FROM guilds WHERE guild = {guild_id}")
    db.commit()

    return url


def arguments_change(guild_id, command: list):
    com = False
    pole = ""
    if command[1] == "timeout":
        pole = "timeout"
    elif command[1] == "year":
        pole = "year"
    elif command[1] == "day":
        pole = "day"
    elif command[1] == "month":
        pole = "month"
    elif command[1] == "realtime":
        pole = "realtime"

    if command[1] in ["timeout", "year", "day", "month", "realtime"]:
        com = True
    
    if com:
        cursor.execute(f"UPDATE guilds SET {pole} = {command[2]} WHERE guild = {guild_id}")
        db.commit()
        return True
    else:
        return False


def create(guild_id, hook_url):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS guilds(
        webhook TEXT,
        run INT,
        guild INT,
        timeout INT,
        realtime INT,
        year INT,
        day INT,
        month INT,
        time TEXT
    )""")

    if cursor.execute(f"SELECT guild FROM guilds WHERE guild = {guild_id}").fetchone() is None:
        cursor.execute(f"INSERT INTO guilds VALUES('{hook_url}', 0, {guild_id}, 4, 60, 2022, 1, 1, '6:00')")
        db.commit()

        hook = DiscordWebhook(url=hook_url, content="Вебхук создан!")
        hook.execute()
        return True
    else:
        return False


def change_time(guild_id):
    time_was = cursor.execute(f"SELECT time FROM guilds WHERE guild = {guild_id}").fetchone()[0]
    year = cursor.execute(f"SELECT year FROM guilds WHERE guild = {guild_id}").fetchone()[0]
    day = cursor.execute(f"SELECT day FROM guilds WHERE guild = {guild_id}").fetchone()[0]
    month = cursor.execute(f"SELECT month FROM guilds WHERE guild = {guild_id}").fetchone()[0]

    _time_ = time_was.split(":")
    _hour = int(_time_[0]) + cursor.execute(f"SELECT timeout FROM guilds WHERE guild = {guild_id}").fetchone()[0]
    _minute = int(_time_[1])
    if _minute >= 60:
        _hour += 1 
        _minute -= 60

    if _hour >= 24:
        _hour -= 24
        day += 1

    if day >= 30:
        day = 0
        month += 1

    if month >= 13:
        year += 1
        month = 1

    time_result = str(_hour) + ":" + str(_minute)
    cursor.execute(f'UPDATE guilds SET time = "{time_result}", day = {day}, month = {month}, year = {year} WHERE guild = {guild_id}')

    return [year, day, month, time_result]


def webhook_send(timezone: list, weather, url):
    webhook = DiscordWebhook(url=url)
    
    month = ""
    for k, v in month_num.items():
        if k == timezone[2]:
            month = v

    embed = DiscordEmbed(title="Время и погода", color=0x4169E1)
    embed.description = f"""
На часах {timezone[3]}
Погода: {weather}

Сегодня {timezone[1]} {month} {timezone[0]} год"""
    webhook.add_embed(embed)

    webhook.execute()


def start(guild_id):
    while cursor.execute(f"SELECT run FROM guilds WHERE guild = {guild_id}").fetchone()[0]:
        weather = random.choice(weathers)
        timemout = change_time(guild_id)
        db.commit()
        url = cursor.execute(f"SELECT webhook FROM guilds WHERE guild = {guild_id}").fetchone()[0]
        webhook_send(timemout, weather, url)
        time.sleep(cursor.execute(f"SELECT realtime FROM guilds WHERE guild = {guild_id}").fetchone()[0]*60)