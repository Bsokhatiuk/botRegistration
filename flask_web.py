from flask import Flask, render_template, request,redirect
import dao.modelDao as dao
import asyncio

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


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
        return redirect('/')
    else:
        return render_template('stepform.html')

if __name__=="__main__":
    dao.db_start()
    app.run(host="0.0.0.0", port=443, debug=True)



