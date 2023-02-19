import os

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from hackathon.apps import HackathonConfig

class VoiceList(APIView):
    voice_file = serializers.FileField()

    def get(self, request):
        print(request.GET)
        if not request.GET:
            model = Voice.objects.all()
            serializer = VoiceSerializer(model, many=True)
            response = Response(serializer.data)
            return response
        elif request.GET['request_type'] == "list":
            model = Voice.objects.all()
            serializer = VoiceSerializer(model, many=True)
            response = Response(serializer.data)
            return response
        elif request.GET['request_type'] == "origin":
            file_path = settings.MEDIA_ROOT + request.GET['file_name']
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read())
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
        elif (request.GET['request_type'] == "noise") or (request.GET['request_type'] == "denoise"):
            origin_path = os.path.splitext(request.GET['file_name'])
            file_path = origin_path[0] + f'_{request.GET["request_type"]}' + origin_path[1]
            file_path = settings.MEDIA_ROOT + file_path
            # noise와 denoise wav file 생성 및 저장
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read())
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
        elif request.GET['request_type'] == "text":
            # origin_path = os.path.splitext(request.GET['file_name'])
            # file_path = origin_path[0] + '_denoise' + origin_path[1]
            file_path = request.GET['file_name']
            file_path = settings.MEDIA_ROOT + file_path
            if os.path.isfile(file_path):
                text = HackathonConfig.sr_model.speech_to_text(file_path)
                response_data = {'sr_result':text}
                return JsonResponse(response_data)
        else:
            raise SuspiciousOperation("Invalid request; see documentation for correct paramaters")


    def post(self, request):
        file_name = request.data['file_name']
        voice_file = request.FILES['voice_file']
        voice = Voice(
            file_name=file_name,
            voice_file=voice_file
        )
        voice.save()
        serializer = VoiceSerializer(data={'file_name':file_name})
        if serializer.is_valid():            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # except:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
