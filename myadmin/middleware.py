from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from accounts import models

class SessionExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)  # Convert back to datetime
                session_duration = timezone.now() - last_activity
                if session_duration.total_seconds() > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    request.session.flush()  # Clear session data
                else:
                    request.session['last_activity'] = timezone.now().isoformat()  # Store as ISO string
            else:
                request.session['last_activity'] = timezone.now().isoformat()  # Store as ISO string
        response = self.get_response(request)
        return response


class AdminUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('admin_id')

        if user_id:
            try:
                # Fetch the user object and attach it to the request
                request.admin_user = models.User.objects.get(id=user_id)
            except models.User.DoesNotExist:
                messages.error(request, "User does not exist.")
                return redirect('login')
        else:
            request.admin_user = None

        return self.get_response(request)

class CacheControlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Set Cache-Control headers
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response