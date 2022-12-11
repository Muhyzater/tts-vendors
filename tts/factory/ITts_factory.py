from abc import ABCMeta, abstractstaticmethod


class ITts_factory(metaclass=ABCMeta):

    def text_to_audio(self, audio_encoding, rate, text, key, tashkeel):

        if self.cache.exists(key):
            return self.cache.get_value(key)
        else:
            audio = self._get_result(audio_encoding, rate, text, tashkeel)
            self.cache.set_value(key, audio)

            return audio

    def _get_result(self):
        pass
