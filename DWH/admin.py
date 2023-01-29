from django.contrib import admin
from .models import User, Event
from django.db.models import QuerySet

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['nickname', 'first_name', 'last_name', 'date_of_birth', 'date_of_start_circle', 'telegram_id',
                    'timezone']
    list_editable = []
    filter_horizontal = []
    ordering = ['nickname']
    list_per_page = 20
    actions = []
    search_fields = ['name']
