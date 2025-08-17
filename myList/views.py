from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from main.models import Media
from django.contrib import messages
from django.views.decorators.http import require_POST

@require_POST
@login_required
def media_list(request):
    post_queries = request.POST
    ml_object = MyListObject.objects.filter(user__id=request.user.id, media_item__id=post_queries['media_item_id'])
    if ml_object and post_queries.get("delete"):
        ml_object[0].delete()

    media_item = Media.objects.get(id=post_queries['media_item_id'])
    user = User.objects.get(id=request.user.id)
    watch_status = MyListStatus.objects.get(id=post_queries['status'])

    if post_queries.get('score') != 'null':
        score = MyListScores.objects.get(id=post_queries['score'])
    else:
        score = None
    
    comment = post_queries['comment']
    
    if ml_object:
        ml_object.update(
            media_item=media_item,
            user=user,
            watch_status=watch_status,
            score=score,
            comment=comment
        )
    else:
        new_object = MyListObject(
            media_item=media_item,
            user=user,
            watch_status=watch_status,
            score=score,
            comment=comment
        ) 
        new_object.save()
    return HttpResponse("done")

def show_user_list(request, username):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to perform this action")
        return redirect('home')
    
    owner = get_object_or_404(User, username=username)
    owner_list = MyListObject.objects.filter(user__username=username).order_by("watch_status__priority_in_list", "media_item__title")

    is_status = request.GET.get('status')
    if is_status and is_status != "0":
        owner_list = owner_list.filter(watch_status__id=is_status)

    is_sort = request.GET.get('sort')
    static_sort = is_sort
    if is_sort:
        if is_sort.find('-') != -1:
            is_sort = is_sort.replace('-', '')
        else:
            is_sort = '-' + is_sort
        if is_sort.find('media_item') != -1:
            is_sort += '__title'
        owner_list = owner_list.order_by(is_sort)

    data = {
        'owner': owner.profile,
        'owner_user': owner,
        'owner_list': owner_list,
        'watch_status': is_status,
        'sort_type': static_sort 
    }
    return render(request, "myList/list.html", data)
