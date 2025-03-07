from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='week_calendar/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("signup/", views.signup, name="signup"),
    path("current-user/", views.get_current_user, name="current-user"),
    path('events-in-range/', views.get_events_in_range, name='get_events_in_range'),
    path('event/', views.get_event_by_id, name='get_event_by_id'),
    path('save-event/', views.save_event, name='save_event'),
    path('delete-event/', views.delete_event, name='delete_event'),
    path('subjects-css/', views.subjects_css, name='subjects_css'),
    path("create-subject/", views.create_subject, name="create_subject"),
    path("update-subject/", views.update_subject, name="update_subject"),
    path('subjects/', views.get_subjects_by_user, name='get_subjects_by_user'),
    path('events-number/', views.get_number_of_events, name='get_number_of_events'),
    path('delete-subject/', views.delete_subject, name='delete_subject'),
]