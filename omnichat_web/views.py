import logging
import os
import json
import requests
from django.utils import timezone
from django import forms
from django.forms.fields import CharField, DateTimeField
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .scripts import openai_script
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


class CompletionForm(forms.Form):
    text = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'message-input',
            'placeholder': 'Type here'
        }
    ))


# class GPTModelForm(forms.Form):
#     prompt = forms.CharField(label=mark_safe(
#         'Prompt:<br/>'), widget=forms.Textarea)
#     examples = forms.CharField(label=mark_safe(
#         'Examples:<br/>'), widget=forms.Textarea)


class GPTModelForm(forms.Form):
    prompt = forms.CharField(label='Prompt:', widget=forms.Textarea(
        attrs={
            'class': 'edit-input',
        }
    ))
    examples = forms.CharField(label='Examples:', widget=forms.Textarea(
        attrs={
            'class': 'edit-input',
        }
    ))


# class CompletionCreateAPIView(CreateAPIView):
#     serializer_class = CompletionSerializer
#     queryset = Message.objects.order_by('send_date')


def index(request):
    return render(request, 'omnichat_web/index.html')


def completions(request):
    messages = openai_script.additional_text.split('\n')
    form = CompletionForm()
    return render(request, 'omnichat_web/completions.html', {'ai_text': messages, 'form': form})


def options(request):
    return render(request, 'bot/options.html')


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
            return redirect('omnichat_web:completions')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CompletionForm()
    messages = openai_script.additional_text.split('\n')
    return render(request, 'omnichat_web/completions.html', {'ai_text': messages, 'form': form})


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
    # return render(request, 'omnichat_web/restchannel.html', {'previous_messages': messages})
    # serializer = MessageSerializer(messages, many=True)
    logger.warn(openai_script.get_full_text())
    # logger.warn(ai_response.encoding)
    return Response(bot_message_data)


def save_conversation(request):
    if openai_script.additional_text.strip():
        openai_script.examples += openai_script.additional_text
    openai_script.additional_text = ""
    form = CompletionForm()
    return render(request, 'omnichat_web/completions.html', {'form': form})


def clear_conversation(request):
    openai_script.additional_text = ""
    return redirect('omnichat_web:completions')


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
            # return HttpResponseRedirect(reverse('omnichat_web:completions', args={'ai_text': ai_text, 'form': form}))
            return render(request, 'omnichat_web/gpt_options.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GPTModelForm(initial={
                            'prompt': openai_script.prompt, 'examples': openai_script.examples})

    return render(request, 'omnichat_web/gpt_options.html', {'form': form})
