from rest_framework.exceptions import APIException


class OpenWeatherAPIException(APIException):
    pass


class NonexistentModeSelected(Exception):
    pass
