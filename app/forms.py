from django import forms
from django.utils.safestring import mark_safe

from app.models import Question, Quiz


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["size", "tag"]


class OneAnswerQCM(forms.Form):
    answer = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'qcm'}))

    template_name = "app/forms/qcm.html"

    def __init__(self, choices, *args, **kwargs):
        super(OneAnswerQCM, self).__init__(*args, **kwargs)
        self.fields["answer"].choices = choices


class OneAnswerCash(forms.Form):
    answer = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Enter a Cash answer'}))

    template_name = "app/forms/cash.html"

    def __init__(self, choices, *args, **kwargs):
        super(OneAnswerCash, self).__init__(*args, **kwargs)
