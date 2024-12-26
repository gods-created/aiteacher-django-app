from django.urls import path
from .views import (
    AIQuestion as AIQuestionViewSet,
    AITraining as AITrainingSet
)

app_name = 'ai'

urlpatterns = [
    path('send_question/', AIQuestionViewSet.as_view({'post': 'send_question'}), name='Send question to AI'),
    path('start_training_model/', AITrainingSet.as_view(), name='Start training AI model')
]
