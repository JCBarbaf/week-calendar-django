from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('events-in-range/', views.get_events_in_range, name='get_events_in_range'),
    path('event/', views.get_event_by_id, name='get_event_by_id'),
    path('subjects-css/', views.subjects_css, name='subjects_css')
]