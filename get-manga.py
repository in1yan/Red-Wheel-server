import requests
from bs4 import BeautifulSoup
import json
import sys

base_url = "https://readm.today"
pop_url = "https://readm.today/popular-manga"
new_url = "https://readm.today/new-manga"
def popm(url):
    pop = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features ='html.parser')
    poster_div = soup.find_all('div',class_='poster-with-subject')
    for manga in poster_div:
        url = base_url+manga.find('a')["href"]
        desc=str(manga.find('p',class_='desktop-only excerpt').text).strip()
        if desc=='':
            desc="Not avilable"
        data = {
            "title":manga.find("h2").text,
            "poster": base_url + manga.find("img")['src'],
            "desc": desc,
            "url":url,
            "chapters":chapter(url)
        }
        print(data)
        pop.append(data)
    return pop

def getm(url):
    manga_data = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features ='html.parser')
    td = soup.find_all('td')[1]
    ch=td.find_all('div')[1]
    title=soup.find('h1').text
    poster_div = soup.find('div',class_='item')
    desc=str(poster_div.find('p').text)
    if desc=='':
        desc="Not avilable"
    data = {
        "title":title,
        "poster": base_url + poster_div.find("img")['src'],
        "desc": desc,
        "url":url,
        "chapters":ch.text
    }
    return data
def getnew(url):
    urls=[]
    new_mangas=[]
    r = requests.get(url)
    soup = BeautifulSoup(r.content,features='html.parser')
    lis = soup.find_all('div',class_='poster-subject')
    print(lis)
    for li in lis:
        urls.append( base_url + li.find('a')["href"] )
    for murl in urls:
        print(murl)
        data = getm(murl)
        print(data)
        new_mangas.append(data)
    return new_mangas
def chapter(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='html.parser')
    td = soup.find_all('td')[1]
    ch=td.find_all('div')[1]
    return ch.text
if __name__ == '__main__':
    if len(sys.argv) == 1:
        data = popm(pop_url) + popm(pop_url+'/2') + popm(pop_url+'/3') + popm(pop_url+'/4')
        data_d = {
        "data":data
        }
        with open('pop.json','w') as f:
            json.dump(data_d,f)
        print('done..')
    elif sys.argv[1] =="--add":
        print(sys.argv[2])
        data = getm(sys.argv[2])
        data_d ={"data":[]}
        try:
            with open('ani-reads.json','r') as f:
                data_d = json.load(f)
                data_array = data_d["data"]
        except (json.JSONDecodeError,FileNotFoundError):
            data_array = []
        data_array.append(data)
        data_d["data"]=data_array
        with open('ani-reads.json','w') as f:
            json.dump(data_d,f)
        print("added...")
    elif sys.argv[1] == "--new":
        data = getnew(new_url)
        data_d = {"data":data}
        with open("new-manga.json",'w') as f:
            json.dump(data_d,f)
        print("done..")

