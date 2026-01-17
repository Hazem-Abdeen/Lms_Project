from django.urls import path
from . import views

app_name = "exams"

urlpatterns = [
    path("", views.exam_list, name="exam-list"),
]
