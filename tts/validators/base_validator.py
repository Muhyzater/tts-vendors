from abc import ABC, abstractmethod
from collections import namedtuple


class BaseValidator(ABC):
    """
    Base class that other validators need to adhere to
    """

    _next_validator = None

    def set_next(self, validator):
        """
        Chain next validator in the chain
        args
        -------------
        validator (BaseValidator): the validator to be added the end of the
        chain
        returns
        -------------
        validator (BaseValidator): the validator at the end of the chain
        """

        self._next_validator = validator
        return validator

    @abstractmethod
    def validate(self, request: dict, configs: dict):
        """
        validate request
        args
        ------------
        request (dict): request to be validated
        configs (dict): app configs
        return
        ------------
        verdict (dict): status of request
        """

        pass

    def validate_next(self, request: dict, configs: dict):
        """
        Invoke next validator if possible
        """

        if self._next_validator:
            return self._next_validator.validate(request, configs)
        else:
            return verdict(is_valid=True, code=200, message="valid")


# a simple namedtuple for a better formatted result
verdict = namedtuple("verdict", ["is_valid", "code", "message"])
