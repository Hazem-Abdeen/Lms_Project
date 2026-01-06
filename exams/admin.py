from django.contrib import admin
from .models import Exam, Question, AnswerChoice, ExamAttempt, AttemptAnswer

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(AnswerChoice)
admin.site.register(ExamAttempt)
admin.site.register(AttemptAnswer)
