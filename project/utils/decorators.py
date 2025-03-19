import asyncio
from functools import wraps
import logging
from typing import Callable


def async_timeout(timeout: float, ):
    def decorator(func: Callable) -> Callable:
        @wraps(wrapped=func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            except asyncio.TimeoutError:
                logging.info(f"Function '{func.__name__}' timed out after {timeout} seconds.")
                return "0"

        return wrapper

    return decorator


def driver_exception_handler(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> bool:
        try:
            _ = func(*args, **kwargs)
            return True
        except Exception as error:
            logging.warning(f"{func} was failed. Exception description:\n{error}")
            return False

    return wrapper
