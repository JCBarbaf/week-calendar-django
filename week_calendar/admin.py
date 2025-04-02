from django.contrib import admin

from .models import Subject, Event, Password_Tokens
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ["event_name", "event_date"]
    list_filter = ["event_date"]

class TokenAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "expiration_date"]
    list_filter = ["expiration_date", "user"]

admin.site.register(Subject)
admin.site.register(Event, EventAdmin)
admin.site.register(Password_Tokens, TokenAdmin)
