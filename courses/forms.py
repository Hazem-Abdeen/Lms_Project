from django import forms
from tinymce.widgets import TinyMCE
from .models import Course, Unit, Lesson


class BaseBootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class CourseForm(BaseBootstrapModelForm):
    class Meta:
        model = Course
        fields = ["name", "grade"]


class UnitForm(BaseBootstrapModelForm):
    class Meta:
        model = Unit
        fields = ["title", "order"]


class LessonForm(BaseBootstrapModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "order", "content"]
        widgets = {
            "content": TinyMCE(attrs={"rows": 20}),
        }
