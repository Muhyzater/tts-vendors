import logging
import time

from tts.api import tts_vendors_service, salma_tts, g_tts, m_tts, text_cache
import requests
from micro_service.micro_service_test_class import MicroServiceTestClass
from factory import tts_factory as factory
from tts.audio_configs import audio_params


class TextToSpeechTest(MicroServiceTestClass):

    text = "أنا سلمى. مساعدتك الشخصية. كيف يمكنني مساعدتك؟"
    generated_text = "الكنافة النابلسية"
    cached_text = "الكنافة النابلسية رائعة, الكنافة النابلسية رائعة"
    english_text = "القسطنطينيّة (بالإنجليزيّة: Constantinople) هي عاصمة "
    abbrev_text = "اشتريت سيارة BMW السريعة"
    vendors = ["salmaai", "google", "microsoft"]

    with open("long_text.txt", "r") as f:
        long_text = f.read()

    with open("long_text_2.txt", "r") as f:
        long_text_2 = f.read()
    salma_params = {
        "text": long_text,
        "vendor": "salmaai",
        "encoding": "wav",
        "rate": 44100,
    }

    google_params = {
        "text": long_text,
        "vendor": "google",
        "encoding": "wav",
        "rate": 44100,
    }

    microsoft_params = {
        "text": long_text,
        "vendor": "microsoft",
        "encoding": "wav",
        "rate": 44100,
    }
    port = 5000
    link_tts = "http://localhost:{}/tts".format(port)

    @classmethod
    def setUpClass(cls):
        super(TextToSpeechTest, cls).setUpClass(
            tts_vendors_service(run=False),
            title="TTS vendors Micro Service",
            description=(
                "Synthesize audio from a given "
                "text comparing audio quality "
                "between Salma, Google and Microsoft"
            ),
        )
        text_cache.flushall()

    def _check_working_text_google(self, params: dict):
        t = time.time()
        response = requests.post(self.link_tts, json=params)
        response_time = time.time() - t
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.content), 0)

    def _check_working_text_salma(self, params: dict):
        t = time.time()
        response = requests.post(self.link_tts, json=params)
        response_time = time.time() - t
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.content), 0)

    def _check_working_text_microsoft(self, params: dict):
        t = time.time()
        response = requests.post(self.link_tts, json=params)
        response_time = time.time() - t
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.content), 0)

    def test_generated_audio_salma(self):
        """
        Implements a text to check if the API is actually generating anything
        from given texts
        """
        logging.info(" testing generated audio ".center(79, "#"))

        self._check_working_text_salma(self.salma_params)
        self._check_working_text_google(self.google_params)
        self._check_working_text_microsoft(self.microsoft_params)

    def test_redis(self):
        """
        Tests if the caching is working
        """
        logging.info(" Testing redis".center(79, "#"))
        for vendor in self.vendors:
            response_1, time_1 = self.__check_redis(vendor)
            response_2, time_2 = self.__check_redis(vendor)
            self.assertEqual(response_1.status_code, 200, "vendor {}".format(vendor))
            self.assertEqual(response_2.status_code, 200, "vendor {}".format(vendor))
            self.assertLess(time_2, time_1, "vendor {}".format(vendor))

    def __check_redis(self, vendor):
        t = time.time()
        if vendor == 'salmaai':
            response = requests.post(self.link_tts, json=self.salma_params)
        elif vendor == 'google':
            response = requests.post(self.link_tts, json=self.google_params)
        elif vendor == 'microsoft':
            response = requests.post(self.link_tts, json=self.microsoft_params)

        response_time = time.time() - t
        return response, response_time

    def test_gen_openapi(self):

        logging.info(" testing OpenAPI generation ".center(79, "#"))

        res = requests.post(self.link_tts, json=self.google_params)
        self.assertEqual(res.status_code, 200, res.content)

        desc = (
            "Synthesize audio from a given text or a previously enqueued\n"
            + "text using its generated key"
        )
        response = requests.post(
            self.link_tts,
            params={
                "text": self.text,
                "vendor": "google",
                "encoding": "mp3",
                "rate": 16000,
            },
        )

        self.assertEqual(response.status_code, 200, response.content)
        self.add_documentation(response, description=desc)

        # Just to tell openapi generator that the parameters are optional
        response = requests.post(self.link_tts, json={"text": self.text})
        self.assertEqual(response.status_code, 200)
        self.add_documentation(response, description=desc)
