class NoPageToParse(Exception):
    """Ошибка выкидывается при исчерпании страниц для парсинга"""
    def __init__(self, url):
        self.url = url