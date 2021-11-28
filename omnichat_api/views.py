from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view
from .scripts import openai_script
import logging

logger = logging.getLogger(__name__)
username = "Test User"
botname = "Test Bot"


# def index(request):
#     return render(request, 'omnichat_web/index.html')

@api_view(['GET', 'POST', ])
def send_message(request):
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
