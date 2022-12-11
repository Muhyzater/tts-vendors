import re

from . import BaseValidator, verdict


class TextValidator(BaseValidator):
    """
    check if the `Content-Type` header exists on the request and have valid
    and supported values
    """

    def validate(self, request: dict, configs: dict):
        text = request["text"]
        # header exists and of valid structure
        if len(text) < 1:
            return verdict(
                is_valid=False, code=400, message="text field shall not be empty"
            )

        return self.validate_next(request, configs)
