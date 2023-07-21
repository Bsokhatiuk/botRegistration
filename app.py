from flask import Flask, render_template, request,redirect
import dao.modelDao as dao
import asyncio
dao.db_start()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/exit", methods=['POST', 'GET'])
def exit():
    return render_template('exit.html')


@app.route("/stepform", methods=['POST', 'GET'])
def stepform():
    if request.method == "POST":
        org_name = request.form['org_name']
        mobile = request.form['mobile']
        city = request.form['city']
        street = request.form['street']
        house = request.form['house']
        password = request.form['password']
        dao.create_admin(123, org_name, mobile, password)
        return redirect('/exit')
    else:
        return render_template('stepform.html')


@app.route("/createservice", methods=['POST', 'GET'])
def createservice():
    if request.method == "POST":
        dao.create_service(request.form['service_name'], request.form['service_price'])
        service_list = dao.get_service()
        return render_template('service_list.html', service_list=service_list)
    else:
        return render_template('createservice.html')

@app.route("/service_list", methods=['GET'])
def service_list():
    service_list = dao.get_service()
    return render_template('service_list.html', service_list=service_list)

@app.route("/service/<int:id>/del", methods=['GET', 'POST'])
def service_delete(id):
    dao.delete_service(id)
    service_list = dao.get_service()
    return render_template('service_list.html', service_list=service_list)

@app.route("/service/<int:id>/upd", methods=['GET', 'POST'])
def service_update(id):
    if request.method == "POST":
        dao.update_service(request.form['service_id'], request.form['service_name'], request.form['service_price'])
        service_list = dao.get_service()
        return render_template('/service_list.html', service_list=service_list)
    else:
        service = dao.get_service_one(id)
        return render_template('/serviceupdate.html', service= service)


@app.route("/serviceupdate", methods=['GET', 'POST'])
def service_update_bd():
    if request.method == "POST":
        dao.update_service(request.form['service_id'], request.form['service_name'], request.form['service_price'])
        service_list = dao.get_service()
        return render_template('/service_list.html', service_list= service_list)
    return render_template('serviceupdate.html')


@app.route("/employeecreate", methods=['POST', 'GET'])
def createemployee():
    if request.method == "POST":
        dao.create_employee(request.form['name'], request.form['phone'], request.form['specialization'])
        employee_list = dao.get_employee_all()
        return render_template('employee_list.html', employee_list=employee_list)
    else:
        return render_template('employeecreate.html')


@app.route("/employee_list", methods=['POST', 'GET'])
def employee_list():
    employee_list = dao.get_employee_all()
    return render_template('employee_list.html', employee_list=employee_list)

@app.route("/employee/<phone>/del", methods=['GET', 'POST'])
def employee_delete(phone):
    dao.delete_employee(phone)
    employee_list = dao.get_employee_all()
    return render_template('employee_list.html', employee_list=employee_list)


@app.route("/employee/<phone>/upd", methods=['GET', 'POST'])
def employee_update(phone):
    if request.method == "POST":
        print(request.form['employee_id'])
        dao.update_employee(request.form['name'], request.form['phone'], request.form['specialization'], request.form['employee_id'],  request.form['info'], request.form['photo'])
        employee_list = dao.get_employee_all()
        return render_template('/employee_list.html', employee_list=employee_list)
    else:
        employee = dao.get_employee_by_phone(phone)
        return render_template('/employee_update.html', employee= employee)
if __name__=="__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)



