import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from freezegun import freeze_time
from src.utils import get_stock


class TestGetStock(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"user_stocks": ["AAPL", "MSFT"]}))
    @patch("requests.get")
    @freeze_time("2025-06-09")  # понедельник
    def test_successful_response(self, mock_get, *_):
        # Настраиваем мок для requests.get
        mock_responses = [
            {"Time Series (Daily)": {"2025-06-06": {"1. open": "150.23"}}},  # данные за пятницу
            {"Time Series (Daily)": {"2025-06-06": {"1. open": "280.54"}}}  # данные за пятницу
        ]
        mock_get.side_effect = [MagicMock(status_code=200, json=lambda: r) for r in mock_responses]

        # Вызываем тестируемую функцию
        result = get_stock("../data/user_settings.json")
        print(result)
        # Проверяем результаты
        self.assertEqual(len(result), 0)
        self.assertEqual(result[0]["symbol"], "AAPL")
        self.assertEqual(result[1]["symbol"], "MSFT")
        self.assertEqual(result[0]["price"], 150.23)
        self.assertEqual(result[1]["price"], 280.54)


if __name__ == '__main__':
    unittest.main()
