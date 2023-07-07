from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from handlers import commands, orders
from state_group import OrdersGroup
import logging
import config


# логирование
logging.basicConfig(level=logging.INFO)


# телеграм-бот
bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

dp.register_message_handler(commands.start_command, commands=['start'])
dp.register_message_handler(commands.help_command, commands=['help'])

dp.register_message_handler(orders.orders_text, Text(equals="Искать заказы", ignore_case=True))
dp.register_callback_query_handler(orders.orders_args, state=OrdersGroup.args)
dp.register_message_handler(orders.orders_query, state=OrdersGroup.query)
dp.register_callback_query_handler(orders.orders_message, state=OrdersGroup.message)


async def on_startup(_):
    print("Доверять другим -- это хорошо, но гораздо лучше не доверять.")


async def on_shutdown(_):
    logging.warning("Меня клонит в сон...")
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Прощай, мой юный друг!")
