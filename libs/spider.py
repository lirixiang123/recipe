import requests
from bs4 import BeautifulSoup

def get_res(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    res = requests.get(url, headers=header).text
    return res

def get_soup(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    res = requests.get(url, headers = header)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

def spider(soup):

    try:
        p=soup.select('div.materials p')[0].get_text()
    except Exception:
        p="无简介"

    m=soup.select('div.zl ul li ')
    main = {}
    for i in m:
        main[i.select('a img')[0]['src']]= i.select('div h4')[0].get_text()

    aux =[]
    a=soup.select('div.fuliao ul li ')
    for i in a:
        aux.append(i.get_text())

    mea_p=soup.select('div.edit p')
    k = []
    for i in mea_p:
        # print(i.get_text())
        k.append(i.get_text())
    k=[x for x in k if x != '']

    mea_img=soup.select('div.edit p img')
    v = []
    for i in mea_img:
        # print(i['src'])

        v.append(i['src'])


    mea = dict(zip(k,v))
    mea_tip = []
    try:
        if k.__len__() > v.__len__():
            for i in range(k.__len__()-v.__len__()):
                mea_tip.append(k[-(k.__len__()-v.__len__()-i)])
            # print(mea_tip)
        else:
            mea_tip.append( "不好意思,木得啦~~")

    except Exception as e:
        print(e)



    return main,aux,p,mea,mea_tip
