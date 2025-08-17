from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.add_media_item, name="addmedia"),
    path('edit/<int:pk>', views.edit_media_item, name="editmedia"),
    path('acceptrequest/<int:pk>/', views.accept_request, name='acceptrequest'),
    path('rejectrequest/<int:pk>/', views.reject_request, name='rejectrequest'),
    path('blockuser/<int:pk>', views.ban_user, name='blockuser')
]
