import requests
import json
from db_api.mysql_model import MySqlModel
RATES_COL = 'rates'



def insert_rates_to_db(rates_dict):
    pass


def get_currency_by_date(date, symbols, base):
    payload = {}
    headers = {
      "apikey": "awojxDd9RxR3XGm6FVt4sSJ1Iflz4bGR"
    }
    url = "https://api.apilayer.com/fixer/{}?base={}&symbols={}".format(date, base, symbols)
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    status_code = response.status_code
    if status_code != 200:
      raise Exception(f"Failed get currencies")
    result = response.text
    response_dict = json.loads(result)
    return json.loads(result)[RATES_COL]


if __name__ == '__main__':
    get_currency_by_date(date="2021-01-01", symbols="ILS,EUR,GBP", base= "USD")


