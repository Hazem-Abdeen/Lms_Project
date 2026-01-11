from django.urls import path, include
from . import views

app_name = "courses"

urlpatterns = [
    # courses
    path("", views.CourseListView.as_view(), name="course-list"),
    path("create/", views.CourseCreateView.as_view(), name="course-create"),

    # units (inside course)
    path("<int:course_id>/units/", views.UnitListView.as_view(), name="unit-list"),
    path("<int:course_id>/units/create/", views.UnitCreateView.as_view(), name="unit-create"),

    # lessons (inside unit)
    path("units/<int:unit_id>/lessons/", views.LessonListView.as_view(), name="lesson-list"),
    path("units/<int:unit_id>/lessons/create/", views.LessonCreateView.as_view(), name="lesson-create"),

    path("tinymce/", include("tinymce.urls")),
]
