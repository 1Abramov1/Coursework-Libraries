from datetime import datetime, timedelta
from pprint import pprint
import requests
from pandas import DataFrame
import pandas as pd
import json


URL_Currense = "https://api.apilayer.com/exchangerates_data/convert"
API_KEY_Currense = "lLSU3JdlytNTvWwQmNBichQwsDgssXUV"

URL_Stocks = "https://www.alphavantage.co/query"
API_KEY_Stocks = "RHOPUON4TD8ISUUV"

def get_time_for_greeting(date_time: str) -> str:
    """ Функция возвращает приветствие в зависимости от текущего времени """

    user_datetime_hour = datetime.now().hour
    if 5 <= user_datetime_hour < 12:
        return " Доброе утро"
    elif 12 <= user_datetime_hour < 18:
        return " Добрый день"
    elif 18 <= user_datetime_hour < 22:
        return " Добрый вечер"
    else:
        return " Доброй ночи"


def get_data_time(date_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]:
    dt = datetime.strptime(date_time, date_format)
    start_of_month = dt.replace(day=1)

    return [
        start_of_month.strftime("%d.%m.%Y %H:%M:%S"),
        dt.strftime("%d.%m.%Y %H:%M:%S")
    ]


def get_path_and_period(path_fo_file: str, period_date: list) -> DataFrame:
    """
        Функция принимает путь к Excel файлу и список дат,
        и возвращает таблицу в заданном периоде
    """
    df = pd.read_excel(path_fo_file, sheet_name="Отчет по операциям")

    print(pd.to_datetime(df["Дата операции"], dayfirst=True))
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")

    filtered_df = df[(df["Дата операции"] >= start_date) &
                  (df["Дата операции"] <= end_date)]
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    return sorted_df


def get_card_with_spend(sorted_df: DataFrame) -> list[dict]:
    """
        Функция принимает DataFrame и возвращает список карт с расходами
    """
    card_spent_transactions = []
    card_sorted = sorted_df[
        [
            "Номер карты",
            "Сумма операции",
            "Кэшбэк",
            "Сумма операции с округлением"
        ]
    ]
    for index, row in card_sorted.iterrows():
        print(index, row)
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"]).replace("*", "")
            total_spent = row["Сумма операции с округлением"]
            cashback = total_spent // 100
            row = {
                "last_digits": last_digits,
                "total_spent": total_spent,
                "cashback": cashback
            }
            card_spent_transactions.append(row)
    return card_spent_transactions


def get_top_transactions(sorted_df: DataFrame, get_top):
    """
       Функция принмает DataFrame и возвращает get_top Топ-транзакций по sum платежа
    """
    top_pay_transactions = []
    sorted_pay_df = sorted_df.sort_values(by="Сумма операции", ascending=False)
    top_transactions = sorted_pay_df.head(get_top)
    top_transactions_sorted = top_transactions[
        [
            "Дата платежа",
            "Сумма операции",
            "Категория",
            "Описание"
        ]
    ]

    for index, row in top_transactions_sorted.iterrows():
        transaction = {
          "date": f"{row['Дата платежа']}",
          "amount": f"{row['Сумма операции']}",
          "category": f"{row['Категория']}",
          "description": f"{row['Описание']}"
        }
        top_pay_transactions.append(transaction)

    return top_pay_transactions


def get_currency(path_to_json: str) -> list[dict]:
    """
       Функция принимает на вход переменную path_to_json и возвращает Курс-валют
    """
    currency_rates = []
    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        currences = data['user_currencies']

        for currence in currences:
            params = {
                "amount": 1,
                "from": f"{currence}",
                "to": "RUB"
            }
            headers = {
                "apikey": f"{API_KEY_Currense}"
            }
            response = requests.request("GET", URL_Currense, headers=headers, data=params)

            status_code = response.status_code
            if status_code == 200:
                result = response.json()
                currency_code_response = result["query"]["from"]
                currency_amount = round(result["result"], 2)
                currency_rates.append({
                  "currency": f"{currency_code_response}",
                  "rate": f"{currency_amount}"
                })

        return currency_rates


def get_stock(path_to_json: str) -> list[dict]:
    stock_rates = []
    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        stocks = data['user_stocks']

        for stock in stocks:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": f"{stock}",
                "apikey": f"{API_KEY_Stocks}"
            }

            response = requests.request("GET", URL_Stocks, params=params)
            status_code = response.status_code
            if status_code == 200:
                result = response.json()
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                stock_response = result["Time Series (Daily)"][yesterday]["1. open"]
                stock_rates.append({
                    f"{stock}": f"{stock_response}"
                })

    return stock_rates
