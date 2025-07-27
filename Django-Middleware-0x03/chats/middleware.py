import os
import logging
from datetime import datetime, time, timedelta
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
        if not (time(18, 0) <= now <= time(21, 0)):
            return HttpResponseForbidden("Access to chat is restricted at this time (allowed between 6PM and 9PM).")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = {}

    def __call__(self, request):
        # Only limit POST requests to the message endpoint
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()
            # Clean up old entries
            self.cleanup_old_entries(ip, now)
            # Initialize if not present
            if ip not in self.ip_message_log:
                self.ip_message_log[ip] = []
            # Check limit
            if len(self.ip_message_log[ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded: Only 5 messages per minute allowed.")
            # Log this message
            self.ip_message_log[ip].append(now)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def cleanup_old_entries(self, ip, now):
        # Remove timestamps older than 1 minute
        if ip in self.ip_message_log:
            self.ip_message_log[ip] = [
                ts for ts in self.ip_message_log[ip]
                if now - ts < timedelta(minutes=1)
            ]