from django.urls import path
from . import views

app_name = 'omnichat_web'

urlpatterns = [
    path('', views.index, name='index'),
    path('options', views.options, name='options'),
    path('completions', views.completions, name='completions'),
    path('create_completion', views.create_completion, name='create_completion'),
    path('create_completion_api', views.create_completion_api,
         name='create_completion_api'),
    path('gpt_options', views.gpt_options, name='gpt_options'),
    path('save_gpt_model', views.gpt_options, name='save_gpt_model'),
    path('save_conversation', views.save_conversation, name='save_conversation'),
    path('clear_conversation', views.clear_conversation, name='clear_conversation'),
]
