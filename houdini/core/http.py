from django.http import HttpResponse

# Helper functions and classes


class HttpResponseUnauthorized(HttpResponse):
    """
    HTTP 401 response
    Used when a request is not signed correctly
    """

    def __init__(self, reason=None):
        if reason is None:
            super().__init__('401 Unauthorized', status=401)
        else:
            super().__init__('401 Unauthorized: ' + reason, status=401)


class HttpResponseConflict(HttpResponse):
    """
    HTTP 409
    Used when a request attempts to create a model that conflicts
    with an existing model in the database
    """

    def __init__(self, reason=None):
        if reason is None:
            super().__init__('409 Conflict', status=409)
        else:
            super().__init__('409 Conflict: ' + reason, status=409)


class HttpResponseInternalServerError(HttpResponse):
    """
    HTTP 500
    Used when the server encounters an unexpected condition
    that prevents it from fulfilling the request.
    """

    def __init__(self, reason=None):
        if reason is None:
            super().__init__('500 Internal Server Error', status=500)
        else:
            super().__init__('500 Internal Server Error: ' + reason, status=500)


class HttpResponseCreated(HttpResponse):
    """
    HTTP 201
    Used when the request to the server has been fulfilled
    and has resulted in one or more new resources being created.
    """

    def __init__(self, reason=None):
        if reason is None:
            super().__init__('201 Created', status=201)
        else:
            super().__init__('201 Created: ' + reason, status=201)
