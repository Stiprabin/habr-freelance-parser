from flask import Flask
from threading import Thread


# веб-приложение
app = Flask(__name__)


@app.route('/')
def home():
    return "И чёрт умеет иной раз сослаться на священное писание."


def run():
    app.run(host="0.0.0.0", port=80)


# запуск веб-приложения в отдельном потоке
def flask_thread():
    thread = Thread(target=run)
    thread.start()
