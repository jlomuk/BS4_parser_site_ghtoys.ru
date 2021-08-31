import json

from settings import DIRECTORY_FOR_DATA


def store_datadict_to_json(datadict):
    """Сохраняет данные в json в папке из переменной DIRECTORY_FOR_DATA"""
    with open(f'{DIRECTORY_FOR_DATA}/data.json', 'w', encoding='utf8') as file:
        json.dump(datadict, file, indent=4, ensure_ascii=False)
