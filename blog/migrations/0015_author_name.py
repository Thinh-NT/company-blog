# Generated by Django 3.2.3 on 2021-05-21 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20210520_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
