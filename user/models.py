from django.db import models
# # Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=30)
    password = models.CharField(verbose_name="密码", max_length=50)
    email = models.EmailField(max_length=50)
    def __str__(self):
      return self.username

    def to_dict(self):
      return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

    def __repr__(self):
        return '<User: %s %s>'%(self.name,self.password)

    class Meta:
      verbose_name = "用户列表"
      verbose_name_plural = verbose_name

