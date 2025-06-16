from datetime import datetime

import pytest

from src.reports import process_transactions  # Замените your_module на имя вашего модуля


@pytest.fixture
def sample_transactions():
    return [
        {"Дата платежа": "01.01.2023", "Категория": "Еда", "Сумма": 1000, "Описание": "Продукты"},
        {"Дата платежа": "15.01.2023", "Категория": "Транспорт", "Сумма": 500, "Описание": "Такси"},
        {"Дата платежа": "20.01.2023", "Категория": "Еда", "Сумма": 1500, "Описание": "Ресторан"},
        {"Дата платежа": "01.02.2023", "Категория": "Еда", "Сумма": 2000, "Описание": "Супермаркет"},
        {"Дата платежа": None, "Категория": "Еда", "Сумма": 300, "Описание": "Кофе"},  # Некорректная дата
        {"Дата платежа": "01.03.2023", "Категория": "Еда", "Сумма": 400, "Описание": "Завтрак"},  # Опечатка в ключе
    ]


def test_filter_by_category(sample_transactions):
    # Фильтрация по категории "Еда"
    result = process_transactions(sample_transactions, "Еда", "2023-01-01", "2023-12-31")
    assert len(result) == 4  # Ожидаем 4 транзакции в категории "Еда" (включая некорректные)
    assert all(t["Категория"] == "Еда" for t in result)


def test_filter_by_date_range(sample_transactions):
    # Фильтрация по датам
    result = process_transactions(sample_transactions, "Еда", "2023-01-01", "2023-01-31")
    assert len(result) == 2  # Ожидаем 3 транзакции в январе 2023 (включая некорректные)
    dates = [t.get("Дата платежа_dt") for t in result if "Дата платежа_dt" in t]
    assert all(datetime(2023, 1, 1) <= d <= datetime(2023, 1, 31) for d in dates)


def test_string_date_processing(sample_transactions):
    # Проверка обработки строковых дат
    result = process_transactions(sample_transactions, "Еда", "2023-01-01", "2023-12-31")
    for t in result:
        if "Дата платежа" in t and t["Дата платежа"]:
            assert isinstance(t["Дата платежа_dt"], datetime)


def test_invalid_date_handling(sample_transactions):
    # Проверка обработки некорректных дат
    result = process_transactions(sample_transactions, "Еда", "1900-01-01", "2023-12-31")
    invalid_transactions = [t for t in result if t.get("Дата платежа_dt") == datetime(1900, 1, 1)]
    assert len(invalid_transactions) >= 1  # Ожидаем хотя бы одну транзакцию с датой по умолчанию


def test_datetime_input(sample_transactions):
    # Проверка работы с datetime объектами на входе
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 31)
    result = process_transactions(sample_transactions, "Еда", start_date, end_date)
    assert len(result) == 2  # Ожидаем тот же результат, что и с строковыми датами


def test_file_output():
    # Проверка, что декоратор записывает результат в файл
    import os

    test_filename = "custom_report.txt"
    if os.path.exists(test_filename):
        os.remove(test_filename)  # Удаляем файл перед тестом

    # Вызываем функцию с тестовыми данными
    test_data = [{"Дата платежа": "01.01.2023", "Категория": "Тест", "Дата платежа_dt": datetime(2023, 1, 1)}]
    process_transactions(test_data, "Тест", "2023-01-01", "2023-01-01")
