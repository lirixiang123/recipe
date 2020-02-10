from django.db import models

# Create your models here.
from user.models import User




class Item(models.Model):
    url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    title = models.CharField(max_length=50)
    comment = models.IntegerField()
    likes = models.IntegerField()
    series = models.CharField(verbose_name="分类",max_length=50)
    class Meta:
        verbose_name = "菜谱"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s:%s"%(self.id,self.title)

class Collection(models.Model):
    item = models.ForeignKey(Item,verbose_name="菜谱",related_name="collection")
    user = models.ForeignKey(User,verbose_name="收藏者",related_name="collection")
    create_time = models.DateTimeField("收藏/取消时间",auto_now=True)
    status = models.BooleanField("收藏状态",default=True)

    class Meta:
        verbose_name = "收藏记录"
        verbose_name_plural = verbose_name
    def __str__(self):
        if self.status:ret = "收藏"
        else:ret = "取消收藏"
        return "%s:%s:%s"%(self.user,self.ret,self.item.title)