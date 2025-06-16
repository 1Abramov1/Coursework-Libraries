import json

from src.services import analise_cashback


def test_analise_cashback_valid_transactions():
    transactions = [
        {"Дата операции": "2023-05-15 12:00:00", "Категория": "Супермаркеты", "Сумма платежа": "-1000", "Кэшбэк": 50},
        {"Дата операции": "2023-05-20 14:30:00", "Категория": "АЗС", "Сумма платежа": "-5000", "Кэшбэк": 250},
    ]
    result = analise_cashback(transactions, 2023, 5)
    expected_result = {"Супермаркеты": 10, "АЗС": 50}
    assert json.loads(result) == expected_result


def test_analise_cashback_no_valid_transactions():
    transactions = [
        {"Дата операции": "2023-06-15 12:00:00", "Категория": "Супермаркеты", "Сумма платежа": "-1000", "Кэшбэк": 50},
        {"Дата операции": "2023-05-20 14:30:00", "Категория": "АЗС", "Сумма платежа": "5000", "Кэшбэк": 250},
    ]
    result = analise_cashback(transactions, 2023, 5)
    assert json.loads(result) == {}


def test_analise_cashback_invalid_transaction_format():
    transactions = [
        {"Дата операции": "invalid_date", "Категория": "Супермаркеты", "Сумма платежа": "-1000", "Кэшбэк": 50},
        {"Категория": "АЗС", "Сумма платежа": "-5000", "Кэшбэк": 250},
    ]
    result = analise_cashback(transactions, 2023, 5)
    assert json.loads(result) == {}


def test_analise_cashback_multiple_transactions_same_category():
    transactions = [
        {"Дата операции": "2023-05-15 12:00:00", "Категория": "Супермаркеты", "Сумма платежа": "-1000", "Кэшбэк": 50},
        {"Дата операции": "2023-05-20 14:30:00", "Категория": "Супермаркеты", "Сумма платежа": "-2000", "Кэшбэк": 100},
    ]
    result = analise_cashback(transactions, 2023, 5)
    expected_result = {"Супермаркеты": 30}
    assert json.loads(result) == expected_result


def test_analise_cashback_zero_cashback():
    transactions = [
        {"Дата операции": "2023-05-15 12:00:00", "Категория": "Супермаркеты", "Сумма платежа": "-1000", "Кэшбэк": 0}
    ]
    result = analise_cashback(transactions, 2023, 5)
    assert json.loads(result) == {}


def test_analise_cashback_positive_payment():
    transactions = [
        {"Дата операции": "2023-05-15 12:00:00", "Категория": "Супермаркеты", "Сумма платежа": "1000", "Кэшбэк": 50}
    ]
    result = analise_cashback(transactions, 2023, 5)
    assert json.loads(result) == {}


def test_analise_cashback_wrong_month():
    transactions = [
        {"Дата операции": "2023-06-15 12:00:00", "Категория": "Супермаркеты", "Сумма платежа": "-1000", "Кэшбэк": 50}
    ]
    result = analise_cashback(transactions, 2023, 5)
    assert json.loads(result) == {}


def test_analise_cashback_empty_transactions():
    result = analise_cashback([], 2023, 5)
    assert json.loads(result) == {}
