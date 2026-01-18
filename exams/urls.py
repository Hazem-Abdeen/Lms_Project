from django.urls import path
from .views import (
    ExamListView, ExamCreateView, ExamDetailView, ExamUpdateView, ExamDeleteView,
    QuestionCreateView, QuestionUpdateView, QuestionDeleteView
)

app_name = "exams"

urlpatterns = [
    path("", ExamListView.as_view(), name="exam_list"),
    path("create/", ExamCreateView.as_view(), name="exam_create"),
    path("<int:pk>/", ExamDetailView.as_view(), name="exam_detail"),
    path("<int:pk>/edit/", ExamUpdateView.as_view(), name="exam_update"),
    path("<int:pk>/delete/", ExamDeleteView.as_view(), name="exam_delete"),

    # Questions
    path("<int:exam_id>/questions/create/", QuestionCreateView.as_view(), name="question_create"),
    path("questions/<int:pk>/edit/", QuestionUpdateView.as_view(), name="question_update"),
    path("questions/<int:pk>/delete/", QuestionDeleteView.as_view(), name="question_delete"),
]
