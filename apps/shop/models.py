from django.db import models

# Create your models here.
from lxml.etree import strip_tags


class Shop(models.Model):
    image = models.CharField(max_length=200)
    price = models.IntegerField()
    deal = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    shop = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    class Meta:
        verbose_name = "商店"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = strip_tags(self.title)[:50]

        super().save(*args, **kwargs)
