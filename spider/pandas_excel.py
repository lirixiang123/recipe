import requests
from bs4 import BeautifulSoup
import pymysql
import time
import json
from PIL import Image
import re
url = 'https://api.bilibili.com/x/web-interface/search/type?jsonp=jsonp&&search_type=video&highlight=1&keyword=美食&page=1'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

res = requests.get(url=url, headers= header)
res=str(res.text)
res = json.loads(res)
for i,j in  enumerate(res["data"]["result"]):
    id = res["data"]["result"][i]["id"]
    title = res["data"]["result"][i]["title"]
    print(id,title)