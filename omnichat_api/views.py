from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils import util_nlpcloud
from omnichat_web.models import AiModel
import logging

logger = logging.getLogger(__name__)
user_name = "Human"
ai_name = "Marilyn Monroe"
current_conversation = ''

# def index(request):
#     return render(request, 'omnichat_web/index.html')


@api_view(['GET', 'POST', ])
def send_message(request):
    global current_conversation
    global user_name
    message_data = request.data

    user_name = message_data.get('sender')
    text = message_data.get('message')
    ai_model = AiModel.objects.get_or_create(name=ai_name)[0]
    current_conversation = f'\n{user_name}: ' + text + f'\n{ai_model.name}:'
    ai_model = AiModel.objects.get_or_create(name=ai_name)[0]
    prompt = ai_model.prompt + '\n\n' + ai_model.examples \
        + current_conversation
    # ai_response = util_openai.create_completion(prompt)
    # ai_text = ai_response.get('choices')[0].get('text').strip()
    ai_response = util_nlpcloud.generate(prompt)
    ai_text = ai_response.get('generated_text').strip()
    current_conversation += ' ' + ai_text + '\n###'
    if message_data.get('learn'):
        ai_model.examples += current_conversation
        current_conversation = ''
        ai_model.save()
    bot_message_data = {'sender': ai_name, 'message': ai_text}
    logger.warn(prompt + ' ' + ai_text + '\n###')
    return Response(bot_message_data)
