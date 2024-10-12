from aiocache import cached

from web_api_template.core.settings import settings


def selective_cache(ttl=60, key_builder=None, alias="default"):
    """Custom cache decorator that allows to selectively enable or disable the cache

    Args:
        ttl (int, optional): Default ttl in seconds. Defaults to 60.
        key_builder (_type_, optional): key builder for the cache. Defaults to None.
        alias (str, optional): cache to use. Defaults to "default".
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Enters every time the function is called
            if settings.CACHE_ENABLED:
                # Caching is enabled, so it caches the function
                return await cached(ttl=ttl, key_builder=key_builder, alias=alias)(
                    func
                )(*args, **kwargs)
            else:
                # Caching disabled, so it calls the function without caching
                return await func(*args, **kwargs)

        return wrapper

    return decorator
