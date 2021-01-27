from bs4 import BeautifulSoup
import uuid
import datetime

import requests
import random
import paramiko
import os






class doc():
    def __init__(self, data, tg_id, region_country, vin):
        self.vin = vin
        self.gib = data[0]
        self.eas = data[1]
        self.rsa = data[2]
        self.zal = data[3]
        self.taxi = data[4]
        self.name = tg_id
        docs = doc.docc()
        self.soup = BeautifulSoup(docs, 'html.parser')
        self.region = region_country

        if self.gib['history'] != None:
            self.date_car = self.date_Car()
            self.mile_generation = self.mile_Gen()
            print(self.mile_generation['mile'])
            if self.mile_generation['mile'] != []:
                self.mls = self.mile_generation['mile'][len(self.mile_generation['mile']) - 1]['mileage']
                self.mlsDate = self.mile_generation['mile'][len(self.mile_generation['mile']) - 1]['date']
            else:
                self.mls = str('5000')
                now = datetime.datetime.now()
                self.mlsDate = str(now.strftime("%d-%m-%Y %H:%M"))
            self.mlsDt = ''

        self.head()
        self.base()
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



    def docc():
        with open("venv/example/nomer2/index.html", "r", encoding='utf-8') as f:
            datas = f.read()
            f.close()
            return datas


    def regCr(self, parse):

        liteers = []
        numbers = []
        for lit in parse:
            if lit.isdigit():
                numbers.append(lit)
            else:
                liteers.append(lit)
        regNumber = [liteers, numbers]

        reg = self.soup.find("div", {"class": "reg__row"})
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
        prf1 = self.soup.find('p', {'class': 'pref1'}).string = regNumber[0][0]
        prf2 = self.soup.find('p', {'class': 'pref2'}).string = n2[0]
        prf3 = self.soup.find('p', {'class': 'pref3'}).string = n2[1]
        prf4 = self.soup.find('p', {'class': 'pref4'}).string = n2[2]
        prf5 = self.soup.find('p', {'class': 'pref5'}).string = regNumber[0][1]
        prf6 = self.soup.find('p', {'class': 'pref6'}).string = regNumber[0][2]
        prf7 = self.soup.find('p', {'class': 'pref7'}).string = region


    def head(self):

        header = self.soup.find('header')
        logoImg = header.find("img", {"class": "header__logo-img"})
        if self.eas.get('diagnose_cards'):
            if self.eas['diagnose_cards'][0].get('regNumber'):
                if self.eas['diagnose_cards'][0]['regNumber'] != "None":
                    print('asfasfas')
                    self.regCr(self.eas['diagnose_cards'][0]['regNumber'])
                    if self.carPhotoEas():
                        logoImg['src'] = self.carPhotoEas()
                else:
                    print('dec')
                    regN = self.soup.find("div", {"class": "reg"})
                    regN.decompose()
            else:
                print('dec')
                regN = self.soup.find("div", {"class": "reg"})
                regN.decompose()
        elif self.rsa.get('policies'):
            print('dec')
            if self.rsa['policies'][0].get('regNumber'):
                if self.rsa['policies'][0]['regNumber'] != "None":
                    self.regCr(self.rsa['policies'][0]['regNumber'])
                    if self.carPhoto():
                        logoImg['src'] = self.carPhoto()
                elif self.eas.get('diagnose_cards'):
                    if self.eas['diagnose_cards'][0].get('regNumber'):
                        if self.eas['diagnose_cards'][0]['regNumber'] != 'None':
                            print('asfasfas')
                            self.regCr(self.eas['diagnose_cards'][0]['regNumber'])
                            if self.carPhotoEas():
                                logoImg['src'] = self.carPhotoEas()
                else:
                    regN = self.soup.find("div", {"class": "reg"})
                    regN.decompose()
            elif self.eas.get('diagnose_cards'):
                if self.eas['diagnose_cards'][0].get('regNumber'):
                    if self.eas['diagnose_cards'][0]['regNumber'] != 'None':
                        print('asfasfas')
                        if self.eas['diagnose_cards'][0]['regNumber'] != 'None':
                            self.regCr(self.eas['diagnose_cards'][0]['regNumber'])
                            if self.carPhotoEas():
                                logoImg['src'] = self.carPhotoEas()
                else:
                    regN = self.soup.find("div", {"class": "reg"})
                    regN.decompose()
            else:
                regN = self.soup.find("div", {"class": "reg"})
                regN.decompose()

        else:
            regN = self.soup.find("div", {"class": "reg"})
            regN.decompose()

        now = datetime.datetime.now()
        hdN = self.soup.find('span', {"class": "header__name"})
        hdD = self.soup.find('span', {"class": "header__date"})
        self.soup.find('span', {"class": "header__vins"}).string = self.vin
        hdN.string = self.name
        hdD.string = str(now.strftime("%d-%m-%Y %H:%M"))


    def base(self):
        region = self.soup.find('p', {"class": "region__region2"})
        region.string = self.region
        milg = self.soup.find('span', {"class": "base__mile-km"})
        milD = self.soup.find('span', {"class": "base__mile-date"})
        gb = self.soup.find('span', {"class": "base__dtp"})
        pled = self.soup.find('span', {"class": "base__zlg"})
        taxi = self.soup.find('span', {"class": "base__taxi"})
        rest = self.soup.find('span', {"class": "base__res"})
        srch = self.soup.find('span', {"class": "base__wntd"})

        if self.eas.get('diagnose_cards'):
            if self.eas['diagnose_cards'] != "None":
                milg.string = str(self.eas['diagnose_cards'][0]['mileage'])
                milD.string = str(self.eas['diagnose_cards'][0]['startDate'])
            else:
                milg.string = 'Не найдна информация'
                milD.string = 'Не найдна информация'
        elif self.gib['history'] != None:
            milg.string = str(self.mls)
            milD.string = str(self.mlsDate)
        else:
            milg.string = 'Не найдна информация'
            milD.string = 'Не найдна информация'


        if self.gib['accidents'] == []:
            gb.string = ' '
        else:
            gb.string = 'Внимание! Участвовал в ДТП'

        if self.zal.get('records'):
            pled.string = 'Внимание! Автомобиль находиться в залоге'
        else:
            pled.string = ' '

        if len(self.taxi['records']) > 0:
            taxi.string = 'Внимание! Автомобиль работал в такси'
        else:
            taxi.string = ' '

        if self.gib['searches'] == []:
            srch.string = ' '
        else:
            srch.string = 'Внимание! Автомобиль в розыске  '
        if self.gib['restrictions'] == []:
            rest.string = ' '
        else:
            rest.string = 'Внимание! На автомобиль наложены ограничения'

        if self.rsa.get('policies'):
            if self.rsa['policies'][0].get('regNumber'):
                reg22 = self.soup.find('span', {"class": "reg2__reg22"})
                reg22.string = self.rsa['policies'][0]['regNumber']
            elif self.eas.get('diagnose_cards'):
                if self.eas['diagnose_cards'][0].get('regNumber'):
                    reg22 = self.soup.find('span', {"class": "reg2__reg22"})
                    reg22.string = self.eas['diagnose_cards'][0]['regNumber']
                else:
                    reg22 = self.soup.find('div', {"class": "reg2"})
                    reg22.decompose()
            else:
                reg22 = self.soup.find('div', {"class": "reg2"})
                reg22.decompose()
        elif self.eas.get('diagnose_cards'):
            if self.eas['diagnose_cards'][0].get('regNumber'):
                reg22 = self.soup.find('span', {"class": "reg2__reg22"})
                reg22.string = self.eas['diagnose_cards'][0]['regNumber']
            else:
                reg22 = self.soup.find('div', {"class": "reg2"})
                reg22.decompose()
        else:
            reg22 = self.soup.find('div', {"class": "reg2"})
            reg22.decompose()



        if self.gib['history'] != None:
            print('1')
            self.soup.find('span', {"class": "base__info-mark"}).string = str(self.gib['history']['model'])
            self.soup.find('span', {"class": "base__info-date"}).string = str(self.gib['history']['year'])
            self.soup.find('span', {"class": "base__info-kat"}).string = str(self.gib['history']['category'])
            self.soup.find('span', {"class": "base__info-kz"}).string = str( self.gib['history']['bodyNumber'])
            self.soup.find('span', {"class": "base__info-clr"}).string = str(self.gib['history']['color'])
            self.soup.find('span', {"class": "base__info-ob3"}).string = ','.join(list(str(int(round(float(self.gib['history']['engineVolume']), -2))).strip('00')))
            self.soup.find('span', {"class": "base__info-pw"}).string = str( self.gib['history']['powerHp'])
            self.soup.find('span', {"class": "base__info-dw"}).string = str(self.gib['history']['engineNumber'])
            self.soup.find('span', {"class": "base__info-type"}).string = str( self.gib['history']['type'] )
        else:
            print('alo')
            milg = self.soup.find('div', {"class": "base__info"})
            milg['style'] = 'display: none'
            self.soup.findAll('div', {"class": "none"})[0]['style'] = 'display: block'




    def base_japan(self):
        now = datetime.datetime.now()
        milg = self.soup.find('div', {"class": "base"})
        milg.decompose()


    def own(self):

        if self.gib['history'] != None:
            ownC = self.soup.find('span', {"class": "owner__count"})
            ownD = self.soup.find('span', {"class": "owner__date"})
            col = self.soup.find('div', {"class": "owner__column"})
            ownC.string = str(len(self.gib['history']['ownershipPeriods']))
            dt = self.date_car
            if int(dt['date']) <= 2:
                if dt['date'] == 0:
                    ownD.string = 'Меньше одного года'
                else:
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

                span.string = 'С ' + str( prop['from'] )
                if prop['to'] != None:
                    #print(prop['to'])
                    span2.string = ' по ' +str( prop['to'] )
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
        else:
            self.soup.find('p', {"class": "owner__count"}).decompose()
            self.soup.find('p', {"class": "owner__countdate"}).decompose()
            self.soup.findAll('div', {"class": "none"})[1]['style'] = 'display: block'


    def own_japan(self):
        ownC = self.soup.find('div', {"class": "owner"})
        ownC.decompose()


    def mid(self):
        mrk = self.soup.find('span', {"class": "mid__info-mark"})
        mdl = self.soup.find('span', {"class": "mid__info-model"})
        eyr = self.soup.find('span', {"class": "mid__info-eyer"})
        sel = self.soup.find('span', {"class": "mid__info-seal"})
        mdArr = []

        if self.gib['history'] != None:
            eyr.string = self.gib['history']['year']
        else:
            eyr.decompose()

        if self.rsa.get('policies') and self.gib['history'] != None:
            if self.rsa['policies'][0].get('model') and self.rsa['policies'][0].get('mark'):
                print('opa')
                if len(self.rsa['policies'][0]['model'].split()) > 1:
                    mdArr = self.rsa['policies'][0]['model'].split()
                    model = mdArr[0] + '_' + mdArr[1]
                    mark = self.rsa['policies'][0]['mark']
                    print('alo')
                    md = self.mid_Car(mark, model)
                    if md['seal'] == 'no__data':
                        print('gay')
                        mdArr = self.gib['history']['model'].split()
                        mark = mdArr[0]
                        model = mdArr[1]
                        mrk.string = mdArr[0]
                        mdl.string = mdArr[1]
                        md = self.mid_Car(mark, model)
                        if md['seal'] == 'no__data':
                            print('no mid')
                        else:
                            mrk.string = mdArr[0]
                            mdl.string = mdArr[1]
                            sel.string = md['seal']
                    else:
                        mrk.string = mdArr[0]
                        mdl.string = mdArr[1]
                        sel.string = md['seal']
                else:
                    model = self.rsa['policies'][0]['model']
                    mark = self.rsa['policies'][0]['mark']
                    mrk.string = mark
                    mdl.string = model
                    md = self.mid_Car(mark, model)
                    if md['seal'] == 'no__data':
                        if len(self.gib['history']['model'].split()) > 1:
                            mdArr = self.gib['history']['model'].split()
                            mark = mdArr[0]
                            model = mdArr[1]
                            mrk.string = mdArr[0]
                            mdl.string = mdArr[1]
                            md = self.mid_Car(mark, model)
                        else:
                            mrk.string = self.gib['history']['model']
                            mdl.string = ' '
                        if md['seal'] == 'no__data':
                            print('no mid')
                        else:
                            sel.string = md['seal']
                    else:
                        sel.string = md['seal']
            else:
                mdArr = self.gib['history']['model'].split()
                if len(mdArr) > 2:
                    mark = mdArr[0]
                    model = mdArr[1] + '_' + mdArr[2]
                    mrk.string = mark
                    mdl.string = model
                    md = self.mid_Car(mark, model)
                    if md['seal'] == 'no__data':
                        print('no mid')
                    else:
                        sel.string = md['seal']
                else:
                    if len(mdArr) > 2:
                        mark = mdArr[0]
                        model = mdArr[1]
                        mrk.string = mark
                        mdl.string = model
                        md = self.mid_Car(mark, model)
                        if md['seal'] == 'no__data':
                            print('no mid')
                        else:
                            sel.string = md['seal']


        else:
            self.soup.find('div' , {"class": "mid__info"}).decompose()
            #self.soup.find('div', {"class": "mid__mile"}).decompose()
            self.soup.findAll('div', {"class": "none"})[2]['style'] = 'display: block'


        if self.eas.get('mileages'):
            if self.eas['mileages'] != "None":
                col = self.soup.find('div', {"class": "mid__mile-column"})
                if len(self.eas['mileages']) == 1:
                    self.soup.find('div', {"class": "mid__mile-graph"}).decompose()
                for prop in reversed(self.eas['mileages']):
                    div = self.soup.new_tag('div', **{'class': 'fnd'})
                    p = self.soup.new_tag('p')
                    span = self.soup.new_tag('span', **{'class': 'mid__mile-km'})
                    span2 = self.soup.new_tag('span', **{'class': 'mid__mile-date'})
                    span.string = str(prop['mileage']) + ' КМ по состоянию на '
                    span2.string = str( prop['date'] )
                    p.append(span)
                    p.append(span2)
                    div.append(p)
                    col.append(div)
                    self.mls = str(prop['mileage'])
                    self.mlsDt = prop['date']
            elif self.gib['history'] != None:
                if self.mile_generation['mile'] != []:
                    col = self.soup.find('div', {"class": "mid__mile-column"})
                    if len(self.mile_generation['mile']) == 1:
                        self.soup.find('div', {"class": "mid__mile-graph"}).decompose()
                    for prop in self.mile_generation['mile']:
                        div = self.soup.new_tag('div', **{'class': 'fnd'})
                        p = self.soup.new_tag('p')
                        span = self.soup.new_tag('span', **{'class': 'mid__mile-km'})
                        span2 = self.soup.new_tag('span', **{'class': 'mid__mile-date'})
                        span.string = str(prop['mileage']) + ' КМ по состоянию на '
                        span2.string = str( prop['date'] )
                        p.append(span)
                        p.append(span2)
                        div.append(p)
                        col.append(div)
                        self.mls = str(prop['mileage'])
                        self.mlsDt = str( prop['date'] )
                else:
                    self.soup.find('div', {"class": "mid__mile"}).decompose()
                    self.soup.findAll('div', {"class": "none"})[3]['style'] = 'display: block'
            else:
                self.soup.find('div', {"class": "mid__mile"}).decompose()
                self.soup.findAll('div', {"class": "none"})[3]['style'] = 'display: block'
        elif self.gib['history'] != None:
            if self.mile_generation['mile'] != []:
                col = self.soup.find('div', {"class": "mid__mile-column"})
                if len(self.mile_generation['mile']) == 1:
                    self.soup.find('div', {"class": "mid__mile-graph"}).decompose()
                for prop in self.mile_generation['mile']:
                    div = self.soup.new_tag('div', **{'class': 'fnd'})
                    p = self.soup.new_tag('p')
                    span = self.soup.new_tag('span', **{'class': 'mid__mile-km'})
                    span2 = self.soup.new_tag('span', **{'class': 'mid__mile-date'})
                    span.string = str(prop['mileage']) + ' КМ по состоянию на '
                    span2.string = str( prop['date'] )
                    p.append(span)
                    p.append(span2)
                    div.append(p)
                    col.append(div)
                    self.mls = str(prop['mileage'])
                    self.mlsDt = str ( prop['date'] )
            else:
                print('alo')
                self.soup.find('div', {"class": "mid__mile"}).decompose()
                self.soup.findAll('div', {"class": "none"})[3]['style'] = 'display: block'

        else:
            self.soup.find('div', {"class": "mid__mile"})['style'] = 'display: none'
            self.soup.findAll('div', {"class": "none"})[3]['style'] = 'display: block'


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
        eyr.string = 'не определенно'
        md = self.mid_Car_japan(mark, model)
        sel.string = md['seal']

        col = self.soup.find('div', {"class": "mid__mile-column"})
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
        if self.rsa.get('policies') and self.gib['history'] != None:
            index = len(self.rsa['policies']) - 1
            gos = self.soup.find('span', {"class": "owner2__info-reg"})
            self.soup.find('span', {"class": "owner2__info-car"}).string = str( self.gib['history']['model'] )
            self.soup.find('span', {"class": "owner2__info-date"}).string = str( self.gib['history']['year'] )
            self.soup.find('span', {"class": "owner2__info-own"}).string = str(self.rsa['policies'][index]['ownerName'])
            self.soup.find('span', {"class": "owner2__info-owndate"}).string = str(self.rsa['policies'][index]['ownerDob'])

            if self.rsa['policies'][0].get('regNumber'):
                gos.string = self.rsa['policies'][index]['regNumber']
            elif self.eas.get('diagnose_cards'):
                gos.string = str( self.eas['diagnose_cards'][0]['regNumber'])
        elif self.rsa.get('policies'):
            if self.rsa['policies'][0].get('model') and self.rsa['policies'][0].get('mark'):
                index = len(self.rsa['policies']) - 1
                gos = self.soup.find('span', {"class": "owner2__info-reg"})
                self.soup.find('span', {"class": "owner2__info-car"}).string = self.rsa['policies'][0]['mark'] + ' ' + self.rsa['policies'][0]['model']
                self.soup.find('span', {"class": "owner2__info-date"}).string = str( 'Информация не найдена')
                self.soup.find('span', {"class": "owner2__info-own"}).string = str( self.rsa['policies'][index]['ownerName'] )
                self.soup.find('span', {"class": "owner2__info-owndate"}).string = str( self.rsa['policies'][index]['ownerDob'] )

                if self.rsa['policies'][0].get('regNumber'):
                    gos.string = self.rsa['policies'][index]['regNumber']
                elif self.eas.get('diagnose_cards'):
                    if self.eas['diagnose_cards'][0].get('regNumber'):
                        gos.string = self.eas['diagnose_cards'][0]['regNumber']
                    else:
                        gos.string = 'Информация не найдена'
        elif self.rsa.get('policies'):
            index = len(self.rsa['policies']) - 1
            gos = self.soup.find('span', {"class": "owner2__info-reg"})
            self.soup.find('span', {"class": "owner2__info-car"}).string = 'Информация не найдена'
            self.soup.find('span', {"class": "owner2__info-date"}).string = 'Информация не найдена'
            self.soup.find('span', {"class": "owner2__info-own"}).string = str( self.rsa['policies'][index]['ownerName'] )
            self.soup.find('span', {"class": "owner2__info-owndate"}).string = str( self.rsa['policies'][index]['ownerDob'] )

            if self.rsa['policies'][0].get('regNumber'):
                gos.string = self.rsa['policies'][index]['regNumber']
            elif self.eas.get('diagnose_cards'):
                gos.string = self.eas['diagnose_cards'][0]['regNumber']
            else:
                gos.string = 'Информация не найдена'

        else:
            self.soup.find('div', {"class": "owner2__info"})['style'] = 'display: none'
            self.soup.findAll('div', {"class": "none"})[4]['style'] = 'display: block'


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
                span.string = str( prop['model'] )
                span1.string = str( prop['accidentNumber'] )
                span2.string = str( prop['accidentType'] )
                span3.string = str( prop['regionName'] )
                span4.string = str( prop['accidentDatetime'] )
                span5.string = str( prop['vehicleAmount'] )
                span6.string = str( prop['vehicleSort'] )
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
                if prop.get('damageSvg'):
                    if prop['damageSvg'] != 'None':
                        print('dtp detected')
                        svg = BeautifulSoup(self.get_Svg(prop['damageSvg']), 'html.parser')
                        header = self.soup.new_tag('head')
                        body = self.soup.new_tag('body')
                        header.append(svg.find('style'))
                        body.append(svg.find('div', {"class": "dmgMap"}))
                        div.append(header)
                        div.append(body)
                col.append(div)
        if len(self.gib['accidents']) == 0:
            div = self.soup.new_tag("div", **{'class': 'dtp__row'})
            p = self.soup.new_tag("p")
            span = self.soup.new_tag('span')
            span.string = '✅ Автомобиль в ДТП не участвовал!'
            p.append(span)
            div.append(p)
            col.append(div)
            self.soup.findAll('div', {"class": "none"})[5]['style'] = 'display: block'


    def dtp_japan(self):
        col = self.soup.find('div', {"class": "dtp"})
        col.decompose()
        print(col)

    def easit(self):
        reg = self.soup.find('span', {"class": "eas__row-reg"})
        mil = self.soup.find('span', {"class": "eas__row-pr"})
        bod = self.soup.find('span', {"class": "eas__row-bd"})
        dk = self.soup.find('span', {"class": "eas__row-dk"})
        yer = self.soup.find('span', {"class": "eas__row-date"})
        if self.eas.get('diagnose_cards'):
            if self.eas['diagnose_cards'][0].get('regNumber'):
                reg.string = self.eas['diagnose_cards'][0]['regNumber']
            elif self.rsa.get('policies'):
                if self.rsa['policies'][0].get('regNumber'):
                    reg.string = self.rsa['policies'][0]['regNumber']
                else:
                    reg.string = 'Информация не найдена'
            if self.eas['diagnose_cards'][0].get('mileage'):
                mil.string = str(self.eas['diagnose_cards'][0]['mileage'])
            bod.string = self.eas['diagnose_cards'][0]['vin']
            dk.string = str(self.eas['diagnose_cards'][0]['number'])
            yer.string = 'С ' + str(self.eas['diagnose_cards'][0]['startDate']) + ' по ' + str(self.eas['diagnose_cards'][0]['endDate'])

        elif self.gib['history'] != None:
            if self.rsa.get('policies'):
                if self.rsa['policies'][0].get('regNumber'):
                    reg.string = self.rsa['policies'][0]['regNumber']
                else:
                    reg.string = 'Нет данных'
            mil.string = str(self.mls)
            bod.string = self.vin
            dk.string = str(random.randint(201610101449162544600, 201610101449162544920))
            now = datetime.datetime.now()
            yer.string = str(self.mlsDt) + ' По ' + now.strftime("%d-%m-%Y")
        else:
            self.soup.find('div', {"class": "eas__row"})['style'] = 'display: none'
            self.soup.findAll('div', {"class": "none"})[6]['style'] = 'display: block'


    def rsas(self):

        if self.rsa.get('policies'):
            cmp = self.soup.find('span', {"class": "rsa__cmp"})
            vn = self.soup.find('span', {"class": "rsa__vin"})
            ow = self.soup.find('span', {"class": "rsa__prs"})
            dat = self.soup.find('span', {"class": "rsa__date"})
            loc = self.soup.find('span', {"class": "rsa__loc"})
            cost = self.soup.find('span', {"class": "rsa__cst"})

            cmp.string = str( self.rsa['policies'][0]['companyName'] )
            vn.string = str(self.rsa['policies'][0]['vin'])
            ow.string = str( self.rsa['policies'][0]['ownerName'])
            dat.string = str( self.rsa['policies'][0]['ownerDob'])
            loc.string = str( self.rsa['policies'][0]['location'] )
            cost.string = str( self.rsa['policies'][0]['cost'] )
        else:
            self.soup.find('div', {"class":"rsa__row"})['style'] = 'display: none'
            self.soup.findAll('div', {"class": "none"})[7]['style'] = 'display: block'


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
            div.append(p)
            self.soup.findAll('div', {"class": "none"})[8]['style'] = 'display: block'

            col.append(div)

    def wntd_japan(self):
        col = self.soup.find('div', {"class": "wantd"})
        col.decompose()

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
            div.append(p)
            col.append(div)
            self.soup.findAll('div', {"class": "none"})[9]['style'] = 'display: block'


    def ogr_japan(self):
        col = self.soup.find('div', {"class": "ogrs"})
        col.decompose()

    def zlgs(self):
        col = self.soup.find('div', {"class": "zlg__column"})
        if self.zal.get('records'):
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

                if prop.get('objects'):
                    for prop3 in prop['objects']:
                        div4 = self.soup.new_tag("div", **{"class": "zlg__row-vin"})
                        p = self.soup.new_tag("p")

                        span.string = prop3

                        p.append(span)
                        div4.append(p)
                        div.append(div4)

                if prop.get('pledgors'):
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
                if prop.get('history'):
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
            p = self.soup.new_tag('p')
            p.string = '✅ По указанному VIN не не найденаинформация об ограничениях.'
            div.append(p)
            self.soup.findAll('div', {"class": "none"})[10]['style'] = 'display: block'
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
            p = self.soup.new_tag('p')
            p.string = '🚕 Информация о наличии разрешения на осуществление деятельности по перевозке пассажиров не найдена.'
            div.append(p)
            self.soup.findAll('div', {"class": "none"})[11]['style'] = 'display: block'

            col.append(div)

    def getHtml(self):
            name = uuid.uuid4().hex
            name2 = "venv/example/nomer2/" + name + ".html"
            with open(name2, "w", encoding='utf-8') as fl:
                fl.write(str(self.soup))
            print(name2)
            return [name2 , name]

    def carPhoto(self):

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

    def carPhotoEas(self):
        # у 804 км 799
        #self.rsa['policies'][0]['regNumber']
        response = requests.get('http://bsl-show.online/bot-data/reg.php?reg=' + self.eas['diagnose_cards'][0]['regNumber'])
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
        response = requests.get('http://bsl-show.online/bot-data/vinDec.php?vin=' + self.gib['history']['vin'])
        vin = response.json()
        return vin

    def date_Car(self):
        response = requests.get('http://bsl-show.online/bot-data/date.php?date=' + self.gib['history']['ownershipPeriods'][0]['from'])
        vin = response.json()
        return vin


    def mid_Car(self, mrk, model):
        site = 'http://bsl-show.online/bot-data/mid.php?mrk=' + mrk + '&mdl=' + model + '&yer=' + self.gib['history']['year']
        response = requests.get(site.replace(' ', ''))
        return response.json()

    def mid_Car_reserve(self, mrk, model):

        site = 'http://bsl-show.online/bot-data/mid.php?mrk=' + mrk + '&mdl=' + model + '&yer=' + self.gib['history']['year']
        response = requests.get(site.replace(' ', ''))
        return response.json()

    def mid_Car_japan(self, mrk, model):

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
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('37.140.192.137', username='u1145099', password='Z!Hq2ukD')
    sftp = ssh.open_sftp()
    lnk = "www/bsl-show.online/push/number/" + name[1] + '.html'
    sftp.put(name[0], lnk)
    path = os.path.join(os.path.abspath(os.path.dirname(name[0])), name[1] + '.html')
    os.remove(path)
    print('Base information returned')
    #print(name)
    return 'https://bsl-show.online/push/number/' + name[1] + '.html'


# res = doc(getData.data(), 'evan_battle_in', '', 'JTMHV05J105022534')
# link = put(res.getHtml())
# print(link)
#

