from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .forms import CreateQuestionForm, CreateQuizForm, OneAnswerQCM, OneAnswerCash
from .models import Question, Quiz, QuestionAnswered, answers, QCM, CASH


def get_answer_form(question):
    if question.question_type == QCM:
        return OneAnswerQCM
    elif question.question_type == CASH:
        return OneAnswerCash


def index(request):
    if request.method == "POST":
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            create_question_form = CreateQuestionForm()
        else:
            create_question_form = form
    else:
        create_question_form = CreateQuestionForm()

    context = {
        "nb_questions": Question.objects.count(),
        "create_question_form": create_question_form,
    }

    return render(request, template_name="app/index.html", context=context)


def quiz_create(request):
    if request.method == "POST":
        form = CreateQuizForm(request.POST)

        if form.is_valid():
            size = form.cleaned_data["size"]
            tag = form.cleaned_data["tag"]
            random_questions = Question.objects.sample(size, tag=tag)

            quiz = Quiz(
                size=size,
                user=request.user,
                tag=tag,
            )

            quiz.save()

            questions = []
            for i, question in enumerate(random_questions):
                object = QuestionAnswered(question=question, order=i)
                object.save()
                questions.append(object)

            quiz.questions.set(questions)
        else:
            form = CreateQuizForm()
    else:
        form = CreateQuizForm()

    return render(request, template_name="app/quiz_create.html", context={"form": form, "data": Quiz.objects.all()})


def quiz_play(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    not_answered_questions = quiz.questions.filter(user_answer__isnull=True)
    not_answered_count = not_answered_questions.count()
    already_answered_count = quiz.size - not_answered_count

    if not_answered_count == 0:
        if not quiz.completed:
            quiz.completed = True
            quiz.save()

        context = {
            "quiz": quiz,
            "score": quiz.score,

        }
        return render(request, template_name="app/quiz_finished.html", context=context)

    current_question = not_answered_questions.all().order_by("order").first()
    choices = [(name, current_question.question.__getattribute__(name)) for name, _ in answers]
    form_class = get_answer_form(current_question.question)

    if request.method == "POST":
        form = form_class(choices, request.POST)

        if form.is_valid():
            answer_given = form.cleaned_data.get("answer")
            print(answer_given)
            if current_question.question.question_type == QCM:
                current_question.user_answer = answer_given
                current_question.is_correct = (answer_given == current_question.question.answer)
                current_question.save()
            elif current_question.question.question_type == CASH:
                current_question.user_answer = answer_given
                current_question.is_correct = (answer_given.lower() == current_question.question.__getattribute__(current_question.question.answer).lower())
                current_question.save()
            return redirect("quiz-play", pk=pk)
    else:

        form = form_class(choices)

    context = {
        "quiz": quiz,
        "question_number": already_answered_count + 1,
        "current_question": current_question,
        "form": form
    }

    return render(request, template_name="app/quiz_play.html", context=context)


class ListQuestionsView(ListView):
    model = Question


class UpdateQuestionView(UpdateView):
    model = Question
    fields = "__all__"
    success_url = reverse_lazy("question-list")


class DeleteQuestionView(DeleteView):
    model = Question
    success_url = reverse_lazy("question-list")


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
