from django.urls import resolve


class DisableCSRF(object):
    """Middleware for disabling CSRF in an specified app name.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        """Preprocess the request.
        """
        print("hello")
        setattr(request, '_dont_enforce_csrf_checks', True)
