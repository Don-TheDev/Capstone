from datetime import timezone
from .models import Message
from rest_framework import serializers
from django.utils import timezone


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['pk', 'sender', 'message', 'send_date']
