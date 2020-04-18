import random
import re
import threading

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from libs.spider_test import get_soup, spider, get_res
from .models import *
from apps.comment.models import Comment
from apps.comment.form import CommentText
# Create your views here.
def get_extra(i):

    soup = get_soup(i.url)
    res = get_res(i.url)
    try:
        p = soup.select('div.materials p')[0].get_text()
    except Exception:
        p = "没有简介"

    try:
        bar =  re.findall(r"""class="big">(.*?)</a>""",res)
        flavor = bar[0]
        technology = bar[1]
        #print(flavor, technology)
    except Exception:
        technology , flavor= "无","无"

    i.p = p
    i.flavor =flavor
    i.technology = technology

def get_image():
    url = "http://www.win4000.com/wallpaper_2285_0_0_1.html"
    res = get_res(url)
    image_list = re.findall(r'<img src="(http://pic1.win4000.com/wallpaper/.*?.jpg)"',res)
    return image_list

from django.views.decorators.cache import cache_page
@cache_page(60 * 15)
def index(request):
    ranking = Item.objects.order_by('-likes')[:27]
    recommend = random.sample(list(Item.objects.all()),5)
    for i in recommend:
        #print(i.url)
        t = threading.Thread(target=get_extra,args=(i,))
        t.start()
        t.join()
    rand = random.sample(list(Item.objects.all()),8)
    image_urls = get_image()[::-1]
    #print(image_urls)
    return render(request, 'index.html', locals())

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
    return render(request, 'browse-recipes.html', locals())

def detail(request):
    id = request.GET.get("id")
    item = Item.objects.get(id = id)
    #print(item.url)
    soup = get_soup(item.url)
    main,aux,p,mea,mea_tip = spider(soup)
    recommend = random.sample(list(Item.objects.exclude(id = id).filter(series__icontains=item.series).order_by('-likes')[:10]),3)
    item_content_type = ContentType.objects.get_for_model(item)
    comments = Comment.objects.filter(content_type= item_content_type,object_id=item.id)[:10]
    form = CommentText()
    return render(request, "recipe-page.html", locals())

#
# from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import weasyprint
#
# @staff_member_required
# def admin_order_pdf(request, order_id):
#     queryset = get_object_or_404(mymodel, id=mymodel_id)
#     html = render_to_string('pdf.html',{'queryset': queryset})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename=\"mymodel_{}.pdf"'.format(mymodel.id)
#     weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
#     return response




def add_collection(request):
    data ={}
    data['status'] = 'success'
    data['a'] = 'uiqwefgi'
    return JsonResponse(data)
