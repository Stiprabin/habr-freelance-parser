from telegram.bot import start_bot
from fastapi import FastAPI
import asyncio


app = FastAPI()


# запуск бота
@app.on_event("startup")
async def home():
    asyncio.create_task(start_bot())
