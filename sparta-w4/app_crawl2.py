from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta


articles = []

common_url = 'https://www.youtube.com/feed/trending?gl='


## HTML을 주는 부분
@app.route('/')
def home():
   return 'This is Home!'

@app.route('/myyoutube2')
def mypage():
   return render_template('index_crawl3.html')


## API 역할을 하는 부분
@app.route('/post', methods=['POST'])
def post():
   global articles

   url_receive = common_url + request.form['c_type']  # 클라이언트로부터 url을 받는 부분


   response = requests.get(url_receive)

   soup = BeautifulSoup(response.text, 'lxml')
   lis = soup.find_all('li', {'class': 'expanded-shelf-content-item-wrapper'})


   articles = []
   for rank, li in enumerate(lis, 1):
      # exception
      title = li.find('a', {'title': True})['title']
      video_link = 'https://www.youtube.com' + li.find('a', {'href': True})['href']
      img_info = li.find('img', {'data-thumb': True})
      hits = li.find_all('li')[3].text

      if img_info != None:
         img_link = img_info['data-thumb']
      else:
         img_link = li.find('img', {'src': True})['src']

      article = {'url': url_receive, 'rank':rank, 'video_link':video_link, 'img_link' :img_link, 'title':title,'hits':hits  }  # 받은 걸 딕셔너리로 만들고,
      articles.append(article)


   print(articles)

   return jsonify({'result': 'success'})

@app.route('/post', methods=['GET'])
def view():

   return jsonify({'result':'success', 'articles':list(articles)})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000)