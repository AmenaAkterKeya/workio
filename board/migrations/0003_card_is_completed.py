# Generated by Django 5.0.6 on 2024-08-20 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_card_content_alter_list_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
