import json
import requests
from flask import Flask,request,jsonify
import get_manga as gm


app = Flask(__name__)




base_url = "https://readm.today"
pop_url = "https://readm.today/popular-manga"
# ua = UserAgent()
urls = []


@app.route('/pages/',methods=['GET'])
def pages():
    if request.method == 'GET':
        url = request.args.get('url')
        ch = request.args.get('ch')
        pages = gm.get_pages(url,ch)
        return jsonify(pages)
@app.route('/popular',methods=['GET'])
def popular():
    with open('pop.json','r') as f:
        data = json.load(f)

    return jsonify(data['data'])
@app.route('/anime-reads',methods=["GET"])
def anime_reads():
    with open('ani-reads.json','r') as f:
        data = json.load(f)
        return jsonify(data['data'])
@app.route('/new-manga',methods=["GET"])
def new_manga():
    with open('new-manga.json','r') as f:
        data = json.load(f)
        return jsonify(data['data'])
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
