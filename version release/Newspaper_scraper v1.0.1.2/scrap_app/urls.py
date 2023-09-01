from django.urls import path
from . import views

urlpatterns = [
    path('', views.scrape_newspaper, name='scrape_newspaper'),
]
