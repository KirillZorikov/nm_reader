import asyncio

from rest_framework.exceptions import APIException, _, _get_error_details
from rest_framework import status

from parsers.models import ParserSettings


TIMEOUT = ParserSettings.objects.first().timeout


class CaptchaDetectedAPIException(APIException):
    status_code = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
    default_detail = ('Captcha detected. Please solve captha, send the results '
                      'to /api/parsers/captcha-solve and retry request')
    default_code = 'captcha_detected'

    def __init__(self, detail=None, code=None, *args, **kwargs):

        detail = {
            'error': {
                'message': self.default_detail,
                'code': self.default_code,
                'image': detail,
                'page_id': int(kwargs.get('page_id') or '-1'),
                'service_slug': kwargs.get('service_name'),
                'browser_id': kwargs.get('browser_id'),
            }
        }
        code = self.default_code

        self.detail = _get_error_details(detail, code)


class TimeoutAPIException(APIException):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    default_detail = _('The response was not ready in time')
    default_code = 'timeout'

    def __init__(self, detail=None, code=None):

        detail = {
            'error': {
                'message': self.default_detail,
                'code': self.default_code
            }
        }
        code = self.default_code

        self.detail = _get_error_details(detail, code)


async def run_async2(func, timeout=0, *args, **kwargs):
    timeout = timeout or TIMEOUT
    try:
        data = await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
    except asyncio.TimeoutError:
        return {
            'success': False,
            'message': 'timeout',
            'exception': TimeoutAPIException()
        }
    except Exception as e:
        return {
            'success': False,
            'message': 'exception',
            'exception': e
        }
    return data


def get_captcha_data(service_slug):
    from translate.api.serializers import CaptchaSerializer
    from parsers.models import Captcha

    return CaptchaSerializer(
        instance=Captcha.objects.annotate_parser_slug().filter(
            parser_slug=service_slug
        ).first()
    ).data
