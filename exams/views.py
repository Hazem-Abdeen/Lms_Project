from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Exam, Question, AnswerChoice, ExamAttempt, AttemptAnswer
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


class StartExamAttemptView(LoginRequiredMixin, View):
    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)

        # BLOCK if already submitted
        submitted = ExamAttempt.objects.filter(
            user=request.user,
            exam=exam,
            status=ExamAttempt.Status.SUBMITTED
        ).first()

        if submitted:
            return redirect("exams:attempt_result", attempt_id=submitted.id)

        # otherwise continue or resume
        attempt, created = ExamAttempt.objects.get_or_create(
            user=request.user,
            exam=exam,
            status=ExamAttempt.Status.IN_PROGRESS,
            defaults={
                "full_mark": exam.questions.aggregate(
                    total=Sum("mark")
                )["total"] or 0,
                "user_mark": 0,
            },
        )

        return redirect("exams:attempt_take", attempt_id=attempt.id)



class TakeExamView(LoginRequiredMixin, View):
    template_name = "exams/attempt_take.html"

    def get(self, request, attempt_id):
        attempt = get_object_or_404(
            ExamAttempt,
            pk=attempt_id,
            user=request.user,
        )

        if attempt.status == ExamAttempt.Status.SUBMITTED:
            return redirect("exams:attempt_result", attempt_id=attempt.id)

        questions = attempt.exam.questions.prefetch_related("choices").all()

        answers_map = dict(
            attempt.answers.values_list("question_id", "selected_choice_id")
        )

        return render(request, self.template_name, {
            "attempt": attempt,
            "exam": attempt.exam,
            "questions": questions,
            "answers_map": answers_map,
        })

    @transaction.atomic
    def post(self, request, attempt_id):
        attempt = get_object_or_404(
            ExamAttempt,
            pk=attempt_id,
            user=request.user,
        )

        if attempt.status == ExamAttempt.Status.SUBMITTED:
            return redirect("exams:attempt_result", attempt_id=attempt.id)

        questions = attempt.exam.questions.prefetch_related("choices").all()

        for q in questions:
            key = f"q_{q.id}"
            choice_id = request.POST.get(key)

            if not choice_id:
                AttemptAnswer.objects.update_or_create(
                    attempt=attempt,
                    question=q,
                    defaults={
                        "selected_choice": None,
                        "is_correct": False,
                        "earned_mark": 0,
                    },
                )
                continue

            choice = get_object_or_404(AnswerChoice, pk=choice_id, question=q)

            is_correct = choice.is_correct
            earned = q.mark if is_correct else 0

            AttemptAnswer.objects.update_or_create(
                attempt=attempt,
                question=q,
                defaults={
                    "selected_choice": choice,
                    "is_correct": is_correct,
                    "earned_mark": earned,
                },
            )

        # update total ONCE
        attempt.user_mark = attempt.answers.aggregate(total=Sum("earned_mark"))["total"] or 0
        attempt.save(update_fields=["user_mark"])

        return redirect("exams:attempt_take", attempt_id=attempt.id)


class SubmitAttemptView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request, attempt_id):
        attempt = get_object_or_404(ExamAttempt, pk=attempt_id, user=request.user)

        if attempt.status == ExamAttempt.Status.SUBMITTED:
            return redirect("exams:attempt_result", attempt_id=attempt.id)

        total = attempt.answers.aggregate(total=Sum("earned_mark"))["total"] or 0

        attempt.user_mark = total
        attempt.status = ExamAttempt.Status.SUBMITTED
        attempt.submitted_at = timezone.now()
        attempt.save(update_fields=["user_mark", "status", "submitted_at"])

        return redirect("exams:attempt_result", attempt_id=attempt.id)


class AttemptResultView(LoginRequiredMixin, View):
    template_name = "exams/attempt_result.html"

    def get(self, request, attempt_id):
        attempt = get_object_or_404(ExamAttempt, pk=attempt_id, user=request.user)

        if attempt.status != ExamAttempt.Status.SUBMITTED:
            return redirect("exams:attempt_take", attempt_id=attempt.id)

        questions = attempt.exam.questions.prefetch_related("choices").all()

        answers = (
            AttemptAnswer.objects
            .filter(attempt=attempt)
            .select_related("question", "selected_choice")
        )
        answers_map = {a.question_id: a for a in answers}

        correct_map = {
            q.id: next((c for c in q.choices.all() if c.is_correct), None)
            for q in questions
        }

        return render(request, self.template_name, {
            "attempt": attempt,
            "exam": attempt.exam,
            "questions": questions,
            "answers_map": answers_map,
            "correct_map": correct_map,
        })
