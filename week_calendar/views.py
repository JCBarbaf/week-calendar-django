from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
import json

from .models import Event, Subject, User

# Create your views here.
@login_required
def index(request):
    user_id = request.user.id
    if not user_id:
        return JsonResponse({'error': 'No user provided'}, status=400)
    subjects = Subject.objects.filter(user=user_id, deleted_at__isnull=True).order_by('id')
    context = {'subjects': subjects}
    return render(request, "week_calendar/index.html", context)

@login_required
def get_current_user(request):
    return JsonResponse({'user_id': request.user.id, 'username': request.user.username})

def get_events_in_range(request):
    start_date = parse_datetime(request.GET.get('start_date'))
    end_date = parse_datetime(request.GET.get('end_date')) + timedelta(days=1) - timedelta(seconds=1)

    if not start_date or not end_date:
        return JsonResponse({'error: Invalid date format'}, status=400)

    events = Event.objects.filter(event_date__range=(start_date, end_date), deleted_at__isnull=True)

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
        'subject': event.subject.id,
        'user': event.user.email
    }
    return JsonResponse({'event': event_data}, status=200)

@csrf_protect
@login_required
@require_http_methods(["POST"])
def save_event(request):
    try:
        event_id = request.POST.get('id')
        event_name = request.POST.get('eventName')
        event_date = request.POST.get('eventDate')
        event_time = request.POST.get('eventTime')
        subject_id = request.POST.get('eventSubject')
        user = request.user

        if not all([event_name, event_date, event_time, subject_id]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            event_datetime = parse_datetime(f"{event_date}T{event_time}")
        except ValueError:
            return JsonResponse({'error': 'Invalid date or time format'}, status=400)

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'Subject not found'}, status=404)

        if event_id:
            try:
                event = Event.objects.get(id=event_id)
                event.event_name = event_name
                event.event_date = event_datetime
                event.subject = subject
                event.updated_at = datetime.now()
                event.save()
                message = "Event updated successfully"
            except Event.DoesNotExist:
                return JsonResponse({'error': 'Event not found'}, status=404)
        else:
            Event.objects.create(
                event_name=event_name,
                event_date=event_datetime,
                subject=subject,
                user=user,
                created_at=datetime.now()
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
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def subjects_css(request):
    subjects = Subject.objects.all()
    context = {'subjects': subjects}
    return render(request, 'week_calendar/subjects.css', context, content_type='text/css')

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

@login_required
def create_subject(request):
    user = request.user
    try:
        new_subject = Subject.objects.create(
            subject_name = 'New subject',
            subject_code = 'SUBJ',
            subject_color = '#ff0000',
            subject_white_text = 'True',
            user = user,
            created_at = datetime.now()
        )

        new_subject.subject_name = f'New subject {new_subject.id}'
        new_subject.subject_code = f'S{new_subject.id}'
        new_subject.save()

        message = "Subject created successfully"

        return JsonResponse({'message': message})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_protect
@require_http_methods(["POST"])
def update_subject(request):
    try:
        data = json.loads(request.body)
        subject_id = data.get("subject_id")
        column_name = data.get("column_name")
        new_value = data.get("new_value")

        if not all([subject_id, column_name]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)

        if not hasattr(subject, column_name):
            return JsonResponse({"error": "Invalid column name"}, status=400)

        field_type = subject._meta.get_field(column_name).get_internal_type()
        if field_type == "BooleanField":
            new_value = new_value.lower() in ["true", "1", "yes"]
        elif field_type in ["IntegerField", "FloatField"]:
            new_value = float(new_value) if "." in new_value else int(new_value)

        setattr(subject, column_name, new_value)
        subject.updated_at = datetime.now()
        subject.save()

        return JsonResponse({"success": True, "message": f"{column_name} updated successfully"})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def get_subjects_by_user(request):

    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error: No user provided'}, status=400)

    subjects = Subject.objects.filter(user=user_id, deleted_at__isnull=True).order_by('id')

    subject_data = [
        {
            'id': subject.id,
            'subject_name': subject.subject_name,
            'subject_code': subject.subject_code,
            'subject_color': subject.subject_color,
            'subject_white_text': subject.subject_white_text
        }
        for subject in subjects
    ]

    return JsonResponse({'subjects': subject_data}, status=200)

def get_number_of_events(request):

    subject_id = request.GET.get('subject_id')
    if not subject_id:
        return JsonResponse({'error: No subject provided'}, status=400)

    events_number = Event.objects.filter(subject_id=subject_id, deleted_at__isnull=True).count()

    return JsonResponse({'eventsNumber': events_number}, status=200)

@csrf_protect
@require_http_methods(["POST"])
def delete_subject(request):
    try:
        subject_id = request.POST.get('id')
        subject = Subject.objects.get(id=subject_id)
        events = Event.objects.filter(subject_id=subject_id)
        events.update(deleted_at=datetime.now())
        subject.deleted_at = datetime.now()
        subject.save()
        return JsonResponse({'message': 'Event updated successfully'})
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)