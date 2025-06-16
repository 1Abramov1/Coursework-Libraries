import json
from datetime import datetime
from typing import Dict

from src.logger_config import get_logger

logger = get_logger("services")


def analise_cashback(transactions: list[dict], year: int, month: int) -> str:
    def is_valid_transaction(transaction_data: dict) -> bool:
        try:
            operation_date = datetime.strptime(transaction_data["Дата операции"], "%Y-%m-%d %H:%M:%S")
            has_cashback = transaction_data.get("Кэшбэк", 0) > 0
            is_negative_payment = float(transaction_data["Сумма платежа"]) < 0
            is_correct_date = operation_date.year == year and operation_date.month == month

            return is_correct_date and has_cashback and is_negative_payment
        except (ValueError, KeyError):
            return False

    logger.info("Выводит правильный формат даты время")

    filtered_data = filter(is_valid_transaction, transactions)

    cashback_by_category: Dict[str, float] = {}
    for transaction in filtered_data:
        category = transaction["Категория"]
        amount = abs(float(transaction["Сумма платежа"]))
        cashback = amount // 100
        cashback_by_category[category] = cashback_by_category.get(category, 0) + cashback

    return json.dumps(cashback_by_category, ensure_ascii=False, indent=4)
