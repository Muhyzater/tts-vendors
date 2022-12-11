from azure.cognitiveservices.speech import ResultReason
from azure.cognitiveservices.speech.audio import (
    AudioOutputConfig,
    PullAudioOutputStream,
)
from azure.cognitiveservices.speech import (
    SpeechConfig,
    SpeechSynthesizer,
    SpeechSynthesisOutputFormat,
)
from google.cloud import texttospeech as gtts
from google.oauth2 import service_account
from tts.audio_configs import audio_params
from tts.factory import ITts_factory
from pydub import AudioSegment
from io import BytesIO
import json
import requests
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class GoogleTTS(ITts_factory):
    def __init__(self, credentials_file, voice_name, cache):
        self.cfg = service_account.Credentials.from_service_account_file(
            credentials_file
        )
        self.lang_code = "-".join(voice_name.split("-")[:2])
        self.voice_name = voice_name
        self.cache = cache

    def _get_result(self, audio_encoding, rate, text, tashkeel):
        text_input = gtts.SynthesisInput(text=text)
        voice_params = gtts.VoiceSelectionParams(
            language_code=self.lang_code, name=self.voice_name
        )
        audio_config = gtts.AudioConfig(
            audio_encoding=audio_params[audio_encoding], sample_rate_hertz=rate
        )
        client = gtts.TextToSpeechClient(credentials=self.cfg)
        response = client.synthesize_speech(
            input=text_input, voice=voice_params, audio_config=audio_config
        )
        audio_bytes = BytesIO(response.audio_content)
        return audio_bytes.getvalue()


class MicrosoftTTS(ITts_factory):
    def __init__(self, credentials_file, voice_name, cache):

        self.lang_code = "-".join(voice_name.split("-")[:2])

        self.config = json.load(open(credentials_file))
        self.speech_config = SpeechConfig(
            subscription=self.config["KEY2"], region=self.config["LOCATION"]
        )
        self.speech_config.speech_synthesis_language = self.lang_code
        self.speech_config.speech_synthesis_voice_name = voice_name
        self.speech_config.set_speech_synthesis_output_format(
            SpeechSynthesisOutputFormat.Raw16Khz16BitMonoPcm
        )
        self.cache = cache

    def _get_result(self, audio_encoding, rate, text, taskheel):

        pull_stream = PullAudioOutputStream()
        audio_config = AudioOutputConfig(stream=pull_stream)
        speech_synthesizer = SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config
        )
        response = speech_synthesizer.speak_text(text)
        if response.reason == ResultReason.SynthesizingAudioCompleted:
            raw_result = BytesIO(response.audio_data)
        else:
            raise Exception("error generating audio!")
        tmp_result = AudioSegment.from_raw(
            raw_result, format="pcm", sample_width=2, channels=1, frame_rate=16000
        )
        tmp_result = tmp_result.set_frame_rate(rate)
        result = BytesIO()
        tmp_result.export(result, audio_encoding)
        return result.getvalue()


class SalmaTTS(ITts_factory):
    def __init__(self, cache):
        self.salma_url = audio_params["salmaTTS_url"]
        self.params = dict(
            diacritize_text=False,
            encoding="mp3",
            streaming=False,
            override_diacritics=False,
            spell_check_text=False,
            normalize_text=True,
        )
        self.cache = cache

    def _get_result(self, audio_encoding, rate, text, tashkeel):
        self.params["bitrate"] = rate
        self.params["encoding"] = audio_encoding
        self.params["diacritize_text"] = tashkeel
        text_input = {"text": text}
        response = requests.post(
            self.salma_url,
            data=text_input,
            params=self.params,
            stream=self.params["streaming"],
        )
        result = BytesIO(response.content)
        return result.getvalue()
