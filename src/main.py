from src.reports import *
from src.services import anylize_cashback
from src.views import main_info


if __name__ == "__main__":
     data_request = "2019-04-10 15:30:00"
     result_view = main_info(data_request)
     #print(result_view)

     resul_services = anylize_cashback("../data/operations.xlsx", 2018, 3)
     print(resul_services)
   