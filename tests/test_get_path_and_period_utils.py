import pandas as pd
import unittest.mock
from unittest.mock import patch
from pandas.testing import assert_frame_equal
from src.utils import get_path_and_period

class TestGetPathAndPeriod(unittest.TestCase):
    @patch("pandas.read_excel")
    def test_get_path_and_period(self, mock_read_excel):
        # 1. Подготовка тестовых данных
        test_data = pd.DataFrame({
            "Дата операции": [
                "01.01.2023 12:00:00",
                "15.01.2023 09:30:00",
                "31.01.2023 23:59:59",
                "01.02.2023 00:00:01"
            ],
            "Данные": [100, 200, 300, 400]
        })

        # Настройка мок-объекта
        mock_read_excel.return_value = test_data

        # 2. Ожидаемый результат после фильтрации и сортировки
        expected_data = pd.DataFrame({
            "Дата операции": [
                "01.01.2023 12:00:00",
                "15.01.2023 09:30:00",
                "31.01.2023 23:59:59"
            ],
            "Данные": [100, 200, 300]
        }).sort_values(by="Дата операции")

        # 3. Вызов тестируемой функции
        start_date = "01.01.2023 00:00:00"
        end_date = "31.01.2023 23:59:59"
        result = get_path_and_period("fake_path.xlsx", [start_date, end_date])

        # 4. Проверка результата
        expected_data["Дата операции"] = pd.to_datetime(expected_data["Дата операции"], dayfirst=True)
        assert_frame_equal(result.reset_index(drop=True), expected_data.reset_index(drop=True))


