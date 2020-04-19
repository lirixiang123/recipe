from django.conf.urls import url
from  .views import Register,user_login,user_logout
urlpatterns = [
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
]
