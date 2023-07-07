from aiogram import executor
from telegram.bot import dp, on_startup, on_shutdown
from fastapi import FastAPI


app = FastAPI()


# запуск бота
@app.on_event("startup")
async def home():
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )
