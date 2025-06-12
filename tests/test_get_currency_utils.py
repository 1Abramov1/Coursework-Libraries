import unittest
from unittest.mock import patch, Mock
from src.utils import get_currency


class TestGetCurrency(unittest.TestCase):

    @patch('requests.request')
    @patch('builtins.open')
    @patch('json.load')
    def test_get_currency(self, mock_json_load, mock_open, mock_request):
        # Подготовка заглушек
        mock_json_load.return_value = {
            "user_currencies": ["USD", "EUR"]
        }

        def mock_response_side_effect(*args, **kwargs):
            currence = kwargs['data']['from']
            return Mock(
                status_code=200,
                json=Mock(return_value={
                    "query": {"from": currence, "to": "RUB"},
                    "result": 75.0
                })
            )

        mock_request.side_effect = mock_response_side_effect

        # Вызов тестируемой функции
        result = get_currency("fake_path.json")

        # Проверка результата
        expected = [
            {"currency": "USD", "rate": "75.0"},
            {"currency": "EUR", "rate": "75.0"}
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()