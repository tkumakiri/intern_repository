from rest_framework.response import Response


def error_response(status, code, error):
    assert 400 <= status < 600
    return Response({"code": code, "error": error}, status=status)


def parse_error_response(param, provided=None):
    # TODO: appropriate error code
    message = f"invalid format for {param}"
    if provided is not None:
        message += f": {provided}"
    return error_response(400, -1, message)


def not_found_response(requested=None):
    # TODO: appropriate error code
    message = ""
    if requested is not None:
        message += f"{requested}: "
    message += "not found"
    return error_response(404, -1, message)


class ProcessRequestError(Exception):
    def __init__(self, response):
        super().__init__(f"custom error: {response}")
        self.response = response
