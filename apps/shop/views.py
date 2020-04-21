import random

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django_redis import get_redis_connection

from .models import Shop
import json
from django.core import serializers
# Create your views here.
from django.views.decorators.cache import cache_page
@cache_page(60 * 15)
def shop(request):
    shop_new = Shop.objects.get_shop_by_type(limit=9,sort='new')
    shop_hot = Shop.objects.get_shop_by_type(limit=9,sort='hot')
    shop_price_asc = Shop.objects.get_shop_by_type(limit=9,sort='asc_price')
    shop_price_desc = Shop.objects.get_shop_by_type(limit=9,sort='desc_price')
    shop_items = Shop.objects.all()[:9]

    context = {
        'shop_new':shop_new,
        'shop_hot':shop_hot,
        'shop_price_asc':shop_price_asc,
        'shop_price_desc':shop_price_desc,
        'shop_items':shop_items,
    }
    return render(request,"shop.html",context)

def detail(request):
    id = request.GET.get("id","")
    shop_item = Shop.objects.get_shop_by_id(id)
    if shop_item is None:
        return redirect(reverse("shop:index"))

    #新品推荐
    shop_recommend = random.sample(list(Shop.objects.all()), 5)
    context = {
        "shop_item":shop_item,
        "shop_recommend":shop_recommend,
    }
    return render(request,'product-page.html',context)

