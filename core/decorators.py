def no_value_wrapper(func):
    """Обертка в случаи отсутствия значения в описании товара"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError:
            return "НЕТ ЗНАЧЕНИЯ"

    return inner