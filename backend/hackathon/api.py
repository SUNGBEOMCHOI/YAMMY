import os

from pydub import AudioSegment
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
            file_path = settings.MEDIA_ROOT + '/' + file_path

            raw_file_path = origin_path[0] + '_raw' + origin_path[1]
            raw_file_path = settings.MEDIA_ROOT + '/' + raw_file_path

            noise_file_path = origin_path[0] + '_noise' + origin_path[1]
            noise_file_path = settings.MEDIA_ROOT + '/' + noise_file_path

            if (request.GET['request_type'] == "noise"):
                HackathonConfig.sr_model.generate_noisy_voice(raw_file_path)
            elif (request.GET['request_type'] == "denoise"):
                origin_path = os.path.splitext(request.GET['file_name'])
                preprocess_file_path = origin_path[0] + f'_preprocess' + origin_path[1]
                preprocess_file_path = settings.MEDIA_ROOT + '/' + preprocess_file_path

                # HackathonConfig.preprocess_model.get_result(raw_file_path) # preprocess
                HackathonConfig.preprocess_model.get_result(noise_file_path) # preprocess
                
                # HackathonConfig.denoise_model.denoise_noisy_voice(noise_file_path)
                HackathonConfig.denoise_model.denoise_noisy_voice(preprocess_file_path)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read())
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
        elif request.GET['request_type'] == "text":
            origin_path = os.path.splitext(request.GET['file_name'])

            file_path = origin_path[0] + f'_raw' + origin_path[1]
            file_path = settings.MEDIA_ROOT + '/'  + file_path
            text = HackathonConfig.sr_model.speech_to_text(file_path)
            print('raw : ', text)

            file_path = origin_path[0] + f'_noise' + origin_path[1]
            file_path = settings.MEDIA_ROOT + '/'  + file_path
            text = HackathonConfig.sr_model.speech_to_text(file_path)
            print('noise : ', text)

            file_path = origin_path[0] + f'_denoise' + origin_path[1]
            file_path = settings.MEDIA_ROOT + '/'  + file_path
            if os.path.isfile(file_path):
                text = HackathonConfig.sr_model.speech_to_text(file_path)
                print('denoise : ', text)
                response_data = {'sr_result':text}
                return JsonResponse(response_data)
        else:
            raise SuspiciousOperation("Invalid request; see documentation for correct paramaters")


    def post(self, request):
        file_name = request.data['file_name']
        wav_file_name = file_name[:-4] + ".wav"
        noise_wav_file_name = file_name[:-8] + "_noise" + ".wav"
        denoise_wav_file_name = file_name[:-8] + "_denoise" + ".wav"

        voice_file = request.FILES['voice_file']
        voice = Voice(
            file_name=file_name,
            voice_file=voice_file
        )
        voice.save()
        serializer = VoiceSerializer(data={'file_name':file_name})
        m4a_file_path = settings.MEDIA_ROOT + '/' + file_name
        wav_file_path = settings.MEDIA_ROOT + '/' + wav_file_name
        denoise_wav_file_path = settings.MEDIA_ROOT + '/' + denoise_wav_file_name
        track = AudioSegment.from_file(m4a_file_path,  format= 'm4a')
        track.export(wav_file_path, format='wav') # wav form으로 저장
        # track.export(denoise_wav_file_path, format='wav') # wav form으로 저장
        if serializer.is_valid():            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # except:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
