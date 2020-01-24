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
    contributor = models.ForeignKey(User, verbose_name="贡献者", null=True)
    class Meta:
        verbose_name = "菜谱"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s:%s"%(self.id,self.title)