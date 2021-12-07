from app import app
from flask import render_template, request, json
from mysql.connector import connect,Error
import redshift_connector
import pymssql
import pyodbc
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

def mongoquery(subject):
    try:    
        con = pyodbc.connect('DRIVER={Devart ODBC Driver for MongoDB};'
                                            'Server=127.0.0.1;'
                                            'Port=27017;'
                                            'Database=adnimerge')
        start = time.time()
        cursor = con.cursor()
        cursor.execute(subject)
        result = cursor.fetchall()
        end = time.time()
        time_elapsed = end - start
        data = []
        columns = [column[0] for column in cursor.description]
        data.append(columns) 
        for row in result:
            data.append(list(row))
        return data, time_elapsed
    except pyodbc.Error as e:
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
        elif dbms == 'MSSQL':
            result, time_elapsed = mssqlquery(subject)
        else:
            result, time_elapsed = mongoquery(subject)
    return json.jsonify(output = result, time_elapsed = str(time_elapsed))
