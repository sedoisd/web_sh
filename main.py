import datetime

from flask import Flask, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)


def main():
    app.run(port=8000, host='127.0.0.1')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    main()