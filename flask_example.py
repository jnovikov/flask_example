import time
from flask import Flask, render_template, request

app = Flask(__name__)


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
    app.run()
