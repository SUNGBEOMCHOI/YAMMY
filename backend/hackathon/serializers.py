from rest_framework import serializers
from .models import Voice

class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voice
        fields = ['file_name', 'voice_file']
