import asyncio

from parsers.models import ParserSettings
from translate.utils import TimeoutAPIException


TIMEOUT = ParserSettings.objects.first().timeout


async def run_async(func, timeout=TIMEOUT, *args, **kwargs):
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
