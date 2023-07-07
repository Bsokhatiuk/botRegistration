import sqlite3 as sq
from datetime import datetime
async def db_start():
    global db
    global cur

    db = sq.connect('sqlite.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users_info (user_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, first_date TEXT, last_date)")

    db.commit()

async def create_user(user_id, first_name, last_name):
    dater = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    user = cur.execute("SELECT * FROM users_info WHERE user_id='{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO  users_info VALUES (?, ?, ?, ?, ?)", (user_id, first_name, last_name, dater, dater))
        db.commit()
    else:
        await update_user_date(user_id, dater)

async def update_user_date(user_id, dater):
    cur.execute("UPDATE users_info SET last_date='{}' WHERE user_id='{}'".format(dater, user_id))
    db.commit()
