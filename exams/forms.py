from django import forms
from .models import Exam, Question, AnswerChoice

class BaseBootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                existing = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = (existing + " form-control").strip()

class ExamForm(BaseBootstrapModelForm):
    class Meta:
        model = Exam
        fields = ["course", "title", "total_marks"]

class QuestionForm(BaseBootstrapModelForm):
    class Meta:
        model = Question
        fields = ["text", "mark", "order"]

class AnswerChoiceForm(BaseBootstrapModelForm):
    class Meta:
        model = AnswerChoice
        fields = ["text", "is_correct"]
