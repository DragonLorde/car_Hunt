from telebot import TeleBot, types

import putFile
from regions import region_codes
from config import TG_TOKEN, API_KEY
from concurrent.futures import ThreadPoolExecutor
from report import report
import requests
import json
import number as numberr
from data_base import *

bot = TeleBot(TG_TOKEN)
defultMessage = \
'👉 Примеры запросов,  которые  я принимаю:\n \
🚘 *Госномер автомобиля.* \n \
_Пример:_ \n \
🚗 *VIN номер автомобиля.*\n \
_Пример:_\n \
📱 *Номер телефона.*\n \
_Пример:_\n \
🌐 *ссылка на обьявление*\n \
_Пример:_'

#здесь обработчики запросов с сообщения вина =>

@bot.callback_query_handler(lambda query: query.data == 'other_funk_vin')
def other_funk_vin(query: types.CallbackQuery):
    mark = types.InlineKeyboardMarkup()
    mark.add(types.InlineKeyboardButton('📝Полный отчет', callback_data='report_vin_query'))
    mark.add(types.InlineKeyboardButton('🚗Получить госномер', callback_data='gosnom_vin_query'))
    mark.add(types.InlineKeyboardButton('🏁Получить пробег', callback_data='probeg_vin'))
    mark.add(types.InlineKeyboardButton('🛃Пройденные ТО', callback_data='to_vin_query'))
    mark.add(types.InlineKeyboardButton('🚕Работа в такси', callback_data='taxi_vin_query'))
    mark.add(types.InlineKeyboardButton('🔥Реестр залогов', callback_data='zalogi_vin_query'))
    bot.edit_message_reply_markup(query.from_user.id, query.message.id, reply_markup=mark)
    bot.answer_callback_query(query.id)

@bot.callback_query_handler(lambda query: query.data == 'report_vin_query')
def report_vin_query(query: types.CallbackQuery):
    rep = report(bot)
    bot.answer_callback_query(query.id, f'запрос на проверку по vin: {query.message.reply_to_message.text} принят')
    with ThreadPoolExecutor() as executor:
        executor.map(rep.vin_report, [query.message.reply_to_message])

@bot.callback_query_handler(lambda query: query.data == 'gosnom_vin_query')
def gosnom_vin_query(query: types.CallbackQuery):
    vin = query.message.json['reply_to_message']['text'].replace(' ', '').upper()
    bot.answer_callback_query(query.id, f'начат поиск госномера по vin: {vin}')
    with ThreadPoolExecutor() as executor:
        executor.map(post_gosnom_vin_query, [query])

