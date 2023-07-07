from soup import get_soup


# удалить лишние пробелы
def remove_spaces(li):
    li = li.split()
    for i in li:
        if i == '':
            li.remove(i)
    return ' '.join(li)


async def parser_habr(url, query, args):

    print(f"Запрос \"{query}\" получен!")
    soup = await get_soup(url + "/tasks/?q=" + query + args)

    # выйти из цикла, если функция вернула Error или "I’m a teapot"
    if soup == "Error":
        return "Error"
    elif soup == "I’m a teapot":
        return "I’m a teapot"

    orders_href_list = []
    orders_list = []

    # получить последнюю страницу
    page_class = soup.find("div", {'class': 'pagination'})

    if page_class is None:
        page_last = 1
    else:
        page_last = int(page_class.find_all('a')[-2].text)

    # создать список со ссылками на заказы
    count = 1
    while count <= page_last:
        try:
            soup = await get_soup(url + f"/tasks/?q={query}&page={count}{args}")
            order_divs = soup.find_all("div", {'class': 'task__title'})

            for order_div in order_divs:
                orders_href_list.append(url + order_div.find('a').get('href'))

        except AttributeError:
            continue

        finally:
            count += 1

    print(f"Список с ссылками на заказы по запросу \"{query}\" создан!")

    # создать список с заказами
    for order_href in orders_href_list:
        try:
            soup = await get_soup(order_href)

            # название
            title = soup.find("h2", {'class': 'task__title'})
            title = remove_spaces(title.text)

            # цена
            price = soup.find("div", {'class': 'task__finance'}).find("span").text

            # дата-отклики-просмотры
            meta = soup.find("div", {'class': 'task__meta'})
            meta = remove_spaces(meta.text)

            # теги
            tags_list = soup.find_all('a', {'class': 'tags__item_link'})
            tags = ''
            for tag in tags_list:
                tags += '#' + tag.text.replace(' ', '_') + ' '

            # добавить заказ в список
            orders_list.append([
                title,
                meta,
                price,
                order_href
            ])

        except AttributeError:
            continue

    print(f"Список с заказами по запросу \"{query}\" создан!")
    return orders_list
