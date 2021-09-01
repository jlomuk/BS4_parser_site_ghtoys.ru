import aiohttp
import asyncio
from bs4 import BeautifulSoup

from core.data_store_methods import store_datadict_to_json
from core.exceptions import NoPageToParse
from core.fields_for_parsing import get_name_product, get_code_product, get_descriptions, get_price
from settings import URL

DATADICT = []


async def get_page_html(session, url):
    """Получение контента страницы по url адресу.
    Возвращает страницу в текстовом виде. При 404 выкидывает исключение."""
    async with session.get(url) as response:
        if response.status == 404:
            raise NoPageToParse(url=url)
        return await response.text()


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


async def create_parser_tast(url, session, page, datadict):
    html_text = await get_page_html(session, url)
    games_list = create_list_with_games_from_html_page(html_text)
    add_data_in_temp_dict(datadict, games_list)
    print(f'страница {page} -- парсинг завершен')
    print('------------------------------------')


async def start_parse():
    """Последовательно перебирает все позиции на каждой странице переданной категории категории."""
    tasks = []
    page = 24
    flag = True
    category = input('введите категорию из url сайта: ').strip()
    async with aiohttp.ClientSession() as session:
        while flag:
            url = URL.format(category, page)
            task = asyncio.create_task(create_parser_tast(url, session, page, DATADICT))
            tasks.append(task)
            if len(tasks) > 3:
                try:
                    await asyncio.gather(*tasks)
                except NoPageToParse as e:
                    flag = False
                    continue
                tasks = []
            page += 1
    store_datadict_to_json(DATADICT)
    print('Успешно завершено')


if __name__ == '__main__':
    asyncio.run(start_parse())
