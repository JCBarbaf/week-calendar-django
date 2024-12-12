from django.contrib import admin

from .models import Subject, Event
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ["event_name", "event_date"]
    list_filter = ["event_date"]

# admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Event, EventAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

