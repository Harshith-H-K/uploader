from django.contrib import admin
from django.urls import path
from base.views import index, upload, download

urlpatterns = [
    path("", index),
    path("upload/", upload),
    path("download/", download),
]
