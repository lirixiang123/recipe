from django.http import JsonResponse
from django.shortcuts import render
from .models import Shop
import json
from django.core import serializers
# Create your views here.
def shop(request):
    shop_items = Shop.objects.all()[:9]
    shop_data = serializers.serialize('json', shop_items)
    shop_data = json.loads(shop_data)
    #print(shop_data)
    return render(request,"shop.html",locals())

def shop_api():
    shop_items = Shop.objects.all()[:10]
    shop_data = serializers.serialize('json',shop_items)
    shop_data = json.loads(shop_data)
    #print(shop_data)
    return JsonResponse(shop_data, safe=False)
