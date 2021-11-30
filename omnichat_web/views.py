import json
import logging
import os

import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils import util_openai, util_nlpcloud

import omnichat_web
from omnichat_web.models import AiModel

from . import forms

logger = logging.getLogger(__name__)
# global server_is_running
# server_is_running = False
username = "Human"
ai_name = "Marilyn Monroe"
# ai_model = AiModel.objects.get_or_create(name=ai_name)[0]
# util_openai.prompt = ai_model.prompt
# util_openai.examples = ai_model.examples
# rasa_rest_url = 'http://localhost:5005/webhooks/rest/webhook'
# global server_thread
current_conversation = ''

# Create your views here.


def index(request):
    return render(request, 'omnichat_web/index.html')


def completions(request):
    messages = []
    if current_conversation:
        cleaned_conversation = current_conversation.replace('\n###', '')
        cleaned_conversation = cleaned_conversation.strip()
        messages = cleaned_conversation.split('\n')
        messages.reverse()
    form = forms.CompletionForm()
    return render(request, 'omnichat_web/completions.html', {'ai_text': messages, 'form': form})


def options(request):
    return render(request, 'bot/options.html')


def gpt_options(request):
    ai_model = AiModel.objects.get_or_create(name=ai_name)[0]
    form = forms.GPTModelForm(initial={
        'prompt': ai_model.prompt, 'examples': ai_model.examples})
    return render(request, 'omnichat_web/gpt_options.html', {'form': form})


def send_message(request):
    global current_conversation
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.CompletionForm(request.POST)
        # check whether it's valid:
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            text = form.cleaned_data.get('text')
            # logger.warn('Log_Human' +
            #             ": " + text)
            current_conversation += '\nHuman: ' + text + '\ndonsai:'
            # ai_response = util_openai.create_completion_with_full()
            ai_model = AiModel.objects.get_or_create(name=ai_name)[0]
            prompt = ai_model.prompt + '\n\n' + ai_model.examples + current_conversation
            # logger.warn("prompt: " + prompt)
            # ai_response = util_openai.create_completion(prompt)
            ai_response = util_nlpcloud.generate(prompt)
            # logger.warn("ai_response: " + ai_response)
            logger.warn("nb_generated_tokens: " + str(ai_response.get('nb_generated_tokens')))
            # ai_text = ai_response.get('choices')[0].get('text')
            ai_text = ai_response.get('generated_text')
            current_conversation += ai_text + '###'
            # logger.warn('Log_AI: ' + ai_text)
            logger.warn(prompt + ai_text + '###')
            return redirect('omnichat_web:completions')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.CompletionForm()
        messages = []
        if current_conversation:
            messages = current_conversation.split('\n')
            messages.reverse()
    return render(request, 'omnichat_web/completions.html', {'ai_text': messages, 'form': form})


def send_message_to_ai():
    pass


def save_conversation(request):
    global current_conversation
    ai_model = AiModel.objects.get_or_create(name=ai_name)[0]
    if current_conversation.strip():
        ai_model.examples += current_conversation
        ai_model.save()
    current_conversation = ""
    return redirect('omnichat_web:completions')


def clear_conversation(request):
    global current_conversation
    current_conversation = ""
    return redirect('omnichat_web:completions')


def save_model(request):
    ai_model = AiModel.objects.get_or_create(name=ai_name)[0]
    # if this is a PUT request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.GPTModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            ai_model.prompt = form.cleaned_data.get('prompt')
            ai_model.examples = form.cleaned_data.get('examples')
            ai_model.save()
            return redirect('omnichat_web:gpt_options')
    else:
        form = forms.GPTModelForm(initial={
            'prompt': ai_model.prompt, 'examples': ai_model.examples})

    return render(request, 'omnichat_web/gpt_options.html', {'form': form})
