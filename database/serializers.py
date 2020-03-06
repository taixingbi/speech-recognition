from rest_framework import serializers
from .models import Ml_test
from .models import Teleconference_transcribe

from rest_framework import filters

class Ml_testSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ml_test
        fields = ['email', 'name']


class Teleconference_transcribeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teleconference_transcribe
        fields = ['filename', 'transcription', 'transcription_baseline']