from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import HttpResponse

from .forms import MediaForm
from .models import TempMedia
from main.models import Media, User, Profile
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db import transaction

def add_media_item(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to perform this action")
        return redirect('home')
    
    user_profile = Profile.objects.get(id=request.user.profile.id)
    if user_profile.is_blocked:
        messages.error(request, "You have been blocked from editing")
        return redirect('home')
    
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            temp_media = form.save(commit=False)
            temp_media.type_of_request = "add"
            temp_media.user = request.user
            temp_media.save()
            form.save_m2m()
            messages.success(request, "Your add request has been submitted for review.")
            return redirect('home')
        else:
            return render(request, 'editor/media_item_form.html', {'form': form})
    else:
        form = MediaForm()

    data = {'form': form}
    return render(request, 'editor/media_item_form.html', data)


def edit_media_item(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to perform this action")
        return redirect('home')

    user_profile = Profile.objects.get(id=request.user.profile.id)
    if user_profile.is_blocked:
        messages.error(request, "You have been blocked from editing")
        return redirect('home')

    media_item = get_object_or_404(Media, pk=pk)

    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            temp_media = form.save(commit=False)
            temp_media.type_of_request = "edit"
            temp_media.user = request.user
            temp_media.media_item = media_item
            temp_media.save()
            form.save_m2m()  
            messages.success(request, "Your edit request has been submitted for review.")
            return redirect('home')
        return render(request, 'editor/media_item_form.html', {'form': form})
    else:
        initial = {
            'title': media_item.title,
            'description': media_item.description,
            'type': media_item.type,
            'status': media_item.status,
            'start_year': media_item.start_year,
            'end_year': media_item.end_year,
            'number_of_seasons': media_item.number_of_seasons,
            'number_of_series': media_item.number_of_series,
            # 'cover': media_item.cover,
        }
        form = MediaForm(initial=initial)
        form.fields['genres'].initial = media_item.genres.values_list('id', flat=True)
        form.fields['studios'].initial = media_item.studios.values_list('id', flat=True)

    return render(request, 'editor/media_item_form.html', {'form': form})

@require_POST
def accept_request(request, pk):
    if not request.user.is_superuser:
        return redirect('home')

    temp_media = get_object_or_404(TempMedia, pk=pk)

    field_names = [f.name for f in Media._meta.fields if f.name != 'id']

    data = {}
    for name in field_names:
        if name == 'cover':
            continue  
        if hasattr(temp_media, name):
            data[name] = getattr(temp_media, name)

    with transaction.atomic():
        if temp_media.type_of_request == "add":
            new = Media(**data)
            new.save()
            new.genres.set(temp_media.genres.all())
            new.studios.set(temp_media.studios.all())
            if temp_media.cover:
                new.cover = temp_media.cover
                new.save(update_fields=['cover'])
        else:
            media_item = temp_media.media_item
            for k, v in data.items():
                setattr(media_item, k, v)
            media_item.save()

            media_item.genres.set(temp_media.genres.all())
            media_item.studios.set(temp_media.studios.all())

            if temp_media.cover:
                media_item.cover = temp_media.cover
                media_item.save(update_fields=['cover'])

        temp_media.delete()

    return redirect(reverse('admin:index'))

@require_POST
def reject_request(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    temp_media = TempMedia.objects.get(pk=pk)
    temp_media.delete()
    return redirect('/admin')

@require_POST
def ban_user(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    user_profile = Profile.objects.get(user=pk)
    user_profile.is_blocked = True
    user_profile.save()
    TempMedia.objects.filter(user=pk).delete()
    return redirect('/admin')
