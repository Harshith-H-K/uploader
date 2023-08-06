from django.contrib import admin
from django.urls import path
from base.views import index, upload

urlpatterns = [
    path("", index),
    path("upload/", upload),
]
