from django.contrib import admin

from .models import User, Subject, Event

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ["event_name", "event_date"]
    list_filter = ["event_date"]

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Event, EventAdmin)

