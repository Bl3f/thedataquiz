from django import forms

from app.models import Question, Quiz


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["size"]


class OneAnswer(forms.Form):
    answer = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, choices, *args, **kwargs):
        super(OneAnswer, self).__init__(*args, **kwargs)
        self.fields["answer"].choices = choices
