from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view
from utils import openai
from omnichat_web.models import AiModel
import logging

logger = logging.getLogger(__name__)
username = "human"
ai_name = "Marilyn Monroe"
current_conversation = ''

# def index(request):
#     return render(request, 'omnichat_web/index.html')


@api_view(['GET', 'POST', ])
def send_message(request):
    global current_conversation
    message_data = request.data
    current_conversation += '\nHuman: ' + \
        message_data.get('message') + '\nAI:'
    ai_model = AiModel.objects.get(name=ai_name)
    prompt = ai_model.prompt + '\n\n' + ai_model.examples \
        + current_conversation
    ai_response = openai.create_completion(prompt)
    ai_text = ai_response.get('choices')[0].get('text').strip()
    current_conversation += ai_text
    if message_data.get('learn'):
        ai_model.examples += current_conversation
        current_conversation = ''
        ai_model.save()
    bot_message_data = {'sender': ai_name, 'message': ai_text}
    logger.warn(prompt + ' ' + ai_text)
    return Response(bot_message_data)
