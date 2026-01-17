from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Exam

@login_required
def exam_list(request):
    exams = Exam.objects.select_related("course").all().order_by("-id")
    return render(request, "exams/exam_list.html", {"exams": exams})
