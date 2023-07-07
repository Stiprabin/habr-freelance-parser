from aiogram import types
from telegram import keyboards


# старт
async def start_command(message: types.Message):
    text = f"<b>Здравствуй, <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>!</b>\n" \
            "Нажми на кнопку ниже, чтобы начать <b>поиск заказов</b>.\n" \
            "Для <b>помрщи</b> используй команду <b>/help</b>.\n"

    await message.answer_sticker(sticker="CAACAgIAAxkBAAEJiZJknf8WjwUeaq2dVCyusAsMweNklwACPyEAAn-wiEmxERO4oCPyAS8E")
    await message.answer(
        text=text,
        reply_markup=keyboards.menu_keyboard
    )


# помрщь
async def help_command(message: types.Message):
    text = "Данный бот — <b>парсер сервиса <a href='https://freelance.habr.com/'>Хабр Фриланс</a></b> для поиска <b>удаленной работы.</b>\n" \
           "Используя его, ты можешь быстро найти подходящие тебе заказы. Чтобы <b>начать поиск</b>, нажми на кнопку ниже."

    await message.answer_sticker(sticker="CAACAgIAAxkBAAEJiY5knf7CfiCTjoB2tJroWbelEyiswAACYg0AA4cJSEASYJUYqZvJLwQ")
    await message.answer(
        text=text,
        disable_web_page_preview=True,
        reply_markup=keyboards.menu_keyboard
    )
