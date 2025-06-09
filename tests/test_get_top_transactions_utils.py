import pytest
import pandas as pd
from pandas import DataFrame
from src.utils import get_top_transactions

def test_get_top_transactions_basic():
    """Тестирование базовой функциональности - возврат top_n транзакций"""
    # Создаем тестовый DataFrame
    data = {
        "Дата платежа": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "Сумма операции": [100, 500, 300],
        "Категория": ["A", "B", "C"],
        "Описание": ["Test1", "Test2", "Test3"]
    }
    df = pd.DataFrame(data)

    # Вызываем функцию
    result = get_top_transactions(df, 2)

    # Проверяем результаты
    assert len(result) == 2
    assert result[0]["amount"] == "500"  # Самая крупная транзакция
    assert result[1]["amount"] == "300"  # Вторая по величине
    assert result[0]["date"] == "2023-01-02"
    assert result[0]["category"] == "B"


def test_get_top_transactions_more_than_available():
    """Тест, когда запрашиваем больше транзакций, чем есть в данных"""
    data = {
        "Дата платежа": ["2023-01-01", "2023-01-02"],
        "Сумма операции": [100, 500],
        "Категория": ["A", "B"],
        "Описание": ["Test1", "Test2"]
    }
    df = pd.DataFrame(data)

    result = get_top_transactions(df, 5)

    assert len(result) == 2  # Должны вернуть все имеющиеся транзакции
    assert result[0]["amount"] == "500"


def test_get_top_transactions_zero_top():
    """Тест с запросом 0 транзакций"""
    data = {
        "Дата платежа": ["2023-01-01"],
        "Сумма операции": [100],
        "Категория": ["A"],
        "Описание": ["Test1"]
    }
    df = pd.DataFrame(data)

    result = get_top_transactions(df, 0)

    assert len(result) == 0
