import asyncio
from flask import Flask, render_template, request,redirect, session
import dao.modelDao as dao
import json
import logging
from utils.loggingFilter import ContextualFilter
import secrets



dao.db_start()
app = Flask(__name__)
token = secrets.token_bytes(32)
print(token)
app.secret_key = token



# from aiogram import Bot, Dispatcher, types, executor
# from config import TOKEN_API
#
# bot = Bot(TOKEN_API)
# dp = Dispatcher(bot)
#
# loop = asyncio.get_event_loop()
# tasks = [loop.create_task(bot.send_message(chat_id=101375229, text='Hellow'))]


@app.route("/")
def index():
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()
    # print(botusername.user_agent)
    # print(id)
    print(request.user_agent)
    return render_template('index.html')


@app.route("/home/<botusername>/<bot_id>/<int:id>")
def home(botusername, bot_id, id):
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()
    # print(botusername.user_agent)
    # print(id)
    session['botusername'] = botusername
    print("-----------------------user_agent",request.user_agent, '----------------------------------')
    print('request',request)
    return render_template('index.html', botusername=botusername, bot_id=bot_id, id=id)

@app.route("/exit", methods=['POST', 'GET'])
def exit():
    return render_template('exit.html')


@app.route("/stepform/<botusername>/<bot_id>/<int:id>", methods=['POST', 'GET'])
def stepform(botusername, bot_id, id):
    if request.method == "POST":
        org_name = request.form['org_name']
        mobile = request.form['mobile']
        city = request.form['city']
        street = request.form['street']
        house = request.form['house']
        password = request.form['password']
        dao.create_admin(id, org_name, mobile, password, botusername, bot_id)
        return redirect('/exit')
    else:
        print(botusername, bot_id, id)
        return render_template('stepform.html')


@app.route("/createservice/<botusername>", methods=['POST', 'GET'])
def createservice(botusername):
    if request.method == "POST":
        dao.create_service(request.form['service_name'], request.form['service_price'], botusername)
        # service_list = dao.get_service()
        url = '/service_list/' + botusername
        return redirect(url)
    else:
        return render_template('createservice.html')

@app.route("/service_list/<botusername>", methods=['GET'])
def service_list(botusername):
    print(session)
    # print(session['botusername'])
    service_list = dao.get_service(botusername)
    return render_template('service_list.html', service_list=service_list, botusername=botusername)

@app.route("/service/<botusername>/<int:id>/del", methods=['GET', 'POST'])
def service_delete(botusername, id):
    dao.delete_service(id, botusername)
    url = '/service_list/' + botusername
    return redirect(url)

@app.route("/service/<botusername>/<int:id>/upd", methods=['GET', 'POST'])
def service_update(botusername, id):
    if request.method == "POST":
        dao.update_service(request.form['service_id'], request.form['service_name'], request.form['service_price'], botusername)
        url = '/service_list/' + botusername
        return redirect(url)
    else:
        service = dao.get_service_one(id, botusername)
        return render_template('/serviceupdate.html', service= service)


@app.route("/serviceupdate/<botusername>", methods=['GET', 'POST'])
def service_update_bd(botusername):
    if request.method == "POST":
        dao.update_service(request.form['service_id'], request.form['service_name'], request.form['service_price'], botusername)
        url = '/service_list/' + botusername
        return redirect(url)
    return render_template('serviceupdate.html')


@app.route("/employeecreate/<botusername>", methods=['POST', 'GET'])
def createemployee(botusername):
    if request.method == "POST":
        dao.create_employee(request.form['name'], request.form['phone'], request.form['specialization'], bot_username=botusername)
        url = '/employee_list/' + botusername
        return redirect(url)
    else:
        return render_template('employeecreate.html')


@app.route("/employee_list/<botusername>", methods=['POST', 'GET'])
def employee_list(botusername):
    employee_list = dao.get_employee_all(botusername)
    return render_template('employee_list.html', employee_list=employee_list, botusername=botusername)

@app.route("/employee/<botusername>/<phone>/del", methods=['GET', 'POST'])
def employee_delete(botusername, phone):
    dao.delete_employee(phone, botusername)
    url = '/employee_list/' + botusername
    return redirect(url)


@app.route("/employee/<botusername>/<phone>/upd", methods=['GET', 'POST'])
def employee_update(botusername, phone):
    if request.method == "POST":
        dao.update_employee(request.form['name'], request.form['phone'], request.form['specialization'], request.form['employee_id'],  request.form['info'], request.form['photo'], bot_username=botusername)
        url = '/employee_list/' + botusername
        return redirect(url)
    else:
        employee = dao.get_employee_by_phone(phone, botusername)
        return render_template('/employee_update.html', employee= employee)


@app.route("/login/<botusername>/<int:id>/<first_name>/<last_name>", methods=['POST', 'GET'])
def login(botusername, id, first_name, last_name):
    if request.method == "POST":
        return redirect("/profile/" + botusername +"/" + str(id) +"/" + request.form['phone'])
    else:
        employees = dao.get_employee_phone_all(botusername)
        for items in employees:
            phone, _id = items
            if _id == id:
                return redirect("/profile/" + botusername + "/" + str(id) + "/" + phone)
        dao.create_user(id, first_name, last_name, bot_username=botusername)
        return render_template('login.html', botusername=botusername, id=id)

@app.route("/login/<botusername>/<int:id>", methods=['POST', 'GET'])
def login_short(botusername, id):
    if request.method == "POST":
        return redirect("/profile/" + botusername +"/" + str(id) +"/" + request.form['phone'])
    else:
        app.logger.warning('Warning level log')
        employees = dao.get_employee_phone_all(botusername)
        for items in employees:
            phone, _id = items
            if _id == id:
                return redirect("/profile/" + botusername + "/" + str(id) + "/" + phone)
        dao.create_user(id, "first_name", "last_name", bot_username=botusername)
        return render_template('login.html', botusername=botusername, id=id)

@app.route("/profile/<botusername>/<int:id>/<phone>", methods=['POST', 'GET'])
def profile(botusername, id, phone):
    if request.method == "POST":
        print('hellow')
        dao.update_employee(request.form['name'], request.form['phone'], request.form['specialization'],
                            id, request.form['about'], request.form['photo'], request.form['email'], botusername)
    employee = dao.get_employee_by_phone(phone, botusername)
    return render_template('profile.html', employee= employee)


@app.route("/calendar/<botusername>/<int:id>", methods=['POST', 'GET'])
def calendar(botusername, id):
    return render_template('calendar.html', id=id)

@app.route("/req/<int:id>", methods=['POST'])
def req(id):
    data = dao.get_employee_all()
    response = app.response_class(
        response=json.dumps({'data':data}),
        status=200,
        mimetype='application/json'
        )
    return response

@app.route("/savedata", methods=['GET'])
def savedata():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        print(json)
    response = app.response_class(
        status=200,
        )
    return response

if __name__=="__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)



