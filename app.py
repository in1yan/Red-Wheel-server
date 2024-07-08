from bs4 import BeautifulSoup
import json
import requests
from flask import Flask,request,jsonify


app = Flask(__name__)




base_url = "https://readm.today"
pop_url = "https://readm.today/popular-manga"
# ua = UserAgent()
urls = []


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
    with open('pop.json','r') as f:
        data = json.load(f)

    return jsonify(data['data'])
@app.route('/anime-reads',methods=["GET"])
def anime_reads():
    with open('ani-reads.json','r') as f:
        data = json.load(f)
        return jsonify(data)
@app.route('/new-manga',methods=["GET"])
def new_manga():
    with open('new-manga.json','r') as f:
        data = json.load(f)
        return jsonify(data)
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
