from abc import ABCMeta, abstractstaticmethod
from tts import tts_google


class TtsFactory:
    @staticmethod
    def get_tts_obj(tts_type, credentials_file, voice_name, cache):
        try:
            if tts_type == "google":
                return tts_google.GoogleTTS(credentials_file,
                                            voice_name,
                                            cache)
            elif tts_type == "microsoft":
                return tts_google.MicrosoftTTS(credentials_file,
                                               voice_name,
                                               cache)
            elif tts_type == "salmaai":
                return tts_google.SalmaTTS(cache)
            else:
                raise AssertionError(
                    "TTS type:{} not supported".format(tts_type))
        except AssertionError as ae:
            print(ae)
