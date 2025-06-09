import pandas as pd
from src.reports import *
from src.services import analise_cashback
from src.views import main_info
from src.config import PATH_TO_XLSX


if __name__ == "__main__":
     data_request = "2018-03-10 15:30:00"
     result_view = main_info(data_request)
     print(result_view)

     resul_services = analise_cashback(PATH_TO_XLSX, 2018, 3)
     print(resul_services)


     df = pd.read_excel(PATH_TO_XLSX, sheet_name="Отчет по операциям")
     result_report = spending_by_category(df, "Пополнения", "2021-12-29")
     print(result_report)