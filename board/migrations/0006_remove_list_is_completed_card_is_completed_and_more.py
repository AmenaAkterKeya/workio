# Generated by Django 5.0.6 on 2024-08-20 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_remove_card_is_completed_list_is_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='card',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Progress',
        ),
    ]
