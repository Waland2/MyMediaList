from django.urls import path, include
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.index, name="home"),
    path(f'{settings.MEDIA_COLLECTION_SLUG}/', views.show_catalogue, name="catalogue"),
    path(f'{settings.MEDIA_ENTITY_SLUG}/<int:media_item_id>/', views.show_media_item),
    path(f'{settings.MEDIA_ENTITY_SLUG}/<int:media_item_id>/<slug:media_item_title>/', views.show_media_item),
    path('register/', views.user_register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('search/', views.show_search, name="search"),
    path('settings/', views.settings),
    path('settings/<slug:username>/', views.show_settings)
]
