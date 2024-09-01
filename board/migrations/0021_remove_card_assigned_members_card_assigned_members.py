# Generated by Django 5.0.6 on 2024-08-31 04:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0020_remove_card_assigned_members_card_assigned_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='assigned_members',
        ),
        migrations.AddField(
            model_name='card',
            name='assigned_members',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_cards', to='board.member'),
        ),
    ]