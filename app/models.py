import random

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

A = 'a'
B = 'b'
C = 'c'
D = 'd'
answers = [(A, A), (B, B), (C, C), (D, D)]


class QuestionManager(models.Manager):
    def sample(self, size=1):
        return random.sample(list(self.all()), size)


class Question(models.Model):
    text = models.TextField(null=False, blank=False)

    a = models.CharField(max_length=128)
    b = models.CharField(max_length=128)
    c = models.CharField(max_length=128, null=True, blank=True)
    d = models.CharField(max_length=128, null=True, blank=True)

    answer = models.CharField(choices=answers, max_length=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def get_absolute_url(self):
        return reverse('question-edit', kwargs={'pk': self.pk})


class QuestionAnswered(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    order = models.IntegerField()
    user_answer = models.CharField(choices=answers, max_length=1, null=True, blank=True)
    is_correct = models.BooleanField(default=None, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)


class Quiz(models.Model):
    size = models.IntegerField()

    completed = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    questions = models.ManyToManyField(QuestionAnswered)

    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    @property
    def score(self):
        return self.questions.filter(is_correct=True).count() / self.size * 100


