from bs4 import BeautifulSoup
import uuid
import datetime
import putFile
import requests
import time


class docN():
    def __init__(self, number, tg_name):

        print('asfasfasfasfafasfasfasfasf')
        self.number = number
        self.name = tg_name
        docs = docN.docc()
        self.soup = BeautifulSoup(docs, 'html.parser')
        self.alls = self.all()
        self.ar = self.arch()
        self.nw = self.neww()

        print('asfasfasfas')

        self.head()
        self.autoFull()
        self.autoNew()

        self.avit()
        self.ul()
        self.dr()
        #print(self.number)
    def docc():
        with open("venv/example/number/index.html", "r", encoding='utf-8') as f:
            datas = f.read()
            f.close()
            return datas

    def head(self):
        nmb = self.soup.find("span", {"class": "header__logo-sp"})
        name = self.soup.find("span", {"class": "header__name"})
        dat = self.soup.find("span", {"class": "header__date"})
        now = datetime.datetime.now()
        dat.string = str(now.strftime("%d-%m-%Y %H:%M"))
        nmb.string = str(self.number)
        name.string = self.name

    def autoFull(self):
        print('asfasf')
        col = self.soup.find("div", {"class": "av__column"})
        pub = self.alls

        print(pub)

        if len(pub['data']) > 0:
            for prop in pub['data']:
                if prop['category'] == 'Автомобили' or prop['category'] == 'Транспорт, Автомобили' or prop['category'] == 'Автомобили с пробегом' or prop['category'] == '23, 2301':
                    div = self.soup.new_tag("div", **{"class": "av__row"})
                    div2 = self.soup.new_tag("div", **{"class": "av__hide hide-s1 hide-op"})
                    imgC = self.soup.new_tag('img', src='document.svg', width='20', height="20", style="cursor: pointer;", **{"class": "show"})
                    p = self.soup.new_tag("p")
                    p2 = self.soup.new_tag("p")
                    p3 = self.soup.new_tag("p")
                    p4 = self.soup.new_tag("p")
                    p5 = self.soup.new_tag("p")
                    p6 = self.soup.new_tag("p")
                    pB = self.soup.new_tag("p")

                    a = self.soup.new_tag("a" , href=prop['url'])
                    a.string = ' Ссылка '
                    p.string = prop['time']
                    if prop['source'] == 'avito.ru':
                        img = self.soup.new_tag('img', src='favAvito.png')
                    elif prop['source'] == 'youla.io':
                        img = self.soup.new_tag('img', src='favYoula.png')
                    elif prop['source'] == 'auto.ru':
                        img = self.soup.new_tag('img', src='favAutoru.png')
                    elif prop['source'] == 'irr.ru':
                        img = self.soup.new_tag('img', src='HcdtRT97_400x400.jpg' ,  width='20', height="20")
                    p2.string = prop['title']
                    p3.string = prop['location']
                    p4.string = prop['category']
                    p5.string = prop['name']
                    p6.string = " ; " + str(prop['phone'])

                    pB.string = prop['description']
                    div2.append(pB)

                    div.append(p)
                    #div.append(img)
                    div.append(a)
                    div.append(p2)
                    div.append(p3)
                    div.append(p4)
                    div.append(p5)
                    div.append(p6)
                    div.append(imgC)
                    div.append(div2)
                    col.append(div)
        else:
            col = self.soup.find("div", {"class": "av__column"})
            div = self.soup.new_tag("div", **{"class": "av__row"})
            p = self.soup.new_tag("p")
            p.string = "Обявлений не найдено"
            div.append(p)
            col.append(div)
            print(col)
            print('asfasf')


    def autoNew(self):
        col = self.soup.find("div", {"class": "av__column"})
        pub = self.nw
        for prop in pub:
                div = self.soup.new_tag("div", **{"class": "av__row"})

                p = self.soup.new_tag("p")
                p2 = self.soup.new_tag("p")


                a = self.soup.new_tag("a" , href=prop['link'])
                a.string = ' Ссылка '

                p.string = prop['title']
                p2.string = "Автомобили с пробегом"

                img = self.soup.new_tag('img', src='gen340_139017.jpg' ,  width='20', height="20")

                div.append(p)
                div.append(img)
                div.append(a)
                div.append(p2)
                col.append(div)
        #print(col)

    def avit(self):
        col = self.soup.find("div", {"class": "avito__column"})
        pub = self.alls

        if len(pub['data']) > 0:
            for prop in pub['data']:
                if prop['source'] == 'avito.ru':
                        div = self.soup.new_tag("div", **{"class": "avito__row"})
                        div2 = self.soup.new_tag("div", **{"class": "av__hide hide-s1 hide-op"})
                        imgC = self.soup.new_tag('img', src='document.svg', width='20', height="20", style="cursor: pointer;", **{"class": "show"})
                        p = self.soup.new_tag("p")
                        p2 = self.soup.new_tag("p")
                        p3 = self.soup.new_tag("p")
                        p4 = self.soup.new_tag("p")
                        p5 = self.soup.new_tag("p")
                        p6 = self.soup.new_tag("p")
                        pB = self.soup.new_tag("p")

                        a = self.soup.new_tag("a" , href=prop['url'])
                        a.string = ' Ссылка '
                        p.string = prop['time']
                        img = self.soup.new_tag('img', src='favAvito.png')

                        p2.string = prop['title']
                        p3.string = prop['location']
                        p4.string = prop['category']
                        p5.string = prop['name']
                        p6.string = "; " + str(prop['phone'])

                        pB.string = prop['description']
                        div2.append(pB)

                        div.append(p)
                        div.append(img)
                        div.append(a)
                        div.append(p2)
                        div.append(p3)
                        div.append(p4)
                        div.append(p5)
                        div.append(p6)
                        div.append(imgC)
                        div.append(div2)
                        col.append(div)
        else:
            div = self.soup.new_tag("div", **{"class": "avito__row"})
            p = self.soup.new_tag("p")
            p.string = "Обявлений не найдено"
            div.append(p)
            col.append(div)

    def ul(self):
        col = self.soup.find("div", {"class": "ul__column"})
        pub = self.alls
        if len(pub['data']) > 0:
            for prop in pub['data']:
                if prop['source'] == 'youla.io':
                    div = self.soup.new_tag("div", **{"class": "ul__row"})
                    div2 = self.soup.new_tag("div", **{"class": "av__hide hide-s1 hide-op"})
                    imgC = self.soup.new_tag('img', src='document.svg', width='20', height="20", style="cursor: pointer;",
                                             **{"class": "show"})
                    p = self.soup.new_tag("p")
                    p2 = self.soup.new_tag("p")
                    p3 = self.soup.new_tag("p")
                    p4 = self.soup.new_tag("p")
                    p5 = self.soup.new_tag("p")
                    p6 = self.soup.new_tag("p")
                    pB = self.soup.new_tag("p")

                    a = self.soup.new_tag("a", href=prop['url'])
                    a.string = ' Ссылка '
                    p.string = prop['time']
                    img = self.soup.new_tag('img', src='favYoula.png')

                    p2.string = prop['title']
                    p3.string = prop['location']
                    p4.string = prop['category']
                    p5.string = prop['name']
                    p6.string = "; " + str(prop['phone'])

                    pB.string = prop['description']
                    div2.append(pB)

                    div.append(p)
                    div.append(img)
                    div.append(a)
                    div.append(p2)
                    div.append(p3)
                    div.append(p4)
                    div.append(p5)
                    div.append(p6)
                    div.append(imgC)
                    div.append(div2)
                    col.append(div)
            # print(col)
        else:
            print('no')
            col = self.soup.find("div", {"class": "ul__column"})
            div = self.soup.new_tag("div", **{"class": "ul__row"})
            p = self.soup.new_tag("p")
            p.string = "Обявлений не найдено"
            div.append(p)
            col.append(div)

    def dr(self):
        col = self.soup.find("div", {"class": "drom__column"})
        pub = self.nw

        for prop in pub:
            div = self.soup.new_tag("div", **{"class": "drom__row"})

            p = self.soup.new_tag("p")
            p2 = self.soup.new_tag("p")

            a = self.soup.new_tag("a", href=prop['link'])
            a.string = ' Ссылка '

            p.string = prop['title']
            p2.string = "Автомобили с пробегом"

            img = self.soup.new_tag('img', src='gen340_139017.jpg', width='20', height="20")

            div.append(p)
            div.append(img)
            div.append(a)
            div.append(p2)
            col.append(div)

            col = self.soup.find("div", {"class": "drom__column"})

        pub2 = self.ar
        for prop in pub2:

                div = self.soup.new_tag("div", **{"class": "drom__row"})

                p = self.soup.new_tag("p")
                p2 = self.soup.new_tag("p")

                a = self.soup.new_tag("a", href=prop['link'])
                a.string = ' Ссылка '

                p.string = prop['title']
                p2.string = "Автомобили с пробегом"

                img = self.soup.new_tag('img', src='gen340_139017.jpg', width='20', height="20")

                div.append(p)
                div.append(img)
                div.append(a)
                div.append(p2)
                col.append(div)


    def arch(self):
        response = requests.get('http://bsl-show.online/bot-data/phnData.php?number=' + str(self.number))
        print(response.text)
        vin = response.json()
        return vin

    def all(self):
        response = requests.get('https://i-find.pro/api/create?login=smilegoldsgames3@gmail.com&token=613b9f648e9c9846884e14253bb7c8bf&phone=' + str(self.number) + '&source=2')
        all = response.json()
        id = all['id']
        time.sleep(3)
        response2 = requests.get('https://i-find.pro/api/result?login=smilegoldsgames3@gmail.com&token=613b9f648e9c9846884e14253bb7c8bf&id=' + str(id) + '&format=json' )
        dat = response2.json()
        return dat

    def neww(self):
        response = requests.get('http://bsl-show.online/bot-data/newPh.php?number=' + str(self.number))
        vin = response.json()
        return vin

    def getHtml(self):
        name = uuid.uuid4().hex
        name2 = "venv/example/number/" + name + ".html"
        with open(name2, "w", encoding='utf-8') as fl:
            fl.write(str(self.soup))
        print(name2)
        return [name2, name]


#res = docN('79199371764' , 'master')

#print( putFile.put(res.getHtml()))


