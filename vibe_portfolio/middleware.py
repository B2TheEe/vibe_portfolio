import re
import time
import logging

from django.core.cache import cache
from django.http import HttpResponse

logger = logging.getLogger('django.security')

_MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


class PayloadSizeLimitMiddleware:
    """Reject any request whose Content-Length exceeds 10 MB before the body is read."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        content_length = request.META.get('CONTENT_LENGTH')
        if content_length:
            try:
                if int(content_length) > _MAX_UPLOAD_BYTES:
                    logger.warning(
                        'Oversized payload rejected | ip=%s path=%s size=%s bytes',
                        _get_client_ip(request), request.path_info, content_length,
                    )
                    return HttpResponse(
                        'Payload too large. Maximum allowed size is 10 MB.',
                        status=413,
                        content_type='text/plain; charset=utf-8',
                    )
            except (ValueError, TypeError):
                pass
        return self.get_response(request)


_AUTH_RE = re.compile(
    r'/(login|logout|password[_-]change|password[_-]reset)',
    re.IGNORECASE,
)

_WINDOW = 15 * 60    # 15 minutes in seconds
_GENERAL_LIMIT = 300 # max requests per window per IP for regular endpoints
_AUTH_LIMIT = 5      # max requests per window per IP for auth endpoints


def _get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


class RateLimitMiddleware:
    """
    Sliding-window rate limiter. Auth endpoints (login/logout/password) are
    limited to 5 requests per 15 minutes; all other endpoints to 300.

    Uses Django's cache backend. For multi-worker deployments configure a
    shared cache (Redis/Memcached) via the CACHES setting so limits are
    enforced across all workers.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = _get_client_ip(request)
        path = request.path_info

        if _AUTH_RE.search(path):
            limit = _AUTH_LIMIT
            cache_key = f'rl:auth:{ip}'
            label = 'auth'
        else:
            limit = _GENERAL_LIMIT
            cache_key = f'rl:gen:{ip}'
            label = 'general'

        now = time.time()
        cutoff = now - _WINDOW
        timestamps = [t for t in (cache.get(cache_key) or []) if t > cutoff]
        timestamps.append(now)
        cache.set(cache_key, timestamps, _WINDOW + 60)

        if len(timestamps) > limit:
            retry_after = max(1, int(timestamps[0] + _WINDOW - now) + 1)
            logger.warning(
                'Rate limit exceeded | ip=%s path=%s type=%s limit=%d',
                ip, path, label, limit,
            )
            if label == 'auth':
                body = (
                    f'Too many login attempts. '
                    f'Try again in {retry_after} seconds.'
                )
            else:
                body = f'Too many requests. Try again in {retry_after} seconds.'
            response = HttpResponse(
                body, status=429, content_type='text/plain; charset=utf-8'
            )
            response['Retry-After'] = str(retry_after)
            return response

        return self.get_response(request)
