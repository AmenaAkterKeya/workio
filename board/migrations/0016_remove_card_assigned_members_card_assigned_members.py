# Generated by Django 5.0.6 on 2024-08-30 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0015_remove_card_assigned_members_card_assigned_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='assigned_members',
        ),
        migrations.AddField(
            model_name='card',
            name='assigned_members',
            field=models.ManyToManyField(blank=True, related_name='assigned_cards', to='board.member'),
        ),
    ]
