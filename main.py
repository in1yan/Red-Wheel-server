from bs4 import BeautifulSoup
import requests
from flask import Flask,request,jsonify
from flask_caching import Cache


app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE':'simple','CACHE_DEFAULT_TIMEOUT':3600})




base_url = "https://readm.today"
pop_url = "https://readm.today/popular-manga"
# ua = UserAgent()
urls = []
@cache.cached(timeout=3600)
def popm():
    pop = []
    r = requests.get(pop_url)
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

@app.route('/pages/',methods=['GET'])
def pages():
    if request.method == 'GET':
        # data=request.json
        # print(data)
        pages = []
        url=request.args.get('url')
        print(url)
        ch=request.args.get('ch')
        r=requests.get(f'{url}/{ch}/all-pages')
        soup = BeautifulSoup(r.content, features='html.parser')
        imgs = soup.find_all('img')
        for img in imgs:
            s =base_url+img['src'].split('?')[0]
            pages.append({'url':s})
            print(s)
        return jsonify(pages[2:])
@app.route('/popular',methods=['GET'])
def popular():
    data = popm()
    return data
app.run(host='0.0.0.0', debug=True)
# chapter('https://readm.today/manga/soIo-IeveIing-220424')