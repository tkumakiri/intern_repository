import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

LOGGER = logging.getLogger("django")


# 我々の API の規約に合うようにハンドラを設定する
def custom_exception_handler(exc, context):
    LOGGER.info("unhandled exception: %s", repr(exc))
    response = exception_handler(exc, context)
    if response is not None:
        original = response.data
        response.data = {
            "code": -1,
            "error": "unhandled error",
            "original": original,
        }
    return response


def error_response(status, code, error):
    assert 400 <= status < 600
    return Response({"code": code, "error": error}, status=status)


def parse_error_response(param, provided=None):
    # TODO: appropriate error code
    message = f"invalid format for {param}"
    if provided is not None:
        message += f": {provided}"
    return error_response(status.HTTP_400_BAD_REQUEST, -1, message)


def not_found_response(requested=None, code=-1):
    # TODO: appropriate error code
    message = ""
    if requested is not None:
        message += f"{requested}: "
    message += "not found"
    return error_response(status.HTTP_404_NOT_FOUND, code, message)


def validation_error_response(details):
    res = error_response(status.HTTP_400_BAD_REQUEST, -1, "validation error")
    res.data["details"] = details
    return res


def integrity_error_response(unique_params=[]):
    return error_response(
        status.HTTP_409_CONFLICT,
        -1,
        f"specified tuple of {', '.join(unique_params)} is already registered",
    )


def not_authenticated_response():
    return error_response(
        status.HTTP_401_UNAUTHORIZED, 1001, "no active user"
    )


def invalid_user_response():
    return error_response(
        status.HTTP_401_UNAUTHORIZED, 3001, "invalid user specified"
    )


def invalid_sender_response():
    return error_response(
        status.HTTP_401_UNAUTHORIZED, 4000, "invalid sender specified"
    )


def receiver_not_exist_response():
    return error_response(
        status.HTTP_404_NOT_FOUND, 4001, "invalid receiver specified"
    )


def receiver_not_followed_response():
    return error_response(
        status.HTTP_401_UNAUTHORIZED, 4002, "receiver not followed by user"
    )


def invalid_central_response():
    return error_response(
        status.HTTP_401_UNAUTHORIZED, 4003, "invalid central specified"
    )


def central_target_no_ff_response():
    return error_response(
        status.HTTP_401_UNAUTHORIZED,
        4004,
        "no ff relation between central and target",
    )


def invalid_author_response():
    return error_response(
        status.HTTP_401_UNAUTHORIZED, 5000, "invalid author specified"
    )


def delete_others_follow_response():
    return error_response(
        status.HTTP_401_UNAUTHORIZED,
        6002,
        "specified follow is not created by user",
    )


def delete_others_good_response():
    return error_response(
        status.HTTP_401_UNAUTHORIZED,
        7002,
        "specified good is not created by user",
    )


class ProcessRequestError(Exception):
    def __init__(self, response):
        super().__init__(f"custom error: {response}")
        self.response = response
