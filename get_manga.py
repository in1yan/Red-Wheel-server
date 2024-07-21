import requests
from bs4 import BeautifulSoup
import json
import sys

base_url = "https://readm.today"
pop_url = "https://kissmanga.in/mangalist/?m_orderby=trending"
new_url = "https://kissmanga.in/mangalist/?m_orderby=new-manga"
def popm(url):
    pop_mangas=[]
    r = requests.get(url)
    soup = BeautifulSoup(r.content,features='html.parser')
    lis = soup.find('div',class_='main-col-inner')
    mangas = lis.find_all('div', class_='item-summary')
    for manga in mangas:
        pop_mangas.append( getm(manga.find('h3').find('a')['href']) ) 
    return new_mangas

def getm(url):
    manga_data = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features ='html.parser')
    title = soup.find('div',class_='post-title').find('h1').text
    poster = soup.find('div',class_='summary_image').find('img')['src']
    description = soup.find('div',class_="description-summary").find('p').text
    chapters = soup.find_all('ul')[5].find('li').find('a').text.split(' ')[1]
    data = {
        "title":title,
        "poster":poster, 
        "desc": description,
        "url":url,
        "chapters": chapters
    }
    print(data)
    return data
def getnew(url):
    new_mangas=[]
    r = requests.get(url)
    soup = BeautifulSoup(r.content,features='html.parser')
    lis = soup.find('div',class_='main-col-inner')
    mangas = lis.find_all('div', class_='item-summary')
    for manga in mangas:
        new_mangas.append( getm(manga.find('h3').find('a')['href']) ) 
    return new_mangas
def get_pages(url,ch):
    pages = []
    r=requests.get(f'{url}/chapter-{ch}')
    soup = BeautifulSoup(r.content,features='html.parser')
    imgs = soup.find('div',class_='read-container').find_all('img')
    for img in imgs:
        pages.append(img['src'].strip())        
    return pages
if __name__ == '__main__':
    if len(sys.argv) == 1:
        data = popm(pop_url) + popm('https://kissmanga.in/mangalist/page/2/?m_orderby=trending')
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
        data = getnew(new_url) + getnew("https://kissmanga.in/mangalist/page/2/?m_orderby=new-manga")
        data_d = {"data":data}
        with open("new-manga.json",'w') as f:
            json.dump(data_d,f)
        print("done..")


