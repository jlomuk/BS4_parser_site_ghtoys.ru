import json


def store_datadict_to_json(datadict):
    """Сохраняет данные в json  в папке files"""
    with open('files/data.json', 'w', encoding='utf8') as file:
        json.dump(datadict, file, indent=4, ensure_ascii=False)
