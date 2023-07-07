# клавиатура для меню
menu_keyboard = {
    'resize_keyboard': True,
    'one_time_keyboard': True,
    'keyboard':
        [
            [{
                'text': 'Искать заказы'
            }]
        ]
    }


# клавиатура для сообщения с полученными заказами
orders_keyboard = {
    'inline_keyboard':
        [
            [
                {
                    'text': '« Назад',
                    'callback_data': 'back'
                },
                {
                    'text': 'Вперед »',
                    'callback_data': 'forward'
                }
            ],
            [{
                'text': 'Завершить поиск',
                'callback_data': 'leave'
            }]
        ]
    }


# клавиатура для выбора условий
def get_args_keyboard(markers=None):
    if markers is None: markers = ['○' for i in range(4)]
    return {
        'inline_keyboard':
            [
                [{
                    'text': f'{markers[0]} Только с отзывами',
                    'callback_data': 'mentioned'
                }],
                [{
                    'text': f'{markers[1]} Только с указанной ценой',
                    'callback_data': 'price'
                }],
                [{
                    'text': f'{markers[2]} Только с безопасной сделкой',
                    'callback_data': 'safe'
                }],
                [{
                    "text": f"{markers[3]} Только срочные",
                    "callback_data": "urgent"
                }],
                [{
                    'text': 'Завершить выбор',
                    'callback_data': 'finish'
                }]
            ]
        }
