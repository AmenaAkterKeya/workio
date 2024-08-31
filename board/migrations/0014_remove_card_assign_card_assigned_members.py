# Generated by Django 5.0.6 on 2024-08-30 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customuser_bio'),
        ('board', '0013_card_assign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='assign',
        ),
        migrations.AddField(
            model_name='card',
            name='assigned_members',
            field=models.ManyToManyField(blank=True, null=True, related_name='assigned_cards', to='account.customuser'),
        ),
    ]
