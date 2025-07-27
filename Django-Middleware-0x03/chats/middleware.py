import os
import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        log_path = os.path.join(os.path.dirname(__file__), '..', 'requests.log')
        log_path = os.path.abspath(log_path)
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        # Restrict access outside 6PM (18:00) to 9PM (21:00)
        if not (time(18, 0) <= now <= time(21, 0)):
            return HttpResponseForbidden("Access to chat is restricted at this time (allowed between 6PM and 9PM).")
        return self.get_response(request)