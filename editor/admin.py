from django.contrib import admin

from .models import TempMedia

@admin.register(TempMedia)
class TempMediaAdmin(admin.ModelAdmin):
    list_display = ['type_of_request',  'title', 'status', 'type']
    list_filter = ['type_of_request', 'title', 'status', 'type']
    search_fields = ['title']
    ordering = ['id']