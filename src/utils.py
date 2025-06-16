import json
from datetime import datetime
from datetime import timedelta
from typing import Any, Dict, List
from requests.models import Response

import pandas as pd
import requests
from pandas import DataFrame

from src.config import API_KEY_CURRENCIES
from src.config import API_KEY_STOCKS
from src.config import URL_Currense
from src.config import URL_Stocks
from src.logger_config import get_logger

logger = get_logger("utils")


def get_time_for_greeting(date_time: str) -> str:
    """Функция возвращает приветствие в зависимости от текущего времени (входной параметр не влияет на приветствие)"""
    current_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_data_time(date_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]:
    """Возвращает начало месяца и переданную дату в формате DD.MM.YYYY HH:MM:SS"""
    dt = datetime.strptime(date_time, date_format)

    start_of_month = dt.replace(day=1)

    formatted_start_of_month = start_of_month.strftime("%d.%m.%Y %H:%M:%S")
    formatted_date_time = dt.strftime("%d.%m.%Y %H:%M:%S")

    return [formatted_start_of_month, formatted_date_time]


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

    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    return sorted_df


def get_card_with_spend(sorted_df: DataFrame) -> list[dict[str, Any]]:
    """
    Функция принимает DataFrame и возвращает список карт с расходами
    """
    card_spent_transactions = []

    # Фильтруем только операции с расходами (отрицательные значения)
    expenses_df = sorted_df[sorted_df["Сумма операции"] < 0].copy()

    # Группируем по номеру карты и суммируем показатели
    grouped = (
        expenses_df.groupby("Номер карты").agg({"Сумма операции с округлением": "sum", "Кэшбэк": "sum"}).reset_index()
    )

    # Создаем список словарей с агрегированными данными
    for _, row in grouped.iterrows():
        last_digits = str(row["Номер карты"]).replace("*", "")
        total_spent = abs(row["Сумма операции с округлением"])
        cashback = row["Кэшбэк"]

        card_row = {
            "last_digits": last_digits,
            "total_spent": total_spent,
            "cashback": cashback,
        }
        card_spent_transactions.append(card_row)

    return card_spent_transactions


def get_top_transactions(sorted_df: DataFrame, get_top: int) -> List[Dict[str, str]]:
    """
    Функция принмает DataFrame и возвращает get_top Топ-транзакций по sum платежа
    """
    top_pay_transactions: List[Dict[str, str]] = []
    sorted_pay_df = sorted_df.sort_values(by="Сумма операции", ascending=False)
    top_transactions = sorted_pay_df.head(get_top)
    top_transactions_sorted = top_transactions[["Дата платежа", "Сумма операции", "Категория", "Описание"]]

    for index, row in top_transactions_sorted.iterrows():
        transaction = {
            "date": f"{row['Дата платежа']}",
            "amount": f"{row['Сумма операции']}",
            "category": f"{row['Категория']}",
            "description": f"{row['Описание']}",
        }
        top_pay_transactions.append(transaction)
    logger.info("возвращает топ-транзакций по sum платежа")
    return top_pay_transactions


def get_currency(path_to_json: str) -> list[dict[str, str]]:
    """
    Функция принимает на вход переменную path_to_json и возвращает Курс-валют
    """
    currency_rates: list[dict[str, str]] = []
    with open(path_to_json, "r", encoding="utf-8") as file:
        data: Dict[str, Any] = json.load(file)
        currences = data["user_currencies"]

        for currence in currences:
            params = {"amount": 1, "from": f"{currence}", "to": "RUB"}
            headers = {"apikey": f"{API_KEY_CURRENCIES}"}
            response = requests.request("GET", URL_Currense, headers=headers, params=params)

            status_code = response.status_code
            if status_code == 200:
                result = response.json()
                currency_code_response = result["query"]["from"]
                currency_amount = round(result["result"], 2)
                currency_rates.append(
                    {
                        "currency": f"{currency_code_response}",
                        "rate": f"{currency_amount}",
                    }
                )

        return currency_rates


def get_stock(path_to_json: str) -> list[dict]:
    """Функция принимает файл json и выдает список словарей
    с содержанием акций и их актуальной стоимостью
    """
    stock_rates = []
    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        stocks = data["user_stocks"]

        for stock in stocks:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": f"{stock}",
                "apikey": f"{API_KEY_STOCKS}",
            }

            response = requests.request("GET", URL_Stocks, params=params)
            status_code = response.status_code
            if status_code == 200:
                result = response.json()
                print(result)
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            if "Time Series (Daily)" in result:
                if yesterday in result["Time Series (Daily)"]:
                    stock_response = result["Time Series (Daily)"][yesterday]["1. open"]
                    stock_rates.append({f"{stock}": f"{stock_response}"})
                else:
                    print(f"Дата {yesterday} отсутствует в ответе API для {stock}")
            else:
                print("Key 'Time Series (Daily)' not found in the API response")

    return stock_rates
