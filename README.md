# CLI currency exchange rates

## Description
Application for obtaining exchange rates for grivna to other specified currency on a specific date

## Requirements
Python 3.10+  
click module  
requests module

## Installation
```
pip install requests
```
```
pip install click
```
```
git clone https://github.com/vmelfx/it_hillel_python_basic_meleshchenko_CLI_currency.git
```

## Usage
To use this application, go to the directory you cloned repo to and run main.py, with the following parameters:
1. To get the hryvnia exchange rate to the specified currency for the current date, run main.py and specify the currency. Input is case-insensitive:  
```
>>> python main.py usd
```
2. To get the hryvnia exchange rate to the specified currency on the specified date, run main.py and specify the currency and the date in the following format:
"YYYY-MM-DD"  
```
>>> python main.py USD --exchange_date 2000-01-01
```
## Features of use
The program receives data from the API of the National Bank of Ukraine, so if you'll try to ask the program about currency that isn't supported you'll get an error:
```
>>> python main.py bch
>>> BCH currency isn't supported!
```
The same is about date: if invalid date provided you will get an error:
```
>>> python main.py USD --exchange_date 2000-0101
>>> Invalid exchange_date 2000-0101!
```
Please note, that the minimum supported year is 1997 and the maxim supported year is current.  
Good luck!
## License
[MIT](https://choosealicense.com/licenses/mit/)
