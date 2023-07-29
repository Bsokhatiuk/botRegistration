import sqlite3 as sq
from datetime import datetime


def db_start():
    global db
    global cur

    db = sq.connect('sqlite.db', check_same_thread=False)
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users_info (user_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, first_date TEXT, last_date TEXT, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS admins (user_id TEXT, org_name TEXT, phone TEXT, password TEXT, bot_username TEXT, bot_id TEXT PRIMARY KEY)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS service (service_id INTEGER PRIMARY KEY AUTOINCREMENT, service_name TEXT NOT NULL UNIQUE, price REAL, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee (employee_id INTEGER, name TEXT NOT NULL, phone TEXT, specialization TEXT, info TEXT, photo BLOB, email TEXT, bot_username TEXT)")
    db.commit()


async def db_start_asc():
    global db
    global cur

    db = sq.connect('sqlite.db', check_same_thread=False)
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users_info (user_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, first_date TEXT, last_date TEXT, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS admins (user_id TEXT, org_name TEXT, phone TEXT, password TEXT, bot_username TEXT, bot_id TEXT PRIMARY KEY)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS service (service_id INTEGER PRIMARY KEY AUTOINCREMENT, service_name TEXT NOT NULL UNIQUE, price REAL, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee (employee_id INTEGER, name TEXT NOT NULL, phone TEXT, specialization TEXT, info TEXT, photo BLOB, email TEXT, bot_username TEXT)")
    db.commit()


def create_admin(user_id, org_name, phone, password, bot_username, bot_id):
    user = cur.execute("SELECT * FROM admins WHERE bot_id='{key}'".format(key=bot_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO  admins VALUES (?, ?, ?, ?, ?, ?)", (user_id, org_name, phone, password, bot_username, bot_id))
        db.commit()


def create_service(service_name, price, bot_username=''):
    service = cur.execute("SELECT * FROM service WHERE service_name='{key}' and bot_username='{key2}'".format(key=service_name, key2=bot_username)).fetchone()
    if not service:
        cur.execute("INSERT INTO service VALUES (?, ?, ?, ?)", (None, service_name, price, bot_username))
        db.commit()


def get_service(bot_username=''):
    service = cur.execute("SELECT * FROM service WHERE bot_username="+bot_username).fetchall()
    return service


def delete_service(service_id, bot_username=''):
    try:
        cur.execute("DELETE FROM service WHERE service_id='{key}' and bot_username='{key2}'".format(key=service_id, key2=bot_username))
        db.commit()
    except Exception as err:
        print(err)


def update_service(service_id, service_name, price, bot_username=''):
    cur.execute(
        "UPDATE service SET service_name = ?, price= ?  WHERE service_id = ? amd bot_username = ?", (service_name, price, service_id, bot_username))
    db.commit()


async def create_user(user_id, first_name, last_name, bot_username=''):
    dater = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    user = cur.execute("SELECT * FROM users_info WHERE user_id='{key}' and bot_username= '{key2}'".format(key=user_id, key2=bot_username)).fetchone()
    if not user:
        cur.execute("INSERT INTO  users_info VALUES (?, ?, ?, ?, ?, ?)", (user_id, first_name, last_name, dater, dater, bot_username))
        db.commit()
    else:
        await update_user_date(user_id, dater)


async def update_user_date(user_id, dater, bot_username=''):
    cur.execute("UPDATE users_info SET last_date='{}' WHERE user_id='{}' and bot_username={}".format(dater, user_id, bot_username))
    db.commit()


def get_service_one(service_id, bot_username=''):
    service = cur.execute("SELECT * FROM service WHERE service_id='{key}' and bot_username='{key2}'".format(key=service_id, key2=bot_username)).fetchone()
    return service

def create_employee(employee_name, phone, specialization, info="", photo="", email="", bot_username=""):
    employee = cur.execute("SELECT * FROM employee WHERE phone='{key}' and bot_username='{key2}'".format(key=phone, key2=bot_username)).fetchone()
    if not employee:
        cur.execute("INSERT INTO employee VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (-1, employee_name, phone, specialization, info, photo, email, bot_username))
        db.commit()


def get_employee_all(bot_username=""):
    employee = cur.execute("SELECT * FROM employee where bot_username=" + bot_username).fetchall()
    return employee


def delete_employee(phone, bot_username=""):
    try:
        cur.execute("DELETE FROM employee WHERE phone='{key}' and bot_username='{key2}' ".format(key=phone, key2=bot_username))
        db.commit()
    except Exception as err:
        print(err)


def update_employee(employee_name, phone, specialization, employee_id=-1, info="", email="", photo="", bot_username=''):
    cur.execute(
        "UPDATE employee SET employee_id = ?, name = ?,specialization= ?, info= ?, photo =?, email=? WHERE phone = ? and ", (employee_id, employee_name, specialization, info, photo, email, phone))
    db.commit()

def get_employee_by_phone(phone, bot_username=''):
    employee = cur.execute("SELECT * FROM employee WHERE phone='{key}' and bot_username='{key2}'".format(key=phone, key2=bot_username)).fetchone()
    return employee

