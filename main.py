from flask import Flask, render_template, request, make_response, redirect, session, render_template_string, config
import sqlite3
from hashlib import md5
import os

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
    id = session.get('id', None)
    return render_template('user.html', username=usr, id=id)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/template/<data>')
def injection(data):
    string = 'User data is {}'.format(data)
    return render_template_string(string)

@app.route('/file')
def send_file():
    filename = request.args.get('file', None)
    if '..' in filename:
        return "STOP HACKING ME YOU FOOL"
    if filename is None:
        return "No such file"
    path = os.path.abspath(os.path.dirname(__file__))
    path = path + '/files/' + filename
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data



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


@app.route('/delete', methods=['POST'])
def delete():
    u_id = session.get('id', None)
    if u_id is None:
        return "Need to login"
    query = "DELETE FROM users WHERE id = ?"
    print("User id is ", u_id)
    db.execute(query, [u_id])
    conn.commit()
    session.pop('id')
    session.pop('username')
    return "User deleted"


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


@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    init_query = 'CREATE TABLE IF NOT EXISTS users(id  integer NOT NULL PRIMARY KEY AUTOINCREMENT,login text,password text)'
    db.execute(init_query)
    conn.commit()
    app.run(port=5001)
