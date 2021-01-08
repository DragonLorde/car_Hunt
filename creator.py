#import getData
from bs4 import BeautifulSoup
import uuid
import datetime
import requests
import random
import paramiko
import time

#from google_trans_new import google_translator




class mang:
    def reg(a):
        liteers = []
        numbers = []
        for lit in a:
            if lit.isdigit():
                numbers.append(lit)
            else:
                liteers.append(lit)
        return [liteers, numbers]

    def regCr(doct, regNumber):
        reg = doct.find("div", {"class": "reg__row"})
        regN = reg.find("div", {"class": "reg__row-r"})
        i = 0
        n2 = []
        for n in regNumber[1]:
            if i <= 2:
                i += 1
                n2.append(n)
        i2 = 0
        n3 = []
        for n4 in regNumber[1]:
            if i2 > 2:
                i2 += 1
                n3.append(n4)
            else:
                i2 += 1
        region = ''.join(n3)
        prf1 = doct.find('p', {'class': 'pref1'})
        prf2 = doct.find('p', {'class': 'pref2'})
        prf3 = doct.find('p', {'class': 'pref3'})
        prf4 = doct.find('p', {'class': 'pref4'})
        prf5 = doct.find('p', {'class': 'pref5'})
        prf6 = doct.find('p', {'class': 'pref6'})
        prf7 = doct.find('p', {'class': 'pref7'})
        prf1.string = regNumber[0][0]
        prf2.string = n2[0]
        prf3.string = n2[1]
        prf4.string = n2[2]
        prf5.string = regNumber[0][1]
        prf6.string = regNumber[0][2]
        prf7.string = region

