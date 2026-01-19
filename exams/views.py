from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Exam, Question, AnswerChoice
from .forms import ExamForm, QuestionForm, ChoiceForm


class ExamListView(ListView):
    model = Exam
    template_name = "exams/exam_list.html"
    context_object_name = "exams"
    ordering = ["-id"]

    def get_queryset(self):
        return Exam.objects.select_related("course").all().order_by("-id")


class ExamCreateView(CreateView):
    model = Exam
    form_class = ExamForm
    template_name = "exams/exam_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["mode"] = "create"
        return ctx

    def get_success_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.object.pk})


class ExamUpdateView(UpdateView):
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


class ExamDeleteView(DeleteView):
    model = Exam
    template_name = "exams/exam_confirm_delete.html"
    success_url = reverse_lazy("exams:exam_list")


class ExamDetailView(DetailView):
    model = Exam
    template_name = "exams/exam_detail.html"
    context_object_name = "exam"

    def get_queryset(self):
        return Exam.objects.select_related("course")

class QuestionCreateView(CreateView):
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


class QuestionUpdateView(UpdateView):
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


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = "exams/question_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.object.exam.pk})

class ChoiceCreateView(CreateView):
    model = AnswerChoice
    form_class = ChoiceForm
    template_name = "exams/choice_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=self.kwargs["question_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.question = self.question
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["question"] = self.question
        ctx["exam"] = self.question.exam
        ctx["mode"] = "create"
        return ctx

    def get_success_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.question.exam.pk})


class ChoiceUpdateView(UpdateView):
    model = AnswerChoice
    form_class = ChoiceForm
    template_name = "exams/choice_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["question"] = self.object.question
        ctx["exam"] = self.object.question.exam
        ctx["mode"] = "edit"
        return ctx

    def get_success_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.object.question.exam.pk})


class ChoiceDeleteView(DeleteView):
    model = AnswerChoice
    template_name = "exams/choice_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.object.question.exam.pk})