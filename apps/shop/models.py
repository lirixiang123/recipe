from django.db import models
from utils.enums import *
from db.base_model import BaseModel

# Create your models here.
from lxml.etree import strip_tags

class ShopManager(models.Manager):
    '''商品模型管理器类'''
    # sort='new' 按照创建时间进行排序
    # sort='hot' 按照商品销量进行排序
    # sort='price' 按照商品的价格进行排序
    # sort= 按照默认顺序排序
    def get_shop_by_type(self,  limit=None, sort='default'):
        '''根据商品类型id查询商品信息'''
        if sort == 'new':
            order_by = ('-create_time',)
        elif sort == 'hot':
            order_by = ('-deal', )
        elif sort == 'price_asc':
            order_by = ('price', )
        elif sort == 'price_desc':
            order_by = ('-price', )
        else:
            order_by = ('-pk', ) # 按照primary key降序排列。

        # 查询数据
        shop_li = self.all().order_by(*order_by)

        # 查询结果集的限制
        if limit:
            shop_li = shop_li[:limit]
        return shop_li

    def get_shop_by_id(self, id):
        '''根据商品的id获取商品信息'''
        try:
            shop_item = self.get(id=id)
        except self.model.DoesNotExist:
            # 不存在商品信息
            shop_item = None
        return shop_item



class Shop(BaseModel):
    image = models.CharField(max_length=200,verbose_name="图片")
    price = models.CharField(max_length=20,verbose_name="商品价格")
    deal = models.CharField(max_length=20,verbose_name="商品销量")
    title = models.CharField(max_length=100,verbose_name="商品名称")
    shop = models.CharField(max_length=50,verbose_name="商店名称")
    location = models.CharField(max_length=50,verbose_name="商店地址")
    stock = models.IntegerField(default=100, verbose_name='商品库存')

    status_choices = ((k,v) for k,v in STATUS_CHOICE.items())
    status = models.SmallIntegerField(default=ONLINE, choices=status_choices, verbose_name='商品状态')

    objects = ShopManager()

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = strip_tags(self.title)[:50]

        super().save(*args, **kwargs)

