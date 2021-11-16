from app import app
from flask import render_template, request, json
from mysql.connector import connect,Error
import redshift_connector
import pymssql
import time

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/querypage')
def querypage():
    return render_template('querypage.html',output = {}, time_elapsed = '-')

def mysqlquery(subject):
    try:
        with connect(
            host = 'database-1.caytflhlgy1t.us-east-2.rds.amazonaws.com',
            port = '3306',
            user = 'admin',
            database ='instacartNormalised',
            password = 'rutgers21'
        ) as connection:
            with connection.cursor() as cursor:
                start = time.time()
                cursor.execute(subject)
                result = cursor.fetchall()
                result.insert(0,cursor.column_names)
                end = time.time()
                time_elapsed = end - start
                return result,time_elapsed
    except Error as e:
        print(e)

def mssqlquery(subject):
    try:
        conn = pymssql.connect('database-2.caytflhlgy1t.us-east-2.rds.amazonaws.com', 'admin', 'rutgers21', 'adnimerge')
        cursor: pymssql.Cursor = conn.cursor(as_dict=True)
        start = time.time()
        cursor.execute(subject)
        result = cursor.fetchall()
        end = time.time()
        time_elapsed = end - start
        return result, time_elapsed
    except Error as e:
        print(e)

def redshiftquery(subject):
    try:
        conn = redshift_connector.connect(
                host = 'project1-redshift.chxau5c0xldf.us-east-2.redshift.amazonaws.com',
                port = 5439,
                user = 'awsuser',
                database ='dev',
                password = 'Rutgers21'
            )
        cursor: redshift_connector.Cursor = conn.cursor()
        start = time.time()
        cursor.execute(subject)
        result = cursor.fetchall()
        end = time.time()
        time_elapsed = end - start
        return result, time_elapsed
    except redshift_connector.Error as e:
        print(e)

@app.route('/submitquery', methods=['POST'])
def submitquery():
    if request.method == 'POST':
        req = request.get_json()
        dbms = req['dbms']
        subject = req['subject']
        if dbms == 'MySQL':
            result, time_elapsed = mysqlquery(subject)
        elif dbms == 'RedShift':
            result, time_elapsed = redshiftquery(subject)
        else:
            result, time_elapsed = mssqlquery(subject)
    return json.jsonify(output = result, time_elapsed = str(time_elapsed))
