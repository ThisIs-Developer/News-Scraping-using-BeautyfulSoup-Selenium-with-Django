# Generated by Django 4.2.4 on 2023-08-27 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HindustanTimesBangla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.TextField()),
                ('sort_description', models.TextField()),
                ('news', models.TextField()),
                ('image_source', models.URLField()),
                ('image_caption', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TV9Bangla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.TextField()),
                ('sort_description', models.TextField()),
                ('news', models.TextField()),
                ('image_source', models.URLField()),
                ('image_caption', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ZeeNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.TextField()),
                ('sort_description', models.TextField()),
                ('news', models.TextField()),
                ('image_source', models.URLField()),
                ('image_caption', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
