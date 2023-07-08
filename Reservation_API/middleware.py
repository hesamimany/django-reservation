import datetime
import time
from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib.sessions.backends.db import SessionStore


class PasswordAttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            ip_address = self._get_client_ip(request)
            password = request.POST.get('password')

            if password:
                attempt_key = f'password_attempt:{ip_address}'
                attempts = request.session.get(attempt_key, 0)
                last_attempt_timestamp_key = f'last_attempt:{ip_address}'
                last_attempt_timestamp = request.session.get(last_attempt_timestamp_key)

                prev = 0
                current = time.time_ns() // 1_000_000_000
                if f'last_attempt:{ip_address}' not in request.session.keys():
                    prev = current
                else:
                    prev = request.session[f'last_attempt:{ip_address}']
                timeout = settings.PASSWORD_ATTEMPT_RESET_TIME

                # Reset the attempt count if the specified time period has passed since the last attempt
                if last_attempt_timestamp and (current - prev) > timeout:
                    attempts = 0
                del request.session[attempt_key]  # Remove the attempt count from the session

                if attempts >= settings.PASSWORD_ATTEMPT_THRESHOLD:
                    return HttpResponseForbidden("Too many password attempts. Please try again later.")

                request.session[attempt_key] = attempts + 1
                request.session[f'last_attempt:{ip_address}'] = current
                # request.session[last_attempt_timestamp_key] = timezone.now()

        response = self.get_response(request)
        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
