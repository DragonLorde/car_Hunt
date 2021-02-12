from telebot import types
from concurrent.futures import ThreadPoolExecutor
from config import API_KEY
import requests
from regions import region_codes
from creator import doc, put
from data_base import write_report
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
        if self.status > 5:
            self.status = 5
        res = '⏱Подготавливаем отчет\n'
        if self.status < 5:
            for i in range(self.status):
                res += '██'
            for i in range(5 - self.status):
                res += '░░'
            res = f'*{res}*' + f'{self.status * 20}%\n' + addType
        else:
            res = '⏱Подготавливаем отчет'
        self.bot.edit_message_text(res, message.chat.id, message.id, parse_mode="Markdown")

    def gosnom_report(self, message):
        try:
            easitoExist = False
            gosnom = message.text.replace(' ', '')
            botMes = self.bot.send_message(message.from_user.id, f'Начата обработка отчета по госномеру {gosnom}')
            self._make_rsa(requests.Session(), f'https://parser-api.com/parser/rsa_api/?key={API_KEY}&regNumber={gosnom}', botMes)
            if self.rsa.get('policies'):
                if self.rsa['policies'][0]['vin'] != None:
                    print('fadad')
                    vin = self.rsa['policies'][0]['vin']
                    print(vin)
                else:
                    easitoExist = True
                    self._make_easito(requests.Session(),
                                      f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&regNumber={gosnom}',
                                      botMes)
                    if self.easito.get('diagnose_cards'):
                        vin = self.easito['diagnose_cards'][0]['vin']
                    else:
                        vin = False
            else:
                easitoExist = True
                self._make_easito(requests.Session(), f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&regNumber={gosnom}', botMes)
                if self.easito.get('diagnose_cards'):
                    vin = self.easito['diagnose_cards'][0]['vin']
                else:
                    vin = False

            if vin:
                with ThreadPoolExecutor() as executor:
                    with requests.Session() as session:
                        if easitoExist == False:
                            executor.map(self._make_easito, [session],
                                             [f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&regNumber={gosnom}'], [botMes])
                        executor.map(self._make_gibdd, [session], [
                            f'https://parser-api.com/parser/gibdd_api/?key={API_KEY}&vin={vin}&types=history,dtp,wanted,restrict'],
                                     [ botMes])
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

                        print(gosnom)
                        lstGosnom = list(gosnom)
                        print(lstGosnom)
                        region = ''
                        for i in range(6, len(lstGosnom)):
                            region += lstGosnom[i]
                        region = region_codes[region]

                        print('bice')
                        print(region)
                        print(gosnom)

                        print('==================')
                        docs = doc(res, message.from_user.username, region, vin)
                        print('dsasdas')
                        link = put(docs.getHtml())
                        self.bot.edit_message_text(
                            f'📝Отчет по машине с \nVin-кодом: {vin} \nи Госномером: {gosnom}  \n\n*Ознакомится с отчетом можно по адресу:*\n{link}',
                            botMes.chat.id, botMes.id, parse_mode="Markdown")
                        write_report(vin, gosnom, '0', link, '0', self.easito, self.gibdd, self.rsa, self.taxi,
                                     self.reestr)
            else:
                self.bot.edit_message_text(
                    f'Увы мы не нашли машину с таком госномером, попробуйте пожалуйста позже',
                    botMes.chat.id, botMes.id, parse_mode="Markdown")
        except requests.exceptions.RequestException:
            self.bot.edit_message_text(
                f'Увы мы не нашли машину с таком госномером, попробуйте пожалуйста позже',
                botMes.chat.id, botMes.id, parse_mode="Markdown")




    def vin_report(self, message):
        vin = message.text.replace(' ', '').upper()
        print(vin)
        botMes = self.bot.send_message(message.from_user.id, f'начата обработка отчета по vin: {vin}')

        with ThreadPoolExecutor() as executor:
            with requests.Session() as session:
                executor.map(self._make_rsa, [session],
                            [f'https://parser-api.com/parser/rsa_api/?key={API_KEY}&vin={vin}'], [botMes])
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

                print(self.rsa['policies'])

                print('some shit')

                if self.rsa.get('policies'):
                    if self.rsa['policies'][0].get('regNumber'):
                        if self.rsa['policies'][0]['regNumber'] != None:
                            print('dsadasdas')
                            gosnom = self.rsa['policies'][0]['regNumber']
                            lstGosnom = list(gosnom)
                            region = ''
                            for i in range(6, len(lstGosnom)):
                                region += lstGosnom[i]
                                print(region)
                            region = region_codes[region]
                            print(region)
                        else:

                            gosnom = 'не найдено'
                            region = ''
                    else:
                        print('danyaPizdit')
                        gosnom = 'не найдено'
                        region = ''
                else:
                    print('danyaPizdit')
                    gosnom = 'не найдено'
                    region = ''
                print('fdsadfsdaf')

                print('>>>>>>>>>>>>>>>>>')
                print(res)
                print(message.from_user.username)
                print(region)
                print(vin)
                print('>>>>>>>>>>>>>>>>>')
                docs = doc(res, message.from_user.username, region, vin)
                print('213456789')
                link = put(docs.getHtml())
                print('13456789')
                self.bot.edit_message_text(
                    f'📝Отчет по машине с \nVin-кодом: {vin} \nи Госномером: {gosnom}\nбыл успешно сгенирирован\n\n*Ознакомится с отчетом можно по адресу:*\n{link}',
                    botMes.chat.id, botMes.id, parse_mode="Markdown")
                if gosnom == 'не найдено':
                    gosnom = ''
                write_report(vin, gosnom, '0', link, '0', self.easito, self.gibdd, self.rsa, self.taxi,
                             self.reestr)



    def _make_rsa(self, session, url, message):
        print('rsa////')
        self.rsa = session.get(url, timeout=None).json()
        self.status += 1
        self._upd_status(message, 'Получена информация из РСА')

    def _make_easito(self, session, url, message):
        print('easito////')
        self.easito = session.get(url).json()
        self.status += 1
        self._upd_status(message, 'Получена информация из ЕАСИТО')

    def _make_gibdd(self, session, url, message):

        count = 0
        have = False
        while have != True and count <= 3:
            print('gibbd///')
            self.gibdd = session.get(url).json()
            if self.gibdd['history'] == None:
                count += 1
                time.sleep(15)
            else:
                have = True
        self.status += 1
        self._upd_status(message, 'Получена информация из ГИБДД')

    def _make_taxi(self, session, url, message):
        print('taxi////')
        self.taxi = session.get(url).json()
        self.status += 1
        self._upd_status(message, 'Получена информация о работе в Такси')

    def _make_reestr(self, session, url, message):
        print('reestr////')
        self.reestr = session.get(url).json()
        self.status += 1
        self._upd_status(message, 'Получена информация из реестра залогов')

