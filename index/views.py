import random
import  requests
from bs4 import BeautifulSoup
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from comment.models import Comment
from comment.form import CommentText
# Create your views here.
def index(request):
    ranking = Item.objects.order_by('-likes')[:5]

    rand = random.sample(list(Item.objects.all()),6)
    all = random.sample(list(Item.objects.all()),27)
     # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(all,9)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            lastest = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            lastest = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            lastest = paginator.page(paginator.num_pages)
    return render(request,'index.html',locals())

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        result =  Item.objects.order_by('-likes')[:8]
        return render(request, 'browse-recipes.html', locals())

    result = Item.objects.filter(title__icontains=q)

    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(result,8)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            result = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            result = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            result = paginator.page(paginator.num_pages)
    return render(request,'browse-recipes.html',locals())

def detail(request):
    id = request.GET.get("id")
    item = Item.objects.get(id = id)
    print(item.url)
    soup = get_soup(item.url)
    main,aux,p,mea,mea_tip = spider(soup)
    recommend = random.sample(list(Item.objects.exclude(id = id).filter(series__icontains=item.series).order_by('-likes')[:10]),3)
    item_content_type = ContentType.objects.get_for_model(item)
    comments = Comment.objects.filter(content_type= item_content_type,object_id=item.id)[:10]
    form = CommentText()
    return render(request,"recipe-page.html",locals())



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



def add_collection(request):
    data ={}
    data['status'] = 'success'
    data['a'] = 'uiqwefgi'
    return HttpResponse(data)
