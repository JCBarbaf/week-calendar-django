from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta

from .models import Event, Subject

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

def subjects_css(request):
    subjects = Subject.objects.all()
    context = {'subjects': subjects}
    return render(request, 'week_calendar/subjects.css', context, content_type='text/css')