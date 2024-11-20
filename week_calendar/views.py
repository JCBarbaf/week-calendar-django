from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
import json

from .models import Event, Subject, User

# Create your views here.
def index(request):
    subjects = Subject.objects.all()
    context = {'subjects': subjects}
    return render(request, "week_calendar/index.html", context)

def get_events_in_range(request):
    start_date = parse_datetime(request.GET.get('start_date'))
    end_date = parse_datetime(request.GET.get('end_date')) + timedelta(days=1) - timedelta(seconds=1)

    if not start_date or not end_date:
        return JsonResponse({'error: Invalid date format'}, status=400)

    events = Event.objects.filter(event_date__range=(start_date, end_date))

    event_data = [
        {
            'id': event.id,
            'event_name': event.event_name,
            'event_date': event.event_date.isoformat(),
            'subject': event.subject.subject_code,
            'user': event.user.email,
        }
        for event in events
    ]

    return JsonResponse({'events': event_data}, status=200)

def get_event_by_id(request):
    event_id = request.GET.get('id')
    if not event_id:
        return JsonResponse({'error: No ID provided'}, status=400)
    event = Event.objects.get(id=event_id)
    event_data = {
        'id': event.id,
        'event_name': event.event_name,
        'event_date': event.event_date.isoformat(),
        'subject': event.subject.subject_code,
        'user': event.user.email
    }
    return JsonResponse({'event': event_data}, status=200)

@csrf_protect
@require_http_methods(["POST"])
def save_event(request):
    try:
        event_id = request.POST.get('id')
        event_name = request.POST.get('eventName')
        event_date = request.POST.get('eventDate')
        event_time = request.POST.get('eventTime')
        subject_code = request.POST.get('eventSubject')
        user_email = request.POST.get('user')

        if not all([event_name, event_date, event_time, subject_code, user_email]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            event_datetime = parse_datetime(f"{event_date}T{event_time}")
        except ValueError:
            return JsonResponse({'error': 'Invalid date or time format'}, status=400)

        try:
            subject = Subject.objects.get(subject_code=subject_code)
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'Subject not found'}, status=404)
        
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if event_id:
            try:
                event = Event.objects.get(id=event_id)
                event.event_name = event_name
                event.event_date = event_datetime
                event.subject = subject
                event.save()
                message = "Event updated successfully"
            except Event.DoesNotExist:
                return JsonResponse({'error': 'Event not found'}, status=404)
        else:
            Event.objects.create(
                event_name=event_name,
                event_date=event_datetime,
                subject=subject,
                user=user
            )
            message = "Event created successfully"

        return JsonResponse({'message': message})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)
    
@csrf_protect
@require_http_methods(["POST"])
def delete_event(request):
    try:
        event_id = request.POST.get('id')
        event = Event.objects.get(id=event_id)
        event.deleted_at = datetime.now()
        event.save()
        return JsonResponse({'message': 'Event updated successfully'})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

def subjects_css(request):
    subjects = Subject.objects.all()
    context = {'subjects': subjects}
    return render(request, 'week_calendar/subjects.css', context, content_type='text/css')