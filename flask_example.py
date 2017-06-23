import time
import sqlite3
from flask import Flask, render_template, request

conn = sqlite3.connect('db.db')

c = conn.cursor()

app = Flask(__name__)


def check_exist(login):
    query = 'SELECT * from users where login = "{}"'.format(login)
    c.execute(query)
    result = c.fetchone()
    if result is None:
        return False
    else:
        return True

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login','')
        password = request.form.get('password','')
        if login == '' or password == '':
            return "Try again pls!"
        asd = 'SELECT * FROM users where login = "" UNION SELECT * from users limit 1 -- " and password = "123"'
        query = 'SELECT * FROM users where login = "{}" and password = "{}"'.format(login,password)
        print(query)
        c.execute(query)
        user = c.fetchone()
        if user is None:
            return "Bad credits"
        else:
            return render_template('name.html',username=user[1])

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        login = request.form.get('login','')
        password = request.form.get('password','')
        if login == '' or password == '':
            return "Try again pls!"
        if check_exist(login):
            return "User with this login already exist"

        insert_query = 'INSERT INTO users (login,password) VALUES ("{}","{}")'.format(
            login,password
        )
        c.execute(insert_query)
        conn.commit()
        return "Succes"

@app.route('/name')
def namepage():
    nm = request.args.get('username', 'Кто-то')
    if nm == '':
        nm = 'Кто-то'
    tm = time.strftime("%a, %d %b %Y",time.gmtime())
    return render_template('name.html', username=nm,time=tm)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    init_query = 'CREATE TABLE IF NOT EXISTS users(id  integer NOT NULL PRIMARY KEY AUTOINCREMENT,login text,password text)'
    c.execute(init_query)
    conn.commit()
    app.run()

