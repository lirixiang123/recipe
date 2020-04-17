from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.comment.form import CommentText
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.http import JsonResponse
from apps.index.models import Item

# Create your views here.


# 错误响应的方法
def error_response(message):
    data = {}
    data['status'] = 'ERROR'
    data['message'] = message
    return JsonResponse(data)


# 正确响应的方法
def success_response(comment_text, comment_user, comment_time):
    data = {}
    data['status'] = 'SUCCESS'
    data['message'] = '评论成功'
    data['comment_text'] = comment_text
    data['comment_user'] = str(comment_user)
    data['comment_time'] = comment_time
    return JsonResponse(data)


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

def comment(request):
    comment_user =request.user
    comment_text = request.POST.get('comment_text','')
    if comment_text.strip() == "":
        message = "评论不能为空"
        return error_response(message)

    content_type = request.POST.get('content_type','')
    object_id = request.POST.get('object_id','')
    print(content_type)
    print(object_id)
    print(comment_text)
    model_class = ContentType.objects.get(model=content_type)



    comment = Comment()
    comment.object_id = object_id
    comment.comment_user = comment_user
    comment.comment_text = comment_text
    comment.content_type = model_class
    comment.save()

    item =  Item.objects.get(id = object_id)
    item.comment = int(item.comment) + 1
    item.save()
    # referer = request.META.get('HTTP_REFERER',reverse('index'))
    # return redirect(referer)
    comment_time = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
    return success_response(comment_text, request.user, comment_time)


def community(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    user_content_type = ContentType.objects.get_for_model(user)
    comments = Comment.objects.filter(content_type=user_content_type)[:10]
    form = CommentText()
    return render(request, "community.html", locals())

def community_api(request):

    comment_user = request.user
    comment_text = request.POST.get('comment_text', '')
    if comment_text.strip() == "":
        message = "评论不能为空"
        return error_response(message)

    content_type = request.POST.get('content_type', '')
    object_id = request.POST.get('object_id', '')
    model_class = ContentType.objects.get(model=content_type)

    comment = Comment()
    comment.object_id = object_id
    comment.comment_user = comment_user
    comment.comment_text = comment_text
    comment.content_type = model_class
    comment.save()

    user = User.objects.get(id=object_id)
    user.comment = int(user.comment) + 1
    user.save()

    comment_time = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
    return success_response(comment_text, request.user, comment_time)

