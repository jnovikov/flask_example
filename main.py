from flask import Flask, render_template, request, make_response, redirect, session
import sqlite3
from hashlib import md5

app = Flask(__name__)
app.secret_key = 'please change me on server'
conn = sqlite3.connect('example.db')
db = conn.cursor()


def hash_string(s):
    return md5(s).hexdigest()


def check_login(user):
    query = 'SELECT * FROM users WHERE login = "{}"'.format(user)
    db.execute(query)
    exist = db.fetchone()
    if exist is None:
        return False
    else:
        return True


@app.route('/user')
def user():
    usr = session.get('username', None)
    id = session.get('id',None)
    return render_template('user.html', username=usr, id=id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def log():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')
        if login == '' or password == '':
            return "Login or password is missing"

        password = hash_string(password)
        query = 'SELECT * FROM users WHERE login = ? and password = ?'
        db.execute(query, [login, password])
        result = db.fetchone()
        if result is None:
            return "No such user or password incorrect"
        session['username'] = result[1]
        session['id'] = result[0]
        return redirect('/user')


@app.route('/delete')
def delete():
    id = session.get('id',None)
    if id is None:
        return "Need to login"
    if check_login(session['username']):
        query = "DELETE FROM users WHERE id = '{}'".format(str(id))
        db.execute(query)
        conn.commit()
        session.pop('id')
        session.pop('username')
        return "User deleted"
    return "User not found"




@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')

        if login == '' or password == '':
            return "Login or password is missing"

        if check_login(login):
            return "This login already exist"

        password = hash_string(password)
        query = 'INSERT INTO users (login,password) VALUES ("{}","{}")'.format(login, password)
        db.execute(query)
        conn.commit()
        return "Success"


if __name__ == '__main__':
    init_query = 'CREATE TABLE IF NOT EXISTS users(id  integer NOT NULL PRIMARY KEY AUTOINCREMENT,login text,password text)'
    db.execute(init_query)
    conn.commit()
    app.run()


'eyJpZCI6MywidXNlcm5hbWUiOiIxMjMifQ.DDQEjQ.OcFfqKdjFw9mr2tOO3AUrKiIbmo'
'http://bit.ly/2tRn8Ff'
