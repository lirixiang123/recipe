"""recipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from apps.user.views import submit,test
from apps.index.views import index,search,detail,add_collection
from apps.video.views import video
from apps.news.views import news
from apps.comment.views import community
from apps.shop.views import shop
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index,name='index'), # 首页
    url(r'^user/', include('apps.user.urls', namespace='user')), # 用户模块
    url(r'^shop/',include('apps.shop.urls',namespace='shop')), #商品模块

    url(r'^submit$',submit,name='submit'),

    url(r'^search/',search,name='search'),
    url(r'^detail/',detail,name='detail'),

    url(r'^video/',video,name='video'),

    url(r'^news/',news,name='news'),




    url(r'^add_collection$',add_collection,name='add_collection'),
    url(r'^test$',test,name='test'),
    url(r'^community/',community,name='community'),

    url('ckeditor',include('ckeditor_uploader.urls')),
    url(r'api/v1/',include('apps.apis.urls',namespace="apis")),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
