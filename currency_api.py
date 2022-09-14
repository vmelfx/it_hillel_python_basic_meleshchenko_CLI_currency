import requests


class NbuCurrency:
    def __init__(self, currency, date=None):
        self.currency = currency
        self.data = date



api_url_currency_data = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json"
response_currency = requests.request("GET", api_url_currency_data)
if response_currency.status_code == requests.codes.ok:
    raw_currency_data = response_currency.json()
    print(raw_currency_data)
else:
    print("Error:", response_currency.status_code, response_currency.text)