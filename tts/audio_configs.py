from google.cloud import texttospeech as gtts
import os

audio_params = dict(
    encoding="mp3",
    service_name="tts-vendors",
    service_version="v0.1.6",
    environment="dev",
    port={"default": 5000, "type": int},
    DEBUG=False,
    suppress_logging=False,
    mp3=gtts.AudioEncoding.MP3,
    wav=gtts.AudioEncoding.LINEAR16,
    vendor="google",
    tashkeel=False,
    google_config=os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "google_creds.json"
    ),
    microsoft_config=os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "microsoft_creds.json"
    ),
    salma_config=os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "salma_creds.json"
    ),
    google_voice="ar-XA-Standard-D",
    microsoft_voice="ar-EG-SalmaNeural",
    root_path={"default": "", "type": str},
    salmaTTS_url="https://yjvhekp74bjkgexwxspeebfb47tqjc.staging.ingress.mawdu.com/tts-api-v4-1-3/tts",
    redis_host={"default": "localhost", "type": str},
    redis_port={"default": 6379, "type": int},
    redis_db={"default": 10, "type": int},
)
