import asyncio
from datetime import datetime, timedelta

from flask import Flask, render_template, request,redirect, session, send_from_directory
import dao.modelDao as dao
import json
from utils import util as ut
import secrets
import logging
import os
from werkzeug.utils import secure_filename
import json


# logging.basicConfig(filename='app_web.log',
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%Y-%m-%d,%H:%M:%S',
#                     level=logging.INFO)

dao.db_start()
app = Flask(__name__)
token = secrets.token_bytes(32)
app.secret_key = token

app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


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
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; id_user='{id}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    # print("-----------------------user_agent",request.user_agent, '----------------------------------')
    # print("-----------------------HTTP_X_FORWARDED_FOR", request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr), '----------------------------------')
    return render_template('index.html', botusername=botusername, bot_id=bot_id, id=id)

@app.route("/exit/<botusername>", methods=['POST', 'GET'])
def exit(botusername):
    return render_template('exit.html')


@app.route("/stepform/<botusername>/<bot_id>/<int:id>", methods=['POST', 'GET'])
def stepform(botusername, bot_id, id):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; id_user='{id}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        org_name = request.form['org_name']
        mobile = request.form['mobile']
        city = request.form['city']
        street = request.form['street']
        house = request.form['house']
        password = request.form['password']
        dao.create_admin(id, org_name, mobile, password, botusername, bot_id)
        session['check'] = 0
        return redirect('/service_list_reg/' + botusername)
    else:
        print(botusername, bot_id, id)
        return render_template('stepform.html')


@app.route("/createservice/<botusername>", methods=['POST', 'GET'])
def createservice(botusername):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")

    if request.method == "POST":
        dao.create_service(request.form['service_name'], request.form['service_price'], request.form['service_duration'], bot_username=botusername)
        # service_list = dao.get_service()
        session['check']=0
        url = '/service_list/' + botusername
        return redirect(url)
    else:
        return render_template('createservice.html')

@app.route("/createservice/<botusername>/reg", methods=['POST', 'GET'])
def createservice_reg(botusername):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")

    if request.method == "POST":
        dao.create_service(request.form['service_name'], request.form['service_price'], request.form['service_duration'], bot_username=botusername)
        # service_list = dao.get_service()
        session['check']=0
        url = '/service_list_reg/' + botusername
        return redirect(url)
    else:
        return render_template('createservice.html')



@app.route("/service_list/<botusername>", methods=['GET'])
def service_list(botusername):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    service_list = dao.get_service(botusername)
    new_service_list = []
    for service in service_list:
        try:
            new_service_list.append((service[0], service[1],  int(service[2]),  service[3]))
        except Exception as err:
            print(err)
            new_service_list.append((service[0], service[1], service[2], service[3]))
    return render_template('service_list.html', service_list=new_service_list, botusername=botusername)

@app.route("/service_list_reg/<botusername>", methods=['GET'])
def service_list_reg(botusername):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    service_list = dao.get_service(botusername)
    new_service_list = []
    for service in service_list:
        try:
            new_service_list.append((service[0], service[1],  int(service[2]),  service[3]))
        except Exception as err:
            print(err)
            new_service_list.append((service[0], service[1], service[2], service[3]))
    return render_template('service_list_reg.html', service_list=new_service_list, botusername=botusername)


@app.route("/service/<botusername>/<int:id>/del", methods=['GET', 'POST'])
def service_delete(botusername, id):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; id_user='{id}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    dao.delete_service(id, botusername)
    url = '/service_list/' + botusername
    return redirect(url)

@app.route("/service/<botusername>/<int:id>/del_reg", methods=['GET', 'POST'])
def service_delete_reg(botusername, id):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; id_user='{id}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    dao.delete_service(id, botusername)
    url = '/service_list_reg/' + botusername
    return redirect(url)

@app.route("/service/<botusername>/<int:id>/upd", methods=['GET', 'POST'])
def service_update(botusername, id):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; id_user='{id}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        print(request.form['service_duration'])
        dur = float(request.form['service_duration'])
        dao.update_service(request.form['service_id'], request.form['service_name'], request.form['service_price'], dur, bot_username=botusername)
        url = '/service_list/' + botusername
        return redirect(url)
    else:
        service = dao.get_service_one(id, botusername)
        return render_template('/serviceupdate.html', service= service)


