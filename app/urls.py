from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    path('questions/', views.ListQuestionsView.as_view(), name='question-list'),
    path('questions/add/', views.CreateQuestionsView.as_view(), name='question-add'),
    path('questions/<int:pk>/', views.UpdateQuestionView.as_view(), name='question-edit'),
    path('questions/<int:pk>/delete', views.DeleteQuestionView.as_view(), name='question-delete'),

    path('quiz/', views.quiz_create, name='quiz-create'),
    path('quiz/<int:pk>/', views.quiz_play, name='quiz-play'),

    path('register/', views.Register.as_view(), name='register'),
]
