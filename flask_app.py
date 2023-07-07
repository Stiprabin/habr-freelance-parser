from aiogram import executor
from telegram.bot import dp, on_startup, on_shutdown
from flask import Flask
from threading import Thread


app = Flask(__name__)


def run():
    app.run(host="0.0.0.0", port=80)


@app.route('/')
def home():
    return "И чёрт умеет иной раз сослаться на священное писание."


# запустить бота и веб-приложение в отдельном потоке
if __name__ == "__main__":
    thread = Thread(target=run)
    thread.start()

    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )
