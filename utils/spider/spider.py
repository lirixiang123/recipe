import re

import requests
from bs4 import BeautifulSoup
import pymysql
import time
import json
from PIL import Image
"""
http://www.meishij.net/zuofa/aoerliangweiboshupian.html
http://www.meishij.net/zuofa/xianxianghuasheng_1.html
http://www.meishij.net/zuofa/denglongqiezi_12.html
http://www.meishij.net/zuofa/yutoudoufutang_30.html
http://www.meishij.net/zuofa/zhumiantiao_1.html
"""

url = "https://api.bilibili.com/x/web-interface/search/type?jsonp=jsonp&&search_type=video&highlight=1&keyword={q}&page=1&danmaku=0"
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

res = requests.get(url=url, headers= header).text

res = json.loads(res)
print(res)