@app.route("/service/<botusername>/<int:id>/upd_reg", methods=['GET', 'POST'])
def service_update_reg(botusername, id):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; id_user='{id}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        print(request.form['service_duration'])
        dur = float(request.form['service_duration'])
        dao.update_service(request.form['service_id'], request.form['service_name'], request.form['service_price'], dur, bot_username=botusername)
        url = '/service_list_reg/' + botusername
        return redirect(url)
    else:
        service = dao.get_service_one(id, botusername)
        return render_template('/serviceupdate.html', service= service)

@app.route("/serviceupdate/<botusername>", methods=['GET', 'POST'])
def service_update_bd(botusername):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        dao.update_service(request.form['service_id'], request.form['service_name'], request.form['service_price'], request.form['service_duration'], botusername)
        url = '/service_list/' + botusername
        return redirect(url)
    return render_template('serviceupdate.html')




@app.route("/employeecreate/<botusername>", methods=['POST', 'GET'])
def createemployee(botusername):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        dao.create_employee(request.form['name'], request.form['phone'], request.form['specialization'], bot_username=botusername)
        url = '/employee_list/' + botusername
        return redirect(url)
    else:
        return render_template('employeecreate.html')

@app.route("/employeecreate/<botusername>/reg", methods=['POST', 'GET'])
def createemployee_reg(botusername):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        dao.create_employee(request.form['name'], request.form['phone'], request.form['specialization'], bot_username=botusername)
        url = '/employee_list_reg/' + botusername
        return redirect(url)
    else:
        return render_template('employeecreate.html')

@app.route("/employee_list/<botusername>", methods=['POST', 'GET'])
def employee_list(botusername):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    employee_list = dao.get_employee_all(botusername)
    return render_template('employee_list.html', employee_list=employee_list, botusername=botusername)

@app.route("/employee_list_reg/<botusername>", methods=['POST', 'GET'])
def employee_list_reg(botusername):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    employee_list = dao.get_employee_all(botusername)
    return render_template('employee_list_reg.html', employee_list=employee_list, botusername=botusername)

@app.route("/employee/<botusername>/<phone>/del", methods=['GET', 'POST'])
def employee_delete(botusername, phone):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    dao.delete_employee(phone, botusername)
    url = '/employee_list/' + botusername
    return redirect(url)


@app.route("/employee/<botusername>/<phone>/upd", methods=['GET', 'POST'])
def employee_update(botusername, phone):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        dao.update_employee(request.form['name'], request.form['phone'], request.form['specialization'], request.form['employee_id'],  request.form['info'], request.form['photo'], bot_username=botusername)
        url = '/employee_list/' + botusername
        return redirect(url)
    else:
        employee = dao.get_employee_by_phone(phone, botusername)
        return render_template('/employee_update.html', employee= employee)



@app.route("/employee/<botusername>/<phone>/del_reg", methods=['GET', 'POST'])
def employee_delete_reg(botusername, phone):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    dao.delete_employee(phone, botusername)
    url = '/employee_list_reg/' + botusername
    return redirect(url)


@app.route("/employee/<botusername>/<phone>/upd_reg", methods=['GET', 'POST'])
def employee_update_reg(botusername, phone):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        dao.update_employee(request.form['name'], request.form['phone'], request.form['specialization'], request.form['employee_id'],  request.form['info'], request.form['photo'], bot_username=botusername)
        url = '/employee_list_reg/' + botusername
        return redirect(url)
    else:
        employee = dao.get_employee_by_phone(phone, botusername)
        return render_template('/employee_update.html', employee= employee)

@app.route("/login/<botusername>/<int:id>/<first_name>/<last_name>", methods=['POST', 'GET'])
def login(botusername, id, first_name, last_name):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; id_user='{id}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
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
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; id_user='{id}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")

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
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; id_user='{id}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        photo = request.files['photo']  # Отримуємо завантажений файл з форми
        if photo:
            filename = botusername + '_' + str(id) +'_' + photo.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filepath)
            selected_options = request.form.getlist('multiSelect')
            if len(selected_options)>0:
                dao.update_employee_service(phone,selected_options,botusername)
            print(selected_options)
            filename = secure_filename(photo.filename)
            photo.save(filename)
            dao.update_employee(request.form['name'], request.form['phone'], request.form['specialization'],
                                           employee_id=id, info=request.form['about'], photo=filename, email=request.form['email'], bot_username=botusername)
        else:
            dao.update_employee(request.form['name'], request.form['phone'], request.form['specialization'],
                                id, request.form['about'], request.form['photo'], request.form['email'], botusername)
    employee = dao.get_employee_by_phone(phone, botusername)
    all_service = dao.get_service(botusername)
    my_service = dao.get_employee_service(phone, botusername)
    print(my_service)
    if my_service==None:
        my_service=[]
    return render_template('profile.html', employee= employee, botusername= botusername, all_service=all_service, my_service= my_service)


