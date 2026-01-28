from django.conf import settings
from django.db import models


class Exam(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="exams"
    )
    title = models.CharField(max_length=200)
    total_marks = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    #computed field
    @property
    def total_marks1(self):
        return self.questions.all().aggregate(sum=models.Sum('mark'))['sum'] or 0


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    mark = models.PositiveSmallIntegerField()
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order} ({self.mark} marks)"


class AnswerChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    # every time this object is saved, run my logic too
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_correct and self.question_id:
            AnswerChoice.objects.filter(
                question_id=self.question_id
            ).exclude(pk=self.pk).update(is_correct=False)

    def __str__(self):
        return self.text[:50]


class ExamAttempt(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        SUBMITTED = "SUBMITTED", "Submitted"
    # STATUS_CHOICES = (
    #     ('IN_PROGRESS', 'In progress'),
    #     ('SUBMITTED', 'Submitted'),
    # )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exam_attempts"
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="attempts"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
    )

    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    full_mark = models.PositiveSmallIntegerField(default=0)
    user_mark = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.exam} ({self.status})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "exam"],
                condition=models.Q(status="IN_PROGRESS"),
                name="unique_in_progress_attempt_per_user_exam",
            )
        ]


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="attempt_answers",
    )
    selected_choice = models.ForeignKey(
        AnswerChoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="selected_in",
    )

    is_correct = models.BooleanField(default=False)
    earned_mark = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["attempt", "question"],
                name="unique_answer_per_question_per_attempt",
            ),
        ]

    def __str__(self):
        return f"{self.attempt} - Q{self.question.order}"
