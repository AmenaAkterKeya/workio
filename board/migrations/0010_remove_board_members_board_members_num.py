# Generated by Django 5.0.6 on 2024-08-23 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_remove_card_is_completed_card_priority_card_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='members',
        ),
        migrations.AddField(
            model_name='board',
            name='members_num',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
