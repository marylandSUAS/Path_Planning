"""Custom client exception types."""

import requests


class InteropError(requests.HTTPError):
    """The interop server reported an error."""

    def __init__(self, response):
        """Create an InteropError.

        Args:
            response: requests.Response object that indicated the error.
        """
        message = '{method} {url} -> {code} Error ({reason}): {message}'
<<<<<<< HEAD
        message = message.format(
            method=response.request.method,
            url=response.request.url,
            code=response.status_code,
            reason=response.reason,
            message=response.text)
=======
        message = message.format(method=response.request.method,
                                 url=response.request.url,
                                 code=response.status_code,
                                 reason=response.reason,
                                 message=response.text)
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5

        super(InteropError, self).__init__(message, response=response)
