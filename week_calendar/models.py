from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.

class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    subject_code = models.CharField(max_length=5)
    subject_color = models.CharField(max_length=7, help_text="hex color code")
    subject_white_text = models.BooleanField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject_name
  
    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    @admin.display(
        ordering="event_date"
    )

    def __str__(self):
        return self.event_name
  
    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

class Password_Tokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
