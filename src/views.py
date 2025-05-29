import json
from typing import Dict, Any
from src.utils import get_time_for_greeting
from src.utils import get_data_time
from src.utils import get_path_and_period
from src.utils import get_card_with_spend, get_top_transactions, get_currency, get_stock

def main_info(date_time: str) -> Dict[str, Any] :
    """
        Главная функция, принимающая на вход строку с датой и временем в формате
        YYYY-MM-DD HH:MM:SS и возвращают JSON-ответ со следующими данными:
        2018-05-20 15:30:00
    """
    # Производится срез всего excel на нужный диапозон
    time_period = get_data_time(date_time)
    sorted_df = get_path_and_period("./data/operations.xlsx", time_period)

    # 1. Приветствие
    greeting = get_time_for_greeting(date_time)

    # 2. Сортировка по каждой карте
    cards = get_card_with_spend(sorted_df)

    # 3. Топ-5 транзакций по сумме платежа.
    top_transactions = get_top_transactions(sorted_df, 5)

    # 4. Курс валют
    currency_rates = get_currency("./data/user_settings.json")

    # 5. Стоимость акций из S&P 500
    stock_prices = get_stock("./data/user_settings.json")

    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data



