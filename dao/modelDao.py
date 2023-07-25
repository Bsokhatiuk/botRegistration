import sqlite3 as sq
from datetime import datetime


def db_start():
    global db
    global cur

    db = sq.connect('sqlite.db', check_same_thread=False)
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users_info (user_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, first_date TEXT, last_date)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS admins (user_id TEXT PRIMARY KEY, org_name TEXT, phone TEXT, password TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS service (service_id INTEGER PRIMARY KEY AUTOINCREMENT, service_name TEXT NOT NULL UNIQUE, price REAL)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee (employee_id INTEGER, name TEXT NOT NULL, phone TEXT, specialization TEXT, info TEXT, photo BLOB, email TEXT)")
    db.commit()


async def db_start_asc():
    global db
    global cur

    db = sq.connect('sqlite.db', check_same_thread=False)
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users_info (user_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, first_date TEXT, last_date)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS admins (user_id TEXT PRIMARY KEY, org_name TEXT, phone TEXT, password TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS service (service_id INTEGER PRIMARY KEY AUTOINCREMENT, service_name TEXT NOT NULL UNIQUE, price REAL)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee (employee_id INTEGER, name TEXT NOT NULL, phone TEXT, specialization TEXT, info TEXT, photo BLOB, email TEXT)")
    db.commit()


def create_admin(user_id, org_name, phone, password):
    user = cur.execute("SELECT * FROM admins WHERE user_id='{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO  admins VALUES (?, ?, ?, ?)", (user_id, org_name, phone, password))
        db.commit()


def create_service(service_name, price):
    service = cur.execute("SELECT * FROM service WHERE service_name='{key}'".format(key=service_name)).fetchone()
    if not service:
        cur.execute("INSERT INTO service VALUES (?, ?, ?)", (None, service_name, price))
        db.commit()


def get_service():
    service = cur.execute("SELECT * FROM service").fetchall()
    return service


def delete_service(service_id):
    try:
        cur.execute("DELETE FROM service WHERE service_id='{key}'".format(key=service_id))
        db.commit()
    except Exception as err:
        print(err)


def update_service(service_id, service_name, price):
    cur.execute(
        "UPDATE service SET service_name = ?, price= ?  WHERE service_id = ?", (service_name, price, service_id))
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


def get_service_one(service_id):
    service = cur.execute("SELECT * FROM service WHERE service_id='{key}'".format(key=service_id)).fetchone()
    return service

def create_employee(employee_name, phone, specialization, info="", photo="", email=""):
    employee = cur.execute("SELECT * FROM employee WHERE phone='{key}'".format(key=phone)).fetchone()
    if not employee:
        cur.execute("INSERT INTO employee VALUES (?, ?, ?, ?, ?, ?, ?)", (-1, employee_name, phone, specialization, info, photo, email))
        db.commit()


def get_employee_all():
    employee = cur.execute("SELECT * FROM employee").fetchall()
    return employee


def delete_employee(phone):
    try:
        cur.execute("DELETE FROM employee WHERE phone='{key}'".format(key=phone))
        db.commit()
    except Exception as err:
        print(err)


def update_employee(employee_name, phone, specialization, employee_id=-1, info="", email="", photo=""):
    cur.execute(
        "UPDATE employee SET employee_id = ?, name = ?,specialization= ?, info= ?, photo =?, email=? WHERE phone = ?", (employee_id, employee_name, specialization, info, photo, email, phone))
    db.commit()

def get_employee_by_phone(phone):
    employee = cur.execute("SELECT * FROM employee WHERE phone='{key}'".format(key=phone)).fetchone()
    return employee

