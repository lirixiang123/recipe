from django.conf.urls import url, include
from  .views import shop,detail
urlpatterns = [
    url(r'^$', shop, name='index'),
    url(r'^detail$', detail, name='detail'),
    url(r'^cart/', include('apps.shop.cart.urls', namespace='cart')), # 购物车模块
]
