from django.db import models
from tinymce.models import HTMLField


class Course(models.Model):
    name = models.CharField(max_length=200)
    grade = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name} (Grade {self.grade})"


class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="units")
    title = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Unit {self.order}: {self.title}"


class Lesson(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField()
    content = HTMLField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Lesson {self.order}: {self.title}"