@app.route("/timesettings/<botusername>/<phone>", methods=['POST', 'GET'])
def timesettings(botusername, phone):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        if 'secondShiftCheckbox' in request.form.keys():
            dao.create_time_settings(phone, is_two_graph=request.form['secondShiftCheckbox'], start_time=request.form['firstShiftStart'], end_time=request.form['firstShiftEnd'], start_time_two=request.form['secondShiftStart'], end_time_two=request.form['secondShiftEnd'], bot_username=botusername)
        else:
            dao.create_time_settings(phone, is_two_graph='off',
                                     start_time=request.form['firstShiftStart'], end_time=request.form['firstShiftEnd'],
                                    bot_username=botusername)
        return redirect('/calendar_month/'+ botusername + "/" + phone)
    else:
        return render_template('time_settings.html', botusername=botusername)


@app.route("/calendar_month/<botusername>/<phone>/2", methods=['POST', 'GET'])
def calendar_month_two(botusername, phone):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        template_month, dater = ut.generate_weekly_schedule_template(request.form['selected-dates'])
        json_string = json.dumps(template_month)
        template_month = ut.generate_weekly_schedule_template(request.form['selected-dates'])
        dao.update_wekly_settings_two(phone, dater, template_two=json_string,  bot_username=botusername)
        return redirect('/schedule/'+botusername+'/'+phone)
    else:
        return render_template('calendar_month.html', botusername=botusername, text='Заповність всій календар на 4 тижні по другій зміні')

@app.route("/calendar_month/<botusername>/<phone>", methods=['POST', 'GET'])
def calendar_month(botusername, phone):
    session['botusername'] = botusername
    if 'history' in session:
        history = session['history']
        history.append(request.endpoint)
    else:
        history = [request.endpoint]
    session['history'] = history
    path = '/'.join(history)
    logging.info(f"botusername='{botusername}'; path='{path}';  user_agent='{request.user_agent}'; ip={request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}")
    if request.method == "POST":
        template_month, dater = ut.generate_weekly_schedule_template(request.form['selected-dates'])
        json_string = json.dumps(template_month)
        dao.create_wekly_settings(phone, dater, template_one=json_string,  bot_username=botusername)
        time_setting = dao.get_time_settings(phone, botusername)
        if time_setting[1]=='off':
            return render_template('exit.html', botusername=botusername)
        else:
            return redirect('/calendar_month/'+ botusername + "/" + phone + "/2")
    else:
        return render_template('calendar_month.html', botusername=botusername, text='Заповність всій календар на 4 тижні по першій зміні')







booked_slots = {
        (9, '2023-08-20'): {"name": "Jane Smith", "phone": "38034034444"},

        (10, '2023-08-21'): {"name": "Jane Smith", "phone": "38034034444"}
        # Add more booked slots here
    }
