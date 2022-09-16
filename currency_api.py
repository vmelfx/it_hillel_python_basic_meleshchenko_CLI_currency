import requests
import click
from datetime import datetime


class NbuCurrency:
    print_decorator_upper = "--------------"
    print_decorator_lower = "=============="

    def __init__(self, currency, exchange_date=None):
        self.currency = currency
        self.exchange_date = exchange_date

    def data_printer(self):
        currency_data = self.get_currency_data(self.currency, self.exchange_date)
        currency_rate = currency_data[0]['rate']
        currency_id = currency_data[0]['cc']
        print(self.print_decorator_upper)
        print(currency_id)
        print(currency_rate)
        print(self.print_decorator_lower)

    def get_currency_data(self, currency, exchange_date):
        if exchange_date is None:
            api_url_currency_data = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?" \
                                    f"valcode={currency}&json"
        else:
            api_url_currency_data = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?" \
                                    f"valcode={currency}&date={exchange_date}&json"
        response_currency = requests.request("GET", api_url_currency_data)
        if response_currency.status_code == requests.codes.ok:
            raw_currency_data = response_currency.json()
            return raw_currency_data
        else:
            print("Error:", response_currency.status_code, response_currency.text)

    @staticmethod
    def get_list_of_currencies():
        api_url_currency_data = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json"
        response_currency = requests.request("GET", api_url_currency_data)
        if response_currency.status_code == requests.codes.ok:
            raw_currency_data = response_currency.json()
            currencies_list = [element['cc'] for element in raw_currency_data]
            return currencies_list
        else:
            print("Error:", response_currency.status_code, response_currency.text)


@click.command()
@click.argument("currency")
@click.option("--exchange_date", "-d")
def main(currency, exchange_date):
    try:
        currencies_list = NbuCurrency.get_list_of_currencies()
        currency = currency.upper()
        if currency not in currencies_list:
            raise NameError
        if exchange_date is not None:
            exchange_date = datetime.strptime(exchange_date, '%Y-%m-%d').date()
            if 1996 < exchange_date.year <= datetime.now().year:
                exchange_date = datetime.strftime(exchange_date, '%Y-%m-%d')
                exchange_date = exchange_date.replace('-', '')
                usd_to_uan_data = NbuCurrency(currency=currency, exchange_date=exchange_date)
                usd_to_uan_data.data_printer()
            else:
                raise ValueError
        else:
            usd_to_uan_data = NbuCurrency(currency=currency)
            usd_to_uan_data.data_printer()
    except ValueError:
        print(f'Invalid exchange_date {exchange_date}!')
        raise SystemExit(1)
    except NameError:
        print(f"{currency} currency isn't supported!")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
