import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import UserRegistrationForm, LoginForm
from .models import Media, Type, Status, Genre, User, Profile
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.http import QueryDict
from myList.models import MyListStatus, MyListScores, MyListObject
from django.views.decorators.http import require_POST
from django.conf import settings as config

words_replace = {
    'sort': {
        'popularity': 'number_of_ratings',
        'release': 'start_year',
    }
}
allowed_get = ['sort', 'status', 'type', 'genres', 'studios']

def index(request):
    return redirect('catalogue')

def show_catalogue(request):
    checked_queries = {}

    for key in request.GET:
        if key in allowed_get:
            checked_queries[key] = request.GET.get(key)
    
    queries = []
    for key in checked_queries:
        if key == 'sort':
            for i in words_replace['sort']:
                checked_queries[key] = checked_queries[key].replace(i, words_replace['sort'][i])
            continue

        if key == 'page':
            continue

        val = checked_queries[key]
        tq =  []
        if key in ['studios']:
            queries.append(["or", [[key + '__name', val]]])
            continue
        for i in val.split(","):
            tq.append([key + "__name", i])
        if key == "genres":
            queries.append(["and", tq])
            continue

        queries.append(["or", tq])     

    filters = Q()
    filterWithAnd = []
    if queries:
        for qur in queries:
            fq = Q()
            if qur[0] == "or":
                for q in qur[1]:
                    fq |= Q(**{q[0]:q[1]})
            elif qur[0] == "and":
                for q in qur[1]:
                    filterWithAnd.append(Q(**{q[0]: q[1]}))
            
            filters &= fq
    
    media = Media.objects.filter(filters).distinct()
    for i in filterWithAnd:
        media = media.filter(i)

    sortBy = checked_queries.get('sort')
    if sortBy:
        try:
            media = media.order_by(sortBy)[::-1] 
        except:
            return redirect('catalogue')
    
    paginator = Paginator(media, config.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.GET.get('media_only'):
        return render(request, 'main/media_only.html', {
            "page_obj": page_obj
        })

    status = Status.objects.all()
    types = Type.objects.all()
    genres = Genre.objects.all()

    query_params = QueryDict('', mutable=True)
    query_params.update(request.GET)

    if not page_number:
        page_number = 1
    query_params['page'] = int(page_number) + 1
    next_page_url = f"?{query_params.urlencode()}"
    query_params['page'] -= 2
    prev_page_url = f"?{query_params.urlencode()}"

    data = {
        "page_obj": page_obj,
        "c_status": status,
        "c_types": types,
        "c_genres": genres,
        "prev_page": prev_page_url, 
        "next_page": next_page_url
    }
    return render(request, 'main/media.html', data)

def show_media_item(request, media_item_id, media_item_title=None):
    media = get_object_or_404(Media, id=media_item_id)

    ml_media_item_info = MyListObject.objects.filter(media_item__id=media_item_id, user__id=request.user.id)
    
    if ml_media_item_info:
        ml_media_item_info = ml_media_item_info[0]
    else:
        ml_media_item_info = None

    seasons_word = ""
    series_word = ""

    if media.number_of_seasons:
        if media.number_of_seasons == 1:
            seasons_word = "season"
        else:
            seasons_word = "seasons"

    if media.number_of_series:
        if media.number_of_series == 1:
            series_word = "episode"
        else:
            series_word = "episodes"
        
    data = {
        "data": media,
        "seasons_word": seasons_word,
        "series_word": series_word,
        "ml_status": MyListStatus.objects.all(),
        "ml_scores": MyListScores.objects.all(),
        "ml_item_info": ml_media_item_info
    }

    return render(request, "main/media_item.html", data)

def show_search(request):
    value = (request.GET.get('search') or '').strip()
    search_result = Media.objects.none()
    if value:
        search_result = Media.objects.filter(title__icontains=value).order_by('-number_of_ratings')
    return render(request, 'main/search_result.html', {"search_result": search_result})

@require_POST
@login_required
def settings(request):
    user_profile = Profile.objects.get(id=request.user.profile.id)
    for key, value in request.POST.items():
        if key in ['is_list_public', 'is_cover_in_list']:
            setattr(user_profile, key, value)
    user_profile.save()
    return HttpResponse('success')

def show_settings(request, username):
    owner = get_object_or_404(User, username=username)
    owner_profile = owner.profile

    if owner.id != request.user.id:
        return redirect('home')
    
    settings = {}
    settings["is_list_public"] = owner_profile.is_list_public
    settings["is_cover_in_list"] = owner_profile.is_cover_in_list

    data = {
        'owner_user': owner,
        'owner_profile': owner_profile,
        'settings': json.dumps(settings)
    }
    return render(request, 'main/settings.html', data)

def user_register(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already registered")
        return redirect('home')
    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            print(reg_form.data)
            print(reg_form.cleaned_data)
            new_user = reg_form.save(commit=False)  
            new_user.set_password(reg_form.cleaned_data['password2'])
            new_user.save()
            login(request, new_user)
            messages.success(request, "Registration successful")
            return redirect('home')
    else:
        reg_form = UserRegistrationForm()
    return render(request, 'main/register.html', {'reg_form': reg_form})

def user_login(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in")
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back!")
                return redirect('home')
            else:
                return render(request, 'main/login.html', {'log_form': form, "status": "error"})
        return
    form = LoginForm()
    return render(request, 'main/login.html', {'log_form': form, "status": None})

def user_logout(request):
    if request.user.is_authenticated:
        messages.success(request, "You have logged out")
        logout(request)

    redirect_url = request.META.get('HTTP_REFERER')
    if redirect_url:
        return redirect(redirect_url)
    else:
        return redirect('home')