class doc(mang):

    def __init__(self, data, tg_name, region_country):
        a = time.time()
        self.gib = data[0]
        self.eas = data[1]
        self.rsa = data[2]
        self.zal = data[3]
        self.taxi = data[4]
        self.name = tg_name
        docs = doc.docc()
        self.soup = BeautifulSoup(docs, 'html.parser')
        self.region = region_country


        if self.gib['history'] != None:
            #self.vin_info_car = self.vin_Info()
            self.date_car = self.date_Car()
            self.mile_generation = self.mile_Gen()
            self.mls = self.mile_generation['mile'][len(self.mile_generation['mile']) - 1]['mileage']
            self.mlsDt = ''


            self.head()
            self.base()
            # self.carPhoto()
            self.own()
            self.mid()
            self.own2()
            self.dtp()

            self.easit()
            self.rsas()
            self.wntd()
            self.ogr()
            self.zlgs()
            self.taxx()
            print('tut ia oi')
        else:
            self.mile_generation = self.mile_Gen_japan()
            self.mls = self.mile_generation['mile'][len(self.mile_generation) - 1]['mileage']
            self.head()
            self.midJApan()
            self.rsas()
            self.easit()
            self.zlgs()
            self.taxx()
            self.own2_japan()
            self.base_japan()
            self.wntd_japan()
            self.own_japan()
            self.ogr_japan()
            self.dtp_japan()
        print(a - time.time(), end='>>>>>>>>>>>\n')

    def docc():
        with open("venv/example/nomer2/index.html", "r", encoding='utf-8') as f:
            datas = f.read()
            f.close()
            return datas

    def head(self):

        header = self.soup.find('header')
        regNumber = mang.reg (self.rsa['policies'][0]['regNumber'])
        mang.regCr(self.soup, regNumber)
        now = datetime.datetime.now()
        hdN = self.soup.find('span', {"class": "header__name"})
        hdD = self.soup.find('span', {"class": "header__date"})
        hdN.string = self.name
        hdD.string = str(now.strftime("%d-%m-%Y %H:%M"))
        #doc.getHtml(soup)
        logoImg = header.find("img", {"class": "header__logo-img"})
        if self.carPhoto():
            logoImg['src'] = self.carPhoto()
        #print(logoImg['src'])
        #doc.getHtml(self.soup)

    def base(self):
        now = datetime.datetime.now()
        region = self.soup.find('p', {"class": "region__region2"})
        region.string = self.region
        milg = self.soup.find('span', {"class": "base__mile-km"})
        milD = self.soup.find('span', {"class": "base__mile-date"})
        gb = self.soup.find('span', {"class": "base__dtp"})
        print('heee')
        if self.eas.get('diagnose_cards'):
            milg.string = str(self.eas['diagnose_cards'][0]['mileage'])
        else:
            print(self.mls)
            milg.string = str(self.mls)

        milD.string = self.mile_generation['mile'][len(self.mile_generation['mile']) - 1]['date']

        if self.gib['accidents'] == []:
            gb.string = 'Не участвовал в ДТП!'
            print(gb)
        else:
            gb.string = 'Внимание! Участвовал в ДТП'
            print(gb)

        print('asfasfsafsafasf')

        reg22 = self.soup.find('span', {"class": "reg2__reg22"})
        reg22.string = self.rsa['policies'][0]['regNumber']
        print(reg22)
        model = self.soup.find('span', {"class": "base__info-mark"})
        yer = self.soup.find('span', {"class": "base__info-date"})
        cat = self.soup.find('span', {"class": "base__info-kat"})
        kz = self.soup.find('span', {"class": "base__info-kz"})
        clr = self.soup.find('span', {"class": "base__info-clr"})
        ob3 = self.soup.find('span', {"class": "base__info-ob3"})
        pwr = self.soup.find('span', {"class": "base__info-pw"})
        dvig = self.soup.find('span', {"class": "base__info-dw"})
        type = self.soup.find('span', {"class": "base__info-type"})
        model.string = self.gib['history']['model']
        yer.string = self.gib['history']['year']
        cat.string = self.gib['history']['category']
        kz.string = self.gib['history']['bodyNumber']
        clr.string = self.gib['history']['color']
        #print(self.vin_info_car)
        print('gaynooo')
        ob3.string = ','.join(list(str(round(int('1396'), -2)).strip('00')))
        pwr.string = self.gib['history']['powerHp']
        dvig.string = self.gib['history']['engineNumber']
        type.string = self.gib['history']['type']
        print('hhhhhhhhhhhhhhhhhhhhh')


    def base_japan(self):
        now = datetime.datetime.now()
        milg = self.soup.find('div', {"class": "base"})
        milg.decompose()


    def own(self):
        print('2')
        ownC = self.soup.find('span', {"class": "owner__count"})
        ownD = self.soup.find('span', {"class": "owner__date"})
        col = self.soup.find('div', {"class": "owner__column"})
        ownC.string = str(len(self.gib['history']['ownershipPeriods']))
        dt = self.date_car
        if int(dt['date']) <= 2:
            ownD.string = str(dt['date']) + ' год'
        elif int(dt['date']) > 2 and int(dt['date']) <= 4:
            ownD.string = str(dt['date']) + ' года'
        elif int(dt['date']) <= 5:
            ownD.string = str(dt['date']) + ' лет'


        for prop in self.gib['history']['ownershipPeriods']:
            div = self.soup.new_tag('div', **{'class':'owner__info-row2 ow-ow'})
            img = self.soup.new_tag('img', src='res/icon/planning.svg')
            div2 = self.soup.new_tag('div')
            p = self.soup.new_tag('p')
            p2 = self.soup.new_tag('p')
            p3 = self.soup.new_tag('p')
            span4 = self.soup.new_tag('span')
            span = self.soup.new_tag('span')
            span2 = self.soup.new_tag('span')
            span3 = self.soup.new_tag('span')

            span.string = 'С ' + prop['from']
            if prop['to'] != None:
                #print(prop['to'])
                span2.string = ' по ' + prop['to']
            else:
                span2.string = ' По сегодняшний день '

            span4.string = str(prop['lastOperation'])
            span3.string = str(prop['personType'])
            div.append(img)
            div2.append(p)
            div2.append(p2)
            div2.append(p3)
            p.string = 'Дата: '
            p2.string = 'Владелец: '
            p3.string = 'Последняя операция: '
            p3.append(span4)
            p.append(span)
            p.append(span2)
            p2.append(span3)
            div.append(div2)
            col.append(div)

    def own_japan(self):
        ownC = self.soup.find('div', {"class": "owner"})
        ownC.decompose()


    def mid(self):
        print('2')

        mrk = self.soup.find('span', {"class": "mid__info-mark"})
        mdl = self.soup.find('span', {"class": "mid__info-model"})
        eyr = self.soup.find('span', {"class": "mid__info-eyer"})
        sel = self.soup.find('span', {"class": "mid__info-seal"})
        #translator = google_translator('en')
        modelProp = self.gib['history']['model'].split()
        #mdArr = []
        # if len(modelProp) >= 3:
        #     translate_text = translator.detect( self.gib['history']['model'])
        #     print(translate_text)
        #     text1 = translator.translate(modelProp[1])
        #     text2 = translator.translate(modelProp[2].lower())
        #     text3 = translator.translate(modelProp[0])
        #     model = text1 + '_' + text2
        #     mark = text3
        #     #print(mark.replace(' ', '') + '-' + model.replace(' ', ''))
        #     mdArr.append(mark.replace(' ', ''))
        #     mdArr.append(model.replace(' ', ''))
        #
        # else:
        #     for mdProp in modelProp:
        #         translate_text = translator.detect(mdProp)
        #         if (translate_text != 'en'):
        #             text = translator.translate(mdProp, lang_tgt='en')
        #             mdArr.append(text)
        #         else:
        #             mdArr.append(mdProp)

        eyr.string = self.gib['history']['year']
        # if modelProp[0].replace(' ', '') == 'ХЕНДЭ':
        #     mdArr[0] = 'hyundai'

       # md = self.mid_Car(mdArr[0], mdArr[1])

       # sel.string = md['seal']
        mrk.string = 'any'
        mdl.string = 'any'

        col = self.soup.find('div', {"class": "mid__mile-column"})
        #print(self.eas['mieages'])
        if self.eas.get('diagnose_cards'):
            for prop in reversed(self.eas['mileages']):
                div = self.soup.new_tag('div', **{'class': 'fnd'})
                p = self.soup.new_tag('p')
                span = self.soup.new_tag('span', **{'class': 'mid__mile-km'})
                span2 = self.soup.new_tag('span', **{'class': 'mid__mile-date'})
                span.string = str(prop['mileage']) + ' КМ по состоянию на '
                span2.string = prop['date']
                p.append(span)
                p.append(span2)
                div.append(p)
                col.append(div)
                self.mls = str(prop['mileage'])
                self.mlsDt = prop['date']
        else:
            for prop in self.mile_generation['mile']:
                div = self.soup.new_tag('div', **{'class': 'fnd'})
                p = self.soup.new_tag('p')
                span = self.soup.new_tag('span', **{'class': 'mid__mile-km'})
                span2 = self.soup.new_tag('span', **{'class': 'mid__mile-date'})
                span.string = str(prop['mileage']) + ' КМ по состоянию на '
                span2.string = prop['date']
                p.append(span)
                p.append(span2)
                div.append(p)
                col.append(div)
                self.mls = str(prop['mileage'])
                self.mlsDt = prop['date']

    def midJApan(self):
        mdS = self.soup.find('div', {"class": "mid"})['class'] = 'mid japan'
        print(mdS)


        mrk = self.soup.find('span', {"class": "mid__info-mark"})
        mdl = self.soup.find('span', {"class": "mid__info-model"})
        eyr = self.soup.find('span', {"class": "mid__info-eyer"})
        sel = self.soup.find('span', {"class": "mid__info-seal"})
        mark = self.rsa['policies'][0]['mark']
        model = self.rsa['policies'][0]['model']
        mrk.string = mark
        mdl.string = model
        now = datetime.datetime.now()

        eyr.string = 'не определенно'
        md = self.mid_Car_japan(mark, model)
        sel.string = md['seal']

        col = self.soup.find('div', {"class": "mid__mile-column"})
        # print(self.eas['mieages'])
        if self.eas.get('diagnose_cards'):
            for prop in reversed(self.eas['mileages']):
                div = self.soup.new_tag('div', **{'class': 'fnd'})
                p = self.soup.new_tag('p')
                span = self.soup.new_tag('span', **{'class': 'mid__mile-km'})
                span2 = self.soup.new_tag('span', **{'class': 'mid__mile-date'})
                span.string = str(prop['mileage']) + ' КМ по состоянию на '
                span2.string = prop['date']
                p.append(span)
                p.append(span2)
                div.append(p)
                col.append(div)
                self.mls = str(prop['mileage'])
                self.mlsDt = '2012-02-13'
        else:
            for prop in self.mile_generation['mile']:
                div = self.soup.new_tag('div', **{'class': 'fnd'})
                p = self.soup.new_tag('p')
                span = self.soup.new_tag('span', **{'class': 'mid__mile-km'})
                span2 = self.soup.new_tag('span', **{'class': 'mid__mile-date'})
                span.string = str(prop['mileage']) + ' КМ по состоянию на '
                span2.string = prop['date']
                p.append(span)
                p.append(span2)
                div.append(p)
                col.append(div)
                self.mls = str(prop['mileage'])
                self.mlsDt = '2012-02-13'


    def own2(self):
        print('3')

        gos = self.soup.find('span', {"class": "owner2__info-reg"})
        car = self.soup.find('span', {"class": "owner2__info-car"})
        yer = self.soup.find('span', {"class": "owner2__info-date"})
        owns = self.soup.find('span', {"class": "owner2__info-own"})
        dat = self.soup.find('span', {"class": "owner2__info-owndate"})
        index = len(self.rsa['policies']) - 1
        print(index)
        gos.string = self.rsa['policies'][0]['regNumber']
        car.string = self.gib['history']['model']
        yer.string = self.gib['history']['year']
        owns.string = self.rsa['policies'][0]['ownerName']
        dat.string = self.rsa['policies'][0]['ownerDob']

    def own2_japan(self):
        gos = self.soup.find('span', {"class": "owner2__info-reg"})
        car = self.soup.find('span', {"class": "owner2__info-car"})
        yer = self.soup.find('span', {"class": "owner2__info-date"})
        owns = self.soup.find('span', {"class": "owner2__info-own"})
        dat = self.soup.find('span', {"class": "owner2__info-owndate"})
        gos.string = self.rsa['policies'][0]['regNumber']
        car.string = self.rsa['policies'][0]['mark'] + ' ' + self.rsa['policies'][0]['model']
        yer.string = 'Информация не найдена'
        owns.string = self.rsa['policies'][0]['ownerName']
        dat.string = self.rsa['policies'][0]['ownerDob']

    def dtp(self):
        print('asfasfasfsa')
        cnt = self.soup.find('span', {"class": "dtp__count"})
        if self.gib['accidents'] != None:
            cnt.string = str(len(self.gib['accidents']))
        else:
            cnt.string = '0'

        col = self.soup.find('div', {"class": "dtp__column"})
        if len(self.gib['accidents']) > 0:
            for prop in self.gib['accidents']:
                div = self.soup.new_tag("div", **{'class': 'dtp__row'})
                p = self.soup.new_tag("p")
                p1 = self.soup.new_tag("p")
                p2 = self.soup.new_tag("p")
                p3 = self.soup.new_tag("p")
                p4 = self.soup.new_tag("p")
                p5 = self.soup.new_tag("p")
                p6 = self.soup.new_tag("p")
                span = self.soup.new_tag("span")
                span1 = self.soup.new_tag("span")
                span2 = self.soup.new_tag("span")
                span3 = self.soup.new_tag("span")
                span4 = self.soup.new_tag("span")
                span5 = self.soup.new_tag("span")
                span6 = self.soup.new_tag("span")
                span.string = prop['model'] + ' ' + prop['mark']
                span1.string = prop['accidentNumber']
                span2.string = prop['accidentType']
                span3.string = prop['regionName']
                span4.string = prop['accidentDatetime']
                span5.string = prop['vehicleAmount']
                span6.string = prop['vehicleSort']
                p.string = 'Автомобиль: '
                p1.string = 'Номер проишествия '
                p2.string = 'Тип: '
                p3.string = 'Регион: '
                p4.string = 'Время: '
                p5.string = 'Количиство ТС участвоваших в ДТП: '
                p6.string = 'Номер ТС в ДТП: '
                p.append(span)
                p1.append(span1)
                p2.append(span2)
                p3.append(span3)
                p4.append(span4)
                p5.append(span5)
                p6.append(span6)
                div.append(p)
                div.append(p1)
                div.append(p2)
                div.append(p3)
                div.append(p4)
                div.append(p5)
                div.append(p6)
                svg = BeautifulSoup(self.get_Svg(prop['damageSvg']), 'html.parser')
                header = self.soup.new_tag('head')
                body = self.soup.new_tag('body')
                header.append(svg.find('style'))
                body.append(svg.find('div', {"class": "dmgMap"}))
                div.append(header)
                div.append(body)
                col.append(div)
        if len(self.gib['accidents']) == 0:
            #print('asfasf')
            div = self.soup.new_tag("div", **{'class': 'dtp__row'})
            p = self.soup.new_tag("p")
            span = self.soup.new_tag('span')
            span.string = '✅ Автомобиль в ДТП не участвовал!'
            p.append(span)
            div.append(p)
            col.append(div)

    def dtp_japan(self):
        col = self.soup.find('div', {"class": "dtp"})
        col.decompose()
        print(col)

    def easit(self):
        print('4')

        reg = self.soup.find('span', {"class": "eas__row-reg"})
        mil = self.soup.find('span', {"class": "eas__row-pr"})
        bod = self.soup.find('span', {"class": "eas__row-bd"})
        dk = self.soup.find('span', {"class": "eas__row-dk"})
        yer = self.soup.find('span', {"class": "eas__row-date"})
        if self.eas.get('diagnose_cards'):
            reg.string = self.rsa['policies'][0]['regNumber']
            mil.string = str(self.eas['diagnose_cards'][0]['mileage'])
            bod.string = self.rsa['policies'][0]['vin']
            dk.string = str(self.eas['diagnose_cards'][0]['number'])
            yer.string = 'С ' + str(self.eas['diagnose_cards'][0]['startDate']) + ' по ' + str(self.eas['diagnose_cards'][0]['endDate'])
        else:
            reg.string = self.rsa['policies'][0]['regNumber']
            mil.string = str(self.mls)
            bod.string = self.rsa['policies'][0]['vin']
            dk.string = str(random.randint(201610101449162544600, 201610101449162544920))
            now = datetime.datetime.now()
            yer.string = str(self.mlsDt) + ' По ' + now.strftime("%d-%m-%Y")

    def rsas(self):
        print('asfasfa')
        cmp = self.soup.find('span', {"class": "rsa__cmp"})
        vn = self.soup.find('span', {"class": "rsa__vin"})
        ow = self.soup.find('span', {"class": "rsa__prs"})
        dat = self.soup.find('span', {"class": "rsa__date"})
        loc = self.soup.find('span', {"class": "rsa__loc"})
        cost = self.soup.find('span', {"class": "rsa__cst"})

        cmp.string = self.rsa['policies'][0]['companyName']
        vn.string = str(self.rsa['policies'][0]['vin'])
        ow.string = self.rsa['policies'][0]['ownerName']
        dat.string = self.rsa['policies'][0]['ownerDob']
        loc.string = self.rsa['policies'][0]['location']
        cost.string = self.rsa['policies'][0]['cost']
        print(cost.string)

    def wntd(self):
        col = self.soup.find('div', {"class": "wantd__column"})
        if len(self.gib['searches']) > 0:
            for prop in self.gib['searches']:
                div = self.soup.new_tag('div', **{'class': 'wantd__row'})
                p = self.soup.new_tag('p')
                p2 = self.soup.new_tag('p')
                p3 = self.soup.new_tag('p')
                span = self.soup.new_tag('span')
                span2 = self.soup.new_tag('span')
                span3 = self.soup.new_tag('span')
                span.append(prop['region'])
                span2.append(prop['model'])
                span3.append(prop['search_date'])
                p.string = 'Место розыска: '
                p2.string = 'Машина: '
                p3.string = 'Дата: '
                p.append(span)
                p2.append(span2)
                p3.append(span3)
                div.append(p)
                div.append(p2)
                div.append(p3)
                col.append(div)
        if len(self.gib['searches']) == 0:
            div = self.soup.new_tag('div', **{'class': 'owner__info-row'})
            img = self.soup.new_tag('img', src='res/icon/check.svg')
            p = self.soup.new_tag('p')
            p.string = '✅ По указанному VIN не не найденаинформация о розыске транспортного средства.'
            #p.append(img)
            div.append(p)
            col.append(div)

    def wntd_japan(self):
        col = self.soup.find('div', {"class": "wantd"})
        col.decompose()
        print(col)

    def ogr(self):
        col = self.soup.find('div', {"class": "ogr__column"})
        if len(self.gib['restrictions']) > 0:
            for prop in self.gib['restrictions']:
                div = self.soup.new_tag('div', **{'class': 'ogr__row'})
                p = self.soup.new_tag('p')
                p2 = self.soup.new_tag('p')
                p3 = self.soup.new_tag('p')
                p4 = self.soup.new_tag('p')
                p5 = self.soup.new_tag('p')
                p6 = self.soup.new_tag('p')
                span = self.soup.new_tag('span')
                span2 = self.soup.new_tag('span')
                span3 = self.soup.new_tag('span')
                span4 = self.soup.new_tag('span')
                span5 = self.soup.new_tag('span')
                span6 = self.soup.new_tag('span')
                span.append(prop['restriction_date'])
                span2.append(prop['region'])
                span3.append(prop['restriction_name'])
                span4.append(prop['organization_name'])
                span5.append(prop['reasons'])
                span6.append(prop['phone'])
                p.string = 'Дата: '
                p2.string = 'Регион: '
                p3.string = 'Тип: '
                p4.string = 'Кто наложил: '
                p5.string = 'Документы: '
                p6.string = 'Телефон пристава: '
                p.append(span)
                p2.append(span2)
                p3.append(span3)
                p4.append(span4)
                p5.append(span5)
                p6.append(span6)
                div.append(p)
                div.append(p2)
                div.append(p3)
                div.append(p4)
                div.append(p5)
                div.append(p6)
                col.append(div)
        if len(self.gib['restrictions']) == 0:
            div = self.soup.new_tag('div', **{'class': 'owner__info-row'})
            img = self.soup.new_tag('img', src='res/icon/check.svg')
            p = self.soup.new_tag('p')
            p.string = '✅ По указанному VIN не не найденаинформация об ограничениях.'
           # p.append(img)
            div.append(p)
            col.append(div)

    def ogr_japan(self):
        col = self.soup.find('div', {"class": "ogrs"})
        col.decompose()
        print(col)

    def zlgs(self):
        col = self.soup.find('div', {"class": "zlg__column"})
        if self.zal.get('records'):
            #print(self.zal['records'][0])
            for prop in self.zal['records']:
                div = self.soup.new_tag("div", **{"class": "zlg__row"})

                div1 = self.soup.new_tag("div", **{"class": "zlg__row-inf"})
                p = self.soup.new_tag("p")
                p2 = self.soup.new_tag("p")
                p3 = self.soup.new_tag("p")
                span = self.soup.new_tag("span")
                span2 = self.soup.new_tag("span")

                span.string = 'Дата-регистрации: ' + prop['register_date']
                span2.string = 'Номер: ' + prop['number']

                p.append(span)
                p2.append(span2)
                p3.string = 'Информация: '

                div1.append(p3)
                div1.append(p)
                div1.append(p2)
                div.append(div1)

                for prop3 in prop['objects']:
                    div4 = self.soup.new_tag("div", **{"class": "zlg__row-vin"})
                    p = self.soup.new_tag("p")

                    span.string = prop3

                    p.append(span)
                    div4.append(p)
                    div.append(div4)

                for prop2 in prop['pledgors']:
                    div2 = self.soup.new_tag("div", **{"class": "zlg__row-laz"})
                    p = self.soup.new_tag("p")
                    p2 = self.soup.new_tag("p")
                    p3 = self.soup.new_tag("p")
                    span = self.soup.new_tag("span")
                    span2 = self.soup.new_tag("span")


                    span.string = 'Тип: ' + prop2['type']
                    span2.string = 'Владелец: ' + prop2['name']

                    p.append(span)
                    p2.append(span2)
                    p3.string = 'Информация: '

                    div2.append(p3)
                    div2.append(p)
                    div2.append(p2)
                    div.append(div2)

                for prop2 in prop['history']:
                    div2 = self.soup.new_tag("div", **{"class": "zlg__row-laz"})
                    p = self.soup.new_tag("p")
                    p2 = self.soup.new_tag("p")
                    p3 = self.soup.new_tag("p")
                    p4 = self.soup.new_tag("p")

                    span = self.soup.new_tag("span")
                    span2 = self.soup.new_tag("span")
                    span3 = self.soup.new_tag("span")


                    span.string = 'Дата: ' + prop2['date']
                    span2.string = 'Тип: ' + prop2['type']
                    span3.string = 'Номер: ' + prop2['number']

                    p.append(span)
                    p2.append(span2)
                    p3.string = 'История: '
                    p4.append(span3)
                    div2.append(p3)
                    div2.append(p)
                    div2.append(p2)
                    div2.append(p4)
                    div.append(div2)

                col.append(div)



        else:
            div = self.soup.new_tag('div', **{'class': 'owner__info-row'})
            #img = self.soup.new_tag('img', src='res/icon/check.svg')
            p = self.soup.new_tag('p')
            p.string = '✅ По указанному VIN не не найденаинформация об ограничениях.'
            #p.append(img)
            div.append(p)
            col.append(div)


    def taxx(self):
        col = self.soup.find('div', {"class": "taxi__column"})
        if len(self.taxi['records']) > 0:
            for prop in self.taxi['records']:
                div = self.soup.new_tag("div", **{"class": "taxi__row"})
                p = self.soup.new_tag("p")
                p2 = self.soup.new_tag("p")
                p3 = self.soup.new_tag("p")
                span = self.soup.new_tag("span")
                span2 = self.soup.new_tag("span")
                span3 = self.soup.new_tag("span")
                span4 = self.soup.new_tag("span")

                span.string = 'Внимание! Автомобиль работал в такси '
                span2.string = 'С ' + prop['dateFrom']
                span3.string = ' по ' + prop['dateFrom']
                span4.string = 'Регион: ' + prop['regionName']

                p2.string = 'Дата: '
                p3.string = 'Регион: '

                p.append(span)
                p2.append(span2)
                p2.append(span3)
                p3.append(span4)

                div.append(p)
                div.append(p2)
                div.append(p3)

                col.append(div)
        else:
            div = self.soup.new_tag('div', **{'class': 'owner__info-row'})
            img = self.soup.new_tag('img', src='res/icon/check.svg')
            p = self.soup.new_tag('p')
            p.string = '🚕 Информация о наличии разрешения на осуществление деятельности по перевозке пассажиров не найдена.'
           # p.append(img)
            div.append(p)
            col.append(div)

    def getHtml(self):
        name = uuid.uuid4().hex
        name2 = "venv/example/nomer2/" + name + ".html"
        with open(name2, "w", encoding='utf-8') as fl:
            fl.write(str(self.soup))
        print(name2)
        return [name2 , name]

    def carPhoto(self):
        # у 804 км 799
        #self.rsa['policies'][0]['regNumber']
        response = requests.get('http://bsl-show.online/bot-data/reg.php?reg=' + self.rsa['policies'][0]['regNumber'])
        if response:
            jsn = response.json()
            if jsn['src']  == 'no__img':
                return False
            else:
                return jsn['src']
        else:
            print('An error has occurred.')
            return False

    def vin_Info(self):
        #KMHHT6KD1AU013407
        #self.rsa['policies'][0]['vin']
        response = requests.get('http://bsl-show.online/bot-data/vinDec.php?vin=' + self.gib['history']['vin'])
        vin = response.json()
        return vin

    def date_Car(self):
        response = requests.get('http://bsl-show.online/bot-data/date.php?date=' + self.gib['history']['ownershipPeriods'][0]['from'])
        vin = response.json()
        #print(vin)
        return vin


    def mid_Car(self, mrk, model):
        print(mrk)
        print(model)
        site = 'http://bsl-show.online/bot-data/mid.php?mrk=' + mrk + '&mdl=' + model + '&yer=' + self.gib['history']['year']
        response = requests.get(site.replace(' ', ''))
        return response.json()

    def mid_Car_japan(self, mrk, model):
        print(mrk)
        print(model)
        site = 'http://bsl-show.online/bot-data/midJapan.php?mrk=' + mrk + '&mdl=' + model;
        response = requests.get(site)
        return response.json()

    def mile_Gen(self):
        site = 'http://bsl-show.online/bot-data/genMile.php?date=' + self.gib['history']['ownershipPeriods'][0]['from']
        response = requests.get(site)
        return response.json()

    def mile_Gen_japan(self):
        site = 'http://bsl-show.online/bot-data/genMile.php?date=' + '2012-07-01'
        response = requests.get(site)
        return response.json()

    def get_Svg(self , link):
        site = link
        response = requests.get(site)
        return response.text



def put(name):
    print('asfasfasfsa')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('37.140.192.137', username='u1145099', password='Z!Hq2ukD')
    sftp = ssh.open_sftp()
    lnk = "www/bsl-show.online/push/number/" + name[1] + '.html'
    sftp.put(name[0], lnk)
    return 'https://bsl-show.online/push/number/' + name[1] + '.html'


# res = doc( , 'gay', 'Волгоградская обл, г Волгоград')
# link = put(res.getHtml())
# print(link)

