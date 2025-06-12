from dotenv import load_dotenv
import os

load_dotenv()

URL_Currense = "https://api.apilayer.com/exchangerates_data/convert"
URL_Stocks = "https://www.alphavantage.co/query"

API_KEY_CURRENCIES = os.getenv("API_KEY_CURRENCIES")
API_KEY_STOCKS = os.getenv("API_KEY_STOCKS")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_XLSX = os.path.join(BASE_DIR, "..", "data", "operations.xlsx")
PATH_TO_JSON = os.path.join(BASE_DIR, "..", "data", "user_settings.json")
