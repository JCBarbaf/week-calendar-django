# Generated by Django 5.2.dev20241101104349 on 2024-11-11 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('week_calendar', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Events',
            new_name='Event',
        ),
        migrations.RenameModel(
            old_name='Subjects',
            new_name='Subject',
        ),
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
    ]