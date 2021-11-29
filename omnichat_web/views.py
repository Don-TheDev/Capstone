import logging
import os
import json
import requests
from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import omnichat_web
from omnichat_web.models import AiModel
from utils import openai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.safestring import mark_safe
from . import forms

logger = logging.getLogger(__name__)
global server_is_running
server_is_running = False
username = "Human"
ai_name = "Marilyn Monroe"
ai_model = AiModel.objects.get_or_create(name=ai_name)[0]
openai.prompt = ai_model.prompt
openai.examples = ai_model.examples
rasa_rest_url = 'http://localhost:5005/webhooks/rest/webhook'
global server_thread

# Create your views here.


def index(request):
    return render(request, 'omnichat_web/index.html')


def completions(request):
    messages = []
    if openai.additional_text:
        messages = openai.additional_text.strip().split('\n')
        messages.reverse()
    form = forms.CompletionForm()
    return render(request, 'omnichat_web/completions.html', {'ai_text': messages, 'form': form})


def options(request):
    return render(request, 'bot/options.html')


def gpt_options(request):
    form = forms.GPTModelForm(initial={
        'prompt': openai.prompt, 'examples': openai.examples})
    return render(request, 'omnichat_web/gpt_options.html', {'form': form})


def send_message(request):
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
            openai.additional_text += '\nHuman: ' + text + '\nAI: '
            # ai_response = openai.create_completion_with_full()
            ai_model = AiModel.objects.get(name=ai_name)
            prompt = ai_model.prompt + '\n\n' + ai_model.examples + '\n' \
                + openai.additional_text
            ai_response = openai.create_completion(prompt)
            ai_text = ai_response.get('choices')[0].get('text')
            openai.additional_text += ai_text
            # logger.warn('Log_AI: ' + ai_text)
            logger.warn(prompt + ai_text)
            return redirect('omnichat_web:completions')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.CompletionForm()
        messages = []
        if openai.additional_text:
            messages = openai.additional_text.split('\n')
            messages.reverse()
    return render(request, 'omnichat_web/completions.html', {'ai_text': messages, 'form': form})


def send_message_to_ai():
    pass


def save_conversation(request):
    if openai.additional_text.strip():
        openai.examples += '\n' + openai.additional_text
    openai.additional_text = ""
    return redirect('omnichat_web:completions')


def clear_conversation(request):
    openai.additional_text = ""
    return redirect('omnichat_web:completions')


def save_model(request):
    ai_model = AiModel.objects.get_or_create(name=ai_name)[0]
    # if this is a PUT request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.GPTModelForm(request.POST)
        # check whether it's valid:
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            ai_model.prompt = form.cleaned_data.get('prompt')
            ai_model.examples = form.cleaned_data.get('examples')
            # logger.warn("AI PK: " + str(ai_model.pk))
            # AiModel.objects.filter(pk=ai_model.pk) \
            #     .update(prompt=prompt, examples=examples)
            ai_model.save()
            openai.prompt = ai_model.prompt
            openai.examples = ai_model.examples
            # logger.warn('Log_Human' +
            #             ": " + text)
            # logger.warn('Full_Text: ' + openai.prompt +
            #             openai.additional_text)
            # logger.warn('Log_AI: ' + ai_text)
            # return HttpResponseRedirect(reverse('omnichat_web:completions', args={'ai_text': ai_text, 'form': form}))
            return redirect('omnichat_web:gpt_options')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.GPTModelForm(initial={
            'prompt': openai.prompt, 'examples': openai.examples})

    return render(request, 'omnichat_web/gpt_options.html', {'form': form})
