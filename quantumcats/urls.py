from django.contrib import admin
from django.urls import path

from game import views

urlpatterns = [
    path("", views.index, name="index"),
    path("catlapse/", views.catlapse, name="catlapse"),
    path("entangle/", views.entangle, name="entangle"),
    path("admin/", admin.site.urls),
]
