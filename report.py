from telebot import types
from concurrent.futures import ThreadPoolExecutor
from config import API_KEY
import requests
from regions import region_codes
from creator import doc, put
import json
import time

class report:
    bot = 0

    easito = 0
    gibdd = 0
    rsa = 0
    taxi = 0
    reestr = 0
    status = 0

    def __init__(self, bot):
        self.bot = bot

    def _upd_status(self, message, addType: str):
        res = ''
        for i in range(self.status):
            res += '██'
        for i in range(5 - self.status):
            res += '░░'
        res = f'*{res}*' + f'{self.status * 20}%\n' + addType
        self.bot.edit_message_text(res, message.chat.id, message.id, parse_mode="Markdown")

    def gibbd_report(self, message):
        try:
            easitoExist = False
            gosnom = message.text.replace(' ', '')
            botMes = self.bot.send_message(message.from_user.id, f'Начата обработка отчета по госномеру {gosnom}')
            self._make_rsa(requests.Session(), f'https://parser-api.com/parser/rsa_api/?key={API_KEY}&regNumber={gosnom}', botMes)
            if self.rsa.get(['policies'][0]['vin']):
                vin = self.rsa['policies'][0]['vin']
            else:
                self._make_easito(requests.Session(), f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&regNumber={gosnom}', botMes)
                easitoExist = True
                vin = self.easito['diagnose_cards'][0]['vin']
            print('dsadasdasdasda')
            with ThreadPoolExecutor() as executor:
                with requests.Session() as session:
                    if easitoExist == False:
                        executor.map(self._make_easito, [session],
                                     [
                                         f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&regNumber={gosnom}'],
                                     [botMes])
                    executor.map(self._make_gibdd, [session], [
                        f'https://parser-api.com/parser/gibdd_api/?key={API_KEY}&vin={vin}&types=history,dtp,wanted,restrict'],
                                 [botMes])
                    executor.map(self._make_taxi, [session],
                                 [f'https://parser-api.com/parser/taxi_api/?regNumber={gosnom}&key={API_KEY}'], [botMes])
                    executor.map(self._make_reestr, [session],
                                 [f'http://parser-api.com/parser/reestr_api/?key={API_KEY}&vin={vin}'], [botMes])
                    executor.shutdown(wait=True)
                    res = [self.gibdd, self.easito, self.rsa, self.reestr, self.taxi]
                    print('========================================')
                    if self.rsa:
                        print(self.rsa)
                    if self.easito:
                        print(self.easito)
                    if self.gibdd:
                        print(self.gibdd)
                    if self.reestr:
                        print(self.reestr)
                    if self.taxi:
                        print(self.taxi)
                    print('========================================')
                    gosnom = self.rsa['policies'][0]['regNumber']
                    lstGosnom = list(gosnom)

                    region = ''
                    for i in range(6, len(lstGosnom)):
                        region += lstGosnom[i]
                    res = doc(res, str(botMes.from_user.username), region_codes[region])
                    link = put(res.getHtml())
                    self.bot.edit_message_text(
                        f'отчет по машине с vin-кодом{vin} и госномером{gosnom} готов\n[ссылка на отчет]({link})',
                        botMes.chat.id, botMes.id, parse_mode="Markdown")
        except requests.exceptions.RequestException:
            self.bot.send_message(message.from_user.id, 'увы мы не нашли машину с таком госномером, попробуйте пожалуйста позже')




    def vin_report(self, message):
        vin = message.text.replace(' ', '').upper()
        print(vin)
        botMes = self.bot.send_message(message.from_user.id, f'начата обработка отчета по vin: {vin}')

        with ThreadPoolExecutor() as executor:
            with requests.Session() as session:
                # executor.map(self._make_rsa, [session],
                #              [f'https://parser-api.com/parser/rsa_api/?key={API_KEY}&vin={vin}'], [botMes])
                executor.map(self._make_gibdd, [session],
                             [f'https://parser-api.com/parser/gibdd_api/?key={API_KEY}&vin={vin}&types=history,dtp,wanted,restrict'],
                             [botMes])
                executor.map(self._make_easito, [session],
                             [f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&vin={vin}'], [botMes])
                executor.map(self._make_taxi, [session],
                             [f'https://parser-api.com/parser/taxi_api/?vin={vin}&key={API_KEY}'], [botMes])
                executor.map(self._make_reestr, [session],
                             [f'http://parser-api.com/parser/reestr_api/?key={API_KEY}&vin={vin}'], [botMes])
                executor.shutdown(wait=True)
                print('1234')
                # with open('gibbd.json', 'r', encoding='utf-8') as gib:
                #     self.gibdd = json.load(gib)
                with open('rsa.json', 'r', encoding='utf-8') as rsas:
                    self.rsa = json.load(rsas)

                res = [self.gibdd, self.easito, self.rsa, self.reestr, self.taxi]
                print('========================================')
                if self.rsa:
                    print(self.rsa)
                if self.easito:
                    print(self.easito)
                if self.gibdd:
                    print(self.gibdd)
                if self.reestr:
                    print(self.reestr)
                if self.taxi:
                    print(self.taxi)
                print('========================================')

                if self.rsa.get('policies'):
                    print('dsadasdas')
                    gosnom = self.rsa['policies'][0]['regNumber']
                    lstGosnom = list(gosnom)
                    region = ''
                    for i in range(6, len(lstGosnom)):
                        region += lstGosnom[i]
                        region = region_codes[region]
                else:
                    gosnom = 'не найдено'
                    region = ''
                print(region)
                docs = doc(res, message.from_user.username, region, vin)
                link = put(docs.getHtml())
                self.bot.edit_message_text(
                    f'отчет по машине с vin-кодом: {vin} и госномером:{gosnom}  готов\n{link}',
                    botMes.chat.id, botMes.id, parse_mode="Markdown")


    def _make_rsa(self, session, url, message):
        self.rsa = session.get(url, timeout=None).json()
        self.status += 1
        self._upd_status(message, 'Получена информация из РСА')

    def _make_easito(self, session, url, message):
        self.easito = session.get(url).json()
        self.status += 1
        self._upd_status(message, 'Получена информация из ЕАСИТО')

    def _make_gibdd(self, session, url, message):
        count = 0
        have = False
        while have != True and count <= 3:
            self.gibdd = session.get(url).json()
            if self.gibdd['history'] == None:
                count += 1
                time.sleep(15)
            else:
                have = True
        self.status += 1
        self._upd_status(message, 'Получена информация из ГИБДД')

    def _make_taxi(self, session, url, message):
        self.taxi = session.get(url).json()
        self.status += 1
        self._upd_status(message, 'Получена информация о работе в Такси')

    def _make_reestr(self, session, url, message):
        self.reestr = session.get(url).json()
        self.status += 1
        self._upd_status(message, 'Получена информация из реестра залогов')

