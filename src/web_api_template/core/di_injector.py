import inspect
import threading
from functools import wraps

from pythondi.container import Container
from pythondi.exceptions import (
    ProviderDoesNotConfiguredException,
)

import sys


_LOCK = threading.RLock()

# TODO: Add support for async injection
# TODO: Change magic strings to constants
# TODO: Cover pytest and unittest for exceptions


def inject(**params):
    """Dependency injector decorator"""

    def inner_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _provider = Container.get()
            if _provider:
                # Case of auto injection
                if not params:
                    annotations = inspect.getfullargspec(func).annotations
                    for k, v in annotations.items():
                        if v in _provider.bindings and k not in kwargs:
                            replacement = _provider.bindings[v]
                            if inspect.isclass(replacement):
                                replacement = replacement()

                            kwargs[k] = replacement
                # Case of manual injection
                else:
                    for k, v in params.items():
                        replacement = v
                        if inspect.isclass(replacement):
                            replacement = replacement()

                        kwargs[k] = replacement

            else:
                # Ignore initialization if testing
                if "pytest" not in sys.modules:
                    raise ProviderDoesNotConfiguredException

            if inspect.iscoroutinefunction(func):

                async def _inject(*args, **kwargs):
                    return await func(*args, **kwargs)

            else:

                def _inject(*args, **kwargs):
                    return func(*args, **kwargs)

            return _inject(*args, **kwargs)

        return wrapper

    return inner_func
