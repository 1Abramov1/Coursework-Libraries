from datetime import datetime, timedelta

import pandas as pd
from typing import Optional


import functools

# Декоратор, который принимает имя файла в качестве параметра
def save_to_file_with_name(filename):  # Параметр filename
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, "a", encoding="utf-8") as f:
                f.write(str(result) + "\n")
            return result
        return wrapper
    return decorator

@save_to_file_with_name("custom_report.txt")
def spending_by_category(transactions: pd.DataFrame,
                             category: str,
                             date: Optional[str] = None) -> dict:
    """
    Возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)

    if not pd.api.types.is_datetime64_any_dtype(transactions["Дата платежа"]):
        transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)

    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата платежа"] >= start_date.strftime("%Y-%m-%d"))
        & (transactions["Дата платежа"] <= end_date.strftime("%Y-%m-%d"))
        ]
    expenses_by_category = filtered_transactions.groupby("Категория")["Сумма операции с округлением"].sum()
    result = expenses_by_category.to_dict()
    return result


    # print(transactions)
    # print(category, date)
    # return {"start_date": start_date}

