from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
    path("exams/", include("exams.urls")),
    path("", lambda request: redirect("/exams/")),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
