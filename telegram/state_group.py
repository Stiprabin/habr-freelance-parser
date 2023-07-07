from aiogram.dispatcher.filters.state import StatesGroup, State


'''
state.proxy() as data:

data['args']
data['markers']
data['message']
data['query']
data['text']
data['index']
'''


# группа состояний для поиска заказов
class OrdersGroup(StatesGroup):
    args = State()
    query = State()
    message = State()
