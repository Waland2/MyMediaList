from django.contrib import admin
from .models import *

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'rating', 'is_published']
    list_filter = ['title', 'status', 'rating', 'is_published']
    search_fields = ['title']
    ordering = ['id']

admin.site.register(Profile)
admin.site.register(Genre)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Studio)

