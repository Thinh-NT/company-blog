# Generated by Django 3.2.3 on 2021-05-18 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_rename_time_stamp_post_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views_count',
            field=models.IntegerField(default=0),
        ),
    ]