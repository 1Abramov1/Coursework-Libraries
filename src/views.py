import json

from src.config import PATH_TO_XLSX, PATH_TO_JSON

from src.utils import (get_card_with_spend, get_currency, get_data_time,
                       get_path_and_period, get_stock, get_time_for_greeting,
                       get_top_transactions)


def main_info(date_time: str) -> dict:
    """
    Главная функция, принимающая на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращают JSON-ответ со следующими данными:
    2018-05-20 15:30:00
    """
    # Производится срез всего excel на нужный диапозон
    time_period = get_data_time(date_time)
    sorted_df = get_path_and_period(PATH_TO_XLSX, time_period)

    # 1. Приветствие
    greeting = get_time_for_greeting(date_time)

    # 2. Сортировка по каждой карте
    cards = get_card_with_spend(sorted_df)

    # 3. Топ-5 транзакций по сумме платежа.
    top_transactions = get_top_transactions(sorted_df, 5)

    # 4. Курс валют
    currency_rates = get_currency(PATH_TO_JSON)

    # 5. Стоимость акций из S&P 500
    stock_prices = get_stock(PATH_TO_JSON)

    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data
