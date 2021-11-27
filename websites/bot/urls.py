from django.urls import path
from . import views

app_name = 'bot'

urlpatterns = [
    path('', views.index, name='index'),
    path('start', views.start_server, name='start_server'),
    path('stop', views.stop_server, name='stop_server'),
    path('options', views.options, name='options'),
    path('train', views.train, name='train'),
    path('rest', views.rest_channel, name='rest'),
    path('messages', views.MessagesCreateAPIView.as_view(), name='messages_api'),
    path('message_list', views.message_list, name='message_list_api'),
    path('send_message', views.send_message, name='send_message_api'),
    path('completions', views.completions, name='completions'),
    path('create_completion', views.create_completion, name='create_completion'),
    path('create_completion_api', views.create_completion_api,
         name='create_completion_api'),
    path('gpt_options', views.gpt_options, name='gpt_options'),
    path('save_gpt_model', views.gpt_options, name='save_gpt_model'),
    path('save_conversation', views.save_conversation, name='save_conversation'),
    path('clear_conversation', views.clear_conversation, name='clear_conversation'),
]
