# Generated by Django 4.2.4 on 2023-08-27 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hindustantimesbangla',
            name='image_source',
            field=models.URLField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='tv9bangla',
            name='image_source',
            field=models.URLField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='zeenews',
            name='image_source',
            field=models.URLField(max_length=1000),
        ),
    ]
