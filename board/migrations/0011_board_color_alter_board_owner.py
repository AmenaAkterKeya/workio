# Generated by Django 5.0.6 on 2024-08-23 07:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customuser_bio'),
        ('board', '0010_remove_board_members_board_members_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='color',
            field=models.CharField(blank=True, default='#FFFFFF', max_length=7),
        ),
        migrations.AlterField(
            model_name='board',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='account.customuser'),
        ),
    ]
