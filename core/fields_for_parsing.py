from core.decorators import no_value_wrapper


@no_value_wrapper
def get_name_product(node):
    return node.find('a').text.strip()


@no_value_wrapper
def get_code_product(node):
    return node.select_one('.shop_article_value').text.strip()


@no_value_wrapper
def get_descriptions(node):
    return node.text.strip()


@no_value_wrapper
def get_price(node):
    return node.find_next_sibling('form').select_one('.shop_price').text.strip()