def post_gosnom_vin_query(query: types.CallbackQuery):
    vin = query.message.json['reply_to_message']['text'].replace(' ', '').upper()
    userID = query.message.json['reply_to_message']['from']['id']
    notFind = False
    res = requests.session().get(f'https://parser-api.com/parser/rsa_api/?key={API_KEY}&vin={vin}').json()
    if res.get(['policies'][0]['regNumber']):
        gosnom = res.get['policies'][0]['regNumber']
    else:
        res = requests.session().get(f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&vin={vin}').json()
        if res.get['diagnose_cards'][0]['vin']:
            gosnom = res['diagnose_cards'][0]['vin']
        else:
            notFind = True
    if notFind:
        bot.reply_to(query.message.reply_to_mgiessage, f'госномер по vin: {vin}\nне найден')
    else:
        bot.reply_to(query.message.reply_to_message, f"госномер: {gosnom}")

@bot.callback_query_handler(lambda query: query.data == 'probeg_vin')
def probeg_vin(query: types.CallbackQuery):
    with ThreadPoolExecutor() as executor:
        executor.map(probeg_post_vin_query, [query])
    bot.answer_callback_query(query.id, 'запрос на получения данных о пробеге принят в обработку')

def probeg_post_vin_query(query: types.CallbackQuery):
    vin = query.message.json['reply_to_message']['text'].replace(' ', '')
    userID = query.message.json['reply_to_message']['from']['id']

    ress = requests.get(f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&vin={vin}')
    res = json.loads(ress.text)
    prob = res['diagnose_cards'][0]['mileage']
    date = res['diagnose_cards'][0]['startDate']
    sen = f'последний зафиксированный пробег:\n{prob}\nдата: {date}'
    bot.send_message(userID, sen)

@bot.callback_query_handler(lambda query: query.data == 'to_vin_query')
def to_vin_query(query: types.CallbackQuery):
    bot.answer_callback_query(query.id, 'запрос на получение ТО в обработке')
    with ThreadPoolExecutor() as executor:
        executor.map(to_post_vin_query, [query])


def to_post_vin_query(query: types.CallbackQuery):
    vin = query.message.json['reply_to_message']['text'].replace(' ', '')
    userName = query.message.json['reply_to_message']['from']['first_name']
    userID = query.message.json['reply_to_message']['from']['id']

    res = requests.get(f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&vin={vin}')
    res = json.loads(res.text)
    sen = f'по vin-коду {vin}\n' \
          f'найдены следующие ТО\n'
    for i in res['mileages']:
        date = i['date']
        mileage = i['mileage']
        sen += f"\nдата: {date}" \
               f"\nпробег: {mileage}" \
               f"\n----------------"
    bot.send_message(userID, sen)


@bot.callback_query_handler(lambda query: query.data == 'taxi_vin_query')
def taxi_vin_query(query: types.CallbackQuery):
    bot.answer_callback_query(query.id, 'запрос на получение информации о нахождении в реестрах такси')
    with ThreadPoolExecutor() as executor:
        executor.map(post_taxi_vin_query, [query])

def post_taxi_vin_query(query: types.CallbackQuery):
    vin = query.message.json['reply_to_message']['text'].replace(' ', '')
    userID = query.message.json['reply_to_message']['from']['id']

    res = requests.get(f'https://parser-api.com/parser/taxi_api/?vin={vin}&key={API_KEY}').json()
    print(res['records'])
    if res['records']:
        a = 'Числилась в реестрах:\n'
        for elem in res['records']:
            date = elem['dateFrom']
            status = elem['isActual']
            a += f'====[TAXI]====\n' \
                 f'в {date}\n'
            if status:
                a += 'статус: активен\n'
            else:
                a += 'статус: неактивен\n'
        bot.reply_to(query.message.reply_to_message, a)
    else:
        bot.reply_to(query.message.reply_to_message, 'Информации в реестрах такси не найдено')

@bot.callback_query_handler(lambda query: query.data == 'zalogi_vin_query')
def zalogi_vin_query(query: types.CallbackQuery):
    bot.answer_callback_query(query.id, 'начата проверка по риестру залогов')
    with ThreadPoolExecutor() as executor:
        executor.map(post_zalogi_vin_query, [query])

def post_zalogi_vin_query(query: types.CallbackQuery):
    vin = query.message.json['reply_to_message']['text'].replace(' ', '')
    userID = query.message.json['reply_to_message']['from']['id']

    res = requests.get(f'http://parser-api.com/parser/reestr_api/?key={API_KEY}&vin={vin}').json()
    if res.get('records'):
        a = ''
        for elem in res['records']:
            dataReg = elem['register_date']
            number = elem['number']
            objects = ''
            pledgors = ''
            pledgees = ''
            history = ''
            for obj in elem['objects']:
                objects += 'обьект'.join(obj).join('\n')
            for pled in elem['pledgors']:
                type = pled['type']
                name = pled['name']
                pledgors += f'тип: {type}\n' \
                            f'именуется: {name}\n' \
                            f'===========\n'
            for pleds in elem['pledgees']:
                type = pleds['type']
                name = pleds['name']
                pledgees += f'тип: {type}\n' \
                            f'именуется: {name}\n' \
                            f'===========\n'
            for hisor in elem['history']:
                date = hisor['date']
                type = hisor['type']
                number = hisor['number']
                history += f'дата: {date}\n' \
                          f'тип: {type}\n' \
                          f'номер: {number}\n' \
                           f'===========\n'
            a += f'дата регистрации: {dataReg}' \
                 f'номер документа: {number}' \
                 f'{objects}'\
                 f'залогодатели:\n{pledgors}' \
                 f'залогодержатели:\n{pledgees}' \
                 f'история:\n{history}'
            bot.send_message(userID, a)
    else:
        bot.send_message(userID, 'По данному vin-коду не найдено залогов')

#здесь обработчики запросов с сообщения госномера =>

@bot.callback_query_handler(lambda query: query.data == "other_funk_gosnom")
def other_funk_gosnom(query: types.CallbackQuery):
    mark = types.InlineKeyboardMarkup()
    mark.add(types.InlineKeyboardButton('📝Полный отчет', callback_data='report_gosnom_query'))
    mark.add(types.InlineKeyboardButton('🚗Получить VIN', callback_data='get_vin_gosnom'))
    mark.add(types.InlineKeyboardButton('🏁Получить пробег', callback_data='probeg_gosnom'))
    mark.add(types.InlineKeyboardButton('🛃Пройденные ТО', callback_data='to_gosnom_query'))
    mark.add(types.InlineKeyboardButton('🚕Работа в такси', callback_data='taxi_gosnom_query'))
    mark.add(types.InlineKeyboardButton('🔥Реестр залогов', callback_data='zalogi_gosnom_query'))
    #mark.add(types.InlineKeyboardButton('****', callback_data='tex_gosnom_query')) #'🔥**Реестр залогов**'
    bot.edit_message_reply_markup(query.from_user.id, query.message.id, reply_markup=mark)
    bot.answer_callback_query(query.id)

@bot.callback_query_handler(lambda query: query.data == 'report_gosnom_query')
def report_gosnom_query(query: types.CallbackQuery):
    rep = report(bot)
    bot.answer_callback_query(query.id, f'Запрос на отчет по госномеру: {query.message.reply_to_message.text} принят')
    with ThreadPoolExecutor() as executor:
        executor.map(rep.gosnom_report, [query.message.reply_to_message])

@bot.callback_query_handler(lambda query: query.data == 'get_vin_gosnom')
def get_vin_gosnom(query: types.CallbackQuery):
    bot.answer_callback_query(query.id, 'Запрос на получение vin в обработке')
    with ThreadPoolExecutor() as executor:
        executor.map(post_vin_gosnom_query, [query])

def post_vin_gosnom_query(query: types.CallbackQuery):
    gosnom = query.message.json['reply_to_message']['text'].replace(' ', '')
    userID = query.message.json['reply_to_message']['from']['id']

    res = requests.get(f'https://parser-api.com/parser/rsa_api/?key={API_KEY}&regNumber={gosnom}')
    if res.text.find('vin') != -1:
        vin = res.json()['policies'][0]['vin']
        print('police')
    else:
        print('try easito')
        res = requests.get(f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&regNumber={gosnom}')
        if res.text.find('diagnose_cards') != -1:
            vin = res.json()['diagnose_cards'][0]['vin']
            print('try easito nice')
        else:
            print('try not nice')
            vin = ' увы не найден'
    bot.reply_to(query.message.reply_to_message, f"*vin:* {vin}", parse_mode="Markdown")

@bot.callback_query_handler(lambda query: query.data == 'probeg_gosnom')
def probeg_gosnom(query: types.CallbackQuery):
    bot.answer_callback_query(query.id, 'запрос на получение пробега принят в обработку')
    with ThreadPoolExecutor() as executor:
        executor.map(post_probeg_gosnom, [query])

def post_probeg_gosnom(query: types.CallbackQuery):
    gosnom = query.message.json['reply_to_message']['text'].replace(' ', '')
    userID = query.message.json['reply_to_message']['from']['id']

    ress = requests.get(f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&regNumber={gosnom}')
    res = json.loads(ress.text)
    prob = res['diagnose_cards'][0]['mileage']
    date = res['diagnose_cards'][0]['startDate']
    sen = f'последний зафиксированный пробег:\n{prob}\nдата: {date}'
    bot.reply_to(query.message.reply_to_message, sen)



@bot.callback_query_handler(lambda query: query.data == 'to_gosnom_query')
def to_gosnom_query(query: types.CallbackQuery):
    bot.answer_callback_query(query.id, 'запрос на получении ТО в обработке')
    with ThreadPoolExecutor() as executor:
        executor.map(post_TO_gosnom_query, [query])


def post_TO_gosnom_query(query):
    gosnom = query.message.json['reply_to_message']['text'].replace(' ', '')
    userName = query.message.json['reply_to_message']['from']['first_name']
    userID = query.message.json['reply_to_message']['from']['id']

    ress = requests.get(f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&regNumber={gosnom}')
    res = json.loads(ress.text)
    sen = f'*по госномеру* {gosnom}\n' \
          f'*найдены следующие ТО*\n'
    for i in res['mileages']:
        date  = i['date']
        mileage = i['mileage']
        sen+= f"\n*дата:* {date}" \
              f"\n*пробег:* {mileage}" \
              f"\n*----------------*"
    print('ayf')
    bot.reply_to(query.message.reply_to_message, sen, parse_mode="Markdown")

@bot.callback_query_handler(lambda query: query.data == 'taxi_gosnom_query')
def taxi_gosnom_query(query: types.CallbackQuery):
    bot.answer_callback_query(query.id, 'запрос на получение информации о нахождении в реестрах такси')
    with ThreadPoolExecutor() as executor:
        executor.map(post_taxi_gosnom_query, [query])

def post_taxi_gosnom_query(query: types.CallbackQuery):
    gosnom = query.message.json['reply_to_message']['text'].replace(' ', '')
    userID = query.message.json['reply_to_message']['from']['id']

    res = requests.get(f'https://parser-api.com/parser/taxi_api/?regNumber={gosnom}&key={API_KEY}').json()
    print(res['records'])
    if res['records']:
        a = 'числилась в реестрах:\n'
        for elem in res['records']:
            date = elem['dateFrom']
            status = elem['isActual']
            a += f'====[TAXI]====\n' \
                 f'в {date}\n'
            if status:
                a += 'статус: активен\n'
            else:
                a += 'статус: неактивен\n'
        bot.reply_to(query.message.reply_to_message, a)
    else:
        bot.reply_to(query.message.reply_to_message, '*информации в реестрах такси не найдено*', parse_mode="Markdown")

@bot.callback_query_handler(lambda query: query.data == 'zalogi_gosnom_query')
def zalogi_gosnom_query(query: types.CallbackQuery):
    bot.answer_callback_query(query.id, 'начата проверка по риестру залогов')
    with ThreadPoolExecutor() as executor:
        executor.map(post_zalogi_gosnom_query, [query])

def post_zalogi_gosnom_query(query: types.CallbackQuery):
    gosnom = query.message.json['reply_to_message']['text'].replace(' ', '')
    userID = query.message.json['reply_to_message']['from']['id']

    res = requests.get(f'http://parser-api.com/parser/reestr_api/?key={API_KEY}&regNumber={gosnom}').json()
    if res.get('records'):
        a = ''
        for elem in res['records']:
            dataReg = elem['register_date']
            number = elem['number']
            objects = ''
            pledgors = ''
            pledgees = ''
            history = ''
            for obj in elem['objects']:
                objects += 'обьект'.join(obj).join('\n')
            for pled in elem['pledgors']:
                type = pled['type']
                name = pled['name']
                pledgors += f'тип: {type}\n' \
                            f'именуется: {name}\n' \
                            f'===========\n'
            for pleds in elem['pledgees']:
                type = pleds['type']
                name = pleds['name']
                pledgees += f'тип: {type}\n' \
                            f'именуется: {name}\n' \
                            f'===========\n'
            for hisor in elem['history']:
                date = hisor['date']
                type = hisor['type']
                number = hisor['number']
                history += f'дата: {date}\n' \
                           f'тип: {type}\n' \
                           f'номер: {number}\n' \
                           f'===========\n'
            a += f'дата регистрации: {dataReg}' \
                 f'номер документа: {number}' \
                 f'{objects}' \
                 f'залогодатели:\n{pledgors}' \
                 f'залогодержатели:\n{pledgees}' \
                 f'история:\n{history}'
            bot.send_message(userID, a)
    else:
        bot.send_message(userID, 'по данному vin-коду не найдено залогов')

@bot.callback_query_handler(lambda query: query.data == 'tex_gosnom_query')
def tex_gosnom_query(query: types.CallbackQuery):
    bot.answer_callback_query(query.id, '')
    with ThreadPoolExecutor() as executor:
        executor.map(post_tex_gosnom_query, [query])

def post_tex_gosnom_query(query: types.CallbackQuery):
    gosnom = query.message.json['reply_to_message']['text'].replace(' ', '')
    userID = query.message.json['reply_to_message']['from']['id']

    res = requests.get(f'https://parser-api.com/parser/eaisto_mileage_api/?key={API_KEY}&regNumber={gosnom}').json()

    a = 'диагностические карты:\n'
    for elem in res['diagnose_cards']:
        number = elem['number']
        startDate = elem['startDate']
        endDate = elem['endDate']
        vin = elem['vin']
        regNumber = elem['regNumber']
        mark = elem['mark']
        model = elem['model']
        mileage = elem['mileage']

        a += f'номер диагностической карты:\n{number}\n' \
             f'начало диагностики:\n{startDate}\n' \
             f'конец диагностики:\n{endDate}\n' \
             f'vin = {vin}\n' \
             f'госномер: {regNumber}\n' \
             f'марка: {mark}\n' \
             f'модель: {model}\n' \
             f'пробег на момент диагностики:\n{mileage}\n' \
             f'============================'
    bot.send_message(userID, a)

#========================================================

@bot.message_handler(content_types=['contact'])
def contact(contact: types.Contact):
    print(contact.contact)
    tgID = contact.contact.user_id
    firstName = contact.contact.first_name
    userName = contact.from_user.username
    lastName = contact.contact.last_name
    phoneNumber = contact.contact.phone_number

    if push_user(tgID, firstName, userName, lastName, phoneNumber):
        bot.send_message(contact.from_user.id, '*😀Рады приветствовать вас!*\n\n' + defultMessage, parse_mode="Markdown")
    else:
        bot.send_message(contact.from_user.id, 'ваш аккаунт уже зарегистрирован')

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = types.KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
    markup.add(contact_button)
    bot.send_message(message.chat.id, 'здравствуйте, для начальной регистрации необходимо получение контактных данных',
                     reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text_worker(message: types.Message):
    text = message.text.replace(' ', '')
    print(text)
    if text.find('$') != -1:
        fssp_start(message)
    elif text.find('https://') != -1 or text.find('http://') != -1:
        start_url(message)
    elif 7 <= len(text) >= 8 and check_gosnom(text):
        gosnom_start(message)
    elif len(text) == 17 and check_vin(text):
        vin_start(message)
    # elif len(text) == 11 or len(text) == 12 and list(text)[0] == '+':
    #     number_start(message)
    elif len(text) >= 11 and check_number(text):
        number_start(message)
    elif check_name(message.text):
        fssp_start(message)
    else:
        bot.send_message(message.from_user.id, 'инструкция')


def check_vin(text:str):
    print('nice cock')
    text = text.upper()
    granted =  ['A', 'E', 'I', 'O', 'U', 'Y', 'B', 'C',
                'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
                'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W',
                'X', 'Z', '1', '2', '3', '4', '5', '6',
                '7', '8', '9', '0']

    res = True
    for i in text:
        if res:
            for l in granted:
                if i == l:
                    break
                if l == '0':
                    res = False
        else:
            return False
    return res



def check_name(text):
    textLst = list(text)
    words = []
    word = ''

    for i in range(len(textLst)):
        if textLst[i] == ' ':
            words.append(word)
        elif i == len(textLst) - 1:
            word += textLst[i]
            words.append(word)
        else:
            word += textLst[i]
    # при условии что слово 1 алгоритм запишет лишь 1 букву

    if len(words[0]) == 1 or len(words) > 3:
        return False
    elif len(words) == 2:
        return 2
    elif len(words) == 3:
        return 3


def check_number(number: str):
    number = number.replace('+', '').replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    nums = ''
    for i in number:
        for a in num:
            if i == a:
                nums += '1'
    if len(number) == len(nums):
        res = True
    else:
        res = False
    return res


def start_url(message: types.Message):
    with ThreadPoolExecutor() as executor:
        executor.map(url, [message])

def url(message: types.Message):

    ress = requests.get(
        f'http://crwl.ru/api/rest/latest/get_ad/?api_key=3c546d52e9d39dd03fb662265c6a193e&url={message.text}')
    res = ress.json()
    # print(res['title'])
    print(res)
    bot.send_message(message.chat.id, res['phone'])

def fssp_start(message:types.Message):
    with ThreadPoolExecutor() as exect:
        exect.map(fssp, [message])

def fssp(message:types.Message):
    fmes = bot.send_message(message.from_user.id, 'запрос по ФСИН в обработке')
    words = check_name(message.text)
    firstName = ''
    lastName = ''

    switch = True

    if words == 2:
        for i in message.text:
            if switch:
                if i == ' ':
                    switch = False
                firstName += i
            else:
                lastName += i
        res = requests.get(
            f'http://parser-api.com/parser/info_api/?type=TYPE_SEARCH_FIZ&regionID=-1&lastName={lastName}'
            f'&firstName={firstName}&key=90342864f3b769f22fd93e57aba51a49')

        print(firstName)
        print(lastName)
        order_persons = list()
        print(
            f'http://parser-api.com/parser/info_api/?type=TYPE_SEARCH_FIZ&regionID=-1&lastName={lastName}'
            f'&firstName={firstName}&key=90342864f3b769f22fd93e57aba51a49')
    else:
        switch = 0
        patronymic = ''
        for i in message.text:
            if i == ' ':
                switch += 1
                continue
            if switch == 0:
                firstName += i
            elif switch == 1:
                lastName += i
            elif switch == 2:
                patronymic += i

        #http://parser-api.com/parser/info_api/?type=TYPE_SEARCH_FIZ&regionID=-1&lastName=%D0%98%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2%D0%B8%D1%87&firstName=%D0%98%D0%B2%D0%B0%D0%BD&key=90342864f3b769f22fd93e57aba51a49&patronymic=%D0%9A%D0%B0%D0%BD%D1%86%D0%B8%D0%B1%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9
        res = requests.get(
            f'http://parser-api.com/parser/info_api/?type=TYPE_SEARCH_FIZ&regionID=-1&'
            f'lastName={lastName}&firstName={firstName}'
            f'&key=90342864f3b769f22fd93e57aba51a49&patronymic={patronymic}')
        print('tyt tri')
    print('ayff')
    res = res.json()

    print(firstName)
    print(lastName)

    a = 'вот кого мне удалось найти:\n'
    if res.get('result'):
        if res['result'] != []:
            for i in res['result']:
                a += i['debtor_name']
                a += '\n'
                a += i['debtor_dob']
                a += '\n-------------\n'
            bot.edit_message_text(a, message.from_user.id, fmes.id)
            print('hello')
        else:
            bot.edit_message_text(f'Нет информации о долгах {lastName} {firstName} ', message.from_user.id, fmes.id)
    else:
        bot.edit_message_text(f'Нет информации о долгах {lastName} {firstName} ', message.from_user.id, fmes.id)


def number_start(message: types.Message):
    with ThreadPoolExecutor() as executor:
        executor.map(number, [message])

def number(message: types.Message):
        numt = message.text.replace('+', '').replace(' ', '').replace('(', '').replace(')', '').replace('-', '')    
        bot.send_message(message.from_user.id,
                         f'заявка на генерацию отчета по номеру {numt} принята \nожидайте от минуты до получаса')
        le = list(numt)
        if le[0] == '+':
            le.remove('+')
        elif le[0] == '8':
            le[0] = '7'
        res = ''.join(le)
        print(message.from_user)
        num = numberr.docN(res, message.from_user.username)
        link = putFile.put(num.getHtml())
        print('hey')
        bot.send_message(message.from_user.id, f'отчет по номеру {res} доступен по сылке\n' + link)


def vin_start(message:types.Message):
    vin = message.text.replace(' ', '')
    mark = types.InlineKeyboardMarkup()
    mark.add(types.InlineKeyboardButton('📝полный отчет', callback_data='report_vin_query'))
    mark.add(types.InlineKeyboardButton('🧿другие функции...', callback_data='other_funk_vin'))
    records = read_reports_by_vin(vin)

    if records:
        ready_reports = 'готовые отчеты:\n'
        for record in records:
            ready_reports += f'от [{record[1]}]({record[0]})\n'
    else:
        ready_reports = ''
    bot.reply_to(message, f'vin: {vin}\n{ready_reports}', reply_markup=mark, parse_mode="Markdown")

def gosnom_start(message:types.Message):
    gosnom = message.text.replace(' ', '').upper()
    gosnomList = list(gosnom)
    records = read_reports_by_reg_number(gosnom)
    records = read_reports_by_reg_number(gosnom)

    if records:
        ready_reports = 'готовые отчеты:\n'
        for record in records:
            ready_reports += f'{record[0]}\nот {record[1]}\n'
    else:
        ready_reports = ''
    if records:
        ready_reports = 'готовые отчеты:\n'
        for record in records:
            ready_reports += f'от [{record[1]}]({record[0]})\n'
    else:
        ready_reports = ''
    region = ''
    for i in range(6, len(gosnom)):
        region += gosnomList[i]
    mark = types.InlineKeyboardMarkup()
    mark.add(types.InlineKeyboardButton("📝полный отчет", callback_data='report_gosnom_query'))
    mark.add(types.InlineKeyboardButton("🧿другие функции...", callback_data= 'other_funk_gosnom'))
    bot.reply_to(message, f"*госномер* {gosnom}\n*зарегистрирован в субьекте РФ*: {region_codes[region]}\n{ready_reports}",
                 reply_markup=mark, parse_mode="Markdown")

def check_gosnom(text):
    lst = list(text)
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    gosnom = ''
    region = ''
    for i in range(len(text)):
        bol = False
        for element in num:
            if lst[i] == element:
                bol = True
        if bol:
            gosnom += '1'
        else:
            gosnom += '0'
        if i > 5:
            region += lst[i]
    if gosnom == '01110011' or gosnom == '011100111' and region in region_codes:
        return True
    else:
        return False


def check_user(message: types.Message):
    resp = client_use(message.from_user.id)
    if resp > 0:
        print(resp, end='>>>>>>>>>\n')
        return resp
    else:
        print('<<<<<<<<<<')
        return True

bot.polling(none_stop=True)

bot.edit_