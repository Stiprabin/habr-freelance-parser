from aiogram import types
from aiogram.dispatcher import FSMContext
from telegram import keyboards
from telegram.state_group import OrdersGroup
from parser import parser_habr
import math


# URL-адрес сервиса
URL = "https://freelance.habr.com"


# отправить сообщение с выбором условий
async def orders_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # условия и маркеры
        data['args'] = [
            '&only_mentioned=',
            '&only_with_price=',
            '&safe_deal=',
            '&only_urgent='
        ]
        data['markers'] = ['○' for i in range(4)]

        data['message'] = await message.answer(
            text="Выбери <b>условия</b> из предложенного списка:",
            reply_markup=keyboards.get_args_keyboard()
        )

    await OrdersGroup.args.set()


# обработать выбор
async def orders_args(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # функция выбора условия
        def set_arg(i):
            if data['args'][i][-1:] == '=':
                data['markers'][i] = '◉'
                data['args'][i] += '1'
            else:
                data['markers'][i] = '○'
                data['args'][i] = data['args'][i][:-1]

        match callback.data:

            case "mentioned":
                set_arg(0)
            case "price":
                set_arg(1)
            case "safe":
                set_arg(2)
            case "urgent":
                set_arg(3)

            # завершить выбор и запросить сообщения с ключевыми словами
            case "finish":
                await data['message'].edit_text(
                    text="Отправь сообщение с ключевыми словами, которые должны присутствовать в <b>описании заказов.</b>",
                    reply_markup=None
                )
                await OrdersGroup.query.set()
                return

        await data['message'].edit_reply_markup(reply_markup=keyboards.get_args_keyboard(data['markers']))


# получить ключевые слова и сгенерировать сообщение с заказами
async def orders_query(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # проблемы со списком с заказами
        async def orders_list_problem(txt):
            await data['message'].delete()
            await message.answer(
                text=txt,
                reply_markup=keyboards.menu_keyboard
            )
            await state.finish()

        # полученное сообщение
        data['query'] = message.text

        data['message'] = await message.answer(text="<b><em>⌛ Жестко ищу заказы...</em></b>",)

        # парсинг
        orders_list = await parser_habr(
            url=URL,
            query=data['query'],
            args=''.join(data['args'])
        )

        # выйти из функции и закрыть FSM, если произошла ошибка
        if orders_list == "Error":
            await orders_list_problem("<b>☢ Произошла ошибка!</b> Попробуй повторить запрос чуть позже.")
            return

        elif orders_list == "I’m a teapot":
            await orders_list_problem("<b>☕ Произошла катастрофа!</b> Я не могу приготовить вам кофе, потому что я чайник")
            return

        text = "<b>📢 Жестко нашел заказы:</b>\n\n"

        # есть ли заказы?
        if not orders_list:
            # выйти из FSM, если их нет
            await orders_list_problem("<b>📢 Нету таких заказов!</b>")
            return
        else:
            # преобразовать полученный список, если заказы есть
            counter = 0
            page = 1
            last_page = math.ceil((orders_list.index(orders_list[-1]) + 1) / 5)

            for order in orders_list:
                text += f"{order[0]}\n" \
                        f"<em>{order[1]}</em>\n" \
                        f"<b><u>{order[2]}</u></b>\n" \
                        f"<u>{order[3]}</u>\n\n"

                counter += 1

                # выйти из цикла, если заказ последний
                if orders_list[-1] == order:
                    break

                # добавить оглавление и номер страницы, если заказ кратен пяти по счету
                if counter == 5:
                    text += f"📖 <em><b>{page} из {last_page}</b></em>~<b>📢 Жестко нашел заказы:</b>\n\n"
                    page += 1
                    counter = 0

            # добавить номер последней страницы и разделить список заказов на страницы
            text += f"📖 <em><b>{last_page} из {last_page}</b></em>"
            text = text.split('~')

            data['text'] = text
            data['index'] = 0

            # отправить первую страницу заказов
            if len(text) == 1:
                await data['message'].delete()
                await message.answer(
                    text=data['text'][data['index']],
                    disable_web_page_preview=True,
                    reply_markup=keyboards.menu_keyboard
                )
                await state.finish()
                return
            else:
                await data['message'].delete()
                data['message'] = await message.answer(
                    text=data['text'][data['index']],
                    disable_web_page_preview=True,
                    reply_markup=keyboards.orders_keyboard
                )

        await OrdersGroup.message.set()


# callback-обработчик для сообщения с заказами
async def orders_message(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # изменить сообщение с заказами
        async def get_response_message():
            await data['message'].edit_text(
                text=data['text'][data['index']],
                disable_web_page_preview=True,
                reply_markup=keyboards.orders_keyboard
            )

        match callback.data:

            # назад
            case "back":
                data['index'] -= 1
                if data['index'] < 0: data['index'] = len(data['text']) - 1
                await get_response_message()

            # вперед
            case "forward":
                data['index'] += 1
                if data['index'] > len(data['text']) - 1: data['index'] = 0
                await get_response_message()

            # выйти из FSM
            case "leave":
                await data['message'].delete_reply_markup()
                await callback.message.answer(
                    text="<b>Поиск завершен!</b>",
                    reply_markup=keyboards.menu_keyboard
                )
                await state.finish()
