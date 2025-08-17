from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.media_list, name='list'),
    path('<slug:username>/', views.show_user_list, name="userlist")
]
