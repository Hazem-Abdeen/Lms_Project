from django.urls import path
from .views import (
    ExamListView, ExamCreateView, ExamDetailView, ExamUpdateView, ExamDeleteView,
    QuestionCreateView, QuestionUpdateView, QuestionDeleteView, ChoiceCreateView, ChoiceUpdateView, ChoiceDeleteView,
    StartExamAttemptView, TakeExamView
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

    # Choices
    path("questions/<int:question_id>/choices/add/", ChoiceCreateView.as_view(), name="choice_create"),
    path("choices/<int:pk>/edit/", ChoiceUpdateView.as_view(), name="choice_update"),
    path("choices/<int:pk>/delete/", ChoiceDeleteView.as_view(), name="choice_delete"),

    path("<int:exam_id>/start/",StartExamAttemptView.as_view(),name="attempt_start",),
    path("attempts/<int:attempt_id>/take/",TakeExamView.as_view(),name="attempt_take",),
]
