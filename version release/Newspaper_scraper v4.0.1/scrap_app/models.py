from django.db import models

class HindustanTimesBangla(models.Model):
    headline = models.TextField()
    sort_description = models.TextField()
    news = models.TextField()
    image_source = models.URLField(max_length=1000)  # Increase max_length if needed
    image_caption = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ZeeNews(models.Model):
    headline = models.TextField()
    sort_description = models.TextField()
    news = models.TextField()
    image_source = models.URLField(max_length=1000)  # Increase max_length if needed
    image_caption = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class TV9Bangla(models.Model):
    headline = models.TextField()
    sort_description = models.TextField()
    news = models.TextField()
    image_source = models.URLField(max_length=1000)  # Increase max_length if needed
    image_caption = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


# class Anandabazar(models.Model):
#     headline = models.TextField()
#     sort_description = models.TextField()
#     news = models.TextField()
#     image_source = models.URLField()
#     image_caption = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
