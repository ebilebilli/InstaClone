# Generated by Django 5.1.7 on 2025-03-11 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
