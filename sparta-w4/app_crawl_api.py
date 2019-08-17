from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return 'This is Home!'

@app.route('/myyoutube')
def mypage():
   return render_template('index_crawl.html')


## API 역할을 하는 부분
# @app.route('/post', methods=['POST'])
# def post():
#    url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분
#    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분
# 
#    headers = {
#       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#    data = requests.get(url_receive, headers=headers)
# 
#    soup = BeautifulSoup(data.text, 'html.parser')
# 
#    og_image = soup.select_one('meta[property="og:image"]')
#    og_title = soup.select_one('meta[property="og:title"]')
#    og_description = soup.select_one('meta[property="og:description"]')
# 
#    url_image = og_image['content']
#    url_title = og_title['content']
#    url_description = og_description['content']
# 
#    video = {'url': url_receive, 'comment': comment_receive, 'image': url_image, 'title': url_title, 'desc': url_description}
# 
#    db.videos.insert_one(video)
# 
#    return jsonify({'result': 'success'})

@app.route('/post', methods=['POST'])
def post():
   
   video_receive = request.form['url_video']  # 클라이언트로부터 url을 받는 부분
   response = requests.get(target_url)

   headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
   data = requests.get(url_receive, headers=headers)
   soup = BeautifulSoup(response.text, "lxml")
   lis = soup.find_all('li', {'class': 'expanded-shelf-content-item-wrapper'})

   title = li.find('a', {'title': True})['title']
   link = 'https://www.youtube.com' + li.find('a', {'href': True})['href']
   img_info = li.find('img', {'data-thumb': True})
   hits = li.find_all('li')[3].text

   if img_info != None:
      img_link = img_info['data-thumb']
   else:
      img_link = li.find('img', {'src': True})['src']
   
   video_image = image_info['content']
   video_title = title['content']
   video_hits = hits['content']

   video = {'video': video_receive, 'image': video_image, 'title': video_title,'hits': video_hits }

   print(video)

   db.videos.insert_one(video)

   return jsonify({'result': 'success'})





@app.route('/post', methods=['GET'])
def view():
   posts = db.videos.find({},{'_id':0})
   return jsonify({'result':'success', 'videos':list(posts)})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000)