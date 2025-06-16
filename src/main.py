import json

import pandas as pd

from src.config import PATH_TO_XLSX
from src.reports import process_transactions
from src.services import analise_cashback
from src.views import main_info

if __name__ == "__main__":
    # Пример использования main_info
    data_request = "2018-03-10 19:30:00"
    result_view = main_info(data_request)
    print(result_view)

    # Загрузка данных из Excel и преобразование в список словарей
    data = pd.read_excel(PATH_TO_XLSX).to_dict("records")

    # Анализ кэшбэка
    result = analise_cashback(data, 2018, 3)
    print(json.loads(result))  # Декодируем JSON для красивого вывода

    # Анализ трат по категории
    resul_services = process_transactions(data, "Пополнения", "2021-12-29", "2021-12-31")
    print(resul_services)
