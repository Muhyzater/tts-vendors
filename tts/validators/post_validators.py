import os
from io import BytesIO

from pydub import AudioSegment
from . import BaseValidator, verdict


class AudioValidator(BaseValidator):
    def validate(self, request: dict, configs: dict):

        supported_files = ["wav", "mp3"]
        supported_vendors = ["google", "microsoft"]

        if request["encoding"] not in supported_files:
            return verdict(
                is_valid=False,
                code=415,
                message="Encoding: {} is not supported".format(request["encoding"]),
            )

        if request["vendor"] not in supported_vendors:
            return verdict(
                is_valid=False,
                code=415,
                message="Vendor: {} is not supported".format(request["vendor"]),
            )

        return self.validate_next(request, configs)
