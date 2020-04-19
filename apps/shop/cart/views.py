from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection

from apps.shop.models import Shop


def cart_add(request):
    """向购物车添加数据"""
    shop_id = request.POST.get('shop_id')
    shop_count = request.POST.get('shop_count')
    print(shop_id,shop_count)
    #数据校验
    if not all([shop_id,shop_count]):
        return JsonResponse({"res":1,"errmsg":"数据不完整"})

    shop_item = Shop.objects.get_shop_by_id(id=shop_id)
    if shop_item is None:
        return JsonResponse({"res":2,"errmsg":"商品不存在"})

    try:
        count = int(shop_count)
    except Exception as e:
        return JsonResponse({"res":3,"errmsg":"商品必须为数字"})

    # 添加商品到购物车
    # 每个用户的购物车记录用一条hash数据保存，格式:cart_用户id: 商品id 商品数量
    conn =get_redis_connection('default')
    cart_key = f'cart_{request.user.id}'
    res = conn.hget(cart_key,shop_id)
    if res is None:
        res = count
    else:
        res = int(res) + count

    #判断商品的库存
    if res >= shop_item.stock:
        #库存不足
        return JsonResponse({"res":4,"errmsg":"商品库存不足"})
    else:
        conn.hset(cart_key,shop_id,res)
    return JsonResponse({"res":5})

def cart_count(request):
    """获取用户购物车中的商品数目"""
    conn = get_redis_connection('default')
    cart_key = f'cart_{request.user.id}'
    res = 0
    res_list = conn.hvals(cart_key)
    for i in res_list:
        res += int(i)
    return JsonResponse({"res":res})
