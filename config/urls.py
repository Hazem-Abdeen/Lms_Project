from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
    path("exams/", include("exams.urls")),
    path("", lambda request: redirect("/exams/")),
]
