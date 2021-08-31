import requests
from bs4 import BeautifulSoup
from time import sleep
from requests.exceptions import ConnectionError

from core.data_store_methods import store_datadict_to_json
from core.exceptions import NoPageToParse
from core.fields_for_parsing import get_name_product, get_code_product, get_descriptions, get_price
from settings import URL


def get_page_html(url):
    """
    Получение контента страницы по url адресу.
    Возвращает страницу в текстовом виде. При 404 выкидывает исключение.
    """
    data_html = requests.get(url, allow_redirects=True)
    if data_html.status_code == 404:
        raise NoPageToParse
    return data_html.text


def create_list_with_games_from_html_page(html_text):
    """Возращает лист с всеми позициями игрушек на странице"""
    bs = BeautifulSoup(html_text, 'lxml')
    games_list = bs.select('.js_shop .item_info ')
    return games_list


def create_dict_with_detail_game(game):
    """Создает словарь с детальным описанием переданой игрушки из магазина"""
    return {
        'name': get_name_product(game),
        'code_product': get_code_product(game),
        'description': get_descriptions(game),
        'price': get_price(game),
    }


def add_data_in_temp_dict(datadict, games_list):
    """Аккумулирует все обработанные позиции в словаре"""
    for game in games_list:
        detail_game = create_dict_with_detail_game(game)
        datadict.append(detail_game)


def start_parse():
    """Последовательно перебирает все позиции на каждой странице категории. """
    page = 1
    datadict = []
    category = input('введите категорию из url сайта: ').strip()
    while True:
        url = URL.format(category, page)
        try:
            html_text = get_page_html(url)
        except ConnectionError:
            sleep(7)
            continue
        except NoPageToParse:
            break
        games_list = create_list_with_games_from_html_page(html_text)
        add_data_in_temp_dict(datadict, games_list)
        print(f'страница {page} -- парсинг завершен')
        print('------------------------------------')
        page += 1
    store_datadict_to_json(datadict)
    print('Успешно завершено')


if __name__ == '__main__':
    start_parse()
