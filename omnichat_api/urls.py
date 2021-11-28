from django.urls import path
from . import views

app_name = 'omnichat_api'

urlpatterns = [
    path('', views.send_message,
         name='index'),
    path('send_message', views.send_message,
         name='send_message'),
]
