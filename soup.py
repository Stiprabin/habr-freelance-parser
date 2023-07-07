from bs4 import BeautifulSoup
import requests
import random
import asyncio


# список с User-Agent'ами
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.4; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/114.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (iPad; CPU OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/114.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (iPod touch; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) FxiOS/114.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/114.0 Firefox/114.0',
    'Mozilla/5.0 (Android 13; Mobile; LG-M255; rv:114.0) Gecko/114.0 Firefox/114.0'
]


# список с адресами "первой страницы"
referer_list = [
    'https://duckduckgo.com/',
    'https://www.google.com/',
    'https://yandex.com/',
    'https://www.yahoo.com/',
    'https://mail.ru/',
    'https://www.bing.com/',
    'https://nigma.net.ru/',
    'https://www.rambler.ru/',
    'https://vk.com/'
]


# вернуть объект BeautifulSoup
async def get_soup(url):
    """
    200 -- запрос выполнен успешно
    429 -- отправлено слишком много запросов
    403 -- доступ запрещен
    503 -- сервер недоступен
    418 -- I’m a teapot
    """
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'Referer': random.choice(referer_list)
    }
    response = requests.get(url=url, headers=headers)

    # проверяем код ответа
    if response.status_code == 429:
        print("Отправлено слишком много запросов. Пойду посплю...")
        await asyncio.sleep(3)
        return await get_soup(url)

    elif response.status_code == 418:
        print("Я не могу приготовить вам кофе, потому что я чайник!")
        return "I’m a teapot"

    elif response.status_code != 200:
        print(f"Error: {response.status_code}. Пiшов нахрен, Iрис") # локальная шутка
        return "Error"

    soup = BeautifulSoup(response.text, "html.parser")
    return soup
