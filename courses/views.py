from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView
from .models import Course, Unit, Lesson


class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"


class CourseCreateView(CreateView):
    model = Course
    fields = ["name", "grade"]
    template_name = "courses/course_form.html"

    def get_success_url(self):
        return reverse("courses:course-list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cancel_url"] = reverse("courses:course-list")
        return ctx

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            field.widget.attrs["class"] = "form-control"
        return form


class UnitListView(ListView):
    model = Unit
    template_name = "courses/unit_list.html"
    context_object_name = "units"

    def get_queryset(self):
        self.course = get_object_or_404(Course, id=self.kwargs["course_id"])
        return Unit.objects.filter(course=self.course).order_by("order")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["course"] = self.course
        ctx["cancel_url"] = reverse("courses:unit-list", args=[self.course.id])
        return ctx


class UnitCreateView(CreateView):
    model = Unit
    fields = ["title", "order"]
    template_name = "courses/unit_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, id=kwargs["course_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.course = self.course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("courses:unit-list", args=[self.course.id])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["course"] = self.course
        ctx["cancel_url"] = reverse("courses:unit-list", args=[self.course.id])
        return ctx

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            field.widget.attrs["class"] = "form-control"
        return form


class LessonListView(ListView):
    model = Lesson
    template_name = "courses/lesson_list.html"
    context_object_name = "lessons"

    def get_queryset(self):
        self.unit = get_object_or_404(Unit, id=self.kwargs["unit_id"])
        return Lesson.objects.filter(unit=self.unit).order_by("order")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["unit"] = self.unit
        ctx["course"] = self.unit.course
        return ctx


class LessonCreateView(CreateView):
    model = Lesson
    fields = ["title", "order", "content"]
    template_name = "courses/lesson_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.unit = get_object_or_404(Unit, id=kwargs["unit_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.unit = self.unit
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("courses:lesson-list", args=[self.unit.id])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["unit"] = self.unit
        ctx["course"] = self.unit.course
        ctx["cancel_url"] = reverse("courses:lesson-list", args=[self.unit.id])
        return ctx

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            field.widget.attrs["class"] = "form-control"
        return form