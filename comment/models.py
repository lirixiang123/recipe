from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    comment_text = RichTextUploadingField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)



    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ['-id']