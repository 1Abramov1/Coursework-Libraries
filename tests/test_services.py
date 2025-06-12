import unittest
import os
import pandas as pd
import json
from tempfile import NamedTemporaryFile
from src.services import analise_cashback

class TestCashbackAnalysis(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.test_data = [
            # Валидные данные (июнь 2021)
            ["10.06.2021 12:00:00", "Супермаркеты", 150, -5000],
            ["15.06.2021 14:30:00", "АЗС", 300, -10000],
            ["20.06.2021 09:15:00", "Супермаркеты", 75, -2500],

            # Некэшбэчные операции (должны игнорироваться)
            ["12.06.2021 11:00:00", "Рестораны", 0, -3000],
            ["18.06.2021 19:00:00", "Транспорт", 0, -1500],

            # Положительные платежи (должны игнорироваться)
            ["05.06.2021 08:45:00", "Пополнение", 50, 10000],

            # Данные за другой период (должны игнорироваться)
            ["03.05.2021 12:00:00", "Супермаркеты", 100, -4000],
            ["10.07.2021 16:00:00", "АЗС", 200, -8000]
        ]

        # Создаем временный Excel-файл
        self.temp_file = NamedTemporaryFile(delete=False, suffix='.xlsx')
        df = pd.DataFrame(
            self.test_data,
            columns=["Дата операции", "Категория", "Кэшбэк", "Сумма платежа"]
        )
        df.to_excel(self.temp_file.name, index=False)

    def tearDown(self):
        # Удаляем временный файл
        self.temp_file.close()
        os.unlink(self.temp_file.name)


    def test_no_cashback_operations(self):
        """Тест при отсутствии кэшбэчных операций"""
        # Запрос данных за апрель 2021 (нет данных)
        result = analise_cashback(self.temp_file.name, 2021, 4)
        data = json.loads(result)
        self.assertDictEqual(data, {})

    def test_ignore_non_cashback(self):
        """Тест игнорирования операций без кэшбэка"""
        result = analise_cashback(self.temp_file.name, 2021, 6)
        data = json.loads(result)

        # Проверяем что категории без кэшбэка отсутствуют
        self.assertNotIn("Рестораны", data)
        self.assertNotIn("Транспорт", data)

    def test_ignore_positive_payments(self):
        """Тест игнорирования положительных платежей"""
        result = analise_cashback(self.temp_file.name, 2021, 6)
        data = json.loads(result)

        # Проверяем что категория пополнения отсутствует
        self.assertNotIn("Пополнение", data)

if __name__ == '__main__':
    unittest.main()


