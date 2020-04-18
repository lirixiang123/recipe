from bs4 import BeautifulSoup
from django.shortcuts import render
import requests
# Create your views here.
from django.views.decorators.cache import cache_page
@cache_page(60 * 15)
def news(request):
    news = news_spider()
    soup = get_soup()
    if not request.GET.get("id"):
        id = 0
    else:
        id = int(request.GET.get("id"))-1
    detail_link = soup.select('div.detail a')[id]['href']
    soup = get_soup(detail_link)
    contents = soup.select('div.content p')
    #print(contents)
    content=" ".join(repr(i) for i in contents)
    #print(content)
    return render(request, "news.html", locals())



def get_soup(url = 'https://www.meishichina.com/News/'):

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

    res = requests.get(url=url, headers= header)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
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
