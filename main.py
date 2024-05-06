from bs4 import BeautifulSoup
import requests
import wget 
import os
from fake_useragent import UserAgent
base_url = "https://readm.today/"
pop_url = "https://readm.today/popular-manga"
ua = UserAgent()
r = requests.get(pop_url)
soup = BeautifulSoup(r.content, features ='html.parser')
poster_div = soup.find_all('div',class_='poster-with-subject')
data_ob = dict()
for manga in poster_div:
    data = {
        "title":manga.find("h2").text,
        "poster": base_url + manga.find("img")['src'],
        "description": manga.find('p',class_='desktop-only excerpt').text,
        "url":base_url+manga.find('a')["href"],
    }

    if data["title"].lower() == "one piece":
        ch=input("enter choice: ")
        f = os.makedirs(data['title']+f"/ch-{ch}")
        r = requests.get(data['url']+f"/{ch}/all-pages")
        print(data['url']+f"/{ch}/all-pages")
        soup = BeautifulSoup(r.content,features='html.parser')
        print('yes')
        url = soup.find_all('img')

        for u in url:
            print(u['src'])
            wget.download(base_url+u['src'],data['title']+f"/ch-{ch}", header=ua.random)



