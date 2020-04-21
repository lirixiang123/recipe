import json

import requests
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page
@cache_page(60 * 15)
def video(request):
    q = request.GET.get('q')
    id = request.GET.get('id')

    if not q:
        q = "美食"
    res = get_json(q)
    video_list = []
    for i in range(len(res["data"]["result"])):
        for j in res["data"]["result"]:
            videos = {}
            videos["id"] = j["id"]
            videos["title"] = j["title"]
            videos["description"] = j["description"]
            videos["tag"] = j["tag"]
            videos["pic"] = j["pic"]
            video_list.append(videos)
    video_list = video_list[:7]
    context = {
        "video_list":video_list,
        "video_id":id,
    }
    # print(video_list)
    return render(request, "video.html", context)


def get_json(q):
    url = f'https://api.bilibili.com/x/web-interface/search/type?jsonp=jsonp&&search_type=video&highlight=1&keyword={q}&page=1&danmaku=0'
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    res = requests.get(url=url, headers= header)
    res=str(res.text)
    res = json.loads(res)
    return res
