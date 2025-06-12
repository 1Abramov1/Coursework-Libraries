import unittest
from src.utils import get_time_for_greeting

class TestGreetingFunction(unittest.TestCase):
    def test_morning(self):
        self.assertEqual(get_time_for_greeting("2025-06-05 05:00:00"), "Доброе утро")
        self.assertEqual(get_time_for_greeting("2025-06-05 07:30:00"), "Доброе утро")
        self.assertEqual(get_time_for_greeting("2025-06-05 11:59:59"), "Доброе утро")

    def test_afternoon(self):
        self.assertEqual(get_time_for_greeting("2025-06-05 12:00:00"), "Добрый день")
        self.assertEqual(get_time_for_greeting("2025-06-05 15:45:00"), "Добрый день")
        self.assertEqual(get_time_for_greeting("2025-06-05 17:59:59"), "Добрый день")

    def test_evening(self):
        self.assertEqual(get_time_for_greeting("2025-06-05 18:00:00"), "Добрый вечер")
        self.assertEqual(get_time_for_greeting("2025-06-05 20:15:00"), "Добрый вечер")
        self.assertEqual(get_time_for_greeting("2025-06-05 21:59:59"), "Добрый вечер")

    def test_night(self):
        self.assertEqual(get_time_for_greeting("2025-06-05 22:00:00"), "Доброй ночи")
        self.assertEqual(get_time_for_greeting("2025-06-05 00:00:00"), "Доброй ночи")
        self.assertEqual(get_time_for_greeting("2025-06-05 03:30:00"), "Доброй ночи")
        self.assertEqual(get_time_for_greeting("2025-06-05 04:59:59"), "Доброй ночи")

    def test_boundary_night_morning(self):
        self.assertEqual(get_time_for_greeting("2025-06-05 04:59:59"), "Доброй ночи")
        self.assertEqual(get_time_for_greeting("2025-06-05 05:00:00"), "Доброе утро")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            get_time_for_greeting("invalid-datetime-format")

    def test_edge_cases(self):
        self.assertEqual(get_time_for_greeting("2025-06-05 23:59:59"), "Доброй ночи")
        self.assertEqual(get_time_for_greeting("2025-06-05 04:00:00"), "Доброй ночи")
        self.assertEqual(get_time_for_greeting("2025-06-05 12:00:01"), "Добрый день")


# Демонстрация работы функции
if __name__ == '__main__':
    # Запуск тестов при выполнении скрипта
    unittest.main(argv=[''], exit=False)
    print("\nДемонстрация работы функции:")

    test_times = [
        "2025-06-05 05:00:00",  # Утро
        "2025-06-05 12:00:00",  # День
        "2025-06-05 18:00:00",  # Вечер
        "2025-06-05 23:00:00",  # Ночь
        "2025-06-05 00:00:00",  # Ночь
    ]

    for time_str in test_times:
        greeting = get_time_for_greeting(time_str)
        print(f"{time_str} -> {greeting}")

