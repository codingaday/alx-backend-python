import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.conf import settings

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Middleware to log user requests"""
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logging
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def __call__(self, request):
        # Get user info (handle anonymous users)
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        logger.info(f"User: {user} - Path: {request.path} - Method: {request.method}")

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts chat access between 9 PM (21:00) and 6 AM (06:00)
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.restricted_start = time(21, 0)  # 9 PM
        self.restricted_end = time(6, 0)    # 6 AM

    def __call__(self, request):
        current_time = datetime.now().time()

        # Check if request is to chat endpoints during restricted hours
        if (request.path.startswith('/api/chats/') or
            request.path.startswith('/api/conversations/')):

            if self.restricted_end < current_time < self.restricted_start:
                return HttpResponseForbidden(
                    "Chat access is restricted between 9 PM and 6 AM"
                )

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to store IP addresses and their request timestamps
        self.ip_request_log = {}
        # Rate limit settings (5 requests per minute)
        self.limit = 5
        self.window = timedelta(minutes=1)

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        
        # Only process POST requests (assuming chat messages are sent via POST)
        if request.method == 'POST':
            current_time = datetime.now()
            
            # Initialize log for new IP addresses
            if ip_address not in self.ip_request_log:
                self.ip_request_log[ip_address] = []
            
            # Remove timestamps older than our time window
            self.ip_request_log[ip_address] = [
                timestamp for timestamp in self.ip_request_log[ip_address]
                if current_time - timestamp < self.window
            ]
            
            # Check if request exceeds the limit
            if len(self.ip_request_log[ip_address]) >= self.limit:
                return HttpResponseForbidden(
                    "Rate limit exceeded. Please wait before sending more messages."
                )
            
            # Add current request timestamp
            self.ip_request_log[ip_address].append(current_time)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define protected paths and required roles
        self.protected_paths = {
            '/api/chat/delete/': ['admin', 'moderator'],
            '/api/chat/ban-user/': ['admin', 'moderator'],
            '/api/chat/view-reports/': ['admin', 'moderator'],
            # Add more paths and their required roles as needed
        }

    def __call__(self, request):
        # Get the requested path
        path = request.path_info

        # Check if the path requires special permissions
        for protected_path, required_roles in self.protected_paths.items():
            if path.startswith(protected_path):
                # Check if user is authenticated
                if not request.user.is_authenticated:
                    return HttpResponseForbidden("Authentication required")

                # Check if user has any of the required roles
                user_role = getattr(request.user, 'role', None)
                if user_role not in required_roles:
                    return HttpResponseForbidden(
                        "You don't have permission to access this resource"
                    )
                break

        response = self.get_response(request)
        return response

