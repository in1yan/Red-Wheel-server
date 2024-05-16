import requests
from bs4 import BeautifulSoup
import json

base_url = "https://readm.today"
pop_url = "https://readm.today/popular-manga"

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
        pop.append(data)
    return pop

def chapter(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='html.parser')
    td = soup.find_all('td')[1]
    ch=td.find_all('div')[1]
    return ch.text
if __name__ == '__main__':
    data = popm(pop_url) + popm(pop_url+'/2')
    data_d = {
    "data":data
    }
    with open('pop.json','w') as f:
        json.dump(data_d,f)
    print('done..')