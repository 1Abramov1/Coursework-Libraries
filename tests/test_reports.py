import pandas as pd
import pytest
from unittest.mock import patch, mock_open
from src.reports import spending_by_category  # Импорт из вашего файла


# Фикстура для стандартного тестового DataFrame
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Дата платежа": [
            "01.01.2023", "15.02.2023", "10.03.2023",
            "05.12.2022", "01.04.2023", "10.05.2023"
        ],
        "Категория": [
            "Еда", "Еда", "Транспорт",
            "Еда", "Еда", "Еда"
        ],
        "Сумма операции с округлением": [
            1000, 2000, 1500, 500, 3000, 4000
        ]
    })

# Тест 1: Основной сценарий (есть данные)
def test_basic_functionality(sample_data):
    with patch("builtins.open", mock_open()) as mock_file:
        result = spending_by_category(sample_data, "Еда", "2023-03-31")

    assert result == {"Еда": 3000}  # 1000 + 2000


# Тест 2: Нет транзакций в категории
def test_no_transactions_in_category(sample_data):
    with patch("builtins.open", mock_open()):
        result = spending_by_category(sample_data, "Развлечения", "2023-03-31")
    assert result != {"Развлечения": {}}


# Тест 3: Транзакции вне периода
def test_transactions_outside_period(sample_data):
    with patch("builtins.open", mock_open()):
        result = spending_by_category(sample_data, "Еда", "2023-03-01")
    assert result != {"Еда": 2000}  # Только февраль


# Тест 4: Граничные даты периода
def test_edge_dates(sample_data):
    with patch("builtins.open", mock_open()):
        result = spending_by_category(sample_data, "Еда", "2023-04-01")
    assert result == {"Еда": 6000}  # 1000 + 2000 + 3000

# Тест 5: Запись результата в файл
def test_file_writing(sample_data):
    with patch("builtins.open", mock_open()) as mock_file:
        result = spending_by_category(sample_data, "Еда", "2023-03-31")

        # Проверка вызова записи в файл
        mock_file.assert_called_with("custom_report.txt", "a", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_called_once_with("{'Еда': 3000}\n")


