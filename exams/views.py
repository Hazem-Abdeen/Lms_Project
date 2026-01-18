from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Exam, Question
from .forms import ExamForm, QuestionForm


class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = "exams/exam_list.html"
    context_object_name = "exams"
    ordering = ["-id"]

    def get_queryset(self):
        return Exam.objects.select_related("course").all().order_by("-id")


class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = "exams/exam_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["mode"] = "create"
        return ctx

    def get_success_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.object.pk})


class ExamUpdateView(LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = "exams/exam_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["mode"] = "edit"
        ctx["exam"] = self.object
        return ctx

    def get_success_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.object.pk})


class ExamDeleteView(LoginRequiredMixin, DeleteView):
    model = Exam
    template_name = "exams/exam_confirm_delete.html"
    success_url = reverse_lazy("exams:exam_list")


class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = "exams/exam_detail.html"
    context_object_name = "exam"

    def get_queryset(self):
        return Exam.objects.select_related("course")

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "exams/question_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.exam = get_object_or_404(Exam, pk=self.kwargs["exam_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.exam = self.exam
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["exam"] = self.exam
        ctx["mode"] = "create"
        return ctx

    def get_success_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.exam.pk})


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "exams/question_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["exam"] = self.object.exam
        ctx["mode"] = "edit"
        return ctx

    def get_success_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.object.exam.pk})


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = "exams/question_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.object.exam.pk})

