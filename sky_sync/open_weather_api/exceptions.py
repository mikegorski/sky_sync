from rest_framework.exceptions import APIException


class ApiException(APIException):
    pass


class SomethingWentWrong(ApiException):
    pass
