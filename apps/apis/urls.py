from django.conf.urls import url
from  .views import comment,community
urlpatterns = [
    url(r'^comment$',comment,name='comment'),
    url(r'^community$',community,name='community'),


]
