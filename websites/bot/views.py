import logging
import os
import threading
import json
import django
from django.views import generic
import requests
from django.utils import timezone
from django import forms
from django.forms.fields import CharField, DateTimeField
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.http import Http404
from django.urls import reverse
from requests import models
from .serializers import MessageSerializer
from .models import Message
from .scripts import openai_script
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.safestring import mark_safe


logger = logging.getLogger(__name__)
global server_is_running
server_is_running = False
username = "Test User"
botname = "Test Bot"
rasa_rest_url = 'http://localhost:5005/webhooks/rest/webhook'
global server_thread

# Create your views here.


class MessageForm(forms.Form):
    text = forms.CharField(label='Message',)


class MessagesCreateAPIView(CreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.order_by('send_date')


class CompletionForm(forms.Form):
    text = forms.CharField(label='',)


class GPTModelForm(forms.Form):
    prompt = forms.CharField(label=mark_safe(
        'Prompt:<br/>'), widget=forms.Textarea)
    examples = forms.CharField(label=mark_safe(
        'Examples:<br/>'), widget=forms.Textarea)


# class CompletionCreateAPIView(CreateAPIView):
#     serializer_class = CompletionSerializer
#     queryset = Message.objects.order_by('send_date')


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CompletionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CompletionForm()

    return render(request, 'name.html', {'form': form})


@api_view()
def message_list(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST', ])
def send_message(request):
    unicode_data = request.body.decode('utf-8')
    logger.warn(unicode_data)
    message_data = request.data
    user_message = Message(sender=message_data.get(
        'sender'), message=message_data.get('message'), send_date=timezone.now())
    user_message.save()
    logger.warn(user_message.sender +
                ": " + user_message.message)
    message_data = json.dumps(message_data)
    rasa_response = requests.post(rasa_rest_url, message_data)
    content = rasa_response.json()
    logger.warn(content)
    if len(content) > 0:
        bot_message_data = content[0]
    else:
        bot_message_data = {'sender': 'N/A',
                            'text': 'No response available'}
    bot_message_data['sender'] = botname
    bot_message = Message(
        sender=botname, message=bot_message_data.get('text'), send_date=timezone.now())
    bot_message.save()
    # logger.warn(bot_message_data['sender'] +
    #             ": " + str(bot_message_data['text']))
    # messages = Message.objects.order_by('send_date')
    # logger.warn(str(messages))
    # return render(request, 'bot/restchannel.html', {'previous_messages': messages})
    # serializer = MessageSerializer(messages, many=True)
    return Response(content)

# class MessagesView(generic.ListView):
#     template_name = 'bot/restchannel.html'
#     context_object_name = 'previous_messages'

#     def get_queryset(self):
#         """Return the list of messages ordered by send date."""
#         return Message.objects.order_by('-send_date')


def index(request):
    return render(request, 'bot/index.html')


def start_server(request):
    global server_is_running
    global server_thread
    server_thread = threading.Thread(target=start_bot)

    logger.warn('server is running when trying to start:' +
                str(server_is_running))
    if not server_is_running:
        server_is_running = True
        server_thread.start()
        return render(request, 'bot/index.html', {'server_is_running': server_is_running, })
    else:
        return render(request, 'bot/index.html', {'server_is_running': server_is_running, 'error_message': "Server is already running", })


def stop_server(request):
    global server_is_running
    global server_thread
    logger.warn('server is running when trying to stop:' +
                str(server_is_running))
    if server_is_running:
        server_is_running = False
        stop_bot()
        server_thread.join()
        return render(request, 'bot/index.html', {'server_is_running': server_is_running})
    else:
        return render(request, 'bot/index.html', {'server_is_running': server_is_running, 'error_message': "Server isn't running"})


def completions(request):
    return create_completion(request)


def gpt_options(request):
    return save_gpt_model(request)


def create_completion(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CompletionForm(request.POST)
        # check whether it's valid:
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            text = form.cleaned_data.get('text')
            # logger.warn('Log_Human' +
            #             ": " + text)
            openai_script.additional_text += 'Human: ' + text + '\nAI:'
            # logger.warn('Full_Text: ' + openai_script.prompt +
            #             openai_script.additional_text)
            ai_response = openai_script.create_completion_with_full()
            ai_text = ai_response.get('choices')[0].get('text')
            openai_script.additional_text += ai_text + '\n'
            # logger.warn('Log_AI: ' + ai_text)
            form = CompletionForm()
            messages = openai_script.additional_text.split('\n')
            # return HttpResponseRedirect(reverse('bot:completions', args={'ai_text': ai_text, 'form': form}))
            return render(request, 'bot/completions.html', {'ai_text': messages, 'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CompletionForm()
    messages = openai_script.additional_text.split('\n')
    return render(request, 'bot/completions.html', {'ai_text': messages, 'form': form})


@api_view(['GET', 'POST', ])
def create_completion_api(request):
    # unicode_data = request.body.decode('utf-8')
    # logger.warn(unicode_data)
    message_data = request.data
    logger.warn('message data:', message_data)
    # logger.warn(message_data.get('sender') +
    #             ": " + message_data.get('message'))
    # message_data = json.dumps(message_data)
    openai_script.additional_text += 'Human: ' + \
        message_data.get('message') + '\nAI:'
    # logger.warn('Full_Text: ' + openai_script.prompt +
    #             openai_script.additional_text)
    ai_response = openai_script.create_completion_with_full()
    ai_text = ai_response.get('choices')[0].get('text')
    openai_script.additional_text += ai_text + '\n'
    bot_message_data = {'sender': botname, 'message': ai_text.strip()}
    # logger.warn(bot_message_data['sender'] +
    #             ": " + str(bot_message_data['text']))
    # messages = Message.objects.order_by('send_date')
    # logger.warn(str(messages))
    # return render(request, 'bot/restchannel.html', {'previous_messages': messages})
    # serializer = MessageSerializer(messages, many=True)
    logger.warn(openai_script.get_full_text())
    # logger.warn(ai_response.encoding)
    return Response(bot_message_data)


def options(request):
    return render(request, 'bot/options.html', {})


def train(request):
    train_bot()
    return render(request, 'bot/options.html', {})


def save_conversation(request):
    if openai_script.additional_text.strip():
        openai_script.examples += openai_script.additional_text
    openai_script.additional_text = ""
    form = CompletionForm()
    return render(request, 'bot/completions.html', {'form': form})


def clear_conversation(request):
    openai_script.additional_text = ""
    form = CompletionForm()
    return render(request, 'bot/completions.html', {'form': form})


def save_gpt_model(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GPTModelForm(request.POST)
        # check whether it's valid:
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            prompt = form.cleaned_data.get('prompt')
            examples = form.cleaned_data.get('examples')
            openai_script.prompt = prompt
            openai_script.examples = examples
            # logger.warn('Log_Human' +
            #             ": " + text)
            # logger.warn('Full_Text: ' + openai_script.prompt +
            #             openai_script.additional_text)
            # logger.warn('Log_AI: ' + ai_text)
            # return HttpResponseRedirect(reverse('bot:completions', args={'ai_text': ai_text, 'form': form}))
            return render(request, 'bot/gpt_options.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GPTModelForm(initial={
                            'prompt': openai_script.prompt, 'examples': openai_script.examples})

    return render(request, 'bot/gpt_options.html', {'form': form})


def rest_channel(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MessageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            message_data = {'sender': username,
                            'message': form.cleaned_data.get('text')}
            user_message = Message(
                sender=username, message=form.cleaned_data.get('text'), send_date=timezone.now())
            user_message.save()
            form = MessageForm()
            # logger.warn(message_data['sender'] +
            #             ": " + message_data['message'])
            message_data = json.dumps(message_data)
            rasa_response = requests.post(rasa_rest_url, message_data)
            content = rasa_response.json()
            if len(content) > 0:
                bot_message_data = content[0]
            else:
                bot_message_data = {'sender': 'N/A',
                                    'text': 'No response available'}
            bot_message_data['sender'] = botname
            bot_message = Message(
                sender=botname, message=bot_message_data.get('text'), send_date=timezone.now())
            bot_message.save()
            # logger.warn(bot_message_data['sender'] +
            #             ": " + str(bot_message_data['text']))
            messages = Message.objects.order_by('send_date')
            logger.warn(str(messages))
            return render(request, 'bot/restchannel.html', {'previous_messages': messages})


# def rest_channel(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MessageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            message_data = {'sender': username,
                            'message': form.cleaned_data.get('text')}
            user_message = Message(
                sender=username, message=form.cleaned_data.get('text'), send_date=timezone.now())
            user_message.save()
            form = MessageForm()
            # logger.warn(message_data['sender'] +
            #             ": " + message_data['message'])
            message_data = json.dumps(message_data)
            rasa_response = requests.post(rasa_rest_url, message_data)
            content = rasa_response.json()
            if len(content) > 0:
                bot_message_data = content[0]
            else:
                bot_message_data = {'sender': 'N/A',
                                    'text': 'No response available'}
            bot_message_data['sender'] = botname
            bot_message = Message(
                sender=botname, message=bot_message_data.get('text'), send_date=timezone.now())
            bot_message.save()
            # logger.warn(bot_message_data['sender'] +
            #             ": " + str(bot_message_data['text']))
            messages = Message.objects.order_by('send_date')
            logger.warn(str(messages))
            return render(request, 'bot/restchannel.html', {'previous_messages': messages})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MessageForm()

    return render(request, 'bot/restchannel.html', {'form': form})


###########################################################


def train_bot():
    os.chdir('C:/Repos/Capstone/bot')
    os.system('cmd /c "conda activate semisupervised')
    os.system('cmd /c "taskkill /F /IM "rasa.exe"')
    os.system('cmd /c "rasa train')
    os.system('cmd /c "echo done')


# def save_conversation():
#     pass


def start_bot():
    os.chdir('C:/Repos/Capstone/bot')
    os.system('cmd /c "conda activate semisupervised')
    os.system('cmd /c "rasa run --cors *')


def stop_bot():
    os.system('cmd /c "taskkill /F /IM "rasa.exe"')
