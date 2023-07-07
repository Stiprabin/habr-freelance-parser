from telegram.bot import start_bot
from fastapi import FastAPI
from threading import Thread


app = FastAPI()


# запуск бота
@app.on_event("startup")
async def home():
    thread = Thread(target=start_bot)
    thread.start()
