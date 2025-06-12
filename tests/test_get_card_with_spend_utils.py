import unittest
import pandas as pd
from src.utils import get_card_with_spend


class TestGetCardWithSpend(unittest.TestCase):

    def test_get_card_with_spend(self):
        # Подготовка тестового DataFrame
        test_data = pd.DataFrame({
            "Номер карты": ["****1234", "****5678"],
            "Сумма операции": [-150, 200],
            "Кэшбэк": [1.5, 2.0],
            "Сумма операции с округлением": [-150, 200],
        })

        # Ожидаемый список
        expected_result = [
            {"last_digits": "1234", "total_spent": -150, "cashback": -2}
        ]

        # Вызов функции и проверка результата
        result = get_card_with_spend(test_data)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()