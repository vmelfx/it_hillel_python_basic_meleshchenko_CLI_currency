import requests


class NbuCurrency:
    print_decorator_upper = "--------------"
    print_decorator_lower = "=============="

    def __init__(self, currency, date=None):
        self.currency = currency
        self.date = date

    def data_printer(self):
        currency_data = self.get_currency_data(self.currency, self.date)
        print(self.print_decorator_upper)
        print(self.currency)
        print(currency_data)
        print(self.print_decorator_lower)

    def get_currency_data(self, currency, date):
        if date is None:
            api_url_currency_data = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?" \
                                    f"valcode={currency}&json"
        else:
            date = date.replace('-', '')
            api_url_currency_data = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?" \
                                    f"valcode={currency}&date={date}&json"
        response_currency = requests.request("GET", api_url_currency_data)
        if response_currency.status_code == requests.codes.ok:
            raw_currency_data = response_currency.json()
            currency = raw_currency_data[0]['rate']
            return currency
        else:
            print("Error:", response_currency.status_code, response_currency.text)


eur_to_uan_data = NbuCurrency(currency='USD', date='2013-01-01')
eur_to_uan_data.data_printer()
