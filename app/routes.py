from app import app
from flask import render_template
from flask import request,redirect
from mysql.connector import connect,Error

def Convert(tup, di):
    for a, b in tup:
        di.setdefault(a, []).append(b)
    return di

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/querypage')
def querypage():
    return render_template('querypage.html',output = '')

def mysqlquery(subject):
    try:
        with connect(
            host = 'database-1.caytflhlgy1t.us-east-2.rds.amazonaws.com',
            port = '3306',
            user = 'admin',
            database ='instacart',
            password = 'rutgers21'
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(subject)
                output = {}
                Convert(cursor.fetchall(),output)
                return output
    except Error as e:
        print(e)

@app.route('/submitquery', methods=['POST'])
def submitquery():
    if request.method == 'POST':
        req = request.form
        dbms = req['dbms']
        subject = req['subject']
        if dbms == 'MySQL':
            result = mysqlquery(subject)
        else:
            print('RedShift')
    return render_template('querypage.html',output = result)
