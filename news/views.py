from bs4 import BeautifulSoup
from django.shortcuts import render
import requests
# Create your views here.
def news(request):
    news = news_spider()
    return render(request,"news.html",locals())

def news_detail(request):
    """资讯详情页"""
    soup = get_soup()
    id = request.GET.get("id")
    # print(id)
    # print(type(id))
    id= int(id)-1
    link = soup.select('div.detail a')[id]['href']
    soup = get_soup(link)
    title = soup.select('div.main a')[0].get_text()
    contents = soup.select('div.content p')
    content=" ".join(repr(e) for e in contents)
    return render(request,"news_detail.html",locals())

def get_soup(url = 'https://www.meishichina.com/News/'):

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

    res = requests.get(url=url, headers= header)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    return soup

def news_spider():
    soup = get_soup()
    k=[]
    titles = soup.select('div.detail a')
    for i in titles[:20]:
        k.append(i.get_text())

    v=[]
    contents = soup.select('div.detail p')[:40]
    for i,j in enumerate(contents):
        if i % 2 == 0:
            content = contents[i].get_text() + " "*4 + contents[i+1].get_text() + "..."
            v.append(content)

    news = dict(zip(k,v))
    return news