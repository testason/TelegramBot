import requests
from bs4 import BeautifulSoup
import pymorphy2
import datetime


class Currency:
    link = 'https://www.cbr.ru/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    def __init__(self):
        self.past_dollar_value = [self.date()]
        self.past_euro_value = [self.date()]

    def dollar_currency(self):
        full_page_dollar = requests.get(self.link, headers=self.headers)
        soup = BeautifulSoup(full_page_dollar.content, 'html.parser')
        convert = soup.find_all("div", {"class": "col-md-2 col-xs-9 _right mono-num"})[0].text.split()[0]
        form = self.correct_form_of_the_ruble(convert)
        date = self.date()

        self.dollar = f"Курс доллара на {date}:\n {convert} {form}"
        return self.dollar

    def euro_currency(self):
        full_page_euro = requests.get(self.link, headers=self.headers)
        soup = BeautifulSoup(full_page_euro.content, 'html.parser')
        convert = soup.find_all("div", {"class": "col-md-2 col-xs-9 _right mono-num"})[2].text.split()[0]
        form = self.correct_form_of_the_ruble(convert)
        date = self.date()
        self.euro = f"Курс евро на {date}:\n {convert} {form}"
        return self.euro

    def correct_form_of_the_ruble(self, number):
        morph = pymorphy2.MorphAnalyzer()
        self.number = float('.'.join(number.split(',')))
        comment = morph.parse('рубль')[0]
        self.correct_form = comment.make_agree_with_number(self.number).word
        return self.correct_form

    def date(self):
        return '.'.join(str(datetime.datetime.now().date()).split('-')[::-1])