@app.route('/schedule/<botusername>/<phone>', methods=['POST', 'GET'])
def schedule(botusername, phone):
    date = datetime.today()
    date_next = date + timedelta(days=1)
    date_plus = date_next + timedelta(days=1)
    data_str = date.strftime('%Y-%m-%d')
    data_next_str = date_next.strftime('%Y-%m-%d')
    data_plus_str = date_plus.strftime('%Y-%m-%d')
    dates = [data_str, data_next_str, data_plus_str]
    print(dates)
    format_dates = [ut.get_format_date(data_str), ut.get_format_date(data_next_str), ut.get_format_date(data_plus_str)]
    employee_service = dao.get_employee_service(phone, botusername)
    time_settings = dao.get_time_settings(phone, botusername)
    day_settings = dao.get_wekly_settings(phone, botusername)
    records = dao.get_user_books_by_employee(phone, botusername)
    all_service = dao.get_service(botusername)
    ph, two_schedule, start, end, start_2, end2, _ = time_settings
    if two_schedule=='on':
        start_day_hour = min(int(start[:2]), int(start_2[:2]))
        end_day_hour = max(int(end[:2]), int(end2[:2]))
    else:
        start_day_hour = int(start[:2])
        end_day_hour = int(end[:2])
    print('employee_service', employee_service)
    print('time_settings', time_settings)
    print('day_settings', day_settings)
    print('records', records)


    if request.method == 'POST':
        selected_slot = request.form.get('selectedSlot')
        patient_name = request.form.get('patientName')
        patient_day = request.form.get('appointmentDay')
        patient_hour = request.form.get('appointmentTime')
        patient_service = request.form.get('service')
        patient_hour = int(patient_hour)
        patient_day = int(patient_day)
        booked_slots[(patient_day,patient_hour)] = patient_name
        # Отримання дати та часу з обраного слоту
        print(patient_name)
        if selected_slot and patient_name:
            print(f"Slot {selected_slot} booked by {patient_name}")
    print(booked_slots)
    return render_template('schedule.html', booked_slots=booked_slots, botusername= botusername, phone=phone, start_day_hour=start_day_hour, end_day_hour=end_day_hour, format_dates=format_dates, dates = dates, all_service= all_service)



@app.route('/schedule/<botusername>/<phone>/<date>', methods=['POST', 'GET'])
def schedule_day(botusername, phone, date):
    date = datetime.strptime(date, '%Y-%m-%d')
    date_next = date + timedelta(days=1)
    date_plus = date_next + timedelta(days=1)
    data_str = date.strftime('%Y-%m-%d')
    data_next_str = date_next.strftime('%Y-%m-%d')
    data_plus_str = date_plus.strftime('%Y-%m-%d')
    format_dates = [ut.get_format_date(data_str), ut.get_format_date(data_next_str), ut.get_format_date(data_plus_str)]
    employee_service = dao.get_employee_service(phone, botusername)
    time_settings = dao.get_time_settings(phone, botusername)
    day_settings = dao.get_wekly_settings(phone, botusername)
    records = dao.get_user_books_by_employee(phone, botusername)

    ph, two_schedule, start, end, start_2, end2, _ = time_settings
    if two_schedule=='on':
        start_day_hour = min(int(start[:2]), int(start_2[:2]))
        end_day_hour = max(int(end[:2]), int(end2[:2]))
    else:
        start_day_hour = int(start[:2])
        end_day_hour = int(end[:2])
    print('employee_service', employee_service)
    print('time_settings', time_settings)
    print('day_settings', day_settings)
    print('records', records)


    if request.method == 'POST':
        selected_slot = request.form.get('selectedSlot')
        patient_name = request.form.get('patientName')
        patient_day = request.form.get('appointmentDay')
        patient_hour = request.form.get('appointmentTime')
        patient_service = request.form.get('service')
        patient_hour = int(patient_hour)
        patient_day = int(patient_day)
        booked_slots[(patient_day,patient_hour)] = patient_name
        # Отримання дати та часу з обраного слоту
        print(patient_name)
        if selected_slot and patient_name:
            print(f"Slot {selected_slot} booked by {patient_name}")
    print(booked_slots)
    return render_template('schedule.html', booked_slots=booked_slots, botusername= botusername, phone=phone, start_day_hour=start_day_hour, end_day_hour=end_day_hour, format_dates=format_dates)


@app.route('/schedule/<botusername>/<phone>/del', methods=['POST'])
def schedule_action(botusername, phone):
    if request.method == 'POST':
        patient_day = request.form.get('appointmentDay')
        patient_hour = request.form.get('appointmentTime')
        print("patient_day", patient_day)
        print("patient_hour", patient_hour)
        patient_hour = int(patient_hour)
        patient_day = int(patient_day)
        selected_slot = (patient_day, patient_hour)
        if selected_slot in booked_slots:
            del booked_slots[selected_slot]
            print(f"Slot {selected_slot} deleted")
        # Додайте реалізацію для інших дій
    return redirect('/schedule')


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


@app.route('/temp')
def index_temp():
    return render_template('temptemp.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return "File uploaded successfully"


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



