# Generated by Django 5.1.7 on 2025-03-10 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_created_at_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
