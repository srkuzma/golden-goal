# Generated by Django 4.0.4 on 2022-05-31 15:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golden_goal', '0007_remove_comment_dislike_counter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 17, 34, 47, 306665)),
        ),
        migrations.AlterField(
            model_name='news',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 17, 34, 47, 306665)),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.CharField(default='images/image_0.png', max_length=250),
        ),
    ]
