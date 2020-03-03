import os
import re
import requests
from bs4 import BeautifulSoup


def get_res(url="https://movie.douban.com/"):
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"}
    response = requests.get(url,headers=headers)
    return response

def down_img():
    list = re.findall('https://.*?(?:.jpg|.gif|.png|.webp)',get_res().text)
    if not os.path.exists('./photos'):os.mkdir("./photos")
    for j in list:
        i=j.split("/")[-1]
        with open('./photos/%s'%i,'wb+') as f:
            data = get_res(url=j).content
            f.write(data)
if __name__ == "__main__":
    get_res()

