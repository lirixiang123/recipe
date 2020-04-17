import json

import requests
from django.shortcuts import render

# Create your views here.
def video(request):
    q = request.GET.get('q')
    if not q:
        q = "美食"
    res = get_json(q)
    videos = {}
    for i,j in  enumerate(res["data"]["result"]):
        videos[res["data"]["result"][i]["id"]] = res["data"]["result"][i]["title"]
    return render(request, "video.html", locals())

def get_json(q):
    url = 'https://api.bilibili.com/x/web-interface/search/type?jsonp=jsonp&&search_type=video&highlight=1&keyword=%s&page=1&danmaku=0'%(q)
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    res = requests.get(url=url, headers= header)
    res=str(res.text)
    res = json.loads(res)
    return res
