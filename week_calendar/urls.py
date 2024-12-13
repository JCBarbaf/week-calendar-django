from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path('events-in-range/', views.get_events_in_range, name='get_events_in_range'),
    path('event/', views.get_event_by_id, name='get_event_by_id'),
    path('save-event/', views.save_event, name='save_event'),
    path('delete-event/', views.delete_event, name='delete_event'),
    path('subjects-css/', views.subjects_css, name='subjects_css'),
    path('login/', auth_views.LoginView.as_view(template_name='week_calendar/login.html'), name='login'),
    path('logout/', CustomLoginView.as_view(), name='logout'),
]