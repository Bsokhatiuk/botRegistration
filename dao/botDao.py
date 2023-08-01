import sqlite3 as sq
from datetime import datetime


async def db_start():
    global db_bot
    global cur_bd
    db_bot = sq.connect('sqlite_bot.db', check_same_thread=False)
    cur_bd = db_bot.cursor()
    cur_bd.execute("CREATE TABLE IF NOT EXISTS users_info (user_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, first_date TEXT, last_date TEXT, role TEXT, phone TEXT)")
    db_bot.commit()
async def create_user(user_id, first_name, last_name, role="USER", phone=''):
    dater = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    user = cur_bd.execute("SELECT * FROM users_info WHERE user_id='{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_bd.execute("INSERT INTO  users_info VALUES (?, ?, ?, ?, ?, ?, ?)",(user_id, first_name, last_name, dater, dater, role, phone))
        db_bot.commit()
    else:
        await update_user_date(user_id, dater)

async def update_user_date(user_id, dater):
    cur_bd.execute("UPDATE users_info SET last_date='{key1}' WHERE user_id='{key2}'".format(key1=dater,key2=user_id))
    db_bot.commit()

async def update_user_role(user_id, role):
    cur_bd.execute("UPDATE users_info SET role='{key1}' WHERE user_id='{key2}'".format(key1=role,key2=user_id))
    db_bot.commit()

async def update_user_phone(user_id, phone):
    cur_bd.execute("UPDATE users_info SET phone='{key1}' WHERE user_id='{key2}'".format(key1=phone,key2=user_id))
    db_bot.commit()