from apps.comment.models import Comment
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

def comment(request):
    comment_user =request.user
    comment_text = request.POST.get('comment_text','')
    if comment_text.strip() == "":
        message = "评论不能为空"
        return error_response(message)

    content_type = request.POST.get('content_type','')
    object_id = request.POST.get('object_id','')
    # print(content_type)
    # print(object_id)
    # print(comment_text)
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

    # user = User.objects.get(id=object_id)
    # print(user.comment_set.filter(comment_user=user)[0].object_id)
    # user.save()

    comment_time = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
    return success_response(comment_text, request.user, comment_time)
