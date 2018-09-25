import urllib.request
import json
import pathlib
from decimal import *

class CurrencyConverter:
    '''
    http://api.fixer.io/latest
    '''
    def __init__(self, url="https://ratesapi.io/api/latest", file="currencies.txt"):
        """
        Creates a new CurrencyConverter object. By default class uses Fixer API to download currencies from web.
        update - retesapi
        :param url: The URL from which data is downloaded
        :param file: The path to the file to which data is saved and read.
        """
        self.url = url
        self.file = file
        self.base = "EUR"
        self.rates = {}
        self.date = ""


    def __str__(self):
        return "Class: {5}:\nURL: {0}\nFile: {1}\n Date: {2}\nBase: {3}\nRates: {4}".format(self.url,self.file,self.date,self.base,self.rates,type(self))

    def convert(self, amount, from_currency, to_currency):
        """
        Converts a specified amount based on the values of the class variables.
        :param amount: Amount to convert
        :param from_currency: From currency
        :param to_currency: To currency
        :return: Converted amount
        """
        getcontext().prec = 48
        amount = Decimal(amount)
        if from_currency != "EUR": # Euro is base currency
            amount = amount / Decimal(self.rates[from_currency]) # amount is converted to Euro

        if to_currency == "EUR":
            return amount
        else:
            return amount * Decimal(self.rates[to_currency])

    def save_rates_to_file(self):
        """Writes to the file currency exchange rates that are in the class variables"""
        with open(self.file, 'w') as outfile:
            json.dump({"date": self.date, "base": self.base, "rates": self.rates}, outfile)

    def load_rates_from_file(self):
        """
        Loads currency exchange rates from a file. If the specified file doesn't exist, the method throws IOError.
        """
        path = pathlib.Path(self.file)
        if path.exists():
            with open(self.file) as json_file:
                data = json.load(json_file)
                self.rates = data["rates"]
                self.date = data["date"]
                self.base = data["base"]
        else:
            raise IOError("The file {0} does not exist or is in another folder".format(self.file))

    def update_exchange_rates(self):
            """
            Updates exchange rates online.
            """
            req = urllib.request.Request(self.url, headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"})
            data = urllib.request.urlopen(req).read()
            data = json.loads(data.decode('utf-8'))  # decodes data into a dictionary.
            self.rates = data["rates"]  # The dictionary should have three keys - "rates", "date" and "base"
            self.date = data["date"]
            self.base = data["base"]
            self.save_rates_to_file()
