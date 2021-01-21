from bs4 import BeautifulSoup
import paramiko
import requests
import uuid
import os


def rename(link, name):
    response = requests.get(link)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find('span', {"class": "header__name"}).string = str(name)
    html = getHtml(soup)
    return put(html)

def getHtml(soup):
        name = uuid.uuid4().hex
        name2 = "venv/example/nomer2/" + name + ".html"
        with open(name2, "w", encoding='utf-8') as fl:
            fl.write(str(soup))
        print(name2)
        return [name2, name]

def put(name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('37.140.192.137', username='u1145099', password='Z!Hq2ukD')
    sftp = ssh.open_sftp()
    lnk = "www/bsl-show.online/push/number/" + name[1] + '.html'
    sftp.put(name[0], lnk)
    # path = os.path.join(os.path.abspath(os.path.dirname(name[0])), name[1] + '.html')
    # os.remove(path)
    print('Base information returned')
    return 'https://bsl-show.online/push/number/' + name[1] + '.html'


