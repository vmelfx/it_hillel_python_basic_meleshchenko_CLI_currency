import requests
import click
from datetime import datetime


class NbuCurrency:
    print_decorator_upper = "--------------"
    print_decorator_lower = "=============="

    def __init__(self, currency, exchange_date=None) -> None:
        self.currency: str = currency
        self.exchange_date: str = exchange_date

    def data_printer(self) -> None:
        """
        This method is responsible for data output. It takes all required data and prints it into console.
        """
        currency_data: list = self.get_currency_data(self.currency, self.exchange_date)
        currency_rate: str = currency_data[0]['rate']
        currency_id: str = currency_data[0]['cc']
        print(self.print_decorator_upper)
        print(currency_id)
        print(currency_rate)
        print(self.print_decorator_lower)

    @staticmethod
    def get_currency_data(currency, exchange_date) -> list:
        """
        Method responsible for getting UAH to other currencies exchange rate data from api.
        :param currency: currency for which you want to know the rate
        :param exchange_date: optional parameter. The date on which you want to receive the exchange rate
        for the specified currency.
        :return: raw (not formatted) data from json. This data will be processed in the data_printer method
        """
        if exchange_date is None:
            api_url_currency_data: str = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?" \
                                    f"valcode={currency}&json"
        else:
            api_url_currency_data: str = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?" \
                                    f"valcode={currency}&date={exchange_date}&json"
        response_currency = requests.request("GET", api_url_currency_data)
        if response_currency.status_code == requests.codes.ok:
            raw_currency_data: list = response_currency.json()
            if raw_currency_data:
                return raw_currency_data
            else:
                print("En empty response from API. Program will be terminated")
                raise SystemExit(1)
        else:
            print("Error:", response_currency.status_code, response_currency.text)
            raise SystemExit(1)

    @staticmethod
    def get_list_of_currencies() -> list:
        """
        This method on each startup asks api about all supported currencies.
        Then, depending on user input program will decide: can it get data from api or not.
        For example, if user input is BCH, program will check, that this currency doesn't exist
        in list returned by api and program will return error.
        :return: list of supported currencies by api
        """
        api_url_currency_data: str = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json"
        response_currency = requests.request("GET", api_url_currency_data)
        if response_currency.status_code == requests.codes.ok:
            raw_currency_data: list = response_currency.json()
            if raw_currency_data:
                currencies_list: list = [element['cc'] for element in raw_currency_data]
                return currencies_list
            else:
                print("En empty response from API. Program will be terminated")
                raise SystemExit(1)
        else:
            print("Error:", response_currency.status_code, response_currency.text)
            raise SystemExit(1)


@click.command()
@click.argument("currency")
@click.option("--exchange_date", "-d")
def main(currency, exchange_date):
    try:
        currencies_list = NbuCurrency.get_list_of_currencies()
        currency: str = currency.upper()
        if currency not in currencies_list:
            # If entered by the user currency doesn't exist in returned by api list of supported currencies
            # NameError will be raised.
            raise NameError
        if exchange_date is not None:
            """
            If exchange_date parameter is presented the following logic will check that given data is
            in correct format and fits the limitations:
            1. The entered date is not less than 1996 - the minimum supported data by api.
            2. The entered date is not greater than current year.
            If these requirements are not met, than the ValueError will be raised.
            """
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
    except Exception:
        print("System error")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
