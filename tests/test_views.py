import json
from src.views import main_info

# Пример теста для проверки структуры JSON

def test_main_info_structure():
    # Вызов функции main_info
    result = main_info("2023-01-15 12:00:00")

    # Преобразование JSON-строки обратно в словарь
    data = json.loads(result)

    # Проверка наличия всех ожидаемых ключей
    assert "greeting" in data, "Missing key: 'greeting'"
    assert "cards" in data, "Missing key: 'cards'"
    assert "top_transactions" in data, "Missing key: 'top_transactions'"
    assert "currency_rates" in data, "Missing key: 'currency_rates'"
    assert "stock_prices" in data, "Missing key: 'stock_prices'"


# Запуск теста
if __name__ == "__main__":
    test_main_info_structure()
    print("All keys are present in the JSON response.")
