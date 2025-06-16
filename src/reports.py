import logging
from datetime import datetime
from typing import Callable, TypeVar, Any, Union, List, Dict

logger = logging.getLogger("reports")

# Тип для транзакции
Transaction = Dict[str, Any]
# Тип для возвращаемого значения декорируемой функции
T = TypeVar('T')

def save_to_file_with_name(filename: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Декоратор, сохраняющий результат функции в файл"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            result = func(*args, **kwargs)
            with open(filename, "a", encoding="utf-8") as f:
                f.write(str(result) + "\n")
            return result
        return wrapper
    return decorator


@save_to_file_with_name("custom_report.txt")
def process_transactions(
    transactions: List[Transaction],
    category: str,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime]
) -> List[Transaction]:
    """
    Обрабатывает транзакции: преобразует даты, фильтрует по категории и диапазону дат

    Args:
        transactions: Список транзакций
        category: Категория для фильтрации
        start_date: Начальная дата (str или datetime)
        end_date: Конечная дата (str или datetime)

    Returns:
        Отфильтрованный список транзакций
    """
    # Локальные переменные с аннотациями
    processed_start_date: datetime = datetime.min
    processed_end_date: datetime = datetime.max

    # Преобразуем входные даты в datetime объекты
    if isinstance(start_date, str):
        try:
            processed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError as e:
            logger.error(f"Ошибка преобразования start_date: {e}")
    else:
        processed_start_date = start_date

    if isinstance(end_date, str):
        try:
            processed_end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError as e:
            logger.error(f"Ошибка преобразования end_date: {e}")
    else:
        processed_end_date = end_date

    # Обрабатываем каждую транзакцию
    for transaction in transactions:
        date_value = transaction.get("Дата платежа")

        # Устанавливаем значения по умолчанию для некорректных данных
        if not date_value or isinstance(date_value, float):
            date_value_str = "01.01.1900"
            transaction["Дата платежа"] = date_value_str
            transaction["Дата платежа_dt"] = datetime.strptime(date_value_str, "%d.%m.%Y")
            continue

        try:
            # Обрабатываем строковые даты
            if isinstance(date_value, str):
                transaction["Дата платежа_dt"] = datetime.strptime(date_value, "%d.%m.%Y")
            # Обрабатываем уже преобразованные даты
            elif isinstance(date_value, datetime):
                transaction["Дата платежа"] = date_value.strftime("%d.%m.%Y")
                transaction["Дата платежа_dt"] = date_value
        except ValueError as e:
            logger.error(f"Ошибка преобразования даты транзакции: {e}")
            date_value_str = "01.01.1900"
            transaction["Дата платежа"] = date_value_str
            transaction["Дата платежа_dt"] = datetime.strptime(date_value_str, "%d.%m.%Y")

    # Фильтрация транзакций
    filtered_transactions: List[Transaction] = [
        t
        for t in transactions
        if t["Категория"] == category
        and processed_start_date <= t.get("Дата платежа_dt", datetime.min) <= processed_end_date
    ]

    return filtered_transactions
