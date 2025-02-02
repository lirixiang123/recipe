from django.shortcuts import render, redirect

from apps.comment.form import CommentText
from utils.decorators import login_required
from .models import Comment
from django.contrib.contenttypes.models import ContentType


# Create your views here.





# def comment(request):
#     # 判断用户是否登录
#     if not request.user.is_authenticated:
#         return error_response('没有登录，不能进行评论')
#     # 得到对应的评论内容（POST请求）
#     comment_text = request.POST['comment_text']
#     # 利用strip()函数去掉两边的空格，判断评论内容是否为空
#     if comment_text.strip() == '':
#         return error_response('评论内容为空')
#     else:
#         # 得到对应的数据
#         content_type = request.POST['content_type']
#         object_id = request.POST['object_id']
#         # 查询对应的ContentType对象和评论的对象是否存在
#         if (not ContentType.objects.filter(model=content_type).exists()) or (not Item.objects.filter(pk=object_id).exists()):
#             return error_response('评论对象不存在')
#         content_type = ContentType.objects.get(model=content_type)
#         # 创建评论
#         comment_data = Comment(content_type=content_type, object_id=object_id, comment_text=comment_text, comment_user=request.user)
#         comment_data.save()
#         # 得到评论的时间
#         comment_time = comment_data.comment_time.strftime('%Y-%m-%d %H:%M:%S')
#         return success_response(comment_text, request.user, comment_time)



@login_required
def community(request):
    user = request.user
    user_content_type = ContentType.objects.get_for_model(user)
    comments = Comment.objects.filter(content_type=user_content_type)[:10]
    form = CommentText()
    return render(request, "community.html", locals())